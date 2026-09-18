# Report plan: themes and triage

Working plan for turning `commit-history.md` into the report. The history is chronological; the
report is organized by theme. This file decides what goes where, and what is left out.

## Audiences (in priority order)

1. **Practitioners**: biologists, bioinformaticians and the staff who support them, who may try to
   do the same. They need the final workflow, what is reliable, what is not, and where the traps
   are. The report is one step in a living literature: say clearly what is done, what is a demo,
   and what is open, so that nobody builds on a claim we did not make.
2. **BioHackathon attendees**: what we did and why, clearly structured. Useful as an example of how
   to report hackathon work.
3. **DBCLS board and program officers**: whether something useful was done that serves the aims of
   the program. Readable from that angle without pandering: every claim true and scoped.

## Key themes

The notes reduce to eleven themes. The first column says where each goes.

| # | Theme | Where | Core content |
|---|---|---|---|
| T1 | The idea: a mine built from RDF described by rdf-config, with the mapping as data | Introduction (done) | Why: HumanMine's per-source loaders, its release stalled at Feb 2022; RDF Portal's reviewed datasets and rdf-config models |
| T2 | How the mapping works | **Approach** | rdf-config model walked from its root; class and field chosen by a fixed precedence; every column an attribute, every link an explicit `via`; one table per multi-valued branch; only the key is required in SPARQL |
| T3 | How curation works | **Approach** + Discussion | The stock HumanMine converter is the reference; every row has a status and a basis; decisions live in `knowledge.yaml`; SSSOM files and a three-way merge keep the curator's edits. Finding: term URIs gave 15 of 243 rules, stock converters 89 |
| T4 | Identity and merging | **Results** (main lesson) + Approach (final rules) | Most real failures were about which key an object merges on: IRI-guessed keys, one key per class, classes with no curated key, genes without an organism, upstream keys that are not unique (D14), ClinVar AlleleID vs VCV, GWASResult with no key |
| T5 | Fitting into an existing mine | **Approach** + Discussion | Source roles (replace, alongside, add); replacement check with accepted gaps; carrying model classes; generated priorities; reducing HumanMine's config for a subset |
| T6 | Working against real SPARQL endpoints | Approach (final fetch strategy, short) + Discussion | Sorted-row limits (200,000; TogoVar 10,000), keyset paging returned wrong results, `VALUES` batching was reliable; IRI vs literal values |
| T7 | The shape of real RDF data | Results + Discussion | OWL structure inside OBO data (blank nodes, properties), multi-valued comments, rdf-config example values read as predicates, flattened blank nodes, "NR" in numeric fields, an empty `mapped_genes`, a mixed `part_of` |
| T8 | How problems were found | Results + Discussion | `check` passed before every real-load failure; each stage (small fetch, full extract, load, use) found a new class of problem; an outside count found the Reactome duplication |
| T9 | The demo mine | **Results** | What was loaded (numbers), what works (search, templates, widgets), what does not and why |
| T10 | InterMine operations | Discussion (one paragraph) + Future Work | A mine is built, not edited; loader bugs (non-ASCII); postprocessing and Solr; build not scripted |
| T11 | How the software was developed | **Approach** (one paragraph) + Discussion | The first version was generated with Claude from the hackathon specification; every later commit was made with Claude Code and reviewed by the authors; see "Decisions needed" |

## Triage

### In the report

**Approach** (about 1-1.5 pages; final design only):

- A figure: the four-step pipeline (models, map, extract, load) with the files each step reads and
  writes. The slides are the starting point.
- Inputs: rdf-config models from `dbcls/rdf-config`; data from RDF Portal endpoints (and TogoVar
  for the GWAS Catalog); HumanMine's model, keys, priorities and `project.xml`.
- Mapping (T2): precedence as two short ordered lists; statuses; `via`; tables; key-only
  required SPARQL. One example, end to end (a Gene and its synonyms).
- Curation (T3): the stock-converter rule; basis; SSSOM; three-way merge.
- Extraction: paging, then key batching past the endpoint's row limit; cleaning (filter before
  transform; required = key).
- Loading (T4, T5): Items XML (why not delimited files, one sentence); item identity; generated
  additions, keys and priorities; source roles; `check`.
- Build scope and the demo build: species and gene-list limits; the 113-gene panel; which source
  loaded how much.
- Development (T11): one honest paragraph.

**Results**:

- A table of the sources in the demo build: endpoint, role, scope, items loaded.
- Curation outcome: rows by status (124 sure, 64 guess, 38 todo, 309 drop).
- What real loads found, as one table grouped by theme (T4, T6, T7): problem, example, fix.
  About 10 rows, not 90.
- The running mine: search, templates, widgets; what is empty and why.

**Discussion**:

- Term URIs were not enough; the stock converters were the real specification (T3).
- rdf-config models document shapes as well as structure; what a translator needs that they do
  not say (identifier fields, which examples are alternatives) (T7). Constructive, as input to
  rdf-config.
- Identity is the hard part of integration (T4).
- Replacing an established pipeline piece by piece (T5).
- Public endpoints: completeness and correctness must be checked (T6).
- A mine is built, not edited; so the build should be scripted (T10).
- Development with an AI assistant: what worked, what needed human checks (T11).
- **Future Work** (subsection): 6-8 bullets drawn from the collected list.

### Left out (the commit history is the record)

- Packaging details: gradle project name, `resources/` directory, version pin, `fork-sync`.
- Transport bugs: redirect handling, Host header, GET fallback.
- Environment problems: the mounted file system, the stalled index build, container restarts,
  the Postgres connection limit.
- The trial stack in detail (ports, staging script, BlueGenes jars): one sentence plus a pointer
  to `LOAD-TRIAL.md`.
- Each individual curation decision (per field, per source).
- Manual database repairs in the trial mine (tracker rows, orphan rows): one sentence in
  Discussion (T10).
- The Solr n-gram fix, the batch-size benchmark numbers, the LinkML schema.
- Superseded rules, unless they make a conceptual point (the ClinVar identifier and the keyset
  paging are the two that do).

### Possible appendix

- Source table with rdf-config name, endpoint, role, and replaced stock source.
- Pointers: repository, `LOAD-TRIAL.md`, `STATUS.md`, `SPEC-DECISIONS.md`, this history.

## For the third audience, without pandering

The facts that matter to them, stated plainly in the normal flow of the report:

- The work uses Japanese national infrastructure (RDF Portal, rdf-config, TogoVar) to rebuild a
  widely used UK resource (HumanMine) whose public releases stopped in February 2022.
- It is an international collaboration (Kyoto University, DBCLS, University of Cambridge) that
  began at the 2026 domestic hackathon and reached a working mine at BH26JP.
- It shows RDF Portal's review guidelines and rdf-config models doing what they were designed
  for: letting a third party reuse the data automatically.
- It is a proof of concept on a 113-gene panel, not a replacement for HumanMine. The open work is
  listed.

## Decisions needed

1. **Development with Claude (T11).** The first version was generated by Claude from the
   specification ("the mostly working tarfile generated by Claude"), the slides credit Claude.ai,
   and every later commit is co-authored with Claude Code. Practitioners and the board both need
   to know this to judge the work. Proposed: one factual paragraph in Approach (how the code was
   made and reviewed) and one in Discussion (what the AI did well, where human checks and real
   loads were essential). How much do you want to say?
2. **Length.** Proposed about 6 pages: Introduction 0.75, Approach 1.5, Results 1.5, Discussion
   and Future Work 1.5, plus references.
3. **Figure.** One pipeline figure (redrawn from slide 2), and possibly a small diagram of one
   rdf-config subject becoming Gene, Synonym and Publication items. Agree?
4. **Terms.** Practitioners may not know InterMine's vocabulary (source, items XML, integration
   key, priorities). Proposed: define each at first use, in a sentence, rather than a glossary.
