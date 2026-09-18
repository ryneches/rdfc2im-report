# Handoff: finishing the report

For Gos, from Russell (18 Sep 2026). Every section of `paper/paper.md` has a first draft. What is
left needs the demo mine on your machine, your unpushed rdfc2im work, and co-author input.

## Where things are

- `paper/paper.md`: the report. `grep -n TODO paper/paper.md` lists every open item; each is
  also below.
- `notes/commit-history.md`: the rdfc2im history, annotated commit by commit, with a collected
  Future Work list at the end. The report is built from it.
- `notes/report-plan.md`: the themes, what goes in which section, what was left out, and why.
- `references.yaml` + `tools/make_bib.py`: the bibliography. Never edit `paper/paper.bib`; add a
  work to `references.yaml` (key, DOI) and run `python3 tools/make_bib.py`.
- `tools/make_figures.py`: draws Figures 1 and 2 into `paper/`. Edit the script and re-run; do not
  edit the images.
- Two git-ignored folders exist only on Russell's machine: `CHECKLIST.md` (the template's
  instructions) and `background/` (source PDFs and summaries). Not needed to finish; ask if
  wanted.

Build the PDF locally with the image CI uses (first pull is about 1.8 GB):

```sh
podman run --rm -v "$PWD":/work:Z -w /work ghcr.io/biohackrxiv/bhxiv-gen-pdf:master gen-pdf paper
```

Or push: CI builds the PDF on every push and attaches it to the Actions run as an artifact. The PDF
is not committed.

The report repository is the `report/` submodule of rdfc2im (`git submodule update --init
--checkout report`). After each report commit, commit the new `report` pointer in rdfc2im too.

## Writing rules we followed

- Approach describes the final design, not the history. A decision that was later reversed goes
  in Discussion only if it makes a conceptual point.
- Every number is checked against the record (`LOAD-TRIAL.md`, `STATUS.md`, or the mine). Where
  there is no record, leave a TODO rather than a guess.
- The report is a proof of concept on a 113-gene panel, not a replacement for HumanMine. Keep
  claims scoped that way.
- Plain, short sentences; define InterMine terms in the glossary.

## Steps

### 1. Bring in your unpushed work

Push or merge your rdfc2im updates first. If they change facts the report states (counts, fixes,
open problems), update Results (Tables 2 and 3), Discussion and Future Work to match. Optionally
add the new commits to `notes/commit-history.md`.

### 2. Checks on the demo mine

1. **Item counts** for HGNC, Ensembl, UniProt and ClinVar: Table 2 (`paper.md`, the TODO cells).
2. **UniProt's endpoint.** The generated queries name `https://rdfportal.org/sib/sparql`, but the
   `sources.yaml` comment and `data_source_url` (from `1a5db72`) say sparql.uniprot.org. Find out
   which was used. If it was sparql.uniprot.org, change Table 2, the Inputs paragraph in Approach,
   and the endpoint box in `tools/make_figures.py` (Figure 2); if it was RDF Portal, fix the
   `sources.yaml` comment and URL in rdfc2im. Then remove the TODO in Approach.
3. **The 7 panel symbols** that HGNC's lookup did not resolve (`9a563af` reports 106 of 113): which
   ones, and are those genes in the mine through NCBI Gene? One sentence in Results if relevant.

### 3. Figure 3: the screenshot

The BlueGenes report page for **CYP2D6**, showing data from as many sources as fit: NCBI Gene and
HGNC identifiers, the Ensembl id, the UniProt protein, ClinVar alleles, GWAS results and
publications. It supports the Results sentence "The BlueGenes report page for a panel gene shows
data from every source on one page", and it is the one figure all readers will understand.

Save it as `paper/figure3-cyp2d6.png` and replace the TODO comment in Results with:

```markdown
![One gene assembled from seven sources: the BlueGenes report page for CYP2D6 in the demonstration
mine. \label{fig:cyp2d6}](figure3-cyp2d6.png){ width=100% }
```

and change "(Figure 3)" in the text to "(Figure \ref{fig:cyp2d6})".

### 4. Co-author items

- **Katayama-san and Kawashima-san:** review the Discussion paragraph "What a translator needs
  from an rdf-config model", and Figure 1's tags for RDF Portal (*per dataset*, *template*,
  *reused*): do they describe how rdf-config models are made and used?
- **Affiliations** (YAML header): Kawashima-san's ORCID lists ROIS / National Institute of
  Genetics, the header uses DBCLS; yours uses Department of Genetics, Cambridge (your ORCID lists
  none). The BH26 site also expands DBCLS as "Database Division for Life Science"; use whichever
  name is current.
- **CRediT roles** (`role:` per author) and **`group`** (now `rdfc2im`): optional; fill in or leave.
- **Acknowledgements:** agree the Claude statement, and add DBCLS, the BH26JP organizers and
  funding.
- **Where the project started:** the Abstract says rdfc2im was developed at BH26JP; the design
  came from the earlier domestic hackathon. Credit it in the Introduction or Abstract if wanted.
- **Appendices:** the section is empty. Fill it (a source table with endpoints and roles, and
  pointers to `LOAD-TRIAL.md`, `STATUS.md` and the commit notes) or delete it with the LaTeX
  wrapper around it.

### 5. Shorten

The draft is 11 pages; the aim was about 6. Candidates, largest first:

- **Drop Figure 2** (the pipeline). Figure 1 carries the main message, and Approach already
  describes the steps. If dropped, delete it from `paper.md`, its call in `make_figures.py`, and the
  cross-reference in Approach.
- **Trim Table 3** (13 rows) to the 8 or so that make distinct points; the rest are in
  `LOAD-TRIAL.md`.
- **Merge Discussion subsections**: "Identity" with "Replacing a pipeline", and "Public SPARQL
  endpoints" with "A mine is built, not edited".
- **Shorten the glossary** to the terms a biologist would not know.
- **Figure 1's small text**: the tags are about 5.5 pt on the page. Reduce the canvas width in
  `figure_ecosystem()` (now 7.2 in) or cut words, then re-run the script.

### 6. Finish

1. `grep -n TODO paper/paper.md` returns nothing.
2. Regenerate: `python3 tools/make_bib.py` and `python3 tools/make_figures.py`.
3. Build the PDF and read it through, especially page 1 (author block) and the tables.
4. Push the report repository, then the `report` pointer in rdfc2im.
5. Submit: download the PDF from the CI run and submit it through BioHackrXiv's portal on OSF
   (see https://index.biohackrxiv.org/for-submitters/). The meeting is `BH26JP`.
