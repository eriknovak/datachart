"""What each chart front is: one `ChartKind` row per front (ADR 0065).

The engine, the builder, and composition branch on a front's row, never on its
chart-type string. `chart_kind()` is the lookup; a name without a row raises
before anything is drawn.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, FrozenSet, List, Mapping, Optional, Tuple, Type

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
from .validate import validate_baseline, validate_date_period, validate_emphasis_rule
from ...config import config
from ...constants import ASPECT_RATIO, ORIENTATION, RADIAL_TYPE

# a function of the charts and settings, returning the charts it rewrote
ChartsStep = Callable[[List[dict], dict], List[dict]]


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
        dict_data: One chart's `data` is a dict (a grid, links, a tree), so
            several charts come as a list of dicts rather than of lists.
        data_keys: The keys one chart's `data` dict must carry; None skips
            the shape check.
        multiplot: Several charts may share one axes.
        subplots: The charts may split into one subplot each.
        single_dataset: Several datasets need `subplots=True`.
        rejects: Parameters the front takes only as None, with the reason
            a value raises.
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
    dict_data: bool = False
    data_keys: Optional[Tuple[str, ...]] = None
    multiplot: bool = True
    subplots: bool = True
    single_dataset: bool = False
    rejects: Mapping[str, str] = field(default_factory=dict)
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


def _radial_layers(charts: List[dict], settings: dict) -> List[Layer]:
    visual = settings.get("type") or RADIAL_TYPE.LINE
    if visual not in RADIAL_LAYER_TYPES:
        raise ValueError(
            f"Invalid radial `type` value {visual!r}. "
            f"Must be one of {sorted(RADIAL_LAYER_TYPES)}."
        )
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
# The table
# ================================================


def _no_emphasis(front: str, reason: str) -> Mapping[str, str]:
    return {"emphasis": f"{front} does not support `emphasis`: {reason}"}


_KINDS = (
    ChartKind(
        "linechart",
        "line chart",
        LineLayer,
        chart_keys=frozenset({"x", "y", "yerr"}),
        tighten_xlim=True,
        emphasis_units=series_units("y"),
        emphasis_by="mean",
    ),
    ChartKind(
        "stackedareachart",
        "stacked area chart",
        StackedAreaLayer,
        chart_keys=frozenset({"x", "y"}),
        tighten_xlim=True,
        emphasis_units=series_units("y"),
        emphasis_by="mean",
    ),
    ChartKind(
        "bumpchart",
        "bump chart",
        BumpLayer,
        chart_keys=frozenset({"x", "y"}),
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
        chart_keys=frozenset({"label", "y", "yerr"}),
        swaps_horizontal_labels=True,
        emphasis_units=bar_units,
        order=sort_bar_charts,
    ),
    ChartKind(
        # a pyramid is the bar seam under mirrored panel furniture (ADR 0017)
        "pyramidchart",
        "pyramid",
        BarLayer,
        chart_keys=frozenset({"label", "y", "yerr"}),
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
        chart_keys=frozenset({"label", "x", "y", "yerr"}),
        build=_radial_layers,
        projection="polar",
        # the front takes a rule and a sort on the bar visual only
        emphasis_units=bar_units,
        order=sort_bar_charts,
    ),
    ChartKind(
        "calendarheatmap",
        "calendar heatmap",
        CalendarHeatmapLayer,
        chart_keys=frozenset({"colorbar", "norm", "vcenter", "vmax", "vmin"}),
        defaults={"aspect_ratio": ASPECT_RATIO.EQUAL, "max_cols": 1},
        dict_data=True,
        data_keys=("date", "value"),
        multiplot=False,
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
        defaults={"max_cols": 1, "orientation": ORIENTATION.HORIZONTAL},
        legend_default=_gantt_legend,
        multiplot=False,
        # a horizontal panel's twin is a second x, off the task rows (ADR 0049)
        overlayable=False,
        emphasis_units=gantt_units,
        order=sort_gantt_charts,
    ),
    ChartKind(
        "dumbbellchart",
        "dumbbell chart",
        DumbbellLayer,
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
        chart_keys=frozenset({"x"}),
        # histograms stack by default; bars group (ADR 0014)
        bar_mode="stack",
        shared_bins=True,
        emphasis_units=series_units("x"),
        emphasis_by="mean",
    ),
    # the ScatterMatrix diagonal's density curves; no front draws it alone
    ChartKind("kde", "density", KdeLayer),
    ChartKind(
        "boxplot",
        "box plot",
        BoxLayer,
        chart_keys=frozenset({"label", "value"}),
        multiplot=False,
        single_dataset=True,
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "violinplot",
        "violin plot",
        ViolinLayer,
        chart_keys=frozenset({"label", "value"}),
        multiplot=False,
        single_dataset=True,
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "swarmplot",
        "swarm plot",
        SwarmLayer,
        chart_keys=frozenset({"label", "value"}),
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "raincloudplot",
        "raincloud plot",
        ViolinLayer,
        chart_keys=frozenset({"label", "value"}),
        build=_raincloud_layers,
        multiplot=False,
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "ridgelineplot",
        "ridgeline plot",
        RidgelineLayer,
        chart_keys=frozenset({"label", "value"}),
        build=_ridgeline_layers,
        multiplot=False,
        group=True,
        emphasis_units=group_units,
        emphasis_by="median",
    ),
    ChartKind(
        "scatterchart",
        "scatter chart",
        ScatterLayer,
        chart_keys=frozenset({"hue", "label", "size", "x", "xerr", "y", "yerr"}),
        emphasis_units=series_units("y"),
        emphasis_by="mean",
    ),
    ChartKind(
        "heatmap",
        "heatmap",
        HeatmapLayer,
        chart_keys=frozenset({"colorbar", "norm", "valfmt", "vcenter", "vmax", "vmin"}),
        dict_data=True,
        data_keys=("z",),
        multiplot=False,
        rejects=_no_emphasis(
            "Heatmap",
            "a heatmap has no series to mute or highlight. Set the `emphasis` "
            "grid on `data` for per-cell roles instead.",
        ),
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
        chart_keys=frozenset({"colorbar", "norm", "valfmt", "vmax", "vmin"}),
        dict_data=True,
        # filled contour bands cover the grid
        gridless=_filled,
        emphasis_units=series_units("z"),
        emphasis_by="mean",
    ),
    ChartKind(
        "hexbinchart",
        "hexbin chart",
        HexbinLayer,
        chart_keys=frozenset(
            {
                "colorbar",
                "gridsize",
                "mincnt",
                "norm",
                "reduce",
                "valfmt",
                "vmax",
                "vmin",
            }
        ),
        dict_data=True,
        rejects=_no_emphasis(
            "HexbinChart",
            "a hexbin chart is a single colormapped layer with no series to "
            "mute or highlight.",
        ),
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
        dict_data=True,
        data_keys=("edges",),
        multiplot=False,
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
        multiplot=False,
        overlayable=False,
    ),
    ChartKind("imagechart", "image chart", ImageLayer, dict_data=True),
    ChartKind(
        "basemapchart",
        "basemap chart",
        BasemapLayer,
        dict_data=True,
        multiplot=False,
        subplots=False,
    ),
    ChartKind(
        "sankeychart",
        "Sankey",
        SankeyLayer,
        dict_data=True,
        data_keys=("links",),
        multiplot=False,
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
        multiplot=False,
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
        "date_period": validate_date_period(settings.get("period")),
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
        # validated here so a bad value fails at the front, like the emphasis roles
        "baseline": validate_baseline(settings.get("baseline")),
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
