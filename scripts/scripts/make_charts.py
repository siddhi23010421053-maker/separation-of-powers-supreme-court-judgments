import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data.csv"

COLORS = {
    "main": "#173d37",
    "gold": "#c69b58",
    "muted": "#9aa59f",
    "grid": "#dedfd5",
    "text": "#172b2a",
}


def load_rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def finish_chart(fig, path):
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="#fffefa")
    plt.close(fig)


def make_year_chart(rows):
    years = ["2021", "2022", "2023", "2024", "2025", "2026"]
    counts = Counter(row["Year"] for row in rows)
    labels = ["2021
(from 1 Sep)", "2022", "2023", "2024", "2025", "2026
(to 31 Aug)"]
    values = [counts[year] for year in years]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    bars = ax.bar(labels, values, color=COLORS["main"], width=0.62)
    ax.set_title("Case summaries by year", loc="left", color=COLORS["text"], fontsize=18, pad=18)
    ax.set_ylabel("Number of cases", color=COLORS["text"])
    ax.set_ylim(0, max(values, default=0) + 2)
    ax.yaxis.grid(True, color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(axis="y", length=0, colors=COLORS["text"])
    ax.tick_params(axis="x", colors=COLORS["text"])
    ax.bar_label(bars, padding=4, color=COLORS["text"], fontsize=10, fontweight="bold")
    fig.text(0.01, 0.01, "Year labels follow the project case list.", color=COLORS["muted"], fontsize=8)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    finish_chart(fig, ROOT / "chart1-per-year.png")


def make_category_chart(rows, field, categories, title, filename):
    counts = Counter(row[field] or "CHECK" for row in rows)
    labels = [*categories, "CHECK"]
    values = [counts[label] for label in labels]
    colors = [COLORS["gold"] if label == "CHECK" else COLORS["main"] for label in labels]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    bars = ax.bar(labels, values, color=colors, width=0.66)
    ax.set_title(title, loc="left", color=COLORS["text"], fontsize=18, pad=18)
    ax.set_ylabel("Number of cases", color=COLORS["text"])
    ax.set_ylim(0, max(values, default=0) + 2)
    ax.yaxis.grid(True, color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(axis="y", length=0, colors=COLORS["text"])
    ax.tick_params(axis="x", colors=COLORS["text"], rotation=12)
    ax.bar_label(bars, padding=4, color=COLORS["text"], fontsize=10, fontweight="bold")
    fig.text(0.01, 0.01, "CHECK marks a field to complete in the dataset.", color=COLORS["muted"], fontsize=8)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    finish_chart(fig, ROOT / filename)


def main():
    rows = load_rows()
    make_year_chart(rows)
    make_category_chart(
        rows,
        "Outcome",
        ["Allowed", "Dismissed", "Partly allowed", "Other"],
        "Recorded case outcomes",
        "chart2-outcome.png",
    )
    make_category_chart(
        rows,
        "Who won",
        ["Individual", "Company", "State or public body", "Association or NGO", "Mixed or unclear"],
        "Recorded prevailing party",
        "chart3-who-won.png",
    )
    print(f"Generated three charts from {len(rows)} rows in {CSV_PATH.name}.")


if __name__ == "__main__":
    main()
