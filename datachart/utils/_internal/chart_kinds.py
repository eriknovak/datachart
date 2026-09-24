"""What each chart front is: one `ChartKind` row per front (ADR 0065).

The engine, the builder, and composition branch on a front's row, never on its
chart-type string. `chart_kind()` is the lookup; a name without a row raises
before anything is drawn.
"""

import math
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Callable,
    FrozenSet,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    Union,
    get_args,
)

from .config_helpers import (
    get_grid_style,
    get_legend_panel_settings,
    get_value_label_style,
)
from .layers import (
    DEFAULT_ORIENTATION,
    Layer,
    Panel,
    LineLayer,
    BumpLayer,
    StackedAreaLayer,
    BarLayer,
    GanttLayer,
    HistogramLayer,
    KdeLayer,
    ScatterLayer,
    BoxLayer,
    SwarmLayer,
    DumbbellLayer,
    ViolinLayer,
    RidgelineLayer,
    HeatmapLayer,
    CalendarHeatmapLayer,
    ContourLayer,
    HexbinLayer,
    ImageLayer,
    BasemapLayer,
    ParallelCoordsLayer,
    RadialLayer,
    SankeyLayer,
    TreemapLayer,
    NetworkLayer,
    RADIAL_LAYER_TYPES,
    build_raincloud_layers,
    rank_bump_charts,
    sort_dumbbell_charts,
    sort_gantt_charts,
    sort_bar_charts,
    bar_units,
    dumbbell_units,
    gantt_units,
    group_units,
    heatmap_units,
    network_units,
    parallel_units,
    series_units,
    treemap_units,
    emphasis_rule_roles,
    resolve_show_values,
    value_axis_grid,
    value_label_font,
)
from .validate import (
    validate_calendar_dates,
    validate_calendar_year,
    validate_dumbbell_records,
    validate_emphasis_rule,
    validate_gantt_groups,
    validate_gantt_sort_by,
    validate_gantt_tasks,
    validate_single_dataset,
    validate_unique_dates,
)
from ...config import config
from ...constants import (
    ASPECT_RATIO,
    AXIS_SCALE,
    BANDWIDTH,
    BAR_MODE,
    BASEMAP_FEATURE,
    BASEMAP_RESOLUTION,
    BUMP_LABEL_POSITION,
    BUMP_RANK,
    CALENDAR_WEEKDAY,
    COLOR_NORM,
    CONTOUR_LEVELS,
    DATE_FORMAT,
    DRAW_POSITION,
    DUMBBELL_SORT_KEY,
    DUMBBELL_VALUE,
    Domain,
    EMPHASIS,
    FIG_SIZE,
    GANTT_DATE_PERIOD,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    HEXBIN_REDUCE,
    LINE_MARKER,
    LINE_STYLE,
    NETWORK_LABEL_POSITION,
    NETWORK_LAYOUT,
    ORIENTATION,
    RADIAL_DIRECTION,
    RADIAL_TYPE,
    RIDGELINE_SCALE,
    SCATTER_MATRIX_DIAGONAL,
    SHOW_GRID,
    SORT,
    STACKED_AREA_BASELINE,
    SWARM_MODE,
    VALUE_FORMAT,
    VIOLIN_INNER,
)
from ...typings import (
    BracketSettingAttrs,
    ColorbarSettingAttrs,
    DLineSettingAttrs,
    EmphasisRuleAttrs,
    HLineSettingAttrs,
    HSpanSettingAttrs,
    LegendSettingAttrs,
    TextSettingAttrs,
    VLineSettingAttrs,
    VSpanSettingAttrs,
)

# the per-chart keys every front shares; a row's `chart_keys` adds its own
CHART_KEYS = frozenset(
    {
        "subtitle",
        "emphasis",
        "style",
        "xticks",
        "xticklabels",
        "xtickrotate",
        "yticks",
        "yticklabels",
        "ytickrotate",
        "vlines",
        "hlines",
        "dlines",
        "brackets",
        "vspans",
        "hspans",
        "texts",
    }
)

# a function of the charts and settings, returning the charts it rewrote
ChartsStep = Callable[[List[dict], dict], List[dict]]

# rewrites the built charts and settings, for charts not one per dataset
Expand = Callable[[List[dict], dict], Tuple[List[dict], dict]]

# a calendar is wide and short: the default figure keeps the default width
# and stacks this much height per row of calendars
CALENDAR_ROW_HEIGHT = 1.9

# the settings the map layer reads from its chart's data
_MAP_KEYS = ("resolution", "highlight", "geometry")


def _never(settings: dict) -> bool:
    return False


def _always(settings: dict) -> bool:
    return True


def _filled(settings: dict) -> bool:
    return bool(settings.get("filled"))


def _bump_legend(charts: List[dict], settings: dict) -> Optional[bool]:
    # without end labels the legend names the lines
    return settings.get("show_labels") is False and not settings.get("subplots")


def _dumbbell_legend(charts: List[dict], settings: dict) -> Optional[bool]:
    if settings.get("subplots"):
        return None
    return (
        settings.get("start_name") is not None or settings.get("end_name") is not None
    )


def _gantt_legend(charts: List[dict], settings: dict) -> Optional[bool]:
    # group headers already name the groups
    return not settings.get("show_group_headers") and any(
        record.get("group") is not None for chart in charts for record in chart["data"]
    )


class DatasetPolicy(Enum):
    """What several datasets of one front draw as, unless `subplots` is set."""

    # every dataset shares one axes
    OVERLAY = "overlay"
    # every dataset takes its own subplot
    SUBPLOT = "subplot"
    # several datasets need `subplots=True`
    RAISE = "raise"


@dataclass(frozen=True)
class ChartKind:
    """Everything the engine, builder, and composition read about a front.

    Attributes:
        name: The chart-type string the front renders under, e.g. `"linechart"`.
        label: The front's name in error messages, e.g. `"box plot"`.
        chart_keys: The front's own per-chart parameters, indexed against the
            charts beside the engine's shared per-chart keys (ADR 0066).
        figure_keys: Shared per-chart keys the front's panel reads whole, so
            they stay figure-level settings.
        defaults: Settings a front fixes when its caller left them unset.
        legend_default: The `show_legend` value when the caller left it None,
            given the charts and settings.
        layer: The layer class drawing each chart; for a front assembled from
            several layers, the class of its primary mark.
        build: Builds all of the front's layers from its charts and settings,
            in place of one `layer` per chart.
        projection: The axes projection, e.g. `"polar"`; None is Cartesian.
        record_keys: The canonical keys of one record, in order; each is a
            remap parameter the builder reads the caller's key name from.
        required_keys: The record keys every record must carry.
        check_records: Raises for records the key check cannot judge, given
            the built charts and settings.
        expand: Rewrites the built charts and settings, for a front whose
            charts are not one per dataset.
        dict_data: One chart's `data` is a dict (a grid, links, a tree), so
            several charts come as a list of dicts rather than of lists.
        data_keys: The keys one chart's `data` dict must carry; None skips
            the shape check.
        datasets: What several datasets draw as when `subplots` is unset.
        subplots: The charts may split into one subplot each.
        rejects: Parameters the front takes only as None, with the reason
            a value raises.
        renamed: Deprecated parameter names the front still takes, mapped
            to their new names; each is removed one release after it ships.
        domains: The constant class each of the front's own constant-typed
            parameters takes (ADR 0068); a shared parameter's comes from its
            `SharedParameter` annotation.
        group: Categories run along one axis and values along the other, so
            the scale keys name the value axis, not a literal one.
        overlayable: `Panel` may overlay the front's figures.
        gridless: Whether the grid is off unless asked, given the settings.
        grid_on_value_axis: A theme's one-axis grid follows the value axis
            when it runs horizontally.
        tighten_xlim: The x limits hug the data instead of a margin.
        bar_mode: The default bar mode of the panel.
        mirrored: The panel mirrors the bars about zero (a pyramid).
        shared_bins: Subplots share one set of histogram bins.
        warns_subplot_legend: `show_legend` warns when the charts split into
            subplots.
        swaps_horizontal_labels: A horizontal subplot swaps its axis labels.
        emphasis_units: Builds the units an `emphasis_rule` reads; None when
            the front takes no rule.
        emphasis_by: The rule's default summary of a unit's values.
        emphasis_ranks: The rule reads ranks, best when lowest.
        prepare: Rewrites the charts before the rule reads them.
        order: Reorders the records after the rule, which breaks ties on
            input order.
    """

    name: str
    label: str
    layer: Type[Layer]
    chart_keys: FrozenSet[str] = frozenset()
    figure_keys: FrozenSet[str] = frozenset()
    defaults: Mapping[str, Any] = field(default_factory=dict)
    legend_default: Optional[Callable[[List[dict], dict], Optional[bool]]] = None
    build: Optional[Callable[[List[dict], dict], List[Layer]]] = None
    projection: Optional[str] = None
    record_keys: Tuple[str, ...] = ()
    required_keys: Tuple[str, ...] = ()
    check_records: Optional[Callable[[List[dict], dict], None]] = None
    expand: Optional[Expand] = None
    dict_data: bool = False
    data_keys: Optional[Tuple[str, ...]] = None
    datasets: DatasetPolicy = DatasetPolicy.OVERLAY
    subplots: bool = True
    rejects: Mapping[str, str] = field(default_factory=dict)
    renamed: Mapping[str, str] = field(default_factory=dict)
    domains: Mapping[str, Type[Domain]] = field(default_factory=dict)
    group: bool = False
    overlayable: bool = True
    gridless: Callable[[dict], bool] = _never
    grid_on_value_axis: bool = False
    tighten_xlim: bool = False
    bar_mode: str = "group"
    mirrored: bool = False
    shared_bins: bool = False
    warns_subplot_legend: bool = True
    swaps_horizontal_labels: bool = False
    emphasis_units: Optional[Callable] = None
    emphasis_by: Optional[str] = None
    emphasis_ranks: bool = False
    prepare: Optional[ChartsStep] = None
    order: Optional[ChartsStep] = None

    @property
    def per_chart_keys(self) -> FrozenSet[str]:
        """The parameters indexed against the charts; the rest are settings."""

        return (CHART_KEYS | self.chart_keys | set(self.record_keys)) - self.figure_keys

    def build_layers(self, charts: List[dict], settings: dict) -> List[Layer]:
        """The front's layers for already prepared charts."""

        if self.build is not None:
            return self.build(charts, settings)
        return [self.layer(chart, settings) for chart in charts]


# ================================================
# Composite builders
# ================================================


def _parallel_layers(charts: List[dict], settings: dict) -> List[Layer]:
    # every dataset is one set of polylines over shared axes
    return [ParallelCoordsLayer(list(charts), settings)]


def _radial_mark(charts: List[dict], settings: dict) -> List[dict]:
    # the visual is read before the emphasis rule and the sort read bars
    visual = settings.get("mark") or RADIAL_TYPE.DEFAULT
    if visual != RADIAL_TYPE.BAR and any(
        settings.get(key) is not None for key in ("sort", "sort_by", "emphasis_rule")
    ):
        raise ValueError(
            "RadialChart takes `sort`, `sort_by`, and `emphasis_rule` on the "
            f"bar visual only; the {visual!r} visual has no bars to order."
        )
    return charts


def _radial_layers(charts: List[dict], settings: dict) -> List[Layer]:
    visual = settings.get("mark") or RADIAL_TYPE.DEFAULT
    return [RADIAL_LAYER_TYPES[visual](chart, settings) for chart in charts]


def _raincloud_layers(charts: List[dict], settings: dict) -> List[Layer]:
    return [
        layer for chart in charts for layer in build_raincloud_layers(chart, settings)
    ]


def _ridgeline_layers(charts: List[dict], settings: dict) -> List[Layer]:
    layers = [RidgelineLayer(chart, settings) for chart in charts]
    if len(layers) > 1:
        # one grid range for every subplot, like the histogram's shared bins
        ranges = [r for r in (layer.padded_range() for layer in layers) if r]
        if ranges:
            shared = (min(r[0] for r in ranges), max(r[1] for r in ranges))
            for layer in layers:
                layer.shared_range = shared
    return layers


# ================================================
# Record checks and expansions
# ================================================


def _check_dumbbells(charts: List[dict], settings: dict) -> None:
    for chart in charts:
        validate_dumbbell_records(chart["data"])


def _check_tasks(charts: List[dict], settings: dict) -> None:
    sort = settings.get("sort")
    sort_key = validate_gantt_sort_by(sort, settings.get("sort_by"))
    for chart in charts:
        validate_gantt_tasks(chart["data"])
        validate_gantt_groups(
            chart["data"],
            sort_key if sort is not None else None,
            settings.get("show_group_headers"),
        )


def _year_panels(charts: List[dict], settings: dict) -> Tuple[List[dict], dict]:
    """One chart per calendar year, on a figure tall enough for their rows."""

    year = settings.get("year")
    charts = [panel for chart in charts for panel in _year_charts(chart, year)]
    if settings.get("figsize") is None:
        rows = math.ceil(len(charts) / settings["max_cols"])
        figsize = (FIG_SIZE.DEFAULT[0], CALENDAR_ROW_HEIGHT * rows)
        settings = {**settings, "figsize": figsize}
    return charts, settings


def _year_charts(chart: dict, year: Optional[int]) -> List[dict]:
    """One chart per year of a dataset, in year order; `year` keeps one.

    The years of one dataset share its value range unless `vmin`/`vmax`
    pin one, so the same value takes the same color on every calendar.
    """

    data = chart["data"]
    dates = validate_calendar_dates(data["date"])
    values = list(data["value"])
    if len(values) != len(dates):
        raise ValueError(
            "CalendarHeatmap `data` needs one value per date: "
            f"{len(dates)} dates, {len(values)} values."
        )
    if not dates:
        raise ValueError("CalendarHeatmap `data` needs at least one date.")
    validate_unique_dates(dates)
    years = {day.year for day in dates}
    validate_calendar_year(year, years)
    if year is not None:
        years = {year}

    by_year = {y: ([], []) for y in sorted(years)}
    for day, value in zip(dates, values):
        if day.year in by_year:
            by_year[day.year][0].append(day)
            by_year[day.year][1].append(value)

    shared = _shared_range(values, chart.get("norm"))
    charts = []
    for y, (year_dates, year_values) in by_year.items():
        panel = dict(chart)
        panel["data"] = {"date": year_dates, "value": year_values}
        panel["year"] = y
        if len(by_year) > 1:
            subtitle = chart.get("subtitle")
            panel["subtitle"] = str(y) if subtitle is None else f"{subtitle} {y}"
            for key, bound in zip(("vmin", "vmax"), shared or ()):
                if panel.get(key) is None:
                    panel[key] = bound
        charts.append(panel)
    return charts


def _shared_range(values: list, norm) -> Optional[Tuple[float, float]]:
    """The (min, max) of the values a normalization can show; None without any.

    A log norm shows the positive values, a logit norm those inside (0, 1);
    the range skips what the norm would mask, as its own autoscale does.
    """

    numbers = [v for v in values if v is not None and not math.isnan(v)]
    if norm == "log":
        numbers = [v for v in numbers if v > 0]
    elif norm == "logit":
        numbers = [v for v in numbers if 0 < v < 1]
    if not numbers:
        return None
    return min(numbers), max(numbers)


def _basemap_chart(charts: List[dict], settings: dict) -> tuple:
    # the basemap's one chart is its features and overlay geometry
    (chart,) = charts
    data = {"features": chart["data"]}
    data.update((key, settings.pop(key)) for key in _MAP_KEYS)
    return [{**chart, "data": data}], settings


# ================================================
# The table
# ================================================


def _no_emphasis(front: str, reason: str) -> Mapping[str, str]:
    return {"emphasis": f"{front} does not support `emphasis`: {reason}"}


_KINDS = (
    ChartKind(
        "linechart",
        "line chart",
        LineLayer,
        record_keys=("x", "y", "yerr"),
        required_keys=("x", "y"),
        tighten_xlim=True,
        emphasis_units=series_units("y"),
        emphasis_by="mean",
    ),
    ChartKind(
        "stackedareachart",
        "stacked area chart",
        StackedAreaLayer,
        domains={"baseline": STACKED_AREA_BASELINE},
        record_keys=("x", "y"),
        required_keys=("x", "y"),
        tighten_xlim=True,
        emphasis_units=series_units("y"),
        emphasis_by="mean",
    ),
    ChartKind(
        "bumpchart",
        "bump chart",
        BumpLayer,
        domains={"rank_by": BUMP_RANK, "label_position": BUMP_LABEL_POSITION},
        record_keys=("x", "y"),
        required_keys=("x", "y"),
        legend_default=_bump_legend,
        # a bump chart's ranks read from the lines and labels
        gridless=_always,
        tighten_xlim=True,
        emphasis_units=series_units("y"),
        emphasis_by="mean",
        # `top` picks the lowest ranks (ADR 0046)
        emphasis_ranks=True,
        # the rule reads the ranks, so they come first
        prepare=rank_bump_charts,
    ),
    ChartKind(
        "barchart",
        "bar chart",
        BarLayer,
        record_keys=("label", "y", "yerr"),
        required_keys=("label", "y"),
        defaults={"orientation": ORIENTATION.VERTICAL},
        swaps_horizontal_labels=True,
        emphasis_units=bar_units,
        order=sort_bar_charts,
    ),
    ChartKind(
        # a pyramid is the bar seam under mirrored panel furniture (ADR 0017)
        "pyramidchart",
        "pyramid",
        BarLayer,
        record_keys=("label", "y", "yerr"),
        required_keys=("label", "y"),
        # the panel mirrors the value ticks to both halves (ADR 0017)
        figure_keys=frozenset({"xticks", "xticklabels", "xtickrotate"}),
        defaults={"pyramid": True, "orientation": ORIENTATION.HORIZONTAL},
        subplots=False,
        # unmirrored data on a mirrored axis would silently mangle (ADR 0017)
        overlayable=False,
        mirrored=True,
        emphasis_units=bar_units,
        order=sort_bar_charts,
    ),
    ChartKind(
        "radialchart",
        "radial chart",
        RadialLayer,
        domains={"mark": RADIAL_TYPE, "direction": RADIAL_DIRECTION},
        # the histogram visual reads `x`, the others `label` and `y`
        record_keys=("label", "x", "y", "yerr"),
        build=_radial_layers,
        projection="polar",
        rejects={
            "scalex": "RadialChart does not support `scalex`: the angular axis "
            "has no scale to change.",
            **{
                name: f"RadialChart does not support `{name}`: straight "
                "reference marks are geometrically meaningless on a polar axes."
                for name in ("vlines", "hlines", "dlines", "brackets")
            },
        },
        renamed={"type": "mark"},
        prepare=_radial_mark,
        # the front takes a rule and a sort on the bar visual only
        emphasis_units=bar_units,
        order=sort_bar_charts,
    ),
    ChartKind(
        "calendarheatmap",
        "calendar heatmap",
        CalendarHeatmapLayer,
        domains={"week_start": CALENDAR_WEEKDAY},
        chart_keys=frozenset({"colorbar", "norm", "vcenter", "vmax", "vmin"}),
        defaults={"aspect_ratio": ASPECT_RATIO.EQUAL, "max_cols": 1},
        dict_data=True,
        data_keys=("date", "value"),
        # one calendar per year of each dataset
        expand=_year_panels,
        datasets=DatasetPolicy.SUBPLOT,
        rejects=_no_emphasis(
            "CalendarHeatmap",
            "a calendar is a single raster layer with no series to mute or "
            "highlight.",
        ),
        overlayable=False,
        gridless=_always,
    ),
    ChartKind(
        "ganttchart",
        "gantt",
        GanttLayer,
        domains={
            "period": GANTT_DATE_PERIOD,
            "value_kind": GANTT_VALUE,
            "sort_by": GANTT_SORT_KEY,
        },
        record_keys=("task", "start", "end", "group", "progress", "depends_on"),
        required_keys=("task", "start", "end"),
        check_records=_check_tasks,
        defaults={"max_cols": 1, "orientation": ORIENTATION.HORIZONTAL},
        legend_default=_gantt_legend,
        datasets=DatasetPolicy.SUBPLOT,
        # a horizontal panel's twin is a second x, off the task rows (ADR 0049)
        overlayable=False,
        emphasis_units=gantt_units,
        order=sort_gantt_charts,
    ),
    ChartKind(
        "dumbbellchart",
        "dumbbell chart",
        DumbbellLayer,
        domains={
            "value_kind": DUMBBELL_VALUE,
            "sort_by": DUMBBELL_SORT_KEY,
            "marker": LINE_MARKER,
            "connector_style": LINE_STYLE,
        },
        record_keys=("label", "start", "end"),
        required_keys=("label", "start", "end"),
        check_records=_check_dumbbells,
        defaults={"orientation": ORIENTATION.HORIZONTAL},
        legend_default=_dumbbell_legend,
        group=True,
        grid_on_value_axis=True,
        emphasis_units=dumbbell_units,
        order=sort_dumbbell_charts,
    ),
    ChartKind(
        "histogram",
        "histogram",
        HistogramLayer,
        record_keys=("x",),
        required_keys=("x",),
        defaults={"orientation": ORIENTATION.VERTICAL},
        # histograms stack by default; bars group (ADR 0014)
        bar_mode="stack",
        shared_bins=True,
        emphasis_units=series_units("x"),
        emphasis_by="mean",
    ),
    # the ScatterMatrix diagonal's density curves; no front draws it alone
    ChartKind("kde", "density", KdeLayer, record_keys=("x",), required_keys=("x",)),
    ChartKind(
        "boxplot",
        "box plot",
        BoxLayer,
        record_keys=("label", "value"),
        required_keys=("label", "value"),
        defaults={"orientation": ORIENTATION.VERTICAL},
        datasets=DatasetPolicy.RAISE,
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "violinplot",
        "violin plot",
        ViolinLayer,
        domains={"inner": VIOLIN_INNER},
        record_keys=("label", "value"),
        required_keys=("label", "value"),
        defaults={"orientation": ORIENTATION.VERTICAL},
        datasets=DatasetPolicy.RAISE,
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "swarmplot",
        "swarm plot",
        SwarmLayer,
        record_keys=("label", "value"),
        required_keys=("label", "value"),
        defaults={"orientation": ORIENTATION.VERTICAL, "mode": SWARM_MODE.SWARM},
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "raincloudplot",
        "raincloud plot",
        ViolinLayer,
        record_keys=("label", "value"),
        required_keys=("label", "value"),
        defaults={
            "orientation": ORIENTATION.VERTICAL,
            "mode": SWARM_MODE.SWARM,
            "show_outliers": True,
        },
        build=_raincloud_layers,
        datasets=DatasetPolicy.SUBPLOT,
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "ridgelineplot",
        "ridgeline plot",
        RidgelineLayer,
        domains={"inner": VIOLIN_INNER, "ridge_scale": RIDGELINE_SCALE},
        record_keys=("label", "value"),
        required_keys=("label", "value"),
        defaults={"orientation": ORIENTATION.HORIZONTAL},
        build=_ridgeline_layers,
        datasets=DatasetPolicy.SUBPLOT,
        renamed={"normalize": "ridge_scale"},
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "scatterchart",
        "scatter chart",
        ScatterLayer,
        record_keys=("x", "y", "size", "hue", "label", "xerr", "yerr"),
        required_keys=("x", "y"),
        emphasis_units=series_units("y"),
        emphasis_by="mean",
    ),
    ChartKind(
        "heatmap",
        "heatmap",
        HeatmapLayer,
        chart_keys=frozenset(
            {"colorbar", "norm", "value_format", "vcenter", "vmax", "vmin"}
        ),
        dict_data=True,
        data_keys=("z",),
        datasets=DatasetPolicy.SUBPLOT,
        rejects=_no_emphasis(
            "Heatmap",
            "a heatmap has no series to mute or highlight. Set the `emphasis` "
            "grid on `data` for per-cell roles instead.",
        ),
        renamed={"show_heatmap_values": "show_values", "valfmt": "value_format"},
        overlayable=False,
        # a raster covers the grid
        gridless=_always,
        warns_subplot_legend=False,
        emphasis_units=heatmap_units,
    ),
    ChartKind(
        "contourchart",
        "contour chart",
        ContourLayer,
        domains={"levels": CONTOUR_LEVELS},
        chart_keys=frozenset(
            {"colorbar", "norm", "value_format", "vcenter", "vmax", "vmin"}
        ),
        dict_data=True,
        renamed={"valfmt": "value_format"},
        # filled contour bands cover the grid
        gridless=_filled,
        emphasis_units=series_units("z"),
        emphasis_by="mean",
    ),
    ChartKind(
        "hexbinchart",
        "hexbin chart",
        HexbinLayer,
        domains={"reduce": HEXBIN_REDUCE},
        chart_keys=frozenset(
            {
                "colorbar",
                "gridsize",
                "mincnt",
                "norm",
                "reduce",
                "value_format",
                "vcenter",
                "vmax",
                "vmin",
            }
        ),
        defaults={"show_colorbars": True},
        dict_data=True,
        rejects=_no_emphasis(
            "HexbinChart",
            "a hexbin chart is a single colormapped layer with no series to "
            "mute or highlight.",
        ),
        renamed={"valfmt": "value_format"},
        # hexagons cover the grid
        gridless=_always,
    ),
    ChartKind(
        "parallelcoords",
        "parallel coordinates",
        ParallelCoordsLayer,
        chart_keys=frozenset({"category_orders", "dimensions", "hue"}),
        build=_parallel_layers,
        subplots=False,
        emphasis_units=parallel_units,
    ),
    ChartKind(
        "networkchart",
        "network",
        NetworkLayer,
        domains={"layout": NETWORK_LAYOUT, "label_position": NETWORK_LABEL_POSITION},
        dict_data=True,
        data_keys=("edges",),
        datasets=DatasetPolicy.SUBPLOT,
        rejects=_no_emphasis(
            "NetworkChart",
            "set the `emphasis` key on the nodes to mute or highlight instead.",
        ),
        overlayable=False,
        emphasis_units=network_units,
    ),
    ChartKind(
        # a grid of scatter, density, and correlation cells, not one panel
        "scattermatrix",
        "scatter matrix",
        ScatterLayer,
        domains={"diagonal": SCATTER_MATRIX_DIAGONAL},
        datasets=DatasetPolicy.SUBPLOT,
        overlayable=False,
    ),
    ChartKind("imagechart", "image chart", ImageLayer, dict_data=True),
    ChartKind(
        "basemapchart",
        "basemap chart",
        BasemapLayer,
        domains={"data": BASEMAP_FEATURE, "resolution": BASEMAP_RESOLUTION},
        dict_data=True,
        datasets=DatasetPolicy.SUBPLOT,
        subplots=False,
        renamed={"features": "data"},
        expand=_basemap_chart,
    ),
    ChartKind(
        "sankeychart",
        "Sankey",
        SankeyLayer,
        dict_data=True,
        data_keys=("links",),
        datasets=DatasetPolicy.SUBPLOT,
        rejects=_no_emphasis(
            "SankeyChart", "a Sankey has no series to mute or highlight."
        ),
        overlayable=False,
    ),
    ChartKind(
        "treemap",
        "treemap",
        TreemapLayer,
        dict_data=True,
        data_keys=("data",),
        datasets=DatasetPolicy.SUBPLOT,
        rejects=_no_emphasis(
            "Treemap",
            "set the `emphasis` key on the records to mute or highlight instead.",
        ),
        overlayable=False,
        emphasis_units=treemap_units,
    ),
)

CHART_KINDS = {kind.name: kind for kind in _KINDS}


def chart_kind(name: str) -> ChartKind:
    """The row of a chart front; raises `ValueError` when it has none."""

    kind = CHART_KINDS.get(name)
    if kind is None:
        raise ValueError(
            f"Chart type {name!r} has no ChartKind row; "
            f"known types are {sorted(CHART_KINDS)}."
        )
    return kind


# ================================================
# Shared parameters
# ================================================


@dataclass(frozen=True)
class SharedParameter:
    """A parameter spelled, typed and defaulted alike on every front taking it.

    Attributes:
        name: The parameter's name.
        annotation: The type of one value, without `Optional`: a parameter
            defaulting to None is annotated `Optional[annotation]`.
        default: The signature default.
        per_chart: The type of the value on a front that indexes it against
            the charts, without `Optional`; None when every front reads it
            whole.
    """

    name: str
    annotation: Any
    default: Any = None
    per_chart: Any = None

    def signature_annotation(self, kind: ChartKind) -> Any:
        """The annotation the parameter carries on the front of `kind`."""

        if self.name in kind.rejects:
            return None
        if self.name in kind.per_chart_keys and self.per_chart is not None:
            annotation = self.per_chart
        else:
            annotation = self.annotation
        return annotation if self.default is not None else Optional[annotation]


def _each(annotation: Any) -> Any:
    # one value for every chart, or one per chart
    return Union[annotation, List[Optional[annotation]]]


def _nested(setting: Any) -> Any:
    # one or several settings for every chart, or those of each chart
    return Union[setting, List[setting], List[Union[setting, List[setting], None]]]


def _setting(name: str, setting: Any) -> SharedParameter:
    return SharedParameter(
        name, Union[setting, List[setting]], per_chart=_nested(setting)
    )


_Number = Union[int, float]
_Ticks = List[_Number]
_Labels = List[str]

# x-axis values, limits, ticks and tick formats are left out: a front's x axis
# holds numbers or dates, and the annotation says which (ADR 0067)
_SHARED = (
    SharedParameter("title", str),
    SharedParameter("xlabel", str),
    SharedParameter("ylabel", str),
    SharedParameter("figsize", Union[FIG_SIZE, Tuple[float, float]]),
    SharedParameter("show_legend", bool),
    SharedParameter("legend", LegendSettingAttrs),
    SharedParameter("show_grid", Union[SHOW_GRID, str, bool]),
    SharedParameter("subplots", bool),
    SharedParameter("max_cols", int),
    SharedParameter("sharex", bool),
    SharedParameter("sharey", bool),
    SharedParameter("aspect_ratio", Union[ASPECT_RATIO, str]),
    SharedParameter("emphasis_rule", EmphasisRuleAttrs),
    SharedParameter("ymin", _Number),
    SharedParameter("ymax", _Number),
    SharedParameter("yticks_format", Union[VALUE_FORMAT, DATE_FORMAT, str]),
    SharedParameter("scalex", Union[AXIS_SCALE, str]),
    SharedParameter("scaley", Union[AXIS_SCALE, str]),
    SharedParameter("orientation", Union[ORIENTATION, str]),
    SharedParameter("sort", Union[SORT, str]),
    SharedParameter("bar_mode", Union[BAR_MODE, str]),
    SharedParameter("show_values", bool),
    SharedParameter("value_step", int),
    SharedParameter("show_yerr", bool),
    SharedParameter("show_area", bool),
    SharedParameter("show_labels", bool),
    SharedParameter("show_outliers", bool),
    SharedParameter("show_colorbars", bool),
    SharedParameter("show_regression", bool),
    SharedParameter("show_correlation", bool),
    SharedParameter("num_bins", int),
    SharedParameter("bandwidth", Union[BANDWIDTH, str, float]),
    SharedParameter("mode", Union[SWARM_MODE, str]),
    SharedParameter("jitter", float, default=0.4),
    SharedParameter("position", Union[DRAW_POSITION, str]),
    SharedParameter(
        "value_format",
        Union[VALUE_FORMAT, str],
        per_chart=Union[VALUE_FORMAT, str, List[Optional[str]]],
    ),
    SharedParameter("subtitle", str, per_chart=_each(str)),
    SharedParameter(
        "emphasis",
        Union[EMPHASIS, str],
        per_chart=Union[EMPHASIS, str, List[Optional[str]]],
    ),
    SharedParameter("xticklabels", _Labels, per_chart=Union[_Labels, List[_Labels]]),
    SharedParameter("xtickrotate", int, per_chart=_each(int)),
    SharedParameter("yticks", _Ticks, per_chart=Union[_Ticks, List[_Ticks]]),
    SharedParameter("yticklabels", _Labels, per_chart=Union[_Labels, List[_Labels]]),
    SharedParameter("ytickrotate", int, per_chart=_each(int)),
    _setting("vlines", VLineSettingAttrs),
    _setting("hlines", HLineSettingAttrs),
    _setting("dlines", DLineSettingAttrs),
    _setting("brackets", BracketSettingAttrs),
    _setting("vspans", VSpanSettingAttrs),
    _setting("hspans", HSpanSettingAttrs),
    _setting("texts", TextSettingAttrs),
    SharedParameter("dimensions", _Labels, per_chart=Union[_Labels, List[_Labels]]),
    SharedParameter("vmin", float, per_chart=_each(float)),
    SharedParameter("vmax", float, per_chart=_each(float)),
    SharedParameter("vcenter", float, per_chart=_each(float)),
    SharedParameter(
        "norm",
        Union[COLOR_NORM, str],
        per_chart=Union[COLOR_NORM, str, List[Optional[str]]],
    ),
    SharedParameter(
        "colorbar", ColorbarSettingAttrs, per_chart=_each(ColorbarSettingAttrs)
    ),
)

# every record key is a remap parameter naming the caller's key (ADR 0069)
RECORD_KEYS = tuple(dict.fromkeys(key for kind in _KINDS for key in kind.record_keys))

SHARED_PARAMETERS = {
    parameter.name: parameter
    for parameter in _SHARED
    + tuple(SharedParameter(key, str, per_chart=_each(str)) for key in RECORD_KEYS)
}


# the x-axis format stays out of the table (ADR 0067) but takes these classes
_X_TICKS_FORMAT_DOMAINS = (VALUE_FORMAT, DATE_FORMAT)


def parameter_domains(name: str, domains: Mapping[str, type]) -> tuple:
    """The constant classes a parameter takes; empty when it takes none.

    A name in `domains` takes that class; a shared parameter takes the
    constant classes in its `SharedParameter` annotation (ADR 0068).
    """

    if name in domains:
        return (domains[name],)
    if name == "xticks_format":
        return _X_TICKS_FORMAT_DOMAINS
    shared = SHARED_PARAMETERS.get(name)
    if shared is None:
        return ()
    return tuple(
        arg
        for arg in get_args(shared.annotation) or (shared.annotation,)
        if isinstance(arg, type) and issubclass(arg, Domain)
    )


def check_domains(params: Mapping[str, Any], domains: Mapping[str, type]) -> None:
    """Raise `ValueError` for a string no constant class of its parameter takes.

    Only strings are checked: a number, bool, pair or callable is another
    type the parameter takes. A list or tuple is checked element-wise, and
    the message names the element, e.g. `emphasis[1]`.
    """

    for name, value in params.items():
        classes = parameter_domains(name, domains)
        if not classes:
            continue
        items = (
            enumerate(value) if isinstance(value, (list, tuple)) else [(None, value)]
        )
        for index, item in items:
            if isinstance(item, str) and not any(c.accepts(item) for c in classes):
                classes[0].check(item, name if index is None else f"{name}[{index}]")


# ================================================
# Readers
# ================================================


def apply_emphasis_rule(kind: ChartKind, charts: List[dict], settings: dict) -> list:
    """The charts with the rule's role written on each unit that set none.

    The rule reads every unit of the charts as one pool, so a count picks
    units across the series and subplots; an explicit role wins.
    """

    rule = validate_emphasis_rule(settings.get("emphasis_rule"), kind.emphasis_by)
    if rule is None:
        return charts
    if kind.emphasis_ranks:
        rule = ({"top": "bottom", "bottom": "top"}.get(rule[0], rule[0]),) + rule[1:]
    charts, units = kind.emphasis_units(charts, settings, rule[2])
    roles = emphasis_rule_roles(rule, [value for value, _ in units])
    for (_, fill), role in zip(units, roles):
        fill(role)
    return charts


def splits_datasets(kind: ChartKind, n_charts: int, subplots: Optional[bool]) -> bool:
    """Whether the charts draw one subplot each: the one dataset policy reader.

    `subplots` wins where the front takes subplots, and warns where it does
    not; unset, the row's `datasets` policy decides, raising for `RAISE`
    when there are several charts.
    """

    if subplots and not kind.subplots:
        warnings.warn(
            f"Chart type '{kind.name}' does not support subplots. "
            "Setting subplots to False..."
        )
        subplots = False
    if subplots:
        return True
    if kind.datasets is DatasetPolicy.RAISE and n_charts > 1:
        validate_single_dataset(n_charts, kind.label)
    return kind.datasets is not DatasetPolicy.OVERLAY


def build_layers(chart_type: str, charts: List[dict], settings: dict) -> List[Layer]:
    """Build the layers for a chart front; style resolution happens here."""

    kind = chart_kind(chart_type)
    if kind.prepare is not None:
        charts = kind.prepare(charts, settings)
    if kind.emphasis_units is not None:
        # the rule breaks ties on input order, so it runs before the sort
        charts = apply_emphasis_rule(kind, charts, settings)
    if kind.order is not None:
        charts = kind.order(charts, settings)
    return kind.build_layers(charts, settings)


def build_chart_panel_settings(
    chart_type: str, settings: dict, mode: str, first_style: dict
) -> dict:
    """Resolve panel-level settings for a chart front at build time.

    Modes: "single" (all layers on the figure's one axes), "subplot" (one layer
    per axes), "composition" (the metadata panel used by grids).
    """

    kind = chart_kind(chart_type)
    show_grid = settings.get("show_grid")
    # a polar panel draws only the set an explicit value names (ADR 0015)
    show_grid_explicit = show_grid is not None
    if show_grid is None and not kind.gridless(settings):
        show_grid = config.get("chart_default_show_grid")
        if kind.grid_on_value_axis:
            orientation = settings.get("orientation") or DEFAULT_ORIENTATION
            show_grid = value_axis_grid(
                show_grid, orientation == ORIENTATION.HORIZONTAL
            )

    # the seam's scale keys are literal; group fronts mean the value axis
    scalex, scaley = settings.get("scalex"), settings.get("scaley")
    if kind.group and settings.get("orientation") == ORIENTATION.HORIZONTAL:
        scalex, scaley = scaley, scalex

    panel_settings = {
        "furniture": Panel.snapshot_furniture(),
        "scalex": scalex,
        "scaley": scaley,
        # horizontal bars and histograms take their scale keys literally
        "literal_scale_keys": not kind.group,
        "show_grid": show_grid,
        "show_grid_explicit": show_grid_explicit,
        "grid_style": get_grid_style(first_style),
        "hatch_cycle": config.get("plot_hatch_cycle"),
        "linestyle_cycle": config.get("plot_linestyle_cycle"),
        "marker_cycle": config.get("plot_marker_cycle"),
        "xmin": settings.get("xmin"),
        "xmax": settings.get("xmax"),
        "ymin": settings.get("ymin"),
        "ymax": settings.get("ymax"),
        "xticks_format": settings.get("xticks_format"),
        "date_period": settings.get("period"),
        "yticks_format": settings.get("yticks_format"),
        "aspect_ratio": (
            ASPECT_RATIO.AUTO
            if settings.get("aspect_ratio") is None
            else settings["aspect_ratio"]
        ),
        **get_legend_panel_settings(settings.get("legend")),
        "bar_mode": settings.get("bar_mode") or kind.bar_mode,
        # the caller's own mode, unresolved, for a panel to adopt (ADR 0005)
        "source_bar_mode": settings.get("bar_mode"),
        "tighten_xlim": kind.tighten_xlim,
        "baseline": settings.get("baseline") or STACKED_AREA_BASELINE.DEFAULT,
        # radial furniture; only polar panels read these
        "startangle": settings.get("startangle"),
        "direction": settings.get("direction"),
        "innerradius": settings.get("innerradius"),
        "show_border": settings.get("show_border"),
        "show_values": resolve_show_values(settings),
        "show_tip_labels": settings.get("show_tip_labels"),
        "value_format": settings.get("value_format"),
        # the tip texts set their own family, rotated along the spoke
        "tip_value_style": {
            k: v
            for k, v in value_label_font(get_value_label_style(first_style)).items()
            if k != "family"
        },
    }

    if kind.mirrored:
        # the mirror is panel furniture (ADR 0017): overlay slots give both
        # sides full width at offset zero, the panel owns limits and ticks
        panel_settings["pyramid"] = True
        panel_settings["bar_mode"] = "overlay"
        panel_settings["pyramid_xmax"] = settings.get("xmax")
        panel_settings["xmax"] = None
        panel_settings["pyramid_xticks"] = settings.get("xticks")
        panel_settings["pyramid_xticklabels"] = settings.get("xticklabels")
        panel_settings["pyramid_xtickrotate"] = settings.get("xtickrotate")

    if mode == "subplot":
        panel_settings["show_legend"] = False
        panel_settings["bar_slotting"] = False
        panel_settings["bar_ticks"] = "subplot"
    else:
        panel_settings["show_legend"] = settings.get("show_legend")
        panel_settings["bar_ticks"] = "group"

    if mode == "composition":
        panel_settings["hide_ticklabels"] = settings.get("hide_ticklabels")
        panel_settings["marks_on_twin"] = settings.get("marks_on_twin")
        panel_settings["hide_ticks"] = settings.get("hide_ticks")
        panel_settings["xlabel"] = settings.get("xlabel")
        panel_settings["ylabel"] = settings.get("ylabel")
        panel_settings["label_styles"] = Panel.snapshot_label_styles()

    return panel_settings
