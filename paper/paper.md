---
title: 'Building InterMine databases from RDF Portal'
title_short: 'BH26JP: InterMine from RDF Portal'
tags:
  - InterMine
  - RDF Portal
  - rdf-config
  - SPARQL
  - data integration
authors:
  - name: Russell Y. Neches
    orcid: 0000-0002-2055-8381
    affiliation: 1
  - name: Shuichi Kawashima
    orcid: 0000-0001-7883-3756
    affiliation: 2
  - name: Toshiaki Katayama
    orcid: 0000-0003-2391-0384
    affiliation: 2
  - name: Gos Micklem
    orcid: 0000-0002-6883-6168
    affiliation: 3
affiliations:
  - name: Institute for Chemical Research, Kyoto University, Kyoto, Japan
    ror: 02kpeqv85
    index: 1
  - name: Database Center for Life Science, Chiba, Japan
    ror: 018q2r417
    index: 2
  - name: Department of Genetics, University of Cambridge, Cambridge, UK
    ror: 013meh722
    index: 3
date: 18 September 2026
cito-bibliography: paper.bib
event: BH26JP
biohackathon_name: "DBCLS BioHackathon 2026"
biohackathon_url: "https://2026.biohackathon.org/"
biohackathon_location: "Matsuyama, Japan"
group: rdfc2im
# URL to project git repo --- should contain the actual paper.md:
git_url: https://github.com/ryneches/rdfc2im-report
# This is the short authors description that is used at the
# bottom of the generated paper (typically the first two authors):
authors_short: Russell Y. Neches \emph{et al.}
---


# Abstract

<!-- TODO: write last, once Results and Discussion are drafted. -->

Table: Glossary. Terms used in this report, as they are used here.

| Term | Meaning |
|------|---------|
| RDF, SPARQL | The W3C standards for data as subject-predicate-object triples, and for querying it. A *SPARQL endpoint* is a web service that answers SPARQL queries. |
| RDF Portal | The DBCLS service that hosts reviewed life science RDF datasets behind public SPARQL endpoints. |
| rdf-config model | A YAML description of one RDF dataset: its classes (*subjects*), the predicates that connect them, how many values each may have, and example values. |
| InterMine, mine | A data warehouse system for biological data, and one database built with it (here, HumanMine). |
| Source | One input to a mine, loaded by its own loader. A *stock* source is one that HumanMine already runs. |
| Converter | The Java code in a stock source that turns a provider's files into InterMine objects. |
| Items XML | InterMine's generic input format: a file of objects (*items*) with their attributes and references. |
| Integration key | The fields InterMine uses to decide that objects from two sources are the same object, for example a gene's NCBI Gene identifier. |
| Priorities | The configuration that decides which source's value wins when two sources give one field different values. |
| Additions | A source's extension to the InterMine data model: the classes and fields it adds. |
| SSSOM | A standard tab-separated format for mappings between vocabularies [@usesMethodIn:Matentzoglu2022SSSOM]. |
| BlueGenes | InterMine's current web interface. |

# Introduction

Integrative analysis in biology depends on bringing independent databases together, so that the
evidence about a gene, a protein or a disease can be queried in one place. InterMine is an
open-source data warehouse system built for this purpose [@citesAsAuthority:Smith2012InterMine].
From one object model, based on the Sequence Ontology, InterMine generates a web interface, a query
builder, template searches, list analysis with enrichment statistics, and a REST API with client
libraries in several languages [@citesAsAuthority:Kalderimis2014InterMine]. HumanMine is the
InterMine instance for human data. Its 2022 release integrated about 40 datasets, among them NCBI
Gene, HGNC, UniProt, the Gene Ontology, Reactome, ClinVar and the GWAS Catalog, into one searchable
database [@citesAsAuthority:Lyne2022HumanMine].

The cost of a mine is in keeping its data current. Each source reaches the warehouse through its
own loader: a parser for a standard format, a custom Java converter, or a file in InterMine's own
XML item format [@Smith2012InterMine]. When a provider changes its release format, its loader must
change too, and a mine with dozens of sources carries dozens of such dependencies. The 2022
HumanMine paper states that the data "are updated quarterly" [@Lyne2022HumanMine]. In September
2026, the public HumanMine still reports its release of 12 February 2022.

Many of the same sources are now available from one service, in one format. RDF Portal, operated by
the Database Center for Life Science (DBCLS), hosts life science datasets in RDF behind public
SPARQL endpoints [@citesAsDataSource:RDFPortal]. It began as the NBDC RDF portal, which reviewed
each submitted dataset against guidelines for interoperability: typed primary resources,
human-readable labels, local identifiers in `dcterms:identifier`, and identifiers.org URIs for
cross-references [@citesAsAuthority:Kawashima2018RDFPortal]. In 2018 the portal held 21 datasets
from Japanese groups, with 45.5 billion triples [@Kawashima2018RDFPortal]. In September 2026 it
lists 64 datasets with 229.2 billion triples, including UniProt, NCBI Gene, HGNC, Ensembl, ClinVar,
Reactome and PubMed [@RDFPortal]. Each dataset on the portal also has an rdf-config model
[@rdfconfig]: a short YAML description of the classes in the dataset, the properties that connect
them, and the form of their values. The portal uses these models to draw schema diagrams, to
generate SPARQL, and to configure its GraphQL and AI-agent interfaces.

Together, these two resources suggest a different way to build a mine. If the structure of each
source is already described in a machine-readable model, then the mapping from that model to the
InterMine model can be written once, as data and not as code. One generic tool can then fetch,
transform and load any source that has such a model. rdfc2im (rdf-config to InterMine) is that
tool. It aligns rdf-config models to the HumanMine data model and records each alignment in a
mapping file that a curator can review. From the mapping it generates SPARQL queries, fetches the
results, and writes InterMine Items XML for the stock InterMine loader. In this report we describe
rdfc2im and its use at the DBCLS BioHackathon 2026, where we built a working HumanMine for a panel
of 113 food- and drug-metabolism genes from nine RDF sources, most of them on RDF Portal. We also
record the problems that only a real InterMine load revealed, which static checks of the mapping
did not.

# Approach

rdfc2im is a command-line tool written in Python. It follows the four steps of the workflow set
out at the previous DBCLS hackathon (Figure 1): prepare the two data models, map
one onto the other, extract the data with SPARQL, and load it into InterMine. Each step writes
plain text files that a person can read. Under version control there are only inputs and
curation decisions; everything else is regenerated.

<!-- TODO Figure 1: the four-step pipeline, redrawn from the domestic hackathon slide 2, with the
files each step reads and writes. Label: fig:pipeline. -->

## Inputs

rdfc2im reads three kinds of input. The first is the rdf-config model of each source, taken from
the rdf-config repository [@usesDataFrom:rdfconfig]: the subjects and predicates of the dataset,
the cardinality of each predicate, example values, prefixes, and the SPARQL endpoint. The second
is HumanMine's own configuration: the InterMine core model, the additions and integration keys of
each source that HumanMine runs, its source list (`project.xml`), and its priorities, taken from
the InterMine and HumanMine repositories. rdfc2im reasons over the InterMine model limited to
HumanMine's sources, plus a short list of model extensions that the project approved (for
example, `Gene.typeOfGene` and `Pathway.description`). The third is the data itself, fetched from
the endpoints that the rdf-config models name. In the demonstration build, every source came from
RDF Portal except the GWAS Catalog, which came from TogoVar.

<!-- TODO confirm with Gos: the UniProt queries name RDF Portal's SIB endpoint, but sources.yaml
says sparql.uniprot.org. See notes/commit-history.md, phase 1. -->

## Mapping

For each source, rdfc2im walks the rdf-config model from a root subject, for example the `Gene`
of NCBI Gene. It binds each subject to an InterMine class, and each predicate to a field of that
class. The first rule that applies decides:

1. an explicit rule for this source;
2. a match between the RDF type or predicate IRI and the ontology term that the InterMine model
   gives a class or field;
3. a general rule for that RDF type or predicate;
4. a match between names;
5. otherwise the row is left for a curator.

Every column that rdfc2im extracts is an attribute of one object. When a value belongs to a
different object, for example a synonym of a gene, the mapping names the reference that connects
the two (`Gene.synonyms`). Objects are linked only where a mapping names the link.

The mapping also decides how the data is split into tables. Each table is one SPARQL query and
one file. The main table holds the root's identifier and its single-valued attributes. Each
multi-valued predicate that creates other objects gets a table of its own, holding the root's
identifier and that one column, so that two multi-valued predicates never multiply each other's
rows. For NCBI Gene this gives five tables: the gene itself, its synonyms, its alternative
names, its Ensembl identifiers and its cross-references.

## Curation

Each source has two mapping files that a curator edits: one row per subject, and one row per
predicate. The predicate file uses the SSSOM layout [@usesMethodIn:Matentzoglu2022SSSOM], with
rdfc2im's own columns declared as extensions. Every row has a *status* and a *basis*. The status
decides whether the row loads: `sure` (backed by evidence), `guess` (a proposal to review) and
`human` (the curator's own edit) load; `todo` (undecided) and `drop` (not loaded, with the
reason) do not. The basis records where the mapping came from, for example a term match or a
named converter.

The reference for curation is the stock HumanMine converter for the same source. A field that the
converter writes is mapped, and its basis names the converter. A field that the converter never
writes, or that the model cannot hold, is dropped with the reason. A field beyond what the
converter writes loads only as a `guess`. A choice that the converter does not settle stays
`todo`. Rules that apply across runs are kept in one reviewable file, with their evidence. When
rdfc2im regenerates the mapping files, a three-way merge against its previous automatic output
keeps every value that the curator changed.

## Extraction

rdfc2im generates one SPARQL query per table. Only the root's identifier is a required pattern.
Everything else is `OPTIONAL`, so a record that lacks one value still loads. A constraint on a
required pattern limits a source, for example to human genes:

```sparql
SELECT DISTINCT ?id ?taxid ?gene_synonym
FROM <http://rdfportal.org/dataset/ncbigene>
WHERE {
  ?Gene a insdc:Gene .
  ?Gene dct:identifier ?id .
  ?Gene ncbio:taxid ?taxid .
  VALUES ?taxid { taxid:9606 }
  OPTIONAL { ?Gene insdc:gene_synonym ?gene_synonym . }
}
```

The fetch step pages through each table in a fixed order. SPARQL endpoints limit how many sorted
rows one query may page through: 200,000 on RDF Portal and 10,000 on TogoVar. A table larger than
the limit is fetched instead in batches of 1,000 root identifiers, listed in a `VALUES` clause. A
table that still cannot be fetched in full is reported as incomplete, never as complete.

The cleaning step turns RDF terms into plain values. For each column it applies a filter to the
raw value, then a chain of transforms, for example taking the local name of an IRI. A row whose
identifier is empty, or fails its filter, is dropped. Any other value that fails its filter is
left empty.

## Loading

rdfc2im writes one Items XML file per source. We chose Items XML over InterMine's loader for
tab-delimited files because it states every reference explicitly, so objects are linked exactly
where the mapping says. The files are loaded by InterMine's standard Items XML loader, registered
as a source type of its own so that rdfc2im's generated keys and model additions travel with it.
No Java code is needed.

Within a source, rows that describe one object become one item: rdfc2im identifies an object by
the first integration key of its class that the row fills. So a gene met in five tables is one
item. Values for numeric fields are checked against the field's type, and a value that does not
fit (such as "NR", for "not reported") is dropped and reported.

rdfc2im also generates the configuration that the mine needs. Each rdfc2im source has one of
three roles. It *replaces* a stock source (NCBI Gene, HGNC, GO, HPO, MP, ClinVar and the GWAS
Catalog). It loads *alongside* a stock source, right after it, filling only what the stock source
leaves empty (UniProt, Reactome). Or it *adds* data that HumanMine did not have (for example
Ensembl and PubMed). The generated additions include every class the mappings use that is not in
InterMine's core model, because removing a stock source also removes the classes it declared. The
generated priorities are HumanMine's own, with each replacing source in the place of the source
it replaces. A final check fails on an unknown field, a link whose type does not fit, two columns
that write one field of one object, or data that a replaced stock source loaded and its
replacement does not, unless that gap is accepted with a reason.

## Scope and the demonstration build

A build can be limited to species and to a list of genes without editing the mapping: the limit
is applied to a copy of the mapping when the queries are generated. Each source names the field
that identifies its genes, and a live lookup translates gene symbols into that source's own
identifiers (NCBI Gene or Ensembl). Where the source data breaks an integration key that
HumanMine assumes, a configured rule decides which object keeps the value. If the rule cannot
decide, no object keeps it. For example, 255 Ensembl identifiers are each claimed by two or more
genes in NCBI Gene; the identifier stays only on a gene that is the one protein-coding claimant.

The demonstration build used a panel of 113 human genes involved in food and drug metabolism, in
seven groups from drug-metabolizing enzymes to taste and appetite receptors. NCBI Gene and
Reactome were loaded in full. HGNC, Ensembl, UniProt, ClinVar and the GWAS Catalog were limited
to the panel, and PubMed to the publications that the other sources cite. The mine was an
InterMine 5 build of HumanMine, served with its database, web application and BlueGenes in
containers on one machine.

# Results

<!-- TODO -->

# Discussion

<!-- TODO -->

## Acknowledgements

<!-- TODO: other acknowledgements (DBCLS, BH26JP organizers, funding). -->

We used Claude (Anthropic) as a programming and writing assistant during this project.
<!-- TODO: agree the exact wording and scope of this statement among the authors. -->

```{=latex}
\AtEndDocument{%
```

# Appendices

<!-- TODO, or remove this section and the LaTeX wrapper around it -->

```{=latex}
}
```
