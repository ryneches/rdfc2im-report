#!/usr/bin/env python3
"""Draw the report's figures into paper/.

Usage: python3 tools/make_figures.py
Needs matplotlib. Writes paper/figure1-pipeline.pdf (vector, fonts embedded) and a PNG preview.

Figure 1: the rdfc2im pipeline - the four steps from the domestic hackathon workflow (models, map,
extract, load), the inputs each takes, the files each writes, and the curator's loop.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paper"

matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "pdf.fonttype": 42,          # embed TrueType, keep text selectable
})

INK = "#222222"
MUTED = "#555555"
STEP_FILL = "#e8eef6"
STEP_EDGE = "#3b5b86"
INPUT_FILL = "#f4f4f4"
INPUT_EDGE = "#888888"
OUT_FILL = "#e9f3ea"
OUT_EDGE = "#3d7a45"
CUR_FILL = "#fdf3e1"
CUR_EDGE = "#a8741a"


def box(ax, x, y, w, h, fill, edge, lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=fill, ec=edge, lw=lw))


def arrow(ax, p, q, color=INK, style="-|>", ls="-", rad=0.0, lw=0.9):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=8, color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=1, shrinkB=1))


def step(ax, x, y, w, h, number, title, command, lines):
    box(ax, x, y, w, h, STEP_FILL, STEP_EDGE, lw=1.2)
    ax.text(x + 0.08, y + h - 0.12, f"{number}  {title}", ha="left", va="top",
            fontsize=11, fontweight="bold", color=STEP_EDGE)
    ax.text(x + 0.08, y + h - 0.42, command, ha="left", va="top", family="DejaVu Sans Mono",
            fontsize=8.5, color=INK)
    ax.text(x + 0.08, y + h - 0.70, "\n".join(lines), ha="left", va="top", color=INK,
            linespacing=1.35)


def labelled(ax, x, y, w, h, fill, edge, title, lines, title_color):
    box(ax, x, y, w, h, fill, edge)
    ax.text(x + 0.08, y + h - 0.10, title, ha="left", va="top", fontweight="bold",
            color=title_color)
    ax.text(x + 0.08, y + h - 0.34, "\n".join(lines), ha="left", va="top", color=MUTED,
            linespacing=1.3)


def figure1():
    fig = plt.figure(figsize=(7.2, 4.2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 7.2)
    ax.set_ylim(0, 4.2)
    ax.axis("off")

    # ---- the four steps (middle row)
    sy, sh, sw = 1.30, 1.62, 1.62
    xs = [0.10, 1.90, 3.70, 5.50]

    # ---- inputs (top row), each directly above the step it feeds
    iy, ih = 3.22, 0.90
    labelled(ax, xs[0], iy, sw, ih, INPUT_FILL, INPUT_EDGE, "rdf-config models",
             ["one per dataset, from", "dbcls/rdf-config"], INK)
    labelled(ax, xs[1], iy, sw, ih, INPUT_FILL, INPUT_EDGE, "HumanMine config",
             ["model, keys,", "project.xml, priorities"], INK)
    labelled(ax, xs[2], iy, xs[3] + sw - xs[2], ih, INPUT_FILL, INPUT_EDGE, "SPARQL endpoints",
             ["RDF Portal: NCBI Gene, HGNC, GO, UniProt,", "Reactome, ClinVar, PubMed, Ensembl", "TogoVar: GWAS Catalog"], INK)

    step(ax, xs[0], sy, sw, sh, "1", "Models", "(every command)",
         ["InterMine model of", "HumanMine's sources", "", "rdf-config", "subject tree"])
    step(ax, xs[1], sy, sw, sh, "2", "Map", "translate",
         ["class and field per", "subject, predicate", "status + basis", "tables, links", "(SSSOM files)"])
    step(ax, xs[2], sy, sw, sh, "3", "Extract", "translate fetch tsv",
         ["a query per table;", "key required,", "the rest OPTIONAL", "paging / key batches", "clean TSV"])
    step(ax, xs[3], sy, sw, sh, "4", "Load", "items project check",
         ["Items XML", "project.xml, keys,", "additions, priorities", "check"])
    for a, b in zip(xs, xs[1:]):
        arrow(ax, (a + sw, sy + sh / 2), (b, sy + sh / 2), color=STEP_EDGE, lw=1.3)

    # ---- inputs feed the steps: short, straight, no crossings
    arrow(ax, (xs[0] + sw / 2, iy), (xs[0] + sw / 2, sy + sh), color=INPUT_EDGE)
    arrow(ax, (xs[1] + 0.30, iy), (xs[0] + sw - 0.25, sy + sh), color=INPUT_EDGE)
    arrow(ax, (xs[2] + sw / 2, sy + sh), (xs[2] + sw / 2, iy), color=INPUT_EDGE, style="<|-|>")

    # ---- curator loop under Map
    cx, cy, cw, ch = 1.25, 0.10, 2.90, 0.95
    labelled(ax, cx, cy, cw, ch, CUR_FILL, CUR_EDGE, "Curator",
             ["edits mapping files and rules;", "stock converters are the reference;", "a three-way merge keeps the edits"], CUR_EDGE)
    arrow(ax, (xs[1] + sw / 2, sy), (xs[1] + sw / 2, cy + ch), color=CUR_EDGE, style="<|-|>")

    # ---- the running mine
    mx, my, mw, mh = 4.45, 0.10, 2.67, 0.95
    labelled(ax, mx, my, mw, mh, OUT_FILL, OUT_EDGE, "HumanMine (InterMine)",
             ["build and integrate; web", "application, REST API, BlueGenes"], OUT_EDGE)
    arrow(ax, (xs[3] + sw / 2, sy), (xs[3] + sw / 2, my + mh), color=OUT_EDGE, lw=1.3)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "figure1-pipeline.pdf")
    fig.savefig(OUT / "figure1-pipeline.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    figure1()
    print("wrote paper/figure1-pipeline.pdf and .png")
