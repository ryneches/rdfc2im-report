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

<!-- TODO -->

# Results

<!-- TODO -->

# Discussion

<!-- TODO -->

## Acknowledgements

<!-- TODO -->

```{=latex}
\AtEndDocument{%
```

# Appendices

<!-- TODO, or remove this section and the LaTeX wrapper around it -->

```{=latex}
}
```
