"""Converts the Natural Earth 1:110m outlines into the bundled basemap arrays.

Downloads the GeoJSON of the four features from the Natural Earth release
repository and writes `natural_earth_110m.npz` with the conversion the finer
resolutions go through on first use. Needs only numpy and the standard
library.

Run from the repo root: python datachart/charts/_basemap/generate.py
"""

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from datachart.constants import BASEMAP_RESOLUTION
from datachart.utils._internal.basemap import BUNDLED, LAYERS, fetch


def main():
    arrays = {}
    for name in LAYERS:
        rows, codes = fetch(name, BASEMAP_RESOLUTION.LOW)
        arrays[name] = rows
        print(f"{name}: {len(rows)} rows")
        if name == "countries":
            arrays[f"{name}_codes"] = codes
    np.savez_compressed(BUNDLED, **arrays)
    print(f"{BUNDLED.name}: {BUNDLED.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
