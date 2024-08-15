"""Module containing the `typings`.

The `typings` module contains the typings for all chart components. The module
is intended to contain the typings for easier input value format checkup.

Attributes:
    ChartAttrs: The union of all chart attributes.

Classes:
    ChartCommonAttrs: The chart attributes common to all chart types.
    VLinePlotAttrs: The vertical line plot attributes.
    HLinePlotAttrs: The horizontal line plot attributes.
    LineChartAttrs: The line chart attributes.
    LineSingleChartAttrs: The single chart attributes for the line chart.
    LineDataPointAttrs: The data point attributes for the line chart.
    BarChartAttrs: The bar chart attributes.
    BarSingleChartAttrs: The single chart attributes for the bar chart.
    BarDataPointAttrs: The data point attributes for the bar chart.
    HistogramChartAttrs: The histogram chart attributes.
    HistogramSingleChartAttrs: The single chart attributes for the histogram chart.
    HistDataPointAttrs: The data point attributes for the histogram chart.
    HeatmapChartAttrs: The heatmap chart attributes.
    HeatmapSingleChartAttrs: The single chart attributes for the heatmap chart.
    HeatmapColorbarAttrs: The heatmap colorbar attributes.

    StyleAttrs: The style typing.
    ColorGeneralStyleAttrs: The typing for the general color style.
    FontStyleAttrs: The typing for the font style.
    AxesStyleAttrs: The typing for the axes style.
    LegendStyleAttrs: The typing for the legend style.
    AreaStyleAttrs: The typing for the area style.
    GridStyleAttrs: The typing for the grid style.
    LineStyleAttrs: The typing for the line style.
    BarStyleAttrs: The typing for the bar style.
    HistStyleAttrs: The typing for the histogram style.
    VLineStyleAttrs: The typing for the vertical line style.
    HLineStyleAttrs: The typing for the horizontal line style.
    HeatmapStyleAttrs: The typing for the heatmap style.

"""

from typing import TypedDict, Union, Tuple, List, Optional

import matplotlib.colors as colors
from .constants import (
    FIG_SIZE,
    FONT_STYLE,
    FONT_WEIGHT,
    HATCH_STYLE,
    LINE_MARKER,
    LINE_STYLE,
    LINE_DRAW_STYLE,
    HISTOGRAM_TYPE,
    LEGEND_ALIGN,
    ORIENTATION,
    COLORS,
    SHOW_GRID,
    SCALE,
)

# ================================================
# Config Definitions
# ================================================


class ColorGeneralStyleAttrs(TypedDict):
    """The typing for the general color style.

    Attributes:
        color_general_singular (Union[COLORS, str, None]): The general color for the singular-typed charts.
        color_general_multiple (Union[COLORS, str, None]): The general color for the multiple-typed charts.

    """

    color_general_singular: Union[COLORS, str, None]
    color_general_multiple: Union[COLORS, str, None]


class FontStyleAttrs(TypedDict):
    """The typing for the font style.

    Attributes:
        font_general_family (Union[str, None]): The general font family.
        font_general_sansserif (Union[List[str], None]): The general sans-serif font.
        font_general_color (Union[str, None]): The general font color.
        font_general_size (Union[int, float, str, None]): The general font size.
        font_general_style (Union[FONT_STYLE, str, None]): The general font style.
        font_general_weight (Union[FONT_WEIGHT, str, None]): The general font weight.

        font_title_size (Union[int, float, str, None]): The title font size.
        font_title_color (Union[str, None]): The title font color.
        font_title_style (Union[FONT_STYLE, str, None]): The title font style.
        font_title_weight (Union[FONT_WEIGHT, str, None]): The title font weight.

        font_subtitle_size (Union[int, float, str, None]): The subtitle font size.
        font_subtitle_color (Union[str, None]): The subtitle font color.
        font_subtitle_style (Union[FONT_STYLE, None]): The subtitle font style.
        font_subtitle_weight (Union[FONT_WEIGHT, None]): The subtitle font weight.

        font_xlabel_size (Union[int, float, str, None]): The xlabel font size.
        font_xlabel_color (Union[str, None]): The xlabel font color.
        font_xlabel_style (Union[FONT_STYLE, str, None]): The xlabel font style.
        font_xlabel_weight (Union[FONT_WEIGHT, str, None]): The xlabel font weight.

        font_ylabel_size (Union[int, float, str, None]): The ylabel font size.
        font_ylabel_color (Union[str, None]): The ylabel font color.
        font_ylabel_style (Union[FONT_STYLE, str, None]): The ylabel font style.
        font_ylabel_weight (Union[FONT_WEIGHT, str, None]): The ylabel font weight.

    """

    # general font style
    font_general_family: Union[str, None]
    font_general_sansserif: Union[List[str], None]
    font_general_color: Union[str, None]
    font_general_size: Union[int, float, str, None]
    font_general_style: Union[FONT_STYLE, str, None]
    font_general_weight: Union[FONT_WEIGHT, str, None]
    # title font style
    font_title_size: Union[int, float, str, None]
    font_title_color: Union[str, None]
    font_title_style: Union[FONT_STYLE, str, None]
    font_title_weight: Union[FONT_WEIGHT, str, None]
    # subtitle font style
    font_subtitle_size: Union[int, float, str, None]
    font_subtitle_color: Union[str, None]
    font_subtitle_style: Union[FONT_STYLE, None]
    font_subtitle_weight: Union[FONT_WEIGHT, None]
    # xlabel font style
    font_xlabel_size: Union[int, float, str, None]
    font_xlabel_color: Union[str, None]
    font_xlabel_style: Union[FONT_STYLE, str, None]
    font_xlabel_weight: Union[FONT_WEIGHT, str, None]
    # ylabel font style
    font_ylabel_size: Union[int, float, str, None]
    font_ylabel_color: Union[str, None]
    font_ylabel_style: Union[FONT_STYLE, str, None]
    font_ylabel_weight: Union[FONT_WEIGHT, str, None]


class AxesStyleAttrs(TypedDict):
    """The typing for the axes style.

    Attributes:
        axes_spines_top_visible (Union[bool, None]): Make the top plot spine visible.
        axes_spines_right_visible (Union[bool, None]): Make the right plot spine visible.
        axes_spines_bottom_visible (Union[bool, None]): Make the bottom plot spine visible.
        axes_spines_left_visible (Union[bool, None]): Make the left plot spine visible.
        axes_spines_width (Union[int, float, None]): The width of the spines.
        axes_spines_zorder (Union[int, None]): The zorder of the spines.
        axes_ticks_length (Union[int, float, None]): The length of the ticks.
        axes_ticks_label_size (Union[int, float, None]): The size of the tick labels.

    """

    axes_spines_top_visible: Union[bool, None]
    axes_spines_right_visible: Union[bool, None]
    axes_spines_bottom_visible: Union[bool, None]
    axes_spines_left_visible: Union[bool, None]
    axes_spines_width: Union[int, float, None]
    axes_spines_zorder: Union[int, None]
    axes_ticks_length: Union[int, float, None]
    axes_ticks_label_size: Union[int, float, None]


class LegendStyleAttrs(TypedDict):
    """The typing for the legend style.

    Attributes:
        plot_legend_shadow (Union[bool, None]): Show the legends shadow.
        plot_legend_frameon (Union[bool, None]): Show the legends frame.
        plot_legend_alignment (Union[LEGEND_ALIGN, str, None]): The legend alignment.
        plot_legend_font_size (Union[int, float, str, None]): The font size within the legend.
        plot_legend_title_size (Union[int, float, str, None]): The title size of the legend.
        plot_legend_label_color (Union[str, None]): The label color of the legend.

    """

    plot_legend_shadow: Union[bool, None]
    plot_legend_frameon: Union[bool, None]
    plot_legend_alignment: Union[LEGEND_ALIGN, str, None]
    plot_legend_font_size: Union[int, float, str, None]
    plot_legend_title_size: Union[int, float, str, None]
    plot_legend_label_color: Union[str, None]


class AreaStyleAttrs(TypedDict):
    """The typing for the area style.

    Attributes:
        plot_area_alpha (Union[float, None]): The alpha value of the area.
        plot_area_color (Union[str, None]): The color of the area.
        plot_area_linewidth (Union[int, float, None]): The line width of the area.
        plot_area_hatch (Union[HATCH_STYLE, str, None]): The hatch style of the area.
        plot_area_zorder (Union[int, None]): The zorder of the area.

    """

    plot_area_alpha: Union[float, None]
    plot_area_color: Union[str, None]
    plot_area_linewidth: Union[int, float, None]
    plot_area_hatch: Union[HATCH_STYLE, str, None]
    plot_area_zorder: Union[int, None]


class GridStyleAttrs(TypedDict):
    """The typing for the grid style.

    Attributes:
        plot_grid_alpha (Union[float, None]): The alpha value of the grid.
        plot_grid_color (Union[str, None]): The color of the grid.
        plot_grid_linewidth (Union[int, float, None]): The line width of the grid.
        plot_grid_linestyle (Union[LINE_STYLE, str, None]): The line style of the grid.
        plot_grid_zorder (Union[int, None]): The zorder of the grid.

    """

    plot_grid_alpha: Union[float, None]
    plot_grid_color: Union[str, None]
    plot_grid_linewidth: Union[int, float, None]
    plot_grid_linestyle: Union[LINE_STYLE, str, None]
    plot_grid_zorder: Union[int, None]


class LineStyleAttrs(TypedDict):
    """The typing for the line chart style.

    Attributes:
        plot_line_color (Union[str, None]): The line color.
        plot_line_alpha (Union[float, None]): The alpha value of the line.
        plot_line_style (Union[LINE_STYLE, str, None]): The line style.
        plot_line_marker (Union[LINE_MARKER, str, None]): The line marker.
        plot_line_width (Union[int, float, None]): The line width.
        plot_line_drawstyle (Union[LINE_DRAW_STYLE, str, None]): The line draw style.
        plot_line_zorder (Union[int, float, None]): The zorder of the line.
        plot_xticks_label_rotate (Union[int, float, None]): The label rotation of the xticks in the line chart.
        plot_yticks_label_rotate (Union[int, float, None]): The label rotation of the yticks in the line chart.

    """

    plot_line_color: Union[str, None]
    plot_line_style: Union[LINE_STYLE, str, None]
    plot_line_marker: Union[LINE_MARKER, str, None]
    plot_line_width: Union[int, float, None]
    plot_line_alpha: Union[float, None]
    plot_line_drawstyle: Union[LINE_DRAW_STYLE, str, None]
    plot_line_zorder: Union[int, float, None]
    plot_xticks_label_rotate: Union[int, float, None]
    plot_yticks_label_rotate: Union[int, float, None]


class BarStyleAttrs(TypedDict):
    """The typing for the bar chart style.

    Attributes:
        plot_bar_color (Union[str, None]): The bar color.
        plot_bar_alpha (Union[float, None]): The alpha value of the bar.
        plot_bar_width (Union[int, float, None]): The width of the bar.
        plot_bar_zorder (Union[int, float, None]): The zorder of the bar.
        plot_bar_hatch (Union[HATCH_STYLE, str, None]): The hatch style of the bar.
        plot_bar_edge_width (Union[int, float, None]): The edge width of the bar.
        plot_bar_edge_color (Union[str, None]): The edge color of the bar.
        plot_bar_error_color (Union[str, None]): The color of the error line of the bar.
        plot_xticks_label_rotate (Union[int, float, None]): The label rotation of the xticks in the bar chart.
        plot_yticks_label_rotate (Union[int, float, None]): The label rotation of the yticks in the bar chart.

    """

    plot_bar_color: Union[str, None]
    plot_bar_alpha: Union[float, None]
    plot_bar_width: Union[int, float, None]
    plot_bar_zorder: Union[int, float, None]
    plot_bar_hatch: Union[HATCH_STYLE, str, None]
    plot_bar_edge_width: Union[int, float, None]
    plot_bar_edge_color: Union[str, None]
    plot_bar_error_color: Union[str, None]
    plot_xticks_label_rotate: Union[int, float, None]
    plot_yticks_label_rotate: Union[int, float, None]


class HistStyleAttrs(TypedDict):
    """The typing for the histogram chart style.

    Attributes:
        plot_hist_color (Union[str, None]): The color of the histogram.
        plot_hist_alpha (Union[float, None]): The alpha value of the histogram.
        plot_hist_zorder (Union[int, float, None]): The zorder of the histogram.
        plot_hist_fill (Union[str, None]): The fill of the histogram.
        plot_hist_hatch (Union[HATCH_STYLE, str, None]): The hatch style in the histogram.
        plot_hist_type (Union[HISTOGRAM_TYPE, str, None]): The type of the histogram.
        plot_hist_align (Union[str, None]): The alignment of the histogram.
        plot_hist_edge_width (Union[int, float, None]): The edge width of the histogram.
        plot_hist_edge_color (Union[str, None]): The edge color of the histogram.
        plot_xticks_label_rotate (Union[int, float, None]): The label rotation of the xticks in the histogram chart.
        plot_yticks_label_rotate (Union[int, float, None]): The label rotation of the yticks in the histogram chart.

    """

    plot_hist_color: Union[str, None]
    plot_hist_alpha: Union[float, None]
    plot_hist_zorder: Union[int, float, None]
    plot_hist_fill: Union[str, None]
    plot_hist_hatch: Union[HATCH_STYLE, str, None]
    plot_hist_type: Union[HISTOGRAM_TYPE, str, None]
    plot_hist_align: Union[str, None]
    plot_hist_edge_width: Union[int, float, None]
    plot_hist_edge_color: Union[str, None]
    plot_xticks_label_rotate: Union[int, float, None]
    plot_yticks_label_rotate: Union[int, float, None]


class VLineStyleAttrs(TypedDict):
    """The typing for the vertical line style.

    Attributes:
        plot_vline_color (Union[str, None]): The color of the vertical line.
        plot_vline_style (Union[LINE_STYLE, str, None]): The style of the vertical line.
        plot_vline_width (Union[int, float, None]): The width of the vertical line.
        plot_vline_alpha (Union[float, None]): The alpha value of the vertical line.

    """

    plot_vline_color: Union[str, None]
    plot_vline_style: Union[LINE_STYLE, str, None]
    plot_vline_width: Union[int, float, None]
    plot_vline_alpha: Union[float, None]


class HLineStyleAttrs(TypedDict):
    """The typing for the horizontal line style.

    Attributes:
        plot_hline_color (Union[str, None]): The color of the horizontal line.
        plot_hline_style (Union[LINE_STYLE, str, None]): The style of the horizontal line.
        plot_hline_width (Union[int, float, None]): The width of the horizontal line.
        plot_hline_alpha (Union[float, None]): The alpha value of the horizontal line.

    """

    plot_hline_color: Union[str, None]
    plot_hline_style: Union[LINE_STYLE, str, None]
    plot_hline_width: Union[int, float, None]
    plot_hline_alpha: Union[float, None]


class HeatmapStyleAttrs(TypedDict):
    """The typing for the heatmap chart style.

    Attributes:
        plot_heatmap_cmap (Union[str, colors.LinearSegmentedColormap, None]): The color map of the heatmap.
        plot_heatmap_alpha (Union[float, None]): The alpha value of the heatmap.
        plot_heatmap_font_size (Union[int, float, str, None]): The font size of the heatmap.
        plot_heatmap_font_color (Union[str, None]): The font color of the heatmap.
        plot_heatmap_font_style (Union[FONT_STYLE, str, None]): The font style of the heatmap.
        plot_heatmap_font_weight (Union[FONT_WEIGHT, str, None]): The font weight of the heatmap.

    """

    plot_heatmap_cmap: Union[str, colors.LinearSegmentedColormap, None]
    plot_heatmap_alpha: Union[float, None]
    plot_heatmap_font_size: Union[int, float, str, None]
    plot_heatmap_font_color: Union[str, None]
    plot_heatmap_font_style: Union[FONT_STYLE, str, None]
    plot_heatmap_font_weight: Union[FONT_WEIGHT, str, None]


class StyleAttrs(
    ColorGeneralStyleAttrs,
    FontStyleAttrs,
    AxesStyleAttrs,
    LegendStyleAttrs,
    AreaStyleAttrs,
    GridStyleAttrs,
    LineStyleAttrs,
    BarStyleAttrs,
    HistStyleAttrs,
    VLineStyleAttrs,
    HLineStyleAttrs,
    HeatmapStyleAttrs,
):
    """The style attributes. Combines all style typings."""

    pass


# ================================================
# Common Chart Attributes
# ================================================


class ChartCommonAttrs(TypedDict):
    """The chart attributes common to all chart types.

    Attributes:
        title (Union[str, None]): The title of the charts.
        xlabel (Union[str, None]): The xlabel of the charts.
        ylabel (Union[str, None]): The ylabel of the charts.
        figsize (Union[FIG_SIZE, Tuple[float, float], None]): The size of the figure.
        xmin (Union[int, float, None]): Determine the minimum x-axis value.
        xmax (Union[int, float, None]): Determine the maximum x-axis value.
        ymin (Union[int, float, None]): Determine the minimum y-axis value.
        ymax (Union[int, float, None]): Determine the maximum y-axis value.
        show_legend (Union[bool, None]): Whether or not to show the legend.
        show_grid (Union[SHOW_GRID, str, None]): Determine which grid lines to show.
        scalex (Union[SCALE, str, None]): The scale of the x-axis.
        scaley (Union[SCALE, str, None]): The scale of the y-axis.
        aspect_ratio (Union[str, None]): The aspect ratio of the charts.

        subplots (Union[bool, None]): Whether or not to create a separate subplot for each chart.
        max_cols (Union[int, None]): The maximum number of columns in the subplots. Active only when `subplots` is `True`.
        sharex (Union[bool, None]): Whether or not to share the x-axis in the subplots. Active only when `subplots` is `True`.
        sharey (Union[bool, None]): Whether or not to share the y-axis in the subplots. Active only when `subplots` is `True`.

    """

    title: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    figsize: Union[FIG_SIZE, Tuple[float, float], None]
    xmin: Union[int, float, None]
    xmax: Union[int, float, None]
    ymin: Union[int, float, None]
    ymax: Union[int, float, None]
    # visibility attributes
    show_legend: Union[bool, None]
    show_grid: Union[SHOW_GRID, str, None]
    scalex: Union[SCALE, str, None]
    scaley: Union[SCALE, str, None]
    aspect_ratio: Union[str, None]
    # the subplot attributes
    subplots: Union[bool, None]
    max_cols: Union[int, None]
    sharex: Union[bool, None]
    sharey: Union[bool, None]


# ================================================
# Vertical and Horizontal Line Attributes
# ================================================


class VLinePlotAttrs(TypedDict):
    """The vertical line plot attributes.

    Attributes:
        x (Union[int, float]): The x-axis position of the line.
        ymin (Union[int, float, None]): The minimum y-axis position value.
        ymax (Union[int, float, None]): The maximum y-axis position value.
        style (Union[VLineStyleAttrs, None]): The vertical line style attributes.
        label (Union[str, None]): The label of the vertical line.

    """

    x: Union[int, float]
    ymin: Union[int, float, None]
    ymax: Union[int, float, None]
    style: Union[VLineStyleAttrs, None]
    label: Union[str, None]


class HLinePlotAttrs(TypedDict):
    """The horizontal line plot attributes.

    Attributes:
        y (Union[int, float]): The x-axis position of the line.
        xmin (Union[int, float, None]): The minimum y-axis position value.
        xmax (Union[int, float, None]): The maximum y-axis position value.
        style (Union[HLineStyleAttrs, None]): The horizontal line style attributes.
        label (Union[str, None]): The label of the horizontal line.

    """

    y: Union[int, float]
    xmin: Union[int, float, None]
    xmax: Union[int, float, None]
    style: Union[HLineStyleAttrs, None]
    label: Union[str, None]


# ================================================
# Line Chart Attributes
# ================================================


class LineDataPointAttrs(TypedDict):
    """The data point attributes for the line chart.

    Attributes:
        x (Union[int, float]): The x-axis value.
        y (Union[int, float]): The y-axis value.
        yerr (Optional[Union[int, float]]): The y-axis error value.

    """

    # the default attributes, could be anything
    x: Union[int, float]
    y: Union[int, float]
    yerr: Optional[Union[int, float]]


class LineSingleChartAttrs(TypedDict):
    """The single chart attributes for the line chart.

    Attributes:
        data (List[LineDataPointAttrs]): The list of data points defining the line chart.
        subtitle (Union[str, None]): The subtitle of the line chart. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the line chart.
        ylabel (Union[str, None]): The ylabel of the line chart.
        style (Union[LineStyleAttrs, None]): The style of the line chart.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLinePlotAttrs, List[VLinePlotAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLinePlotAttrs, List[HLinePlotAttrs], None]): The horizontal lines to be plot.
        x (Union[str, None]): The key name in `data` that contains the x-axis value. Defaults to `"x"`.
        y (Union[str, None]): The key name in `data` that contains the y-axis value. Defaults to `"y"`.
        yerr (Union[str, None]): The key name in `data` that contains the y-axis error value. Defaults to `"yerr"`.

    """

    data: List[LineDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[LineStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLinePlotAttrs, List[VLinePlotAttrs]]
    hlines: Union[HLinePlotAttrs, List[HLinePlotAttrs]]

    x: Union[str, None] = "x"  # the name of the x attribute in data
    y: Union[str, None] = "y"  # the name of the y attribute in data
    yerr: Union[str, None] = "yerr"  # the name of the yerr attribute in data


class LineChartAttrs(ChartCommonAttrs):
    """The line chart attributes.

    Attributes:
        charts (Union[LineSingleChartAttrs, List[LineSingleChartAttrs]]): The line chart definitions.
        show_yerr (Union[bool, None]): Whether or not to show the y-axis errors.
        show_area (Union[bool, None]): Whether or not to show the area under the lines.

    """

    charts: Union[LineSingleChartAttrs, List[LineSingleChartAttrs]]
    show_yerr: Union[bool, None]
    show_area: Union[bool, None]


# ================================================
# Bar Chart Attributes
# ================================================


class BarDataPointAttrs(TypedDict):
    """The data point attributes for the bar chart.

    Attributes:
        label (str): The label.
        y (Union[int, float]): The y-axis value.
        yerr (Optional[Union[int, float]]): The y-axis error value.

    """

    # the default attributes, could be anything
    label: str
    y: Union[int, float]
    yerr: Optional[Union[int, float]]


class BarSingleChartAttrs(TypedDict):
    """The single chart attributes for the bar chart.

    Attributes:
        data (List[BarDataPointAttrs]): The list of data points defining the bar chart.
        subtitle (Union[str, None]): The subtitle of the bar chart. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the bar chart.
        ylabel (Union[str, None]): The ylabel of the bar chart.
        style (Union[BarStyleAttrs, None]): The style of the bar chart.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLinePlotAttrs, List[VLinePlotAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLinePlotAttrs, List[HLinePlotAttrs], None]): The horizontal lines to be plot.
        label (Union[str, None]): The key name in `data` that contains the label value. Defaults to `"label"`.
        y (Union[str, None]): The key name in `data` that contains the y-axis value. Defaults to `"y"`.
        yerr (Union[str, None]): The key name in `data` that contains the y-axis error value. Defaults to `"yerr"`.

    """

    data: List[BarDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[BarStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLinePlotAttrs, List[VLinePlotAttrs]]
    hlines: Union[HLinePlotAttrs, List[HLinePlotAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    y: Union[str, None]  # the name of the y attribute in data
    yerr: Union[str, None]  # the name of the yerr attribute in data


class BarChartAttrs(ChartCommonAttrs):
    """The bar chart attributes.

    Attributes:
        charts (Union[BarSingleChartAttrs, List[BarSingleChartAttrs]]): The bar chart definitions.
        show_yerr (Union[bool, None]): Whether or not to show the y-axis errors.
        orientation (Union[ORIENTATION, str, None]): The orientation of the bar charts.

    """

    charts: Union[BarSingleChartAttrs, List[BarSingleChartAttrs]]
    show_yerr: Union[bool, None]
    orientation: Union[ORIENTATION, str, None]


# ================================================
# Hist Chart Attributes
# ================================================


class HistDataPointAttrs(TypedDict):
    """The data point attributes for the histogram chart.

    Attributes:
        x (Union[int, float]): The x-axis value.

    """

    # the default attributes, could be anything
    x: Union[int, float]


class HistogramSingleChartAttrs(TypedDict):
    """The single chart attributes for the histogram chart.

    Attributes:
        data (List[HistDataPointAttrs]): The list of data points defining the histogram chart.
        subtitle (Union[str, None]): The subtitle of the histogram chart. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the histogram chart.
        ylabel (Union[str, None]): The ylabel of the histogram chart.
        style (Union[HistStyleAttrs, None]): The style of the histogram chart.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLinePlotAttrs, List[VLinePlotAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLinePlotAttrs, List[HLinePlotAttrs], None]): The horizontal lines to be plot.
        x (Union[str, None]): The key name in `data` that contains the x-axis value. Defaults to `"x"`.

    """

    data: List[HistDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[HistStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLinePlotAttrs, List[VLinePlotAttrs]]
    hlines: Union[HLinePlotAttrs, List[HLinePlotAttrs]]

    x: Union[str, None]  # the name of the x attribute in data


class HistogramChartAttrs(ChartCommonAttrs):
    """The histogram chart attributes.

    Attributes:
        charts (Union[HistogramSingleChartAttrs, List[HistogramSingleChartAttrs]]): The histogram chart definitions.
        orientation (Union[ORIENTATION, str, None]): The orientation of the histogram charts.
        num_bins (Union[int, None]): The number of bins the data points are split in to create the histogram.
        show_density (Union[bool, None]): Whether or not to plot the density histogram.
        show_cumulative (Union[bool, None]): Whether or not to plot the cumulative histogram.

    """

    charts: Union[HistogramSingleChartAttrs, List[HistogramSingleChartAttrs]]
    orientation: Union[ORIENTATION, str, None]
    num_bins: Union[int, None]
    show_density: Union[bool, None]
    show_cumulative: Union[bool, None]


# ================================================
# Heatmap Chart Attributes
# ================================================


class HeatmapColorbarAttrs(TypedDict):
    """The heatmap colorbar attributes.

    Attributes:
        orientation (Union[ORIENTATION, str, None]): The orientation.

    """

    orientation: Union[ORIENTATION, str, None]


class HeatmapSingleChartAttrs(TypedDict):
    """The single chart attributes for the heatmap chart.

    Attributes:
        data (List[List[Union[int, float, None]]]): The list of data points defining the heatmap chart.
        subtitle (Union[str, None]): The subtitle of the heatmap chart. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the heatmap chart.
        ylabel (Union[str, None]): The ylabel of the heatmap chart.
        style (Union[HeatmapStyleAttrs, None]): The style of the heatmap chart.

        norm (Union[NORMALIZE, str, None]): The value normalization.
        vmin (Union[str, None]): The minimum value to normalize the data points.
        vmax (Union[str, None]): The maximum value to normalize the data points.

        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.

        colorbar (Union[HeatmapColorbarAttrs, None]): The heatmap colorbar attributes.

    """

    data: List[List[Union[int, float, None]]]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[HeatmapStyleAttrs, None]

    norm: Union[str, None]
    vmin: Union[float, None]
    vmax: Union[float, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    colorbar: Union[HeatmapColorbarAttrs, None]


class HeatmapChartAttrs(ChartCommonAttrs):
    """The heatmap chart attributes.

    Attributes:
        charts (Union[HeatmapSingleChartAttrs, List[HeatmapSingleChartAttrs]]): The heatmap chart definitions.
        show_colorbars (Union[bool, None]): Whether or not to plot the density histogram.
        show_heatmap_values (Union[bool, None]): Whether or not to plot the heatmap values.

    """

    charts: Union[HeatmapSingleChartAttrs, List[HeatmapSingleChartAttrs]]
    show_colorbars: Union[bool, None]
    show_heatmap_values: Union[bool, None]


# ================================================
# Chart Attributes
# ================================================


ChartAttrs = Union[
    LineChartAttrs, BarChartAttrs, HistogramChartAttrs, HeatmapChartAttrs
]
"""The union of all chart attributes."""
