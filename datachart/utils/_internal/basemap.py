"""The basemap outlines, fetched from Natural Earth on first use into a
local cache (ADR 0061, 0062).

Every set is a float32 `(n, 2)` array of longitude and latitude per feature,
a `NaN` row between one outline and the next. Polygon rings are oriented so
a filled path draws their holes: exteriors counter-clockwise, holes
clockwise. The countries also carry one Natural Earth `ADM0_A3` code per
ring.
"""

import functools
import json
import os
import pathlib
import tempfile
import urllib.request

import numpy as np

from ...constants import BASEMAP_RESOLUTION
from .validate import BASEMAP_FEATURE_RESOLUTIONS, BASEMAP_RESOLUTIONS

# a tagged release, so every download converts the same outlines
SOURCE = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "v5.1.2/geojson/ne_{resolution}_{layer}.geojson"
)
# feature name -> Natural Earth layer
LAYERS = {
    "coastline": "coastline",
    "land": "land",
    "countries": "admin_0_countries",
    # land boundaries only: a country outline would redraw the coastline
    "borders": "admin_0_boundary_lines_land",
    "lakes": "lakes",
    "rivers": "rivers_lake_centerlines",
    "roads": "roads",
}
# the key of a country: ISO_A3 is -99 for France and Norway, this never is
COUNTRY_KEY = "ADM0_A3"
CACHE_ENV = "DATACHART_CACHE_DIR"
# 1:10m roads is a 50 MB GeoJSON; 60 s does not finish it (ADR 0062)
DOWNLOAD_TIMEOUT = 300


def cache_dir() -> pathlib.Path:
    """Where the downloaded resolutions are kept."""

    configured = os.environ.get(CACHE_ENV)
    if configured:
        return pathlib.Path(configured)
    base = os.environ.get("XDG_CACHE_HOME") or pathlib.Path.home() / ".cache"
    return pathlib.Path(base) / "datachart"


def _signed_area(ring: np.ndarray) -> float:
    """Twice the ring's signed area; positive when counter-clockwise."""

    x, y = ring[:, 0], ring[:, 1]
    return float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def _outlines(geometry: dict) -> list:
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
            if (_signed_area(ring) > 0) != (i == 0):
                ring = ring[::-1]
            rings.append(ring)
    return rings


def convert(collection: dict) -> tuple:
    """A GeoJSON feature collection as `NaN`-separated float32 lon/lat rows,
    and the country code of each outline ("" where a feature has none)."""

    parts, codes = [], []
    for feature in collection["features"]:
        code = (feature.get("properties") or {}).get(COUNTRY_KEY) or ""
        for outline in _outlines(feature["geometry"]):
            parts += [outline[:, :2], np.full((1, 2), np.nan)]
            codes.append(code)
    rows = np.concatenate(parts[:-1]).astype(np.float32)
    return rows, np.array(codes, dtype="U3")


def fetch(feature: str, resolution: str) -> tuple:
    """Download one Natural Earth layer and convert it."""

    url = SOURCE.format(resolution=resolution, layer=LAYERS[feature])
    try:
        with urllib.request.urlopen(url, timeout=DOWNLOAD_TIMEOUT) as response:
            return convert(json.load(response))
    except (OSError, ValueError, KeyError) as error:
        raise RuntimeError(
            f"Cannot download the 1:{resolution} basemap {feature!r} from {url}: "
            f"{error}. A basemap needs the network once per feature and scale; "
            f"after that it is read from {cache_dir()}."
        ) from error


@functools.lru_cache(maxsize=None)
def load_outlines(feature: str, resolution: str) -> dict:
    """One feature's `rows` and `codes`, downloaded into the cache once."""

    path = cache_dir() / f"natural_earth_{resolution}_{feature}.npz"
    if not path.exists():
        rows, codes = fetch(feature, resolution)
        path.parent.mkdir(parents=True, exist_ok=True)
        # written aside and renamed, so an interrupted write leaves no half file
        with tempfile.NamedTemporaryFile(
            dir=path.parent, suffix=".npz", delete=False
        ) as partial:
            np.savez_compressed(partial, rows=rows, codes=codes)
        os.replace(partial.name, path)
    with np.load(path) as cached:
        return {"rows": cached["rows"].astype(float), "codes": cached["codes"]}


def load_basemap(feature: str, resolution: str = BASEMAP_RESOLUTION.LOW) -> np.ndarray:
    """One feature as `(n, 2)` lon/lat rows, `NaN` between outlines."""

    return load_outlines(feature, resolution)["rows"]


def load_country_codes(resolution: str = BASEMAP_RESOLUTION.LOW) -> np.ndarray:
    """The `ADM0_A3` code of each country outline, in outline order."""

    return load_outlines("countries", resolution)["codes"]


def prewarm(resolution: str) -> list:
    """Cache every feature Natural Earth publishes at the scale, so later
    maps need no network; returns the features."""

    features = [
        feature
        for feature in LAYERS
        if resolution in BASEMAP_FEATURE_RESOLUTIONS.get(feature, BASEMAP_RESOLUTIONS)
    ]
    for feature in features:
        load_outlines(feature, resolution)
    return features
