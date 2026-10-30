import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data.csv").open(encoding="utf-8-sig", newline="") as source:
    rows = list(csv.DictReader(source))

GREEN, GOLD, GRID = "#173d37", "#c69b58", "#dedfd5"


def save_bars(labels, values, title, ylabel, filename, partial=()):
    fig, ax = plt.subplots(figsize=(9, 4.8))
    bars = ax.bar(labels, values, color=[GOLD if label in partial else GREEN for label in labels])
    ax.set_title(title, loc="left", fontsize=18, color=GREEN, pad=18)
    ax.set_ylabel(ylabel, color=GREEN)
    ax.set_ylim(0, max(values, default=0) + 2)
    ax.yaxis.grid(True, color=GRID, linewidth=.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="both", length=0, colors=GREEN)
    ax.bar_label(bars, padding=4, color=GREEN, fontsize=10, fontweight="bold")
    fig.tight_layout()
    fig.savefig(ROOT / filename, dpi=200, bbox_inches="tight", facecolor="#fffefa")
    plt.close(fig)


years = ["2021", "2022", "2023", "2024", "2025", "2026"]
year_counts = Counter(row["Year"] for row in rows)
save_bars(["2021 (from 1 Sep)", "2022", "2023", "2024", "2025", "2026 (to 31 Aug)"], [year_counts[y] for y in years], "Case summaries by year", "Number of cases", "chart1-per-year.png")
for field, categories, title, filename in [
    ("Outcome", ["Allowed", "Dismissed", "Partly allowed", "Other", "CHECK"], "Recorded case outcomes", "chart2-outcome.png"),
    ("Who won", ["Individual", "Company", "State or public body", "Association or NGO", "Mixed or unclear", "CHECK"], "Recorded prevailing party", "chart3-who-won.png"),
]:
    counts = Counter(row[field] or "CHECK" for row in rows)
    save_bars(categories, [counts[x] for x in categories], title, "Number of cases", filename, partial=("CHECK",))
print(f"Generated three charts from {len(rows)} rows.")
