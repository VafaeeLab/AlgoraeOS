"""Regenerate the README figures (light and dark variants) from the dataset.

Usage:  python scripts/make_figures.py
Writes assets/figures/*.svg and assets/vafaee_lab_logo_dark.png.
"""
import collections
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "assets", "figures")

THEMES = {
    "light": {"series": "#2a78d6", "text": "#1f2328", "muted": "#59636e", "grid": "#d1d9e0"},
    "dark": {"series": "#3987e5", "text": "#f0f6fc", "muted": "#9198a1", "grid": "#3d444d"},
}
METRICS = [("synergy_loewe", "Loewe"), ("synergy_bliss", "Bliss"), ("synergy_hsa", "HSA"), ("synergy_zip", "ZIP")]
TISSUE_LABELS = {
    "haematopoietic_and_lymphoid": "Blood & lymphoid",
    "large_intestine": "Large intestine",
    "urinary_tract": "Urinary tract",
    "soft_tissue": "Soft tissue",
}


def load():
    cells = {r["drugcomb_cell_line_id"]: r for r in csv.DictReader(open(os.path.join(DATA, "cell_lines.csv"), encoding="utf-8"))}
    scores = {m: [] for m, _ in METRICS}
    by_tissue = collections.Counter()
    lines_by_tissue = collections.defaultdict(set)
    with open(os.path.join(DATA, "AlgoraeOS_DrugComb_curated_synergy.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            for m, _ in METRICS:
                scores[m].append(float(r[m]))
            t = cells[r["cell_line_id"]]["tissue"] or "unknown"
            by_tissue[t] += 1
            lines_by_tissue[t].add(r["cell_line_id"])
    return scores, by_tissue, lines_by_tissue


def style(ax, th):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(th["grid"])
    ax.tick_params(colors=th["muted"], labelsize=9, length=0)


def synergy_figure(scores, th, path):
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.6), sharey=True)
    bins = list(range(-100, 101, 5))
    for ax, (m, label) in zip(axes, METRICS):
        v = scores[m]
        ax.hist(v, bins=bins, color=th["series"], edgecolor="none", rwidth=0.82)
        ax.axvline(0, color=th["muted"], lw=0.8, ls=(0, (3, 3)))
        style(ax, th)
        ax.set_title(label, color=th["text"], fontsize=11, fontweight="bold", loc="left")
        ax.set_xlim(-100, 100)
        ax.set_xticks([-100, -50, 0, 50, 100])
        ax.yaxis.grid(True, color=th["grid"], lw=0.6)
        ax.set_axisbelow(True)
        pos = 100 * sum(x > 10 for x in v) / len(v)
        ax.text(0.98, 0.92, f"{pos:.1f}% > 10", transform=ax.transAxes, ha="right", va="top", color=th["muted"], fontsize=9)
    axes[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{int(y / 1000)}k"))
    axes[0].set_ylabel("Combinations", color=th["muted"], fontsize=9)
    fig.supxlabel("Synergy score (negative = antagonistic, positive = synergistic)", color=th["muted"], fontsize=9, y=0.02)
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


def tissue_figure(by_tissue, lines_by_tissue, th, path):
    items = by_tissue.most_common()[::-1]
    names = [TISSUE_LABELS.get(t, t.replace("_", " ").capitalize()) for t, _ in items]
    vals = [n for _, n in items]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    bars = ax.barh(names, vals, color=th["series"], height=0.68)
    style(ax, th)
    ax.spines["bottom"].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(axis="y", colors=th["text"], labelsize=9.5)
    for bar, (t, n) in zip(bars, items):
        k = len(lines_by_tissue[t])
        ax.text(bar.get_width() + max(vals) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{n:,}  ·  {k} cell line{'s' if k > 1 else ''}", va="center", color=th["muted"], fontsize=8.5)
    ax.set_xlim(0, max(vals) * 1.28)
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


def dark_logo():
    """Vafaee Lab logo with its black lettering turned white for dark backgrounds."""
    src = Image.open(os.path.join(ROOT, "assets", "vafaee_lab_logo.png")).convert("RGBA")
    px = src.load()
    w, h = src.size
    for x in range(w):
        for y in range(h):
            r, g, b, a = px[x, y]
            if r > 235 and g > 235 and b > 235:  # white background -> transparent
                px[x, y] = (255, 255, 255, 0)
            elif max(r, g, b) - min(r, g, b) < 25 and max(r, g, b) < 140:  # grey/black lettering -> white
                px[x, y] = (240, 246, 252, a)
    src.save(os.path.join(ROOT, "assets", "vafaee_lab_logo_dark.png"), optimize=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})
    scores, by_tissue, lines_by_tissue = load()
    for name, th in THEMES.items():
        synergy_figure(scores, th, os.path.join(OUT, f"synergy_distributions_{name}.svg"))
        tissue_figure(by_tissue, lines_by_tissue, th, os.path.join(OUT, f"tissue_coverage_{name}.svg"))
    dark_logo()
    print("figures written to", OUT)


if __name__ == "__main__":
    main()
