#!/usr/bin/env python3
"""Draw the report's figures into paper/.

Usage: python3 tools/make_figures.py
Needs matplotlib. Writes each figure as a vector PDF (fonts embedded) and a PNG preview.

Figure 1 (figure1-ecosystem): how a mine gets its data today, and with RDF Portal and rdfc2im -
which steps are custom or shared, manual or automatic, and where provenance lives.
Figure 2 (figure2-pipeline): the rdfc2im pipeline - the four steps from the domestic hackathon
workflow (models, map, extract, load), the inputs each takes, and the curator's loop.
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


def figure_pipeline():
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
    fig.savefig(OUT / "figure2-pipeline.pdf")
    fig.savefig(OUT / "figure2-pipeline.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 1: the ecosystem
CUSTOM_FILL, CUSTOM_EDGE = "#fbe3d2", "#b5561c"     # custom code, one per source
CURATED_FILL, CURATED_EDGE = "#fdf3e1", "#a8741a"   # curated data, one per source
SHARED_FILL, SHARED_EDGE = STEP_FILL, STEP_EDGE      # shared infrastructure or generic tool
PROV_INK = "#3d3d3d"


def pill(ax, x, y, text, edge):
    """A small tag at (x, y) = its left edge and vertical centre.  Returns its right edge."""
    tx = ax.text(x, y, text, ha="left", va="center", fontsize=7.5, color=edge,
                 bbox=dict(boxstyle="round,pad=0.22,rounding_size=0.3", fc="white", ec=edge, lw=0.8))
    r = ax.figure.canvas.get_renderer()
    bb = tx.get_window_extent(r).transformed(ax.transData.inverted())
    return bb.x1 + 0.03          # the text's right edge plus the box padding


def eco_box(ax, x, y, w, h, fill, edge, title, lines, tags):
    box(ax, x, y, w, h, fill, edge, lw=1.1)
    ax.text(x + 0.08, y + h - 0.10, title, ha="left", va="top", fontweight="bold", color=edge,
            fontsize=9.5)
    ax.text(x + 0.08, y + h - 0.36, "\n".join(lines), ha="left", va="top", color=INK,
            fontsize=8.5, linespacing=1.3)
    tx = x + 0.10
    for tag in tags:
        tx = pill(ax, tx, y + 0.16, tag, edge) + 0.10


def figure_ecosystem():
    W, H = 7.2, 5.3
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    def panel_title(y, text):
        ax.text(0.10, y, text, ha="left", va="center", fontsize=10.5, fontweight="bold", color=INK)

    def provenance(y, lines):
        ax.text(0.10, y, "Provenance:", ha="left", va="top", fontsize=8.5, fontweight="bold",
                color=PROV_INK)
        ax.text(1.02, y, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=PROV_INK,
                linespacing=1.3)

    # (a) today --------------------------------------------------------------
    panel_title(5.13, "(a)  HumanMine today")
    ay, ah = 3.50, 1.30
    eco_box(ax, 0.10, ay, 1.75, ah, INPUT_FILL, INPUT_EDGE, "Data providers",
            ["NCBI Gene, HGNC,", "UniProt, GO, ClinVar,", "GWAS Catalog, ..."], ["own formats"])
    for k in (2, 1):                                   # a stack: one loader per source
        box(ax, 2.25 + 0.07 * k, ay + 0.07 * k, 2.60, ah, CUSTOM_FILL, CUSTOM_EDGE, lw=0.8)
    eco_box(ax, 2.25, ay, 2.60, ah, CUSTOM_FILL, CUSTOM_EDGE, "One loader per source",
            ["a Java converter or a format", "parser, written and maintained", "by the mine's developers"],
            ["per source", "manual", "code"])
    eco_box(ax, 5.25, ay, 1.85, ah, OUT_FILL, OUT_EDGE, "HumanMine",
            ["integrated database,", "web application,", "REST API"], [])
    arrow(ax, (1.85, ay + ah / 2), (2.25, ay + ah / 2), color=INK, lw=1.2)
    arrow(ax, (5.00, ay + ah / 2), (5.25, ay + ah / 2), color=INK, lw=1.2)
    provenance(3.32, ["a DataSet for each loader; how each value was derived",
                      "is written in that loader's Java code"])

    ax.plot([0.10, W - 0.10], [2.82, 2.82], color="#bbbbbb", lw=0.8)

    # (b) this work ----------------------------------------------------------
    panel_title(2.64, "(b)  With RDF Portal and rdfc2im")
    by, bh = 1.12, 1.30
    eco_box(ax, 0.10, by, 1.30, bh, INPUT_FILL, INPUT_EDGE, "Providers",
            ["the same", "data"], [])
    eco_box(ax, 1.60, by, 1.95, bh, SHARED_FILL, SHARED_EDGE, "RDF Portal",
            ["RDF and an rdf-config", "model for each dataset;", "review; SPARQL"],
            ["per dataset", "template", "reused"])
    eco_box(ax, 3.75, by, 1.80, bh, SHARED_FILL, SHARED_EDGE, "rdfc2im",
            ["one tool for all sources:", "queries, items, mine", "configuration"],
            ["shared", "automatic"])
    eco_box(ax, 5.75, by, 1.35, bh, OUT_FILL, OUT_EDGE, "HumanMine",
            ["stock loader,", "no new Java"], [])
    for x0, x1 in ((1.40, 1.60), (3.55, 3.75), (5.55, 5.75)):
        arrow(ax, (x0, by + bh / 2), (x1, by + bh / 2), color=INK, lw=1.2)

    # the curated mapping feeds rdfc2im from below
    my_, mh_ = 0.08, 0.80
    eco_box(ax, 3.75, my_, 3.35, mh_, CURATED_FILL, CURATED_EDGE, "Curated mapping",
            ["one file per source; every row records its evidence"],
            ["per source", "manual", "data"])
    arrow(ax, (4.65, my_ + mh_), (4.65, by), color=CURATED_EDGE, lw=1.1)
    provenance(0.86, ["reviewed RDF Portal dataset", "\u2192 mapping row (status,", "evidence) \u2192 item"])

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "figure1-ecosystem.pdf")
    fig.savefig(OUT / "figure1-ecosystem.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    figure_ecosystem()
    figure_pipeline()
    print("wrote paper/figure1-ecosystem and paper/figure2-pipeline (.pdf, .png)")
