from typing import TypedDict, Union, Tuple, List, Optional

import matplotlib.colors as colors
from .constants import (
    FONT_STYLE,
    FONT_WEIGHT,
    HATCH_STYLE,
    LINE_MARKER,
    LINE_STYLE,
    LINE_DRAW_STYLE,
    LEGEND_ALIGN,
)

# ================================================
# Config Definitions
# ================================================

ColorGeneralAttrs = TypedDict(
    "ColorGeneralAttrs",
    {
        "color.general.singular": Union[str, None],
        "color.general.multiple": Union[str, None],
    },
)

FontConfigAttrs = TypedDict(
    "FontConfigAttrs",
    {
        # general font configuration
        "font.general.family": Union[str, None],
        "font.general.sans-serif": Union[List[str], None],
        "font.general.color": Union[str, None],
        "font.general.size": Union[int, float, str, None],
        "font.general.style": Union[FONT_STYLE, None],
        "font.general.weight": Union[FONT_WEIGHT, None],
        # title font configuration
        "font.title.size": Union[int, float, str, None],
        "font.title.color": Union[str, None],
        "font.title.style": Union[FONT_STYLE, None],
        "font.title.weight": Union[FONT_WEIGHT, None],
        # subtitle font configuration
        "font.subtitle.size": Union[int, float, str, None],
        "font.subtitle.color": Union[str, None],
        "font.subtitle.style": Union[FONT_STYLE, None],
        "font.subtitle.weight": Union[FONT_WEIGHT, None],
        # xlabel font configuration
        "font.xlabel.size": Union[int, float, str, None],
        "font.xlabel.color": Union[str, None],
        "font.xlabel.style": Union[FONT_STYLE, None],
        "font.xlabel.weight": Union[FONT_WEIGHT, None],
        # ylabel font configuration
        "font.ylabel.size": Union[int, float, str, None],
        "font.ylabel.color": Union[str, None],
        "font.ylabel.style": Union[FONT_STYLE, None],
        "font.ylabel.weight": Union[FONT_WEIGHT, None],
    },
)

AxesConfigAttrs = TypedDict(
    "AxesConfigAttrs",
    {
        "axes.spines.top.visible": Union[bool, None],
        "axes.spines.right.visible": Union[bool, None],
        "axes.spines.bottom.visible": Union[bool, None],
        "axes.spines.left.visible": Union[bool, None],
        "axes.spines.width": Union[int, float, None],
        "axes.spines.zorder": Union[int, None],
        "axes.ticks.length": Union[int, float, None],
        "axes.ticks.label.size": Union[int, float, None],
    },
)

LegendConfigAttrs = TypedDict(
    "LegendConfigAttrs",
    {
        "plot.legend.shadow": Union[bool, None],
        "plot.legend.frameon": Union[bool, None],
        "plot.legend.alignment": Union[LEGEND_ALIGN, None],
        "plot.legend.font.size": Union[int, float, str, None],
        "plot.legend.title.size": Union[int, float, str, None],
        "plot.legend.label.color": Union[str, None],
    },
)

AreaConfigAttrs = TypedDict(
    "AreaConfigAttrs",
    {
        "plot.area.alpha": Union[float, None],
        "plot.area.color": Union[str, None],
        "plot.area.line.width": Union[int, float, None],
        "plot.area.hatch": Union[HATCH_STYLE, None],
        "plot.area.zorder": Union[int, None],
    },
)

GridConfigAttrs = TypedDict(
    "GridConfigAttrs",
    {
        "plot.grid.alpha": Union[float, None],
        "plot.grid.color": Union[str, None],
        "plot.grid.linewidth": Union[int, float, None],
        "plot.grid.linestyle": Union[LINE_STYLE, None],
        "plot.grid.zorder": Union[int, None],
    },
)

LineConfigAttrs = TypedDict(
    "LineConfigAttrs",
    {
        "plot.line.color": Union[str, None],
        "plot.line.style": Union[LINE_STYLE, None],
        "plot.line.marker": Union[LINE_MARKER, None],
        "plot.line.width": Union[int, float, None],
        "plot.line.alpha": Union[float, None],
        "plot.line.drawstyle": Union[LINE_DRAW_STYLE, None],
        "plot.line.zorder": Union[int, float, None],
        "plot.xticks.label.rotate": Union[int, float, None],
        "plot.yticks.label.rotate": Union[int, float, None],
    },
)

BarConfigAttrs = TypedDict(
    "BarConfigAttrs",
    {
        "plot.bar.color": Union[str, None],
        "plot.bar.alpha": Union[float, None],
        "plot.bar.width": Union[int, float, None],
        "plot.bar.zorder": Union[int, float, None],
        "plot.bar.hatch": Union[HATCH_STYLE, None],
        "plot.bar.edge.width": Union[int, float, None],
        "plot.bar.edge.color": Union[str, None],
        "plot.bar.error.color": Union[str, None],
        "plot.xticks.label.rotate": Union[int, float, None],
        "plot.yticks.label.rotate": Union[int, float, None],
    },
)

HistConfigAttrs = TypedDict(
    "HistConfigAttrs",
    {
        "plot.hist.color": Union[str, None],
        "plot.hist.alpha": Union[float, None],
        "plot.hist.zorder": Union[int, float, None],
        "plot.hist.fill": Union[str, None],
        "plot.hist.hatch": Union[HATCH_STYLE, None],
        "plot.hist.type": Union[str, None],
        "plot.hist.align": Union[str, None],
        "plot.hist.edge.width": Union[int, float, None],
        "plot.hist.edge.color": Union[str, None],
        "plot.xticks.label.rotate": Union[int, float, None],
        "plot.yticks.label.rotate": Union[int, float, None],
    },
)

VLineConfigAttrs = TypedDict(
    "VLineConfigAttrs",
    {
        "plot.vline.color": Union[str, None],
        "plot.vline.style": Union[LINE_STYLE, None],
        "plot.vline.width": Union[int, float, None],
        "plot.vline.alpha": Union[float, None],
    },
)

HLineConfigAttrs = TypedDict(
    "HLineConfigAttrs",
    {
        "plot.hline.color": Union[str, None],
        "plot.hline.style": Union[LINE_STYLE, None],
        "plot.hline.width": Union[int, float, None],
        "plot.hline.alpha": Union[float, None],
    },
)

HeatmapConfigAttrs = TypedDict(
    "HeatmapConfigAttrs",
    {
        "plot.heatmap.cmap": Union[str, colors.LinearSegmentedColormap, None],
        "plot.heatmap.alpha": Union[float, None],
        "plot.heatmap.font.size": Union[int, float, str, None],
        "plot.heatmap.font.color": Union[str, None],
        "plot.heatmap.font.style": Union[FONT_STYLE, None],
        "plot.heatmap.font.weight": Union[FONT_WEIGHT, None],
    },
)


class ConfigAttrs(
    ColorGeneralAttrs,
    FontConfigAttrs,
    AxesConfigAttrs,
    LegendConfigAttrs,
    AreaConfigAttrs,
    GridConfigAttrs,
    LineConfigAttrs,
    BarConfigAttrs,
    HistConfigAttrs,
    VLineConfigAttrs,
    HLineConfigAttrs,
    HeatmapConfigAttrs,
):
    pass


# ================================================
# Common Definitions
# ================================================


class ChartCommonAttrs(TypedDict):
    title: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    sharex: Union[bool, None]
    sharey: Union[bool, None]
    subplots: Union[bool, None]
    max_cols: Union[int, None]
    aspect_ratio: Union[str, None]
    figsize: Union[Tuple[float, float], None]
    xmin: Union[int, float, None]
    xmax: Union[int, float, None]
    ymin: Union[int, float, None]
    ymax: Union[int, float, None]
    # visibility attributes
    show_legend: Union[bool, None]
    show_grid: Union[str, None]
    # chart scale attributes
    log_scale: Union[bool, None]


# ================================================
# Vertical and Horizontal Line Definitions
# ================================================


class VLineAttrs(TypedDict):
    x: Union[int, float]
    ymin: Union[int, float, None]
    ymax: Union[int, float, None]
    style: Union[VLineConfigAttrs, None]
    label: Union[str, None]


class HLineAttrs(TypedDict):
    y: Union[int, float]
    xmin: Union[int, float, None]
    xmax: Union[int, float, None]
    style: Union[HLineConfigAttrs, None]
    label: Union[str, None]


# ================================================
# Line Chart Definitions
# ================================================


class LineDataPointAttrs(TypedDict):
    # the default attributes, could be anything
    x: Union[int, float]
    y: Union[int, float]
    yerr: Optional[Union[int, float]]


class LineDataAttrs(TypedDict):
    data: List[LineDataPointAttrs]
    x: Union[str, None]  # the name of the x attribute in data
    y: Union[str, None]  # the name of the y attribute in data
    yerr: Union[str, None]  # the name of the yerr attribute in data
    style: Union[LineConfigAttrs, None]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineAttrs, List[VLineAttrs]]
    hlines: Union[HLineAttrs, List[HLineAttrs]]


class LineChartAttrs(ChartCommonAttrs):
    charts: Union[LineDataAttrs, List[LineDataAttrs]]
    show_yerr: Union[bool, None]
    show_area: Union[bool, None]


# ================================================
# Bar Chart Definitions
# ================================================


class BarDataPointAttrs(TypedDict):
    # the default attributes, could be anything
    label: str
    y: Union[int, float]
    yerr: Optional[Union[int, float]]


class BarDataAttrs(TypedDict):
    data: List[BarDataPointAttrs]
    label: Union[str, None]  # the name of the label attribute in data
    y: Union[str, None]  # the name of the y attribute in data
    yerr: Union[str, None]  # the name of the yerr attribute in data
    style: Union[BarConfigAttrs, None]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineAttrs, List[VLineAttrs]]
    hlines: Union[HLineAttrs, List[HLineAttrs]]


class BarChartAttrs(ChartCommonAttrs):
    charts: Union[BarDataAttrs, List[BarDataAttrs]]
    show_yerr: Union[bool, None]
    orientation: Union[str, None]


# ================================================
# Hist Chart Definitions
# ================================================


class HistDataPointAttrs(TypedDict):
    # the default attributes, could be anything
    x: Union[int, float]


class HistDataAttrs(TypedDict):
    data: List[HistDataPointAttrs]
    x: Union[str, None]  # the name of the x attribute in data
    style: Union[HistConfigAttrs, None]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineAttrs, List[VLineAttrs]]
    hlines: Union[HLineAttrs, List[HLineAttrs]]


class HistChartAttrs(ChartCommonAttrs):
    charts: Union[HistDataAttrs, List[HistDataAttrs]]
    orientation: Union[str, None]
    num_bins: Union[int, None]
    show_density: Union[bool, None]
    show_cumulative: Union[bool, None]


# ================================================
# Heatmap Chart Definitions
# ================================================


class HeatmapColorbarAttrs(TypedDict):
    orientation: Union[str, None]


class HeatmapDataAttrs(TypedDict):
    data: List[List[Union[int, float, None]]]
    style: Union[HeatmapConfigAttrs, None]
    norm: Union[str, None]
    vmin: Union[float, None]
    vmax: Union[float, None]

    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    colorbar: Union[HeatmapColorbarAttrs, None]


class HeatmapChartAttrs(ChartCommonAttrs):
    charts: Union[HistDataAttrs, List[HistDataAttrs]]
    show_colorbars: Union[bool, None]
    show_heatmap_vals: Union[bool, None]


# ================================================
# Union Chart Definition
# ================================================

UnionChartAttrs = Union[
    LineChartAttrs, BarChartAttrs, HistChartAttrs, HeatmapChartAttrs
]
