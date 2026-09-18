# rdfc2im report

The BioHackrXiv report for [rdfc2im](https://github.com/intermineorg/rdfc2im), a tool that
translates RDF Portal data (described by DBCLS rdf-config) into InterMine items and loads it into
a HumanMine build.

The report is `paper/paper.md`, with references in `paper/paper.bib`. CI builds
`paper/paper.pdf` on every push to `main`.

This repository is also mounted as the optional `report/` submodule of rdfc2im. To fetch it
there:

```sh
git submodule update --init --checkout report
```

## License

[CC-BY 4.0](LICENSE).
