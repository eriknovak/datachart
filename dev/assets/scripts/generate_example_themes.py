"""Generates docs/assets/imgs/example-themes.png — the same grouped bar chart
under every predefined theme, tiled two rows deep, for the README.

Each theme renders its own figure so the theme's fonts and furniture apply
whole; the tiles are then pasted side by side.

Run from the repo root: python docs/assets/scripts/generate_example_themes.py
"""

import io
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.charts import BarChart
from datachart.config import config
from datachart.constants import THEME

OUT = pathlib.Path(__file__).resolve().parents[1] / "imgs" / "example-themes.png"
THEMES = [name for name in vars(THEME) if name.isupper()]
COLUMNS = 4
TILE = (5.0, 4.0)
DPI = 150

QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
REVENUE = {"North": [12, 19, 15, 22], "South": [9, 14, 18, 16], "West": [7, 11, 13, 20]}


def tile(theme):
    """The grouped bar chart under `theme`, as a raster of the tile size."""

    config.set_theme(getattr(THEME, theme))
    figure = BarChart(
        data=[
            [{"label": q, "y": y} for q, y in zip(QUARTERS, values)]
            for values in REVENUE.values()
        ],
        subtitle=list(REVENUE),
        show_legend=True,
        title=theme.capitalize(),
        xlabel="Quarter",
        ylabel="Revenue (M€)",
        figsize=TILE,
    )
    buffer = io.BytesIO()
    # no facecolor: a tile keeps the ground its theme sets (ADR 0058)
    figure.savefig(buffer, format="png", dpi=DPI)
    plt.close(figure)
    config.reset_config()
    return Image.open(buffer).convert("RGB")


def main():
    tiles = [tile(theme) for theme in THEMES]
    width, height = tiles[0].size
    rows = -(-len(tiles) // COLUMNS)
    sheet = Image.new("RGB", (width * COLUMNS, height * rows), "white")
    for i, image in enumerate(tiles):
        sheet.paste(image, ((i % COLUMNS) * width, (i // COLUMNS) * height))
    sheet.save(OUT)
    print(OUT.name, sheet.size)


if __name__ == "__main__":
    main()
