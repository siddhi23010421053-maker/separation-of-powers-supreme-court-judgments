import csv
import html
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data.csv"

COLORS = {
    "background": "#fffefa",
    "ink": "#172b2a",
    "main": "#173d37",
    "gold": "#c69b58",
    "muted": "#78847f",
    "grid": "#e6e5dc",
    "track": "#f0efe8",
}


def load_rows():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    if not rows:
        raise ValueError(f"No data rows found in {CSV_PATH.name}.")
    return rows


def make_chart(title, labels_and_values, path, note, highlight_check=False):
    row_height = 48
    chart_left = 350
    chart_width = 530
    row_top = 150
    chart_bottom = row_top + len(labels_and_values) * row_height
    height = chart_bottom + 78
    max_value = max((value for _, value in labels_and_values), default=0)
    axis_max = max(5, math.ceil(max_value / 5) * 5)
    tick_values = sorted({round(axis_max * index / 4) for index in range(5)})

    chart_title = html.escape(title)
    description = html.escape(
        "; ".join(f"{label}: {value}" for label, value in labels_and_values)
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 {height}" '
        f'role="img" aria-labelledby="chart-title chart-description">',
        f"<title id=\"chart-title\">{chart_title}</title>",
        f'<desc id="chart-description">{description}</desc>',
        f'<rect width="960" height="{height}" rx="8" fill="{COLORS["background"]}"/>',
        f'<text x="44" y="46" fill="{COLORS["muted"]}" font-family="Arial, sans-serif" '
        'font-size="18" font-weight="700" letter-spacing="1.5">DATASET SNAPSHOT</text>',
        f'<text x="44" y="82" fill="{COLORS["ink"]}" font-family="Arial, sans-serif" '
        f'font-size="36" font-weight="700">{chart_title}</text>',
        f'<text x="44" y="108" fill="{COLORS["muted"]}" font-family="Arial, sans-serif" '
        'font-size="20">Number of cases</text>',
    ]

    if highlight_check:
        parts.extend(
            [
                f'<rect x="790" y="30" width="12" height="12" rx="3" fill="{COLORS["gold"]}"/>',
                f'<text x="809" y="41" fill="{COLORS["muted"]}" font-family="Arial, sans-serif" '
                'font-size="18">CHECK field</text>',
            ]
        )

    for tick in tick_values:
        x = chart_left + chart_width * tick / axis_max
        parts.extend(
            [
                f'<line x1="{x:.1f}" y1="{row_top - 13}" x2="{x:.1f}" '
                f'y2="{chart_bottom - 8}" stroke="{COLORS["grid"]}" stroke-width="1"/>',
                f'<text x="{x:.1f}" y="{chart_bottom + 20}" text-anchor="middle" '
                f'fill="{COLORS["muted"]}" font-family="Arial, sans-serif" '
                f'font-size="18">{tick}</text>',
            ]
        )

    for index, (label, value) in enumerate(labels_and_values):
        center_y = row_top + index * row_height + row_height / 2
        bar_width = chart_width * value / axis_max
        fill = COLORS["gold"] if highlight_check and label == "CHECK" else COLORS["main"]
        parts.extend(
            [
                f'<text x="44" y="{center_y + 5:.1f}" fill="{COLORS["ink"]}" '
                'font-family="Arial, sans-serif" font-size="26">'
                f'{html.escape(label)}</text>',
                f'<rect x="{chart_left}" y="{center_y - 10:.1f}" width="{chart_width}" '
                f'height="20" rx="10" fill="{COLORS["track"]}"/>',
                f'<rect x="{chart_left}" y="{center_y - 10:.1f}" width="{bar_width:.1f}" '
                f'height="20" rx="10" fill="{fill}"/>',
                f'<text x="{chart_left + bar_width + 12:.1f}" y="{center_y + 5:.1f}" '
                f'fill="{COLORS["ink"]}" font-family="Arial, sans-serif" '
                f'font-size="20" font-weight="700">{value}</text>',
            ]
        )

    parts.extend(
        [
            f'<text x="44" y="{height - 20}" fill="{COLORS["muted"]}" '
            'font-family="Arial, sans-serif" font-size="18">'
            f'{html.escape(note)}</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def main():
    rows = load_rows()
    year_counts = Counter(row.get("Year", "").strip() for row in rows)
    make_chart(
        "Case summaries by year",
        [
            ("2021 (from 1 Sep)", year_counts["2021"]),
            ("2022", year_counts["2022"]),
            ("2023", year_counts["2023"]),
            ("2024", year_counts["2024"]),
            ("2025", year_counts["2025"]),
            ("2026 (to 31 Aug)", year_counts["2026"]),
        ],
        ROOT / "chart1-per-year.svg",
        "Year labels follow the project case list.",
    )
    make_chart(
        "Recorded case outcomes",
        list(Counter(row.get("Outcome", "").strip() or "CHECK" for row in rows).items()),
        ROOT / "chart2-outcome.svg",
        "CHECK marks an outcome to complete in the dataset.",
        highlight_check=True,
    )
    make_chart(
        "Recorded prevailing party",
        list(Counter(row.get("Who won", "").strip() or "CHECK" for row in rows).items()),
        ROOT / "chart3-who-won.svg",
        "CHECK marks a prevailing-party field to complete in the dataset.",
        highlight_check=True,
    )
    print(f"Generated three SVG charts from {len(rows)} rows in {CSV_PATH.name}.")


if __name__ == "__main__":
    main()
