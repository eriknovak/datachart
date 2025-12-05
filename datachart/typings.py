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
    ScatterChartAttrs: The scatter chart attributes.
    ScatterSingleChartAttrs: The single chart attributes for the scatter chart.
    ScatterDataPointAttrs: The data point attributes for the scatter chart.
    BoxChartAttrs: The box plot chart attributes.
    BoxSingleChartAttrs: The single chart attributes for the box plot.
    BoxDataPointAttrs: The data point attributes for the box plot.
    ParallelCoordsChartAttrs: The parallel coordinates chart attributes.
    ParallelCoordsSingleChartAttrs: The single chart attributes for the parallel coordinates chart.
    ParallelCoordsDataPointAttrs: The data point attributes for the parallel coordinates chart.

    StyleAttrs: The style typing.
    ColorStyleAttrs: The typing for the general color style.
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
    ScatterStyleAttrs: The typing for the scatter chart style.
    RegressionStyleAttrs: The typing for the regression line style.
    BoxStyleAttrs: The typing for the box plot style.
    ParallelCoordsStyleAttrs: The typing for the parallel coordinates chart style.

"""

from typing import TypedDict, Union, Tuple, List, Optional, Dict

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
    LEGEND_LOCATION,
    ORIENTATION,
    COLORS,
    SHOW_GRID,
    SCALE,
    ASPECT_RATIO,
)

# ================================================
# Config Definitions
# ================================================


class ColorStyleAttrs(TypedDict):
    """The typing for the general color style.

    Attributes:
        color_general_singular (Union[COLORS, str, None]): The general color for the singular-typed charts.
        color_general_multiple (Union[COLORS, str, List[str], None]): The general color for the multiple-typed charts (palette name or list of hex colors).
        color_parallel_hue (Union[COLORS, str, List[str], None]): The color palette for parallel coords hue categories (palette name or list of hex colors).

    """

    color_general_singular: Union[COLORS, str, List[str], None]
    color_general_multiple: Union[COLORS, str, List[str], None]
    color_parallel_hue: Union[COLORS, str, List[str], None]


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
        plot_legend_location (Union[LEGEND_LOCATION, str, None]): The legend location.
        plot_legend_font_size (Union[int, float, str, None]): The font size within the legend.
        plot_legend_title_size (Union[int, float, str, None]): The title size of the legend.
        plot_legend_label_color (Union[str, None]): The label color of the legend.

    """

    plot_legend_shadow: Union[bool, None]
    plot_legend_frameon: Union[bool, None]
    plot_legend_alignment: Union[LEGEND_ALIGN, str, None]
    plot_legend_location: Union[LEGEND_LOCATION, str, None]
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
        plot_bar_value_fontsize (Union[int, float, None]): The font size of the bar value labels.
        plot_bar_value_color (Union[str, None]): The color of the bar value labels.
        plot_bar_value_padding (Union[int, float, None]): The padding between bar edge and value label.
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
    plot_bar_value_fontsize: Union[int, float, None]
    plot_bar_value_color: Union[str, None]
    plot_bar_value_padding: Union[int, float, None]
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


class ScatterStyleAttrs(TypedDict):
    """The typing for the scatter chart style.

    Attributes:
        plot_scatter_color (Union[str, None]): The scatter marker color.
        plot_scatter_alpha (Union[float, None]): The alpha value of the markers.
        plot_scatter_size (Union[int, float, None]): The marker size.
        plot_scatter_marker (Union[LINE_MARKER, str, None]): The marker shape.
        plot_scatter_zorder (Union[int, float, None]): The zorder of the scatter.
        plot_scatter_edge_width (Union[int, float, None]): The edge width of markers.
        plot_scatter_edge_color (Union[str, None]): The edge color of markers.

    """

    plot_scatter_color: Union[str, None]
    plot_scatter_alpha: Union[float, None]
    plot_scatter_size: Union[int, float, None]
    plot_scatter_marker: Union[LINE_MARKER, str, None]
    plot_scatter_zorder: Union[int, float, None]
    plot_scatter_edge_width: Union[int, float, None]
    plot_scatter_edge_color: Union[str, None]


class RegressionStyleAttrs(TypedDict):
    """The typing for regression line style.

    Attributes:
        plot_regression_color (Union[str, None]): The regression line color.
        plot_regression_alpha (Union[float, None]): The alpha of the regression line.
        plot_regression_width (Union[int, float, None]): The line width.
        plot_regression_style (Union[LINE_STYLE, str, None]): The line style.
        plot_regression_ci_alpha (Union[float, None]): Confidence interval alpha.

    """

    plot_regression_color: Union[str, None]
    plot_regression_alpha: Union[float, None]
    plot_regression_width: Union[int, float, None]
    plot_regression_style: Union[LINE_STYLE, str, None]
    plot_regression_ci_alpha: Union[float, None]


class BoxStyleAttrs(TypedDict):
    """The typing for the box plot style.

    Attributes:
        plot_box_color (Union[str, None]): The box fill color.
        plot_box_alpha (Union[float, None]): The alpha value of the box.
        plot_box_linewidth (Union[int, float, None]): The line width of the box.
        plot_box_edgecolor (Union[str, None]): The edge color of the box.
        plot_box_outlier_marker (Union[LINE_MARKER, str, None]): The outlier marker style.
        plot_box_outlier_size (Union[int, float, None]): The outlier marker size.
        plot_box_outlier_color (Union[str, None]): The outlier marker color.
        plot_box_outlier_edge_color (Union[str, None]): The outlier marker edge color.
        plot_box_median_color (Union[str, None]): The median line color.
        plot_box_median_linewidth (Union[int, float, None]): The median line width.
        plot_box_whisker_linewidth (Union[int, float, None]): The whisker line width.
        plot_box_cap_linewidth (Union[int, float, None]): The cap line width.
        plot_xticks_label_rotate (Union[int, float, None]): The label rotation of the xticks.
        plot_yticks_label_rotate (Union[int, float, None]): The label rotation of the yticks.

    """

    plot_box_color: Union[str, None]
    plot_box_alpha: Union[float, None]
    plot_box_linewidth: Union[int, float, None]
    plot_box_edgecolor: Union[str, None]
    plot_box_outlier_marker: Union[LINE_MARKER, str, None]
    plot_box_outlier_size: Union[int, float, None]
    plot_box_outlier_color: Union[str, None]
    plot_box_outlier_edge_color: Union[str, None]
    plot_box_median_color: Union[str, None]
    plot_box_median_linewidth: Union[int, float, None]
    plot_box_whisker_linewidth: Union[int, float, None]
    plot_box_cap_linewidth: Union[int, float, None]
    plot_xticks_label_rotate: Union[int, float, None]
    plot_yticks_label_rotate: Union[int, float, None]


class ParallelCoordsStyleAttrs(TypedDict):
    """The typing for the parallel coordinates chart style.

    Attributes:
        plot_parallel_color (Union[str, None]): The line color.
        plot_parallel_alpha (Union[float, None]): The alpha value of the lines.
        plot_parallel_width (Union[int, float, None]): The line width.
        plot_parallel_style (Union[LINE_STYLE, str, None]): The line style.
        plot_parallel_marker (Union[LINE_MARKER, str, None]): The marker style for data points.
        plot_parallel_zorder (Union[int, None]): The draw order of data lines.
        plot_parallel_axis_color (Union[str, None]): The vertical axis line color.
        plot_parallel_axis_width (Union[int, float, None]): The vertical axis line width.
        plot_parallel_axis_zorder (Union[int, None]): The vertical axis line draw order.
        plot_parallel_tick_color (Union[str, None]): The tick mark color.
        plot_parallel_tick_width (Union[int, float, None]): The tick mark line width.
        plot_parallel_tick_length (Union[float, None]): The tick mark length.
        plot_parallel_tick_label_size (Union[int, float, None]): The tick label font size.
        plot_parallel_tick_label_color (Union[str, None]): The tick label font color.
        plot_parallel_tick_label_bg_color (Union[str, None]): The tick label background color.
        plot_parallel_tick_label_bg_alpha (Union[float, None]): The tick label background alpha.
        plot_parallel_dim_label_size (Union[int, float, None]): The dimension label font size.
        plot_parallel_dim_label_color (Union[str, None]): The dimension label font color.
        plot_parallel_dim_label_rotation (Union[int, float, None]): The dimension label rotation.
        plot_parallel_dim_label_pad (Union[int, float, None]): The dimension label padding from axis.

    """

    plot_parallel_color: Union[str, None]
    plot_parallel_alpha: Union[float, None]
    plot_parallel_width: Union[int, float, None]
    plot_parallel_style: Union[LINE_STYLE, str, None]
    plot_parallel_marker: Union[LINE_MARKER, str, None]
    plot_parallel_zorder: Union[int, None]
    plot_parallel_axis_color: Union[str, None]
    plot_parallel_axis_width: Union[int, float, None]
    plot_parallel_axis_zorder: Union[int, None]
    plot_parallel_tick_color: Union[str, None]
    plot_parallel_tick_width: Union[int, float, None]
    plot_parallel_tick_length: Union[float, None]
    plot_parallel_tick_label_size: Union[int, float, None]
    plot_parallel_tick_label_color: Union[str, None]
    plot_parallel_tick_label_bg_color: Union[str, None]
    plot_parallel_tick_label_bg_alpha: Union[float, None]
    plot_parallel_dim_label_size: Union[int, float, None]
    plot_parallel_dim_label_color: Union[str, None]
    plot_parallel_dim_label_rotation: Union[int, float, None]
    plot_parallel_dim_label_pad: Union[int, float, None]


class StyleAttrs(
    ColorStyleAttrs,
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
    ScatterStyleAttrs,
    RegressionStyleAttrs,
    BoxStyleAttrs,
    ParallelCoordsStyleAttrs,
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
        aspect_ratio (Union[ASPECT_RATIO, str, None]): The aspect ratio of the charts.

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
    aspect_ratio: Union[ASPECT_RATIO, str, None]
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

    x: Union[str, None]  # the name of the x attribute in data (default: "x")
    y: Union[str, None]  # the name of the y attribute in data (default: "y")
    yerr: Union[str, None]  # the name of the yerr attribute in data (default: "yerr")


class LineChartAttrs(ChartCommonAttrs):
    """The line chart attributes.

    Attributes:
        charts (Union[LineSingleChartAttrs, List[LineSingleChartAttrs]]): The line chart definitions.
        show_yerr (Union[bool, None]): Whether or not to show the y-axis errors.
        show_area (Union[bool, None]): Whether or not to show the area under the lines.
        scalex (Union[SCALE, str, None]): The scale of the x-axis.
        scaley (Union[SCALE, str, None]): The scale of the y-axis.

    """

    charts: Union[LineSingleChartAttrs, List[LineSingleChartAttrs]]
    show_yerr: Union[bool, None]
    show_area: Union[bool, None]
    scalex: Union[SCALE, str, None]
    scaley: Union[SCALE, str, None]


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
        scaley (Union[SCALE, str, None]): The scale of the y-axis.

    """

    charts: Union[BarSingleChartAttrs, List[BarSingleChartAttrs]]
    show_yerr: Union[bool, None]
    orientation: Union[ORIENTATION, str, None]
    scaley: Union[SCALE, str, None]


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
        scaley (Union[SCALE, str, None]): The scale of the y-axis.

    """

    charts: Union[HistogramSingleChartAttrs, List[HistogramSingleChartAttrs]]
    orientation: Union[ORIENTATION, str, None]
    num_bins: Union[int, None]
    show_density: Union[bool, None]
    show_cumulative: Union[bool, None]
    scaley: Union[SCALE, str, None]


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
# Scatter Chart Attributes
# ================================================


class ScatterDataPointAttrs(TypedDict):
    """The data point attributes for the scatter chart.

    Attributes:
        x (Union[int, float]): The x-axis value.
        y (Union[int, float]): The y-axis value.
        size (Optional[Union[int, float]]): The marker size (for bubble charts).
        hue (Optional[str]): The category for color grouping.

    """

    x: Union[int, float]
    y: Union[int, float]
    size: Optional[Union[int, float]]
    hue: Optional[str]


class ScatterSingleChartAttrs(TypedDict):
    """The single chart attributes for the scatter chart.

    Attributes:
        data (List[ScatterDataPointAttrs]): The list of data points defining the scatter chart.
        subtitle (Union[str, None]): The subtitle of the scatter chart. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the scatter chart.
        ylabel (Union[str, None]): The ylabel of the scatter chart.
        style (Union[ScatterStyleAttrs, None]): The style of the scatter chart.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): The ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLinePlotAttrs, List[VLinePlotAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLinePlotAttrs, List[HLinePlotAttrs], None]): The horizontal lines to be plot.
        x (Union[str, None]): The key name in `data` that contains the x-axis value. Defaults to `"x"`.
        y (Union[str, None]): The key name in `data` that contains the y-axis value. Defaults to `"y"`.
        size (Union[str, None]): The key name in `data` that contains the marker size value.
        hue (Union[str, None]): The key name in `data` that contains the hue/category value.

    """

    data: List[ScatterDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[ScatterStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLinePlotAttrs, List[VLinePlotAttrs]]
    hlines: Union[HLinePlotAttrs, List[HLinePlotAttrs]]

    x: Union[str, None]
    y: Union[str, None]
    size: Union[str, None]
    hue: Union[str, None]


class ScatterChartAttrs(ChartCommonAttrs):
    """The scatter chart attributes.

    Attributes:
        charts (Union[ScatterSingleChartAttrs, List[ScatterSingleChartAttrs]]): The scatter chart definitions.
        show_regression (Union[bool, None]): Whether or not to show the regression line.
        show_ci (Union[bool, None]): Whether or not to show the confidence interval around the regression.
        ci_level (Union[float, None]): The confidence interval level (default 0.95).
        scalex (Union[SCALE, str, None]): The scale of the x-axis.
        scaley (Union[SCALE, str, None]): The scale of the y-axis.
        size_range (Union[Tuple[float, float], None]): The min/max marker sizes for bubble charts.

    """

    charts: Union[ScatterSingleChartAttrs, List[ScatterSingleChartAttrs]]
    show_regression: Union[bool, None]
    show_ci: Union[bool, None]
    ci_level: Union[float, None]
    scalex: Union[SCALE, str, None]
    scaley: Union[SCALE, str, None]
    size_range: Union[Tuple[float, float], None]


# ================================================
# Box Plot Attributes
# ================================================


class BoxDataPointAttrs(TypedDict):
    """The data point attributes for the box plot.

    Attributes:
        label (str): The category label.
        value (Union[int, float]): The numeric value.

    """

    label: str
    value: Union[int, float]


class BoxSingleChartAttrs(TypedDict):
    """The single chart attributes for the box plot.

    Attributes:
        data (List[BoxDataPointAttrs]): The list of data points defining the box plot.
        subtitle (Union[str, None]): The subtitle of the box plot. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the box plot.
        ylabel (Union[str, None]): The ylabel of the box plot.
        style (Union[BoxStyleAttrs, None]): The style of the box plot.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): The ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLinePlotAttrs, List[VLinePlotAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLinePlotAttrs, List[HLinePlotAttrs], None]): The horizontal lines to be plot.
        label (Union[str, None]): The key name in `data` that contains the label value. Defaults to `"label"`.
        value (Union[str, None]): The key name in `data` that contains the value. Defaults to `"value"`.

    """

    data: List[BoxDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[BoxStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLinePlotAttrs, List[VLinePlotAttrs]]
    hlines: Union[HLinePlotAttrs, List[HLinePlotAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    value: Union[str, None]  # the name of the value attribute in data


class BoxChartAttrs(ChartCommonAttrs):
    """The box plot chart attributes.

    Attributes:
        charts (Union[BoxSingleChartAttrs, List[BoxSingleChartAttrs]]): The box plot definitions.
        show_outliers (Union[bool, None]): Whether or not to show outliers.
        show_notch (Union[bool, None]): Whether or not to show notched boxes for median CI.
        orientation (Union[ORIENTATION, str, None]): The orientation of the box plots.

    """

    charts: Union[BoxSingleChartAttrs, List[BoxSingleChartAttrs]]
    show_outliers: Union[bool, None]
    show_notch: Union[bool, None]
    orientation: Union[ORIENTATION, str, None]


# ================================================
# Parallel Coordinates Chart Attributes
# ================================================


class ParallelCoordsDataPointAttrs(TypedDict):
    """The data point attributes for the parallel coordinates chart.

    A dictionary where keys are dimension names and values are numeric values.
    Can optionally include a 'hue' key for categorical coloring.

    Attributes:
        hue (Optional[str]): The category for color grouping.

    """

    hue: Optional[str]


class ParallelCoordsSingleChartAttrs(TypedDict):
    """The single chart attributes for the parallel coordinates chart.

    Attributes:
        data (List[ParallelCoordsDataPointAttrs]): The list of data points.
        subtitle (Union[str, None]): The subtitle of the chart.
        style (Union[ParallelCoordsStyleAttrs, None]): The style of the chart.
        dimensions (Union[List[str], None]): The dimensions to include and their order.
        hue (Union[str, None]): The key name in `data` for categorical coloring.
        category_orders (Union[Dict[str, List[str]], None]): Custom order for categorical dimensions.

    """

    data: List[ParallelCoordsDataPointAttrs]
    subtitle: Union[str, None]
    style: Union[ParallelCoordsStyleAttrs, None]
    dimensions: Union[List[str], None]
    hue: Union[str, None]
    category_orders: Union[Dict[str, List[str]], None]


class ParallelCoordsChartAttrs(ChartCommonAttrs):
    """The parallel coordinates chart attributes.

    Attributes:
        charts (Union[ParallelCoordsSingleChartAttrs, List[ParallelCoordsSingleChartAttrs]]): The chart definitions.

    """

    charts: Union[ParallelCoordsSingleChartAttrs, List[ParallelCoordsSingleChartAttrs]]


# ================================================
# Chart Attributes
# ================================================


ChartAttrs = Union[
    LineChartAttrs,
    BarChartAttrs,
    HistogramChartAttrs,
    HeatmapChartAttrs,
    ScatterChartAttrs,
    BoxChartAttrs,
    ParallelCoordsChartAttrs,
]
"""The union of all chart attributes."""
