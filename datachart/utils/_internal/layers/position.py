"""Draw-position layers: image and basemap."""

import warnings
from collections import defaultdict
from typing import List
import numpy as np
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from ..basemap import load_basemap, load_country_codes
from ..colors import get_colormap
from ..validate import (
    BASEMAP_FEATURES,
    BASEMAP_FILLED,
    validate_basemap_availability,
    validate_basemap_features,
    validate_basemap_geometry,
    validate_basemap_highlight,
    validate_basemap_source,
    validate_image,
    validate_image_extent,
)
from ..config_helpers import get_image_style, get_basemap_style
from ....constants import BASEMAP_FEATURE, BASEMAP_RESOLUTION, DRAW_POSITION
from .base import Layer

# an image's or basemap's rung (ADR 0054, 0060, 0062): below under the
# gridlines (0.5), above over the marks (3) and under the reference lines
DRAW_ZORDER = {DRAW_POSITION.BELOW: 0.25, DRAW_POSITION.ABOVE: 3.25}


def draw_zorder_key(position: str) -> str:
    """An image's or basemap's key in a Panel overlay's zorder table."""

    return f"draw_{position}"


def _split_outlines(rows: np.ndarray) -> List[np.ndarray]:
    """The outlines of `NaN`-separated rows; empty ones dropped."""

    breaks = np.flatnonzero(np.isnan(rows).any(axis=1))
    parts = np.split(rows, breaks)
    return [part[np.isfinite(part).all(axis=1)] for part in parts if len(part)]


def _filled_path(outlines: List[np.ndarray]) -> Path:
    """One compound path of closed rings; a ring wound the other way is a hole."""

    rings = [ring for ring in outlines if len(ring) >= 3]
    vertices = np.concatenate([np.vstack([ring, ring[:1]]) for ring in rings])
    codes = np.concatenate(
        [
            [Path.MOVETO] + [Path.LINETO] * (len(ring) - 1) + [Path.CLOSEPOLY]
            for ring in rings
        ]
    )
    return Path(vertices, codes)


class DrawPositionLayer(Layer):
    """A layer that carries no series, on the rung its `DRAW_POSITION` picks.

    Takes no cycle color, no legend entry and no emphasis (ADR 0054, 0060).
    """

    takes_color = False
    position: str = DRAW_POSITION.DEFAULT

    @property
    def zorder_key(self) -> str:
        return draw_zorder_key(self.position)

    def rung(self, ctx) -> float:
        """The layer's zorder: its position's rung unless the panel set one."""

        return DRAW_ZORDER[self.position] if ctx.z_order is None else ctx.z_order


class ImageLayer(DrawPositionLayer):
    """A picture stretched over its extent in data coordinates (ADR 0060)."""

    # the picture fills its extent; the axes end where it does
    ticks_at_axis_ends = False

    kind = "image"

    def _resolve_style(self):
        data = self.chart.get("data") or {}
        self.image = validate_image(data.get("image"))
        self.extent = validate_image_extent(data.get("extent"))
        self.position = self.settings.get("position") or DRAW_POSITION.DEFAULT
        style = get_image_style(self.style)
        if self.image.ndim == 2:
            style["cmap"] = get_colormap(style["cmap"])
            style["vmin"] = self.settings.get("vmin")
            style["vmax"] = self.settings.get("vmax")
        else:
            # an RGB(A) picture carries its own colors
            style.pop("cmap", None)
        self.image_style = style

    def value_data(self):
        return np.array(self.extent[2:])

    def category_data(self):
        return np.array(self.extent[:2])

    def draw(self, ax, ctx):
        z_order = self.rung(ctx)
        ax.imshow(
            self.image,
            extent=self.extent,
            origin="upper",
            zorder=z_order,
            **self.image_style,
        )
        # imshow pins the view to the extent; earlier marks must count too
        ax.autoscale_view()


class BasemapLayer(DrawPositionLayer):
    """Coastlines, land, borders, lakes, rivers and roads in longitude and
    latitude (ADR 0062).

    Composed with data it leaves the limits to the data; alone it frames its
    own outlines.
    """

    kind = "basemap"

    def _resolve_style(self):
        data = self.chart.get("data") or {}
        geometry = data.get("geometry")
        validate_basemap_source(
            data.get("features"),
            geometry,
            data.get("resolution"),
            data.get("highlight"),
        )
        self.highlight = ()
        if geometry is None:
            features = validate_basemap_features(data.get("features"))
            resolution = data.get("resolution") or BASEMAP_RESOLUTION.DEFAULT
            validate_basemap_availability(features, resolution)
            outlines = [(f, load_basemap(f, resolution)) for f in features]
            self.highlight = validate_basemap_highlight(data.get("highlight"), features)
            if BASEMAP_FEATURE.COUNTRIES in features:
                self.country_codes = load_country_codes(resolution)
                self._warn_missing_countries(resolution)
        else:
            outlines = validate_basemap_geometry(geometry)
        # bottom up, the caller's order kept within one feature
        self.outlines = sorted(outlines, key=lambda o: BASEMAP_FEATURES.index(o[0]))
        self.position = self.settings.get("position") or DRAW_POSITION.DEFAULT
        self.feature_style = get_basemap_style(self.style)
        lakes = self.feature_style[BASEMAP_FEATURE.LAKES]
        lakes.setdefault("facecolor", self.ground)

    def _warn_missing_countries(self, resolution: str) -> None:
        """Warn about highlighted codes the map at this scale does not draw."""

        missing = sorted(set(self.highlight) - set(self.country_codes))
        if missing:
            warnings.warn(
                f"The basemap at 1:{resolution} draws no country coded "
                f"{missing}: too small at this scale, or not a Natural Earth "
                "ADM0_A3 code. A finer `resolution` may draw it."
            )

    def _draw_countries(self, ax, rows, z_order) -> list:
        """One patch per country, so an enclave keeps its own fill.

        Returns the paths of the highlighted countries, for their outline.
        """

        style = self.feature_style[BASEMAP_FEATURE.COUNTRIES]
        rings = defaultdict(list)
        for code, ring in zip(self.country_codes, _split_outlines(rows)):
            rings[code].append(ring)
        codes = list(rings)
        faces = [
            style["highlight"] if code in self.highlight else style["facecolor"]
            for code in codes
        ]
        paths = [_filled_path(rings[code]) for code in codes]
        ax.add_collection(
            PatchCollection(
                [PathPatch(path) for path in paths],
                facecolors=faces,
                edgecolors="none",
                zorder=z_order,
            ),
            autolim=False,
        )
        return [path for code, path in zip(codes, paths) if code in self.highlight]

    def bounds(self) -> tuple:
        """The `(xmin, xmax, ymin, ymax)` the outlines span."""

        rows = np.concatenate([rows for _, rows in self.outlines])
        rows = rows[np.isfinite(rows).all(axis=1)]
        (x0, y0), (x1, y1) = rows.min(axis=0), rows.max(axis=0)
        return float(x0), float(x1), float(y0), float(y1)

    def draw(self, ax, ctx):
        z_order = self.rung(ctx)
        highlighted = []
        for feature, rows in self.outlines:
            if feature == BASEMAP_FEATURE.COUNTRIES:
                highlighted = self._draw_countries(ax, rows, z_order)
                continue
            outlines = _split_outlines(rows)
            style = self.feature_style[feature]
            # a basemap never widens the view; a lone one frames it in render
            if feature in BASEMAP_FILLED:
                # add_artist, unlike add_patch, leaves the data limits alone
                ax.add_artist(
                    PathPatch(
                        _filled_path(outlines),
                        edgecolor="none",
                        zorder=z_order,
                        **style,
                    )
                )
            else:
                ax.add_collection(
                    LineCollection(outlines, zorder=z_order, **style), autolim=False
                )
        edge = self.feature_style[BASEMAP_FEATURE.COUNTRIES]
        if highlighted and edge.get("edge_width"):
            # added last, so the borders and the coastline never cross it
            ax.add_collection(
                PatchCollection(
                    [PathPatch(path) for path in highlighted],
                    facecolors="none",
                    edgecolors=edge["edge_color"],
                    linewidths=edge["edge_width"],
                    zorder=z_order,
                ),
                autolim=False,
            )
