"""Grid layers: heatmap, calendar heatmap, contour, and hexbin."""

import math
from collections import defaultdict
from datetime import date, timedelta
from typing import Callable, List, Optional, Union
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator
from matplotlib.collections import LineCollection, PathCollection, PolyCollection
from matplotlib.colors import (
    CenteredNorm,
    LinearSegmentedColormap,
    TwoSlopeNorm,
    to_rgba_array,
)
from matplotlib.patches import Rectangle
from ..colors import get_colormap
from ..validate import (
    AXIS_TEMPORAL,
    validate_contour_levels,
    validate_filled_levels,
    validate_emphasis,
    validate_emphasis_rule,
    validate_two_slope_bounds,
)
from ..config_helpers import (
    get_heatmap_cmap,
    get_attr_value,
    resolve_font_family,
    get_heatmap_style,
    get_heatmap_font_style,
    get_heatmap_edge_style,
    get_calendar_month_line_style,
    get_contour_style,
    get_contour_label_style,
    get_hexbin_style,
    get_colorbar_setting,
    get_value_label_style,
)
from ...stats import iqr
from ....constants import (
    CALENDAR_WEEKDAY,
    COLORBAR_LOCATION,
    CONTOUR_LEVELS,
    HEXBIN_REDUCE,
    COLOR_NORM,
    ORIENTATION,
    AXIS_SCALE,
    VALUE_FORMAT,
)
from ....config import config
from .base import (
    COLORBAR_FRACTION,
    EMPHASIS_BACKGROUND,
    EMPHASIS_HIGHLIGHT,
    EMPHASIS_Z_OFFSET,
    HIGHLIGHT_WIDTH_SCALE,
    InkStroke,
    Layer,
    _fill_role,
    _format_value,
    _keep_role,
    _px_to_points,
    _scalar,
    _span_text,
    _step_label,
    _value_tab_bbox,
    axis_kind,
    emphasis_rule_roles,
    get_chart_data,
    resolve_show_values,
    step_edges,
    theme_default,
)
from .ticks import _column_tz, date_labels, to_date_numbers
from .bar import _LockedBarLocator

DEFAULT_VALUE_FORMAT = VALUE_FORMAT.DEFAULT


# cell luminance below which heatmap value text switches to white
HEATMAP_TEXT_DARK_LUMINANCE = 0.5


# the norms that hold `vcenter` in the middle of a diverging cmap (ADR 0056)
CENTRED_NORMS = (COLOR_NORM.CENTERED, COLOR_NORM.TWOSLOPE)


# the low end of a sequential cmap vanishes on white: iso-lines sample from here
CONTOUR_LINE_CMAP_START = 0.3


# the cmap sample that stands in for a cmap-colored contour in the legend
CONTOUR_SWATCH = 0.7


def get_chart_grid(chart: dict, kind: str, dtype=float) -> tuple:
    """The validated (x, y, z) of a gridded chart; x and y are None when absent."""

    z = get_chart_data("z", chart)
    if z is None:
        raise ValueError(f"A {kind} chart requires the `z` grid in `data`.")
    if isinstance(z, (list, tuple)) and all(isinstance(r, (list, tuple)) for r in z):
        for index, row in enumerate(z[1:], start=1):
            if len(row) != len(z[0]):
                raise ValueError(
                    f"The {kind} `z` grid is ragged: row {index} has {len(row)} "
                    f"value(s), row 0 has {len(z[0])}."
                )
    z = np.asarray(z, dtype=dtype)
    if z.ndim != 2:
        raise ValueError(
            f"The {kind} `z` attribute must be a 2-D grid, got {z.ndim} dimension(s)."
        )
    n_rows, n_cols = z.shape
    axes = []
    for attr, extent, name in (("x", n_cols, "column"), ("y", n_rows, "row")):
        values = get_chart_data(attr, chart)
        if values is not None:
            values = np.asarray(values)
            if values.ndim != 1 or len(values) != extent:
                raise ValueError(
                    f"The {kind} `{attr}` attribute must hold one value per {name} "
                    f"of `z` ({extent}), got {values.shape}."
                )
        axes.append(values)
    return axes[0], axes[1], z


COLORBAR_PAD = 0.03


def _draw_colorbar(
    ax: plt.Axes,
    mappable,
    setting: dict,
    aspect_locked: bool = False,
    centre: Optional[float] = None,
) -> None:
    """Draw a colorbar on the edge the resolved setting names (ADR 0035).

    `centre` is the value a centred norm holds fixed: the bar marks it
    alongside its even ticks, so the sign reads off the scale (ADR 0056).
    A `ticks` setting is the user's own list and replaces both.
    """

    colorbar = _place_colorbar(ax, mappable, setting, aspect_locked)
    fmt = _value_formatter(setting["format"])
    if fmt is not None:
        colorbar.formatter = fmt
        colorbar.update_ticks()
    ticks = setting["ticks"]
    if ticks is None and centre is not None:
        ticks = sorted(set(colorbar.get_ticks()) | {centre})
    if ticks is not None:
        # set_ticks widens the bar to every tick; keep it to the mapped range
        low, high = colorbar.vmin, colorbar.vmax
        slack = (high - low) * 1e-9
        colorbar.set_ticks([t for t in ticks if low - slack <= t <= high + slack])
    if setting["label"]:
        colorbar.set_label(setting["label"], **setting["label_style"])
    furniture = setting["furniture"]
    ticks_style = {"labelcolor": furniture["labelcolor"]}
    if furniture["color"] is not None:
        ticks_style["color"] = furniture["color"]
    colorbar.ax.tick_params(which="both", **ticks_style)
    if furniture["outline"] is not None:
        colorbar.outline.set_edgecolor(furniture["outline"])
    # tick labels take no family through tick_params; restyled directly
    family = setting["label_style"]["family"]
    for label in colorbar.ax.get_xticklabels() + colorbar.ax.get_yticklabels():
        label.set_fontfamily(family)


def _place_colorbar(ax: plt.Axes, mappable, setting: dict, aspect_locked: bool):
    """Place the bar on its edge and size it against the axes.

    The layout engine places it clear of titles and neighbouring axes; an
    aspect-locked axes instead carves it from its own box, which the engine
    would size to the grid cell rather than the box.
    """

    location, orientation = setting["location"], setting["orientation"]
    if not aspect_locked:
        # the layout engine keeps a colorbar at its own aspect (20:1 by
        # default), which shortens it beside a narrow axes: size it to the
        # axes slot instead
        bbox = ax.get_position()
        width, height = ax.figure.get_size_inches()
        along, across = bbox.height * height, bbox.width * width
        if orientation == ORIENTATION.HORIZONTAL:
            along, across = across, along
        return ax.figure.colorbar(
            mappable,
            ax=ax,
            location=location,
            fraction=COLORBAR_FRACTION,
            pad=COLORBAR_PAD,
            aspect=along / (across * COLORBAR_FRACTION),
        )
    cax = ax.inset_axes((0, 0, 1, 1))
    cax.set_axes_locator(_LockedBarLocator(ax, location))
    kwargs = {"orientation": orientation}
    if location == COLORBAR_LOCATION.LEFT:
        # a left bar reads outward; the other edges keep matplotlib's tick side
        kwargs["ticklocation"] = location
    return ax.figure.colorbar(mappable, cax=cax, **kwargs)


def _value_formatter(valfmt):
    """A value format as a matplotlib formatter; None keeps the default.

    Takes all `_format_value` takes, so ticks print as value labels do,
    with the typographic minus of matplotlib's own formatters.
    """

    if valfmt is None or isinstance(valfmt, mticker.Formatter):
        return valfmt
    return mticker.FuncFormatter(
        lambda value, _pos=None: mticker.Formatter.fix_minus(
            _format_value(valfmt, value)
        )
    )


def heatmap_cell_roles(chart: dict, z: list) -> list:
    """A copy of the heatmap's per-cell `emphasis` grid, aligned to `z`.

    Absent roles read as a grid of None; a grid of another shape, or a cell
    role that is not one, raises.
    """

    roles = chart["data"].get("emphasis") if isinstance(chart["data"], dict) else None
    if roles is None:
        return [[None] * len(row) for row in z]
    shape = [len(row) for row in z]
    if (
        not isinstance(roles, list)
        or [len(row) if isinstance(row, list) else -1 for row in roles] != shape
    ):
        raise ValueError(
            "The heatmap `emphasis` grid must hold one role per cell of `z` "
            f"({len(z)} rows of {shape[0] if shape else 0})."
        )
    return [
        [
            validate_emphasis(role, f"heatmap cell ({i}, {j}) `emphasis`")
            for j, role in enumerate(row)
        ]
        for i, row in enumerate(roles)
    ]


def _luminance(rgba) -> float:
    """The perceived brightness of a color, 0 (black) to 1 (white)."""

    r, g, b = rgba[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def colormap_scaling(chart: dict) -> dict:
    """The `norm`, `vmin` and `vmax` a colormapped draw call takes.

    A centred norm is an instance holding `vcenter` in the middle of the
    colormap and carrying the bounds itself: `centered` folds them into one
    half-range each side of `vcenter`, `twoslope` keeps them apart.
    Any other norm passes by name beside the bounds.
    """

    norm, vmin, vmax = chart.get("norm"), chart.get("vmin"), chart.get("vmax")
    if norm not in CENTRED_NORMS:
        return {"norm": norm, "vmin": vmin, "vmax": vmax}
    vcenter = chart.get("vcenter")
    vcenter = 0.0 if vcenter is None else vcenter
    if norm == COLOR_NORM.TWOSLOPE:
        validate_two_slope_bounds(vcenter, vmin, vmax)
        return {"norm": TwoSlopeNorm(vcenter, vmin, vmax)}
    halfrange = max(
        (abs(bound - vcenter) for bound in (vmin, vmax) if bound is not None),
        default=None,
    )
    return {"norm": CenteredNorm(vcenter, halfrange)}


class HeatmapLayer(Layer):
    ticks_at_axis_ends = False
    kind = "heatmap"
    overlayable = False
    # the theme keys the cells, values, and borders read
    style_prefix = "plot_heatmap"

    def _resolve_style(self):
        self.show_colorbar = self.settings.get("show_colorbar")
        self.colorbar = get_colorbar_setting(self.chart.get("colorbar"))
        self.colorbar_edge = self._colorbar_edge(self.show_colorbar)
        self.centred = self.chart.get("norm") in CENTRED_NORMS
        self.scaling = colormap_scaling(self.chart)
        self.vcenter = self.scaling["norm"].vcenter if self.centred else None
        # every centred norm maps its centre to the middle of the colormap
        self.step_centre = 0.5 if self.centred else None
        heatmap_style = get_heatmap_style(self.style, self.style_prefix, self.centred)
        heatmap_style["cmap"] = get_colormap(heatmap_style["cmap"])
        self.heatmap_style = heatmap_style
        self.font_style = get_heatmap_font_style(self.style, self.style_prefix)
        self.edge_style = get_heatmap_edge_style(self.style, self.style_prefix)
        self.frame_color = self.style.get(
            "plot_heatmap_frame_color",
            config.get("plot_heatmap_frame_color") or "#000000",
        )
        self.frame_width = config.get("axes_spines_width") or 0.8
        self._resolve_cell_values()
        x, y, self.z = self._grid()
        self.cell_roles = heatmap_cell_roles(self.chart, self.z)
        self.highlight_color = config["font_general_color"]
        self.date_axes = {
            axis
            for axis, labels in (("x", x), ("y", y))
            if axis_kind(labels) == AXIS_TEMPORAL
        }
        self._label_axes(x, y)

    def _resolve_cell_values(self) -> None:
        """The cell value switch, as set or the theme default, and its text."""

        self.show_cell_values = bool(resolve_show_values(self.settings))
        formatter = _value_formatter(
            self.chart.get("value_format", DEFAULT_VALUE_FORMAT)
        )
        self.cell_text = lambda value: formatter(value, None)

    def _grid(self) -> tuple:
        """The validated (x, y, z); x and y are None when not given, z lists."""

        x, y, z = get_chart_grid(self.chart, "heatmap", dtype=object)
        z = [[(np.nan if item is None else item) for item in row] for row in z]
        return x, y, z

    def _label_axes(self, x, y):
        # x/y default the tick attrs so the panel applies them like explicit
        # ones; cells are categories, so unnamed ones tick at their index
        chart = dict(self.chart)
        rows, cols = len(self.z), len(self.z[0]) if self.z else 0
        for axis, labels, count in (("x", x, cols), ("y", y, rows)):
            if chart.get(f"{axis}ticks") is not None:
                continue
            if labels is None:
                labels = list(range(count))
            chart[f"{axis}ticks"] = list(range(len(labels)))
            chart[f"{axis}ticklabels"] = chart.get(f"{axis}ticklabels") or (
                date_labels(labels, self.settings.get(f"{axis}ticks_format"))
                if axis_kind(labels) == AXIS_TEMPORAL
                else [str(label) for label in labels]
            )
        self.chart = chart

    def date_label_axes(self):
        return self.date_axes

    def target_extent(self, ax, point) -> Optional[float]:
        """Half the smaller side of the cell holding `point`, in points.

        `imshow` centers cell (row, col) on (col, row), so a point rounds
        to its cell and the borders sit half a unit out.
        """

        col, row = round(point[0]), round(point[1])
        n_rows, n_cols = len(self.z), len(self.z[0]) if self.z else 0
        if not (0 <= row < n_rows and 0 <= col < n_cols):
            return None
        value = self.z[row][col]
        # a blank cell (off the calendar year, or a gap) draws no mark
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return None
        corners = ax.transData.transform(
            [(col - 0.5, row - 0.5), (col + 0.5, row + 0.5)]
        )
        width, height = np.abs(corners[1] - corners[0])
        return _px_to_points(ax, min(width, height) / 2)

    def draw(self, ax, ctx):
        data = self.z

        # the panel owns the aspect; imshow's own "equal" would size the
        # colorbar to a box the panel then stretches
        im = ax.imshow(
            data,
            aspect="auto",
            **self.scaling,
            **self._cell_style(),
        )
        label = self.label(ctx)
        self.register_hover(im, lambda index: self._cell_datum(label, *index))
        if self.value_etch_steps:
            self._draw_cell_steps(ax, im)
        self._draw_cell_emphasis(ax)

        if self.show_cell_values:
            self._draw_cell_values(ax, im)

        if self.edge_style.get("linewidth"):
            self._draw_cell_borders(ax, len(data), len(data[0]))

        if self.show_colorbar and self.value_etch_steps:
            self._draw_even_step_legend(ax, im.norm, self.colorbar["label"])
        elif self.show_colorbar:
            _draw_colorbar(ax, im, self.colorbar, ctx.aspect_locked, self.vcenter)

        self._draw_frame(ax)

    def _draw_cell_steps(self, ax, im) -> None:
        """The cells as etched value steps over the image, left clear for hover."""

        im.autoscale_None()
        values = np.asarray(self.z, dtype=float)
        steps = value_steps(
            im.norm(np.ma.masked_invalid(values)),
            len(self.value_etch_steps),
            self.step_centre,
        )
        rows, cols = np.indices(values.shape)
        squares = np.array([[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5]])

        def cells(mask):
            centres = np.column_stack([cols[mask], rows[mask]])
            return PolyCollection([squares + centre for centre in centres])

        # a muted cell keeps its fade (ADR 0045)
        alpha = self._cell_style().get("alpha")
        alphas = np.broadcast_to(1.0 if alpha is None else alpha, values.shape)
        self._draw_value_steps(ax, steps, cells, im.get_zorder(), alphas)
        # an array: the image may already hold the per-cell fade array
        im.set_alpha(np.zeros(values.shape))

    def _cell_datum(self, label, row, col) -> dict:
        """The hover datum of a cell: the indices the tick labels name."""

        return {
            "label": label,
            "x": col,
            "y": row,
            "value": _scalar(self.z[row][col]),
        }

    def _draw_cell_values(self, ax, im) -> None:
        """Print each cell's value at its centre; a blank cell stays bare."""

        tab = get_value_label_style(self.style).get("tab")
        if self.value_etch_steps:
            im.autoscale_None()
            steps = value_steps(
                im.norm(np.ma.masked_invalid(np.asarray(self.z, dtype=float))),
                len(self.value_etch_steps),
                self.step_centre,
            )
        for i, row in enumerate(self.z):
            for j, value in enumerate(row):
                if np.isnan(value):
                    continue
                font_style = dict(self.font_style)
                # a faded cell is light whatever its value
                if (
                    self.cell_roles[i][j] != EMPHASIS_BACKGROUND
                    and _luminance(im.cmap(im.norm(value)))
                    < HEATMAP_TEXT_DARK_LUMINANCE
                ):
                    font_style["color"] = "#FFFFFF"
                if self.value_etch_steps:
                    # a value over the etching reads through a halo of the
                    # ground, or a tab where the etching is lines that cross it
                    font_style["color"] = self.font_style.get("color")
                    hatch = self.value_etch_steps[steps[i][j]][1]
                    if tab and set(hatch) & set("/\\x+|-"):
                        font_style["bbox"] = _value_tab_bbox(tab)
                    else:
                        font_style["path_effects"] = self.value_halo
                text = ax.text(
                    j, i, self.cell_text(value), ha="center", va="center", **font_style
                )
                self.register_limit_mark(text, j, i)

    def _cell_style(self) -> dict:
        """The image style; background cells fade to the muted alpha (ADR 0045).

        A fade rather than the muted color keeps a muted cell on the colormap
        and leaves the areas around the picked cells clean.
        """

        style = self.heatmap_style
        roles = self.cell_roles
        if not any(role == EMPHASIS_BACKGROUND for row in roles for role in row):
            return style
        alpha = 1.0 if style.get("alpha") is None else style["alpha"]
        faded = alpha * self.muted_alpha
        return {
            **style,
            "alpha": np.array(
                [
                    [faded if role == EMPHASIS_BACKGROUND else alpha for role in row]
                    for row in roles
                ]
            ),
        }

    def _draw_cell_emphasis(self, ax) -> None:
        """Outline the highlighted cells in the bolder highlight stroke."""

        width = HIGHLIGHT_WIDTH_SCALE * max(
            self.edge_style.get("linewidth") or 0, self.frame_width
        )
        for i, row in enumerate(self.cell_roles):
            for j, role in enumerate(row):
                if role != EMPHASIS_HIGHLIGHT:
                    continue
                ax.add_patch(
                    Rectangle(
                        (j - 0.5, i - 0.5),
                        1,
                        1,
                        facecolor="none",
                        edgecolor=self.highlight_color,
                        linewidth=width,
                        # over the cell borders, under the cell values
                        zorder=2,
                    )
                )

    def _draw_frame(self, ax) -> None:
        # heatmaps always draw a full frame, regardless of theme spine visibility
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(self.frame_color)
            spine.set_linewidth(self.frame_width)

    def _draw_cell_borders(self, ax, n_rows, n_cols):
        # imshow centers cell (i, j) on (j, i), so the boundaries sit at half-integers
        left, right = -0.5, n_cols - 0.5
        top, bottom = -0.5, n_rows - 0.5
        segments = [[(left, i + 0.5), (right, i + 0.5)] for i in range(n_rows - 1)]
        segments += [[(j + 0.5, top), (j + 0.5, bottom)] for j in range(n_cols - 1)]
        # autolim=False keeps the borders from widening the image's tight limits
        ax.add_collection(
            LineCollection(segments, zorder=1, **self.edge_style), autolim=False
        )


# calendar heatmap furniture (ADR 0044): month and weekday labels, in week order
MONTH_LABELS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# every other weekday is labelled: seven labels overlap at the default cell size
WEEKDAY_LABEL_STEP = 2


CALENDAR_MONTH_LINE_ZORDER = 2


def week_row(day: date, week_start: str) -> int:
    """The row of a day in a week column: 0 is the week start, 6 the day before it."""

    offset = 6 if week_start == CALENDAR_WEEKDAY.SUNDAY else 0
    return (day.weekday() - offset) % 7


def calendar_layout(
    year: int, week_start: str, first_month: int, last_month: int
) -> tuple:
    """The cell of every day of the months drawn: `(cells, n_weeks)`, cells as `(row, col)`.

    Columns are weeks, rows weekdays from the week start down; the days of
    the first and last week that fall outside the drawn months hold no cell.
    """

    first = date(year, first_month, 1)
    end = date(year + 1, 1, 1) if last_month == 12 else date(year, last_month + 1, 1)
    n_days = (end - first).days
    first_row = week_row(first, week_start)
    cells = {
        first + timedelta(days=i): divmod(first_row + i, 7)[::-1] for i in range(n_days)
    }
    return cells, (first_row + n_days + 6) // 7


def _resolve_flag(settings: dict, key: str, default: bool = True) -> bool:
    """A boolean setting; None takes the default."""

    value = settings.get(key)
    return default if value is None else bool(value)


class CalendarHeatmapLayer(HeatmapLayer):
    """One year of dated values as a weeks-by-weekdays grid of cells (ADR 0044).

    The cells, value labels, and colorbar are the heatmap's; the layer adds
    the year layout, month separators, and the month and weekday labels.
    The drawn range spans the months holding data, whole months at a time.
    """

    kind = "calendarheatmap"
    style_prefix = "plot_calendar_heatmap"

    def _resolve_style(self):
        self.week_start = (
            theme_default("calendarheatmap", self.settings, "week_start", self.style)
            or CALENDAR_WEEKDAY.DEFAULT
        )
        self.month_line_style = get_calendar_month_line_style(self.style)
        self.show_month_labels = _resolve_flag(self.settings, "show_month_labels")
        self.show_weekday_labels = _resolve_flag(self.settings, "show_weekday_labels")
        super()._resolve_style()

    def _resolve_cell_values(self) -> None:
        """The shared `show_values` and `value_format` vocabulary (ADR 0033)."""

        self.show_cell_values = resolve_show_values(self.settings)
        value_format = self.settings.get("value_format")
        self.value_format = (
            DEFAULT_VALUE_FORMAT if value_format is None else value_format
        )
        self.cell_text = lambda value: _format_value(self.value_format, value)

    def _grid(self) -> tuple:
        """The 7 x n_weeks grid of the months holding data; NaN off them and on missing days."""

        self.year = self.chart["year"]
        months = {day.month for day in self.chart["data"]["date"]}
        self.months = range(min(months), max(months) + 1)
        self.cells, n_weeks = calendar_layout(
            self.year, self.week_start, self.months[0], self.months[-1]
        )
        # python scalars, as the heatmap holds them: a whole number prints whole
        z = [[np.nan] * n_weeks for _ in range(7)]
        self.dates = {}
        data = self.chart["data"]
        for day, value in zip(data["date"], data["value"]):
            row, col = self.cells[day]
            self.dates[(row, col)] = day
            z[row][col] = np.nan if value is None else value
        return None, None, z

    def _label_axes(self, x, y):
        chart = dict(self.chart)
        chart["xticks"], chart["xticklabels"] = [], []
        chart["yticks"], chart["yticklabels"] = [], []
        if self.show_month_labels:
            # a month's label sits over the middle of its weeks
            spans = defaultdict(list)
            for day, (_, col) in self.cells.items():
                spans[day.month].append(col)
            chart["xticks"] = [
                (min(cols) + max(cols)) / 2 for _, cols in sorted(spans.items())
            ]
            chart["xticklabels"] = [MONTH_LABELS[month - 1] for month in self.months]
        if self.show_weekday_labels:
            start = 6 if self.week_start == CALENDAR_WEEKDAY.SUNDAY else 0
            chart["yticks"] = list(range(0, 7, WEEKDAY_LABEL_STEP))
            chart["yticklabels"] = [
                WEEKDAY_LABELS[(start + row) % 7] for row in chart["yticks"]
            ]
        self.chart = chart

    def _cell_datum(self, label, row, col) -> dict:
        day = self.dates.get((row, col))
        value = self.z[row][col]
        return {
            "label": label,
            "date": day.isoformat() if day is not None else None,
            "value": None if np.isnan(value) else _scalar(value),
        }

    def draw(self, ax, ctx):
        super().draw(ax, ctx)
        if self.month_line_style.get("linewidth"):
            self._draw_month_separators(ax)
        # the labels alone name the rows and columns
        ax.tick_params(which="both", length=0)

    def _draw_frame(self, ax) -> None:
        # the month separators and cell borders are the calendar's only lines
        for spine in ax.spines.values():
            spine.set_visible(False)

    def _draw_cell_borders(self, ax, n_rows, n_cols):
        # borders sit between two days of the year, never around the blank
        # cells the first and last week hold off the year
        segments = []
        for day, (row, col) in self.cells.items():
            if row < 6 and day + timedelta(days=1) in self.cells:
                segments.append([(col - 0.5, row + 0.5), (col + 0.5, row + 0.5)])
            if day + timedelta(days=7) in self.cells:
                segments.append([(col + 0.5, row - 0.5), (col + 0.5, row + 0.5)])
        ax.add_collection(
            LineCollection(segments, zorder=1, **self.edge_style), autolim=False
        )

    def _draw_month_separators(self, ax) -> None:
        """A stepped line along the left edge of every month but the first."""

        paths = []
        for month in self.months[1:]:
            row, col = self.cells[date(self.year, month, 1)]
            left, right = col - 0.5, col + 0.5
            if row == 0:
                paths.append([(left, -0.5), (left, 6.5)])
            else:
                paths.append(
                    [(right, -0.5), (right, row - 0.5), (left, row - 0.5), (left, 6.5)]
                )
        lines = LineCollection(
            paths, zorder=CALENDAR_MONTH_LINE_ZORDER, **self.month_line_style
        )
        lines.set_gid("month-separators")
        ax.add_collection(lines, autolim=False)


# rule-of-thumb level counts stay readable in this range (ADR 0022)
CONTOUR_LEVELS_MIN = 4


CONTOUR_LEVELS_MAX = 20


# the fd rule on a flat surface (IQR 0) has no bin width; match auto's density
CONTOUR_LEVELS_FLAT = 8


def contour_levels(
    z: List[List[Union[int, float]]], rule: Union[str, int, List[float], None]
) -> Union[List[float], int, None]:
    """Picks the contour levels of a 2-D grid by a rule of thumb.

    The rules of `CONTOUR_LEVELS` are evaluated on the per-axis resolution
    of the grid, `n = sqrt(cells)`: `"rice"` targets `2 * n ** (1/3)` levels
    and `"fd"` the value range over `2 * IQR * n ** (-1/3)`. The count is
    clamped to the 4–20 range and snapped to round values across the range of
    `z`. `"auto"` (or `None`) returns `None`, leaving the choice to
    matplotlib; an integer passes through and a list of level values comes
    back sorted and deduplicated.

    Args:
        z: The 2-D grid of values.
        rule: A rule of `CONTOUR_LEVELS`, a target level count, or an explicit
            list of level values.

    Returns:
        The level values, the target count, or `None` for the automatic rule.

    Raises:
        ValueError: If the rule is not one of `CONTOUR_LEVELS`, or the list
            is empty or holds a non-finite or non-numeric value.
    """
    if rule is None:
        return None
    if isinstance(rule, (int, np.integer)) and not isinstance(rule, bool):
        return rule
    if not isinstance(rule, str):
        return validate_contour_levels(rule)
    if rule == CONTOUR_LEVELS.AUTO:
        return None

    values = np.asarray(z, dtype=float).ravel()
    values = values[np.isfinite(values)]
    n = math.sqrt(values.size)
    if rule == CONTOUR_LEVELS.RICE:
        k = math.ceil(2 * n ** (1 / 3))
    else:
        h = 2 * iqr(values) * n ** (-1 / 3)
        k = math.ceil(np.ptp(values) / h) if h > 0 else CONTOUR_LEVELS_FLAT
    k = int(np.clip(k, CONTOUR_LEVELS_MIN, CONTOUR_LEVELS_MAX))
    ticks = MaxNLocator(nbins=k).tick_values(values.min(), values.max())
    return [float(t) for t in ticks]


# one layer for lines and fills, also the 2-D density chart (ADR 0022)
class ContourLayer(Layer):
    """A gridded surface drawn as iso-lines or filled bands."""

    ticks_at_axis_ends = False

    kind = "contour"

    def _resolve_style(self):
        self.fill = bool(self.settings.get("fill"))
        self.surface = self.fill
        self.show_labels = self.settings.get("show_labels")
        self.show_colorbar = self.settings.get("show_colorbar")
        self.colorbar = get_colorbar_setting(self.chart.get("colorbar"))
        self.colorbar_edge = self._colorbar_edge(self.fill and self.show_colorbar)
        style = get_contour_style(self.style)
        self.centred = self.chart.get("norm") in CENTRED_NORMS
        self.scaling = colormap_scaling(self.chart)
        self.vcenter = self.scaling["norm"].vcenter if self.centred else None
        cmap = style.pop("cmap")
        if self.centred:
            cmap = get_heatmap_cmap(self.style, "plot_contour", diverging=True)
        self.cmap = get_colormap(cmap)
        # lines take a pinned contour cmap only, past its washed-out low end
        self.line_cmap = None
        cmap_pinned = get_attr_value("plot_contour_cmap", self.style, config)
        if not self.fill and cmap_pinned is not None:
            self.line_cmap = LinearSegmentedColormap.from_list(
                f"{self.cmap.name}_lines",
                self.cmap(np.linspace(CONTOUR_LINE_CMAP_START, 1, 256)),
            )
        self.contour_style = style
        self.label_style = get_contour_label_style(self.style)
        # clabel takes no font family; the level labels are restyled after
        self.label_family = resolve_font_family()
        self.x, self.y, self.z = self._grid()
        # a grid of missing values alone draws nothing
        self.empty = not np.isfinite(self.z).any()
        if self.empty:
            self.levels, self.extend, self.band_edges = None, "neither", None
            return
        self.levels = contour_levels(self.z, self.settings.get("levels"))
        if self.fill:
            validate_filled_levels(self.levels)
        self.extend, self.band_edges = self._coverage()

    def _coverage(self) -> tuple:
        """How filled bands reach past explicit levels, and every band's edges.

        A surface beyond the list's ends fills in the end colors; each such
        overflow band spans from the end level to the surface extreme.
        """

        if not isinstance(self.levels, list):
            return "neither", None
        edges = list(self.levels)
        low, high = np.nanmin(self.z), np.nanmax(self.z)
        below, above = low < edges[0], high > edges[-1]
        if below:
            edges.insert(0, float(low))
        if above:
            edges.append(float(high))
        if below and above:
            return "both", edges
        return ("min" if below else "max" if above else "neither"), edges

    def _grid(self) -> tuple:
        """The validated (x, y, z) arrays; x and y default to the indices."""

        x, y, z = get_chart_grid(self.chart, "contour")
        n_rows, n_cols = z.shape
        self._x_kind = axis_kind(x)
        if x is None:
            x = np.arange(n_cols)
        elif self._x_kind == AXIS_TEMPORAL:
            self.x_tz = _column_tz(x)
            x = to_date_numbers(x)
        else:
            x = x.astype(float)
        y = np.arange(n_rows) if y is None else y.astype(float)
        return x, y, z

    def x_kind(self):
        return self._x_kind

    def value_data(self):
        return self.y

    def category_data(self):
        return None if self._x_kind == AXIS_TEMPORAL else self.x

    def y_range(self):
        return (float(self.y.min()), float(self.y.max()))

    def draw(self, ax, ctx):
        if self.empty:
            return
        style = dict(self.contour_style)
        if ctx.z_order is not None:
            style["zorder"] = ctx.z_order
        scaling = dict(self.scaling)
        label = self.label(ctx)

        if self.fill:
            for key in ("color", "linewidths", "linestyles"):
                style.pop(key, None)
            if ctx.emphasis == EMPHASIS_BACKGROUND:
                style["alpha"] = self.muted_alpha
            bands = ax.contourf(
                self.x,
                self.y,
                self.z,
                levels=self.levels,
                extend=self.extend,
                cmap=self.cmap,
                **scaling,
                **style,
            )
            # a legend proxy: the contour set itself carries no legend handle
            proxy = ax.fill_between(
                [], [], [], color=self.cmap(CONTOUR_SWATCH), label=label
            )
            edges = self.band_edges or list(bands.levels)
            self.register_hover(bands, self._level_resolver(bands, label, edges))
            if self.value_etch_steps:
                self._draw_relief(ax, ctx, bands, proxy, edges)
            elif self.show_colorbar:
                _draw_colorbar(
                    ax, bands, self.colorbar, ctx.aspect_locked, self.vcenter
                )
            return
        self._draw_lines(ax, ctx, self.show_labels, legend_proxy=True)

    def _draw_relief(self, ax, ctx, bands, proxy, edges) -> None:
        """Filled bands as a relief map: etched steps, then labelled level lines.

        A band takes the step of its middle value under the bands' norm; the
        legend merges consecutive bands that share a step, and the legend
        proxy wears the middle step. `edges` bound every drawn band.
        """

        levels = np.asarray(edges, dtype=float)
        middles = (levels[:-1] + levels[1:]) / 2
        n = len(self.value_etch_steps)
        bands.autoscale_None()
        steps = value_steps(bands.norm(middles), n)
        wash, hatch = self.value_etch_steps[n // 2]
        proxy.set(facecolor=wash, hatch=hatch or None)
        proxy.set_path_effects([self._etch_effect(1.0)])
        paths = bands.get_paths()

        def band_paths(mask):
            return PathCollection(
                [paths[i] for i in np.flatnonzero(mask)],
                transform=bands.get_transform(),
            )

        self._draw_value_steps(ax, steps, band_paths, bands.get_zorder())
        bands.set_alpha(0)
        self._draw_lines(ax, ctx, True, legend_proxy=False)
        if not self.show_colorbar:
            return
        entries = []
        for k, low, high in zip(steps, levels[:-1], levels[1:]):
            if entries and entries[-1][0] == k:
                entries[-1][2] = high
            else:
                entries.append([k, low, high])
        self._draw_step_legend(
            ax,
            [(k, _step_label(low, high)) for k, low, high in entries],
            self.colorbar["label"],
        )

    def _draw_lines(self, ax, ctx, show_labels, legend_proxy: bool) -> None:
        """The level lines, optionally labelled, with a legend proxy."""

        style = dict(self.contour_style)
        if ctx.z_order is not None:
            style["zorder"] = ctx.z_order
        scaling = dict(self.scaling)
        label = self.label(ctx)
        # a pinned line color beats the cmap; a muted background beats both
        by_level = (
            self.line_cmap is not None
            and "color" not in style
            and ctx.emphasis != EMPHASIS_BACKGROUND
        )
        style = self._merge_color("color", ctx.color, style)
        self._apply_emphasis(style, ctx.emphasis, width_key="linewidths")
        color = style.pop("color", None)
        if by_level:
            palette = {"cmap": self.line_cmap, **scaling}
            color = self.line_cmap(CONTOUR_SWATCH)
        else:
            palette = {"colors": [color]}
        lines = ax.contour(
            self.x, self.y, self.z, levels=self.levels, **palette, **style
        )
        if self.ink_stroke is not None:
            lines.set_path_effects([InkStroke(**self.ink_stroke)])
        self.register_hover(lines, self._level_resolver(lines, label))
        if legend_proxy:
            ax.plot(
                [],
                [],
                color=color,
                linewidth=style["linewidths"],
                linestyle=style["linestyles"],
                label=label,
            )
        if show_labels:
            label_style = dict(self.label_style)
            fmt = _value_formatter(self.chart.get("value_format"))
            if fmt is not None:
                label_style["fmt"] = fmt
            if ctx.emphasis == EMPHASIS_BACKGROUND:
                label_style["colors"] = self.muted_color
            # a relief's labels sit over the etching and read through a halo
            halo = self.value_halo if self.fill and self.value_etch_steps else []
            for text in ax.clabel(lines, **label_style):
                text.set_fontfamily(self.label_family)
                text.set_path_effects(halo)

    @staticmethod
    def _level_resolver(contours, label, edges=None) -> Callable:
        """A level line reports its level; a filled band the two edges it lies between."""

        levels = [_scalar(level) for level in (edges or contours.levels)]

        def resolve(index):
            i = index[0]
            if contours.filled:
                return {"label": label, "level": _span_text(levels[i], levels[i + 1])}
            return {"label": label, "level": levels[i]}

        return resolve


# the `reduce` attr of a hexbin chart, as the numpy reducer of a hexagon's `c`
HEXBIN_REDUCERS = {
    HEXBIN_REDUCE.MEAN: np.mean,
    HEXBIN_REDUCE.SUM: np.sum,
    HEXBIN_REDUCE.MEDIAN: np.median,
    HEXBIN_REDUCE.MIN: np.min,
    HEXBIN_REDUCE.MAX: np.max,
}


class HexbinLayer(Layer):
    """Scattered points binned into hexagons, colored by count or by `c` (ADR 0024)."""

    ticks_at_axis_ends = False

    kind = "hexbin"
    surface = True

    def _resolve_style(self):
        self.show_colorbar = self.settings.get("show_colorbar")
        # value_format is the tick format the colorbar setting falls back on
        self.colorbar = get_colorbar_setting(
            self.chart.get("colorbar"), self.chart.get("value_format")
        )
        self.colorbar_edge = self._colorbar_edge(self.show_colorbar)
        self.centred = self.chart.get("norm") in CENTRED_NORMS
        self.scaling = colormap_scaling(self.chart)
        self.vcenter = self.scaling["norm"].vcenter if self.centred else None
        style = get_hexbin_style(self.style)
        if self.centred:
            style["cmap"] = get_heatmap_cmap(self.style, "plot_hexbin", diverging=True)
        style["cmap"] = get_colormap(style["cmap"])
        self.hexbin_style = style
        self.x, self.y, self.c = self._columns()
        self.grid_size = self.chart.get("grid_size")
        if self.grid_size is None:
            self.grid_size = get_attr_value("plot_hexbin_gridsize", self.style, config)
        self.min_count = self.chart.get("min_count")
        # bins exist only once drawn, so the rule resolves in draw (ADR 0045)
        self.emphasis_rule = validate_emphasis_rule(self.settings.get("emphasis_rule"))
        self.highlight_color = config["font_general_color"]
        self.frame_width = config.get("axes_spines_width") or 0.8
        # counts need no reducer; `c` defaults to the mean
        self.reduce = None
        self.value_name = "count"
        if self.c is not None:
            name = self.chart.get("reduce")
            if name is None:
                name = HEXBIN_REDUCE.DEFAULT
            self.reduce = HEXBIN_REDUCERS[name]
            self.value_name = str(name)

    def _columns(self) -> tuple:
        """The validated (x, y, c) columns; c is None when absent."""

        x = get_chart_data("x", self.chart)
        y = get_chart_data("y", self.chart)
        if x is None or y is None:
            raise ValueError(
                "A hexbin chart requires the `x` and `y` columns in `data`."
            )
        self._x_kind = axis_kind(x)
        if self._x_kind == AXIS_TEMPORAL:
            self.x_tz = _column_tz(x)
            x = to_date_numbers(x)
        else:
            x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        c = get_chart_data("c", self.chart)
        c = None if c is None else np.asarray(c, dtype=float)
        for name, column in (("y", y), ("c", c)):
            if column is not None and column.shape != x.shape:
                raise ValueError(
                    f"The hexbin `{name}` column must hold one value per `x` "
                    f"({len(x)}), got {len(column)}."
                )
        return x, y, c

    def x_kind(self):
        return self._x_kind

    def value_data(self):
        return self.y

    def category_data(self):
        return None if self._x_kind == AXIS_TEMPORAL else self.x

    def y_range(self):
        if len(self.y) == 0:
            return None
        return (float(self.y.min()), float(self.y.max()))

    def draw(self, ax, ctx):
        style = dict(self.hexbin_style)
        if ctx.z_order is not None:
            style["zorder"] = ctx.z_order
        tiles = ax.hexbin(
            self.x,
            self.y,
            C=self.c,
            gridsize=self.grid_size,
            # hexagons bin in the axes' scale; a later log scale would warp them
            xscale="log" if ctx.category_scale == AXIS_SCALE.LOG else "linear",
            yscale="log" if ctx.value_scale == AXIS_SCALE.LOG else "linear",
            reduce_C_function=self.reduce,
            mincnt=self.min_count,
            **self.scaling,
            **style,
        )
        label = self.label(ctx)
        values = tiles.get_array()
        if self.emphasis_rule is not None:
            self._apply_bin_emphasis(ax, tiles, values)
        if self.value_etch_steps:
            self._draw_bin_steps(ax, tiles, values, self.emphasis_rule is not None)

        def resolve(index):
            cx, cy = tiles.get_offsets()[index[0]]
            value = _scalar(values[index[0]])
            return {
                "label": label,
                "x": _scalar(cx),
                "y": _scalar(cy),
                self.value_name: value,
            }

        self.register_hover(tiles, resolve)
        if self.show_colorbar and self.value_etch_steps:
            self._draw_even_step_legend(ax, tiles.norm, self.colorbar["label"])
        elif self.show_colorbar:
            _draw_colorbar(ax, tiles, self.colorbar, ctx.aspect_locked, self.vcenter)

    def _draw_bin_steps(self, ax, tiles, values, faded: bool) -> None:
        """The bins as etched value steps under their outlines.

        `faded` bins carry the emphasis fade in their face alphas. A count bin
        holding no point draws nothing, outline included.
        """

        alphas = tiles.get_facecolors()[:, 3] if faded else None
        # the emphasis fade already scaled the norm and dropped the array
        if not faded:
            tiles.autoscale_None()
        steps = value_steps(tiles.norm(values), len(self.value_etch_steps))
        if self.c is None:
            steps = np.where(np.ma.filled(values, 0) == 0, -1, steps)
        empty = steps < 0
        hexagon = tiles.get_paths()[0].vertices
        offsets = tiles.get_offsets()

        def bins(mask):
            collection = PolyCollection(
                [hexagon],
                offsets=offsets[mask],
                offset_transform=tiles.get_offset_transform(),
            )
            collection.set_transform(tiles.get_transform())
            return collection

        self._draw_value_steps(ax, steps, bins, tiles.get_zorder() - 0.01, alphas)
        tiles.set_array(None)
        tiles.set_facecolor("none")
        edges = np.array(to_rgba_array(tiles.get_edgecolor()), dtype=float)
        edges = np.broadcast_to(edges, (len(steps), 4)).copy()
        edges[empty, 3] = 0.0
        # a collection alpha would overwrite the per-bin edge alphas
        tiles.set_alpha(None)
        tiles.set_edgecolor(edges)

    def _apply_bin_emphasis(self, ax, tiles, values) -> None:
        """Fade the bins the rule rejects and outline the ones it picks.

        The bin colors are fixed from the colormap first so the fade holds, as
        a heatmap's muted cells fade; the outlines draw as their own
        collection so no neighbour covers them.
        """

        values = np.asarray(values, dtype=float)
        # an empty count bin holds no points to rank, so it never matches
        ranked = np.where(values == 0, np.nan, values) if self.c is None else values
        roles = emphasis_rule_roles(self.emphasis_rule, ranked)
        background = np.array([role == EMPHASIS_BACKGROUND for role in roles])
        tiles.autoscale_None()
        faces = tiles.to_rgba(values)
        alpha = tiles.get_alpha()
        faces[:, 3] = 1.0 if alpha is None else alpha
        faces[background, 3] *= self.muted_alpha
        tiles.set_array(None)
        tiles.set_alpha(None)
        tiles.set_facecolor(faces)

        picked = ~background
        if not picked.any():
            return
        width = HIGHLIGHT_WIDTH_SCALE * max(
            float(np.max(tiles.get_linewidth())), self.frame_width
        )
        outline = PolyCollection(
            [tiles.get_paths()[0].vertices],
            offsets=tiles.get_offsets()[picked],
            offset_transform=tiles.get_offset_transform(),
            facecolors="none",
            edgecolors=self.highlight_color,
            linewidths=width,
            zorder=tiles.get_zorder() + EMPHASIS_Z_OFFSET[EMPHASIS_HIGHLIGHT],
        )
        outline.set_transform(tiles.get_transform())
        ax.add_collection(outline, autolim=False)


def value_steps(normed, n: int, centre: Optional[float] = None) -> np.ndarray:
    """The step, 0 to `n - 1`, of each value normalized to [0, 1]; -1 where missing."""

    normed = np.ma.masked_invalid(np.ma.asarray(normed, dtype=float))
    values = normed.filled(0.0)
    if centre is None:
        steps = np.clip(np.floor(values * n), 0, n - 1).astype(int)
    else:
        inner = step_edges(n, centre)[1:-1]
        steps = np.clip(np.searchsorted(inner, values, side="right"), 0, n - 1)
    return np.where(np.ma.getmaskarray(normed), -1, steps)


def heatmap_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per cell, by its value; a blank cell never matches."""

    filled, units = [], []
    for chart in charts:
        z = get_chart_grid(chart, "heatmap", dtype=object)[2]
        roles = heatmap_cell_roles(chart, z)
        for i, row in enumerate(z):
            for j, value in enumerate(row):
                # a blank cell draws nothing to mute
                if value is None or math.isnan(value):
                    units.append((math.nan, _keep_role))
                else:
                    units.append((value, _fill_role(roles[i], j)))
        filled.append({**chart, "data": {**chart["data"], "emphasis": roles}})
    return filled, units
