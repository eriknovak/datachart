from typing import TypedDict, Union, Tuple, List

from schema.constants import LineStyle, LineMarker, LineDrawStyle, FontStyle, FontWeight


# ================================================
# Config Definitions
# ================================================


LineConfigAttrs = TypedDict(
    "LineConfigAttrs",
    {
        "plot.line.color": Union[str, None],
        "plot.line.alpha": Union[float, None],
        "plot.line.width": Union[int, float, None],
        "plot.line.style": Union[LineStyle, None],
        "plot.line.marker": Union[LineMarker, None],
        "plot.line.drawstyle": Union[LineDrawStyle, None],
    },
)

AreaConfigAttrs = TypedDict(
    "AreaConfigAttrs",
    {
        "plot.area.alpha": Union[float, None],
        "plot.area.color": Union[str, None],
        "plot.area.linewidth": Union[int, float, None],
    },
)

GridConfigAttrs = TypedDict(
    "GridConfigAttrs",
    {
        "plot.grid.alpha": Union[float, None],
        "plot.grid.color": Union[str, None],
        "plot.grid.linewidth": Union[int, float, None],
        "plot.grid.linestyle": Union[LineStyle, None],
    },
)


AxesConfigAttrs = TypedDict(
    "AxesConfigAttrs",
    {
        "axes.spines.top.visible": Union[bool, None],
        "axes.spines.right.visible": Union[bool, None],
        "axes.spines.left.visible": Union[bool, None],
        "axes.spines.bottom.visible": Union[bool, None],
        "axes.spines.width": Union[int, float, None],
        "axes.ticks.length": Union[int, float, None],
        "axes.ticks.label.size": Union[int, float, None],
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
        "font.general.style": Union[FontStyle, None],
        "font.general.weight": Union[FontWeight, None],
        "font.title.size": Union[int, float, str, None],
        # title font configuration
        "font.title.color": Union[str, None],
        "font.title.style": Union[FontStyle, None],
        "font.title.weight": Union[FontWeight, None],
        # subtitle font configuration
        "font.subtitle.size": Union[int, float, str, None],
        "font.subtitle.color": Union[str, None],
        "font.subtitle.style": Union[FontStyle, None],
        "font.subtitle.weight": Union[FontWeight, None],
        # xlabel font configuration
        "font.xlabel.size": Union[int, float, str, None],
        "font.xlabel.color": Union[str, None],
        "font.xlabel.style": Union[FontStyle, None],
        "font.xlabel.weight": Union[FontWeight, None],
        # ylabel font configuration
        "font.ylabel.size": Union[int, float, str, None],
        "font.ylabel.color": Union[str, None],
        "font.ylabel.style": Union[FontStyle, None],
        "font.ylabel.weight": Union[FontWeight, None],
    },
)


class ConfigAttrs(LineConfigAttrs, AreaConfigAttrs, AxesConfigAttrs, FontConfigAttrs):
    pass


# ================================================
# Common Definitions
# ================================================


class ChartCommonAttrs(TypedDict):
    figsize: Union[Tuple[int, int], None]
    title: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    sharex: Union[bool, None]
    sharey: Union[bool, None]


class DataPointAttrs(TypedDict):
    x: Union[int, float]
    y: Union[int, float]


# ================================================
# Line Chart Definitions
# ================================================


class LineDataAttrs(TypedDict):
    data: List[DataPointAttrs]
    x: Union[str, None]
    y: Union[str, None]
    delta: Union[str, None]
    style: Union[LineConfigAttrs, None]
    subtitle: Union[str, None]


class LineChartAttrs(ChartCommonAttrs):
    charts: Union[LineDataAttrs, List[LineDataAttrs]]
    show_confidence_interval: Union[bool, None]
    show_separate: Union[bool, None]
    show_grid: Union[bool, None]


# ================================================
# Line Chart Definitions
# ================================================


class BarDataPointAttrs(DataPointAttrs):
    label: Union[str, None]


class BarDataAttrs(TypedDict):
    data: List[BarDataPointAttrs]
    x: Union[str, None]
    y: Union[str, None]
    subtitle: Union[str, None]


class BarChartAttrs(ChartCommonAttrs):
    charts: Union[BarDataAttrs, List[BarDataAttrs]]
    show_separate: Union[bool, None]
