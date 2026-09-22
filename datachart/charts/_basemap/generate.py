"""Converts the Natural Earth 1:110m outlines into the bundled basemap arrays.

Downloads the GeoJSON of the four features from the Natural Earth release
repository and writes `natural_earth_110m.npz`: one float32 `(n, 2)` array of
longitude and latitude per feature, a `NaN` row between one outline and the
next. Polygon rings are oriented so a filled path draws their holes: exteriors
counter-clockwise, holes clockwise. Needs only numpy and the standard library.

Run from the repo root: python datachart/charts/_basemap/generate.py
"""

import json
import pathlib
import urllib.request

import numpy as np

# a tagged release, so a rerun reproduces the committed bundle
SOURCE = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "v5.1.2/geojson/ne_110m_{}.geojson"
)
# bundled feature name -> Natural Earth layer
LAYERS = {
    "coastline": "coastline",
    "land": "land",
    # land boundaries only: a country outline would redraw the coastline
    "borders": "admin_0_boundary_lines_land",
    "lakes": "lakes",
}
OUTPUT = pathlib.Path(__file__).resolve().parent / "natural_earth_110m.npz"


def signed_area(ring: np.ndarray) -> float:
    """Twice the ring's signed area; positive when counter-clockwise."""

    x, y = ring[:, 0], ring[:, 1]
    return float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def outlines(geometry: dict) -> list:
    """The geometry's outlines as arrays, polygon rings oriented and unclosed."""

    kind, coords = geometry["type"], geometry["coordinates"]
    if kind == "LineString":
        return [np.array(coords)]
    if kind == "MultiLineString":
        return [np.array(line) for line in coords]
    polygons = [coords] if kind == "Polygon" else coords
    rings = []
    for polygon in polygons:
        for i, ring in enumerate(polygon):
            ring = np.array(ring)[:-1]
            # exterior counter-clockwise, holes clockwise
            if (signed_area(ring) > 0) != (i == 0):
                ring = ring[::-1]
            rings.append(ring)
    return rings


def convert(layer: str) -> np.ndarray:
    """One Natural Earth layer as `NaN`-separated float32 lon/lat rows."""

    with urllib.request.urlopen(SOURCE.format(layer)) as response:
        collection = json.load(response)
    parts = []
    for feature in collection["features"]:
        for outline in outlines(feature["geometry"]):
            parts += [outline[:, :2], np.full((1, 2), np.nan)]
    return np.concatenate(parts[:-1]).astype(np.float32)


def main():
    arrays = {name: convert(layer) for name, layer in LAYERS.items()}
    np.savez_compressed(OUTPUT, **arrays)
    for name, array in arrays.items():
        print(f"{name}: {len(array)} rows")
    print(f"{OUTPUT.name}: {OUTPUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
