"""Module containing the `typings`.

The `typings` module holds the dictionary contracts of the package: the records
a chart's `data` takes, the settings passed beside it (reference lines and
bands, texts, legend, emphasis rule, colorbar), and the style keys a chart's
`style` and the theme accept. A per-chart contract is documented on that
chart's reference page; the shared ones on the typings page.

"""

import os
import warnings
from datetime import date, datetime
from typing import TypedDict, Union, Tuple, List, Optional, Dict, Literal

import numpy as np
import matplotlib.colors as colors
from PIL.Image import Image as PILImage
from .constants import (
    ARROW_STYLE,
    ASPECT_RATIO,
    BAR_MODE,
    BASEMAP_FEATURE,
    CALENDAR_WEEKDAY,
    COLORBAR_LOCATION,
    COLORS,
    EMPHASIS,
    FIG_SIZE,
    FONT_STYLE,
    FONT_WEIGHT,
    GANTT_ARROW_ENTRY,
    HATCH_STYLE,
    HEXBIN_REDUCE,
    HISTOGRAM_TYPE,
    LEGEND_ALIGN,
    LEGEND_LOCATION,
    LINE_DRAW_STYLE,
    LINE_MARKER,
    LINE_STYLE,
    NETWORK_LAYOUT,
    NETWORK_LABEL_POSITION,
    ORIENTATION,
    SHOW_GRID,
    VALUE_FORMAT,
)

# ================================================
# Config Definitions
# ================================================


class ColorStyleAttrs(TypedDict):
    """The typing for the general color style.

    Attributes:
        color_general_singular (Union[COLORS, str, List[str], None]): The colors used where a chart needs one color rather than a series palette: the parallel coords numeric hue ramp and the network node base color (palette name, single color, or list of hex colors).
        color_general_multiple (Union[COLORS, str, List[str], None]): The colors used when the datasets share one coordinate space, which is the default for every chart (palette name, single color, or list of hex colors).
        color_parallel_hue (Union[COLORS, str, List[str], None]): The color palette for parallel coords hue categories (palette name, single color, or list of hex colors); `None` takes `color_general_multiple`.
        color_parallel_hue_continuous (Union[COLORS, str, List[str], None]): The sequential ramp for parallel coords numeric hue columns (palette name, single color, or list of hex colors).
        muted_color (Union[str, None]): The color applied to background-emphasis layers.
        muted_alpha (Union[float, None]): The alpha applied to background-emphasis layers.

    """

    color_general_singular: Union[COLORS, str, List[str], None]
    color_general_multiple: Union[COLORS, str, List[str], None]
    color_parallel_hue: Union[COLORS, str, List[str], None]
    color_parallel_hue_continuous: Union[COLORS, str, List[str], None]
    muted_color: Union[str, None]
    muted_alpha: Union[float, None]


class FontStyleAttrs(TypedDict):
    """The typing for the font style.

    Attributes:
        font_general_family (Union[str, None]): The general font family.
        font_general_sansserif (Union[List[str], None]): The general sans-serif font.
        font_general_serif (Union[List[str], None]): The general serif font stack, used when the family is "serif".
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
    font_general_serif: Union[List[str], None]
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
        figure_facecolor (Union[str, None]): The color of the figure ground.
            `None` keeps matplotlib's.
        axes_facecolor (Union[str, None]): The color of the axes ground; label
            halos and etch washes take it. `None` keeps matplotlib's.
        axes_spines_color (Union[str, None]): The color of the spines. `None`
            keeps matplotlib's.
        axes_ticks_color (Union[str, None]): The color of the tick marks. `None`
            keeps matplotlib's.
    """

    axes_spines_top_visible: Union[bool, None]
    axes_spines_right_visible: Union[bool, None]
    axes_spines_bottom_visible: Union[bool, None]
    axes_spines_left_visible: Union[bool, None]
    axes_spines_width: Union[int, float, None]
    axes_spines_zorder: Union[int, None]
    axes_ticks_length: Union[int, float, None]
    axes_ticks_label_size: Union[int, float, None]
    figure_facecolor: Union[str, None]
    axes_facecolor: Union[str, None]
    axes_spines_color: Union[str, None]
    axes_ticks_color: Union[str, None]


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
        plot_legend_title (Union[str, None]): The legend title; an empty string draws none.
        plot_legend_ncols (Union[int, None]): The number of legend columns.
        plot_legend_edge_color (Union[str, None]): The legend frame color.
            `None` keeps matplotlib's.
        plot_legend_face_color (Union[str, None]): The legend background color.
            `None` keeps matplotlib's.
    """

    plot_legend_shadow: Union[bool, None]
    plot_legend_frameon: Union[bool, None]
    plot_legend_alignment: Union[LEGEND_ALIGN, str, None]
    plot_legend_location: Union[LEGEND_LOCATION, str, None]
    plot_legend_font_size: Union[int, float, str, None]
    plot_legend_title_size: Union[int, float, str, None]
    plot_legend_label_color: Union[str, None]
    plot_legend_title: Union[str, None]
    plot_legend_ncols: Union[int, None]
    plot_legend_edge_color: Union[str, None]
    plot_legend_face_color: Union[str, None]


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


class StackedAreaStyleAttrs(TypedDict):
    """The typing for the stacked area chart style.

    The fill takes the `plot_area_*` keys (color, hatch, zorder) and the
    outline the `plot_line_*` keys; these keys switch what is specific to a stack.

    Attributes:
        plot_stackedarea_alpha (Union[float, None]): The alpha value of the stacked bands.
        plot_stackedarea_outline (Union[bool, None]): Whether each band draws its top edge as a line.
        plot_stackedarea_edge_color (Union[str, None]): The stroke color between the bands.
        plot_stackedarea_edge_width (Union[float, None]): The stroke width between the bands.

    """

    plot_stackedarea_alpha: Union[float, None]
    plot_stackedarea_outline: Union[bool, None]
    plot_stackedarea_edge_color: Union[str, None]
    plot_stackedarea_edge_width: Union[float, None]


class BumpStyleAttrs(TypedDict):
    """The typing for the bump chart style.

    The line takes the `plot_line_*` keys (color, alpha, style, zorder);
    these keys set what is specific to a bump chart.

    Attributes:
        plot_bump_line_width (Union[int, float, None]): The line width.
        plot_bump_marker (Union[LINE_MARKER, str, None]): The marker at every period.
        plot_bump_marker_size (Union[int, float, None]): The marker size.
        plot_bump_label_padding (Union[int, float, None]): The gap between a line end and its end label, in points.

    """

    plot_bump_line_width: Union[int, float, None]
    plot_bump_marker: Union[LINE_MARKER, str, None]
    plot_bump_marker_size: Union[int, float, None]
    plot_bump_label_padding: Union[int, float, None]


class SankeyStyleAttrs(TypedDict):
    """The typing for the Sankey chart style.

    Attributes:
        plot_sankey_node_width (Union[float, None]): The node bar width as a fraction of the horizontal span.
        plot_sankey_node_pad (Union[float, None]): The vertical span shared by the gaps of the tallest column.
        plot_sankey_node_edge_color (Union[str, None]): The node stroke color.
        plot_sankey_node_edge_width (Union[float, None]): The node stroke width.
        plot_sankey_link_color (Union[str, None]): Which node colors a ribbon: "source", "target", or "grey".
        plot_sankey_link_alpha (Union[float, None]): The ribbon alpha.
        plot_sankey_label_halo_width (Union[float, None]): The width of the halo, in the axes face color, behind labels; 0 disables it.
        plot_sankey_node_fill (Union[bool, None]): Whether the node bars are filled; `False` draws them as outlines.
    """

    plot_sankey_node_width: Union[float, None]
    plot_sankey_node_pad: Union[float, None]
    plot_sankey_node_edge_color: Union[str, None]
    plot_sankey_node_edge_width: Union[float, None]
    plot_sankey_link_color: Union[str, None]
    plot_sankey_link_alpha: Union[float, None]
    plot_sankey_label_halo_width: Union[float, None]
    plot_sankey_node_fill: Union[bool, None]


class TreemapStyleAttrs(TypedDict):
    """The typing for the treemap style.

    Attributes:
        plot_treemap_edge_color (Union[str, None]): The stroke color of leaf tiles and group borders.
        plot_treemap_edge_width (Union[float, None]): The leaf tile stroke width.
        plot_treemap_group_edge_width (Union[float, None]): The width of the border around a group.
        plot_treemap_group_pad (Union[float, None]): The gap between top-level records and, at every level, the gutter between a group's border and its children, as a fraction of the span.
        plot_treemap_level_shade (Union[float, None]): How much lighter than its parent each level is, 0 to 1, applied once more per level; 0 keeps the group color.
        plot_treemap_level_font_scale (Union[float, None]): The label font scale applied once more per nesting level.
        plot_treemap_min_fontsize (Union[float, None]): The smallest font size a label shrinks to before it is dropped.
        plot_treemap_highlight_edge_width (Union[float, None]): The border width of a highlighted record.
        plot_treemap_label_halo_width (Union[float, None]): The width of the halo, in the axes face color, behind labels; 0 disables it.
        plot_treemap_etch_density (Union[List[int], None]): With `plot_etch` and a hatch cycle, how many times each nesting level repeats its top-level group's pattern, outermost first (a level past the list is blank); every box fills with the axes face so outer etching never shows through. `None` keeps the colored tiles.
    """

    plot_treemap_edge_color: Union[str, None]
    plot_treemap_edge_width: Union[float, None]
    plot_treemap_group_edge_width: Union[float, None]
    plot_treemap_group_pad: Union[float, None]
    plot_treemap_level_shade: Union[float, None]
    plot_treemap_level_font_scale: Union[float, None]
    plot_treemap_min_fontsize: Union[float, None]
    plot_treemap_highlight_edge_width: Union[float, None]
    plot_treemap_label_halo_width: Union[float, None]
    plot_treemap_etch_density: Union[List[int], None]


class NetworkStyleAttrs(TypedDict):
    """The typing for the network chart style.

    Attributes:
        plot_network_node_color (Union[str, None]): The node marker color; overrides the color cycle.
        plot_network_node_alpha (Union[float, None]): The alpha value of the node markers.
        plot_network_node_marker (Union[LINE_MARKER, str, None]): The node marker shape.
        plot_network_node_size (Union[int, float, None]): The marker area of a node without `size`.
        plot_network_node_size_min (Union[int, float, None]): The marker area of the smallest sized node.
        plot_network_node_size_max (Union[int, float, None]): The marker area of the largest sized node.
        plot_network_node_edge_color (Union[str, None]): The node stroke color.
        plot_network_node_edge_width (Union[int, float, None]): The node stroke width.
        plot_network_edge_style (Union[ARROW_STYLE, str, None]): The edge geometry: `ARROW_STYLE.CURVE` or `ARROW_STYLE.STRAIGHT`.
        plot_network_edge_curve (Union[float, None]): The bow of a curved edge; the sign picks the side.
        plot_network_edge_color (Union[str, None]): The edge color.
        plot_network_edge_alpha (Union[float, None]): The edge alpha.
        plot_network_edge_width_min (Union[int, float, None]): The width of the lightest edge, and of an edge without `weight`.
        plot_network_edge_width_max (Union[int, float, None]): The width of the heaviest edge.
        plot_network_highlight_edge_width (Union[float, None]): The stroke width of a highlighted node.
        plot_network_label_halo_width (Union[float, None]): The width of the halo, in the axes face color, behind labels; 0 disables it.
        plot_network_label_family (Union[str, None]): The font family of the node labels; `None` keeps the general font.
        plot_network_group_alpha (Union[float, None]): The alpha of the disc in the group color behind each cluster of the grouped layout; 0 disables it.
        plot_network_group_linestyle (Union[LINE_STYLE, str, None]): Draws each cluster's mark as a ring in this line style and the edge color instead of a disc. `None` draws the disc.
        plot_network_edge_ink_stroke (Union[Dict[str, float], None]): The pen the edges are drawn with, as for `plot_ink_stroke`, plus `swell` (the pressure swell amplitude) and `noise` (the grain); a directed edge draws as a stroked shaft with a small head. `None` draws plain edges.
    """

    plot_network_node_color: Union[str, None]
    plot_network_node_alpha: Union[float, None]
    plot_network_node_marker: Union[LINE_MARKER, str, None]
    plot_network_node_size: Union[int, float, None]
    plot_network_node_size_min: Union[int, float, None]
    plot_network_node_size_max: Union[int, float, None]
    plot_network_node_edge_color: Union[str, None]
    plot_network_node_edge_width: Union[int, float, None]
    plot_network_edge_style: Union[ARROW_STYLE, str, None]
    plot_network_edge_curve: Union[float, None]
    plot_network_edge_color: Union[str, None]
    plot_network_edge_alpha: Union[float, None]
    plot_network_edge_width_min: Union[int, float, None]
    plot_network_edge_width_max: Union[int, float, None]
    plot_network_highlight_edge_width: Union[float, None]
    plot_network_label_halo_width: Union[float, None]
    plot_network_label_family: Union[str, None]
    plot_network_group_alpha: Union[float, None]
    plot_network_group_linestyle: Union[LINE_STYLE, str, None]
    plot_network_edge_ink_stroke: Union[Dict[str, float], None]


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
        plot_bar_value_fontsize (Union[int, float, None]): Alias of `plot_value_fontsize`.
        plot_bar_value_color (Union[str, None]): Alias of `plot_value_color`.
        plot_bar_value_padding (Union[int, float, None]): Alias of `plot_value_padding`.
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


class ValueLabelStyleAttrs(TypedDict):
    """The typing for the value labels: the numbers a chart prints beside its
    marks when `show_values` is on. One style serves every chart that takes
    `show_values`; the `plot_bar_value_*` keys of `BarStyleAttrs` are aliases.

    Attributes:
        plot_value_fontsize (Union[int, float, None]): The font size of the value labels.
        plot_value_color (Union[str, None]): The color of the value labels.
        plot_value_padding (Union[int, float, None]): The gap between a mark and its value label, in points.
        plot_value_halo_width (Union[int, float, None]): The width, in points, of the halo, in the axes face color, stroked around the value labels so they stay legible over marks and lines. `None` or `0` draws no halo.
        plot_value_tab (Union[Dict[str, Union[float, str]], None]): The tab a value label is set on, a rounded box in the ground color like a label ribbon on an engraved chart. Keys: `facecolor`, `edgecolor`, `line_width` (points), `pad` (in font sizes) and `rounding` (in font sizes). `None` draws no tab.

    """

    plot_value_fontsize: Union[int, float, None]
    plot_value_color: Union[str, None]
    plot_value_padding: Union[int, float, None]
    plot_value_halo_width: Union[int, float, None]
    plot_value_tab: Union[Dict[str, Union[float, str]], None]


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


class DLineStyleAttrs(TypedDict):
    """The typing for the diagonal line style.

    Attributes:
        plot_dline_color (Union[str, None]): The color of the diagonal line.
        plot_dline_style (Union[LINE_STYLE, str, None]): The style of the diagonal line.
        plot_dline_width (Union[int, float, None]): The width of the diagonal line.
        plot_dline_alpha (Union[float, None]): The alpha value of the diagonal line.

    """

    plot_dline_color: Union[str, None]
    plot_dline_style: Union[LINE_STYLE, str, None]
    plot_dline_width: Union[int, float, None]
    plot_dline_alpha: Union[float, None]


class BracketStyleAttrs(TypedDict):
    """The typing for the pairwise comparison bracket style.

    Attributes:
        plot_bracket_color (Union[str, None]): The color of the bracket line and its text.
        plot_bracket_width (Union[int, float, None]): The width of the bracket line.
        plot_bracket_tick (Union[int, float, None]): The length of the bracket's end ticks, in points.
        plot_bracket_alpha (Union[float, None]): The alpha value of the bracket.

    """

    plot_bracket_color: Union[str, None]
    plot_bracket_width: Union[int, float, None]
    plot_bracket_tick: Union[int, float, None]
    plot_bracket_alpha: Union[float, None]


class VSpanStyleAttrs(TypedDict):
    """The typing for the vertical reference band style.

    Attributes:
        plot_vspan_color (Union[str, None]): The fill color of the band. Defaults to the theme's muted color.
        plot_vspan_alpha (Union[float, None]): The alpha value of the band.
        plot_vspan_hatch (Union[HATCH_STYLE, str, None]): The hatch pattern of the band.
        plot_vspan_edge_color (Union[str, None]): The edge color of the band; the hatch draws in it.
        plot_vspan_edge_width (Union[int, float, None]): The edge line width of the band.
        plot_vspan_zorder (Union[int, float, None]): The zorder of the band. Defaults to sit over the grid and under the marks.

    """

    plot_vspan_color: Union[str, None]
    plot_vspan_alpha: Union[float, None]
    plot_vspan_hatch: Union[HATCH_STYLE, str, None]
    plot_vspan_edge_color: Union[str, None]
    plot_vspan_edge_width: Union[int, float, None]
    plot_vspan_zorder: Union[int, float, None]


class HSpanStyleAttrs(TypedDict):
    """The typing for the horizontal reference band style.

    Attributes:
        plot_hspan_color (Union[str, None]): The fill color of the band. Defaults to the theme's muted color.
        plot_hspan_alpha (Union[float, None]): The alpha value of the band.
        plot_hspan_hatch (Union[HATCH_STYLE, str, None]): The hatch pattern of the band.
        plot_hspan_edge_color (Union[str, None]): The edge color of the band; the hatch draws in it.
        plot_hspan_edge_width (Union[int, float, None]): The edge line width of the band.
        plot_hspan_zorder (Union[int, float, None]): The zorder of the band. Defaults to sit over the grid and under the marks.

    """

    plot_hspan_color: Union[str, None]
    plot_hspan_alpha: Union[float, None]
    plot_hspan_hatch: Union[HATCH_STYLE, str, None]
    plot_hspan_edge_color: Union[str, None]
    plot_hspan_edge_width: Union[int, float, None]
    plot_hspan_zorder: Union[int, float, None]


class TextStyleAttrs(TypedDict):
    """The typing for the text annotation style.

    Attributes:
        plot_text_color (Union[str, None]): The text color; falls back to the general font color.
        plot_text_size (Union[int, float, str, None]): The text font size.
        plot_text_weight (Union[FONT_WEIGHT, str, None]): The text font weight.
        plot_text_halign (Union[str, None]): The horizontal alignment of the text.
        plot_text_valign (Union[str, None]): The vertical alignment of the text.
        plot_text_alpha (Union[float, None]): The alpha value of the text.
        plot_text_box_visible (Union[bool, None]): Whether to draw the background box.
        plot_text_box_style (Union[str, None]): The matplotlib box style (e.g. `"round,pad=0.4"`).
        plot_text_box_facecolor (Union[str, None]): The face color of the box.
        plot_text_box_edgecolor (Union[str, None]): The edge color of the box.
        plot_text_box_edge_width (Union[int, float, None]): The edge width of the box.
        plot_text_box_alpha (Union[float, None]): The alpha value of the box.
        plot_text_arrow_style (Union[ARROW_STYLE, str, None]): The connector look (see `ARROW_STYLE`) or a raw matplotlib arrow style.
        plot_text_arrow_curve (Union[float, None]): The connector curvature; overrides the look's own.
        plot_text_arrow_color (Union[str, None]): The connector color.
        plot_text_arrow_width (Union[int, float, None]): The connector line width.

    """

    plot_text_color: Union[str, None]
    plot_text_size: Union[int, float, str, None]
    plot_text_weight: Union[FONT_WEIGHT, str, None]
    plot_text_halign: Union[str, None]
    plot_text_valign: Union[str, None]
    plot_text_alpha: Union[float, None]
    plot_text_box_visible: Union[bool, None]
    plot_text_box_style: Union[str, None]
    plot_text_box_facecolor: Union[str, None]
    plot_text_box_edgecolor: Union[str, None]
    plot_text_box_edge_width: Union[int, float, None]
    plot_text_box_alpha: Union[float, None]
    plot_text_arrow_style: Union[ARROW_STYLE, str, None]
    plot_text_arrow_curve: Union[float, None]
    plot_text_arrow_color: Union[str, None]
    plot_text_arrow_width: Union[int, float, None]


class HeatmapStyleAttrs(TypedDict):
    """The typing for the heatmap chart style.

    Attributes:
        plot_heatmap_cmap (Union[str, List[str], colors.LinearSegmentedColormap, None]): The color map of the heatmap (palette name, single color, list of hex colors, or colormap).
        plot_heatmap_cmap_diverging (Union[str, List[str], colors.LinearSegmentedColormap, None]): The color map a centred `norm` (`"centered"` or `"twoslope"`) draws in, in place of `plot_heatmap_cmap`; a `plot_heatmap_cmap` set in the chart's own style still wins.
        plot_heatmap_alpha (Union[float, None]): The alpha value of the heatmap.
        plot_heatmap_font_size (Union[int, float, str, None]): The font size of the heatmap.
        plot_heatmap_font_color (Union[str, None]): The font color of the heatmap.
        plot_heatmap_font_style (Union[FONT_STYLE, str, None]): The font style of the heatmap.
        plot_heatmap_font_weight (Union[FONT_WEIGHT, str, None]): The font weight of the heatmap.
        plot_heatmap_frame_color (Union[str, None]): The color of the frame always drawn around heatmap axes.
        plot_heatmap_edge_width (Union[int, float, None]): The width of the borders drawn between the cells (0 draws none).
        plot_heatmap_edge_color (Union[str, None]): The color of the borders drawn between the cells.

    """

    plot_heatmap_cmap: Union[str, List[str], colors.LinearSegmentedColormap, None]
    plot_heatmap_cmap_diverging: Union[
        str, List[str], colors.LinearSegmentedColormap, None
    ]
    plot_heatmap_alpha: Union[float, None]
    plot_heatmap_font_size: Union[int, float, str, None]
    plot_heatmap_font_color: Union[str, None]
    plot_heatmap_font_style: Union[FONT_STYLE, str, None]
    plot_heatmap_font_weight: Union[FONT_WEIGHT, str, None]
    plot_heatmap_frame_color: Union[str, None]
    plot_heatmap_edge_width: Union[int, float, None]
    plot_heatmap_edge_color: Union[str, None]


class GanttStyleAttrs(TypedDict):
    """The typing for the gantt chart style.

    The range bars take the `plot_bar_*` keys (color, alpha, edge, hatch,
    zorder); these keys set what is specific to a gantt chart.

    Attributes:
        plot_gantt_bar_height (Union[int, float, None]): The height of a task bar, as a fraction of its row.
        plot_gantt_progress_color (Union[str, None]): The color of the progress bar; `None` darkens the task bar's color.
        plot_gantt_progress_alpha (Union[float, None]): The alpha value of the progress bar.
        plot_gantt_progress_height (Union[int, float, None]): The height of the progress bar, as a fraction of the task bar.
        plot_gantt_dependency_color (Union[str, None]): The color of the dependency arrows.
        plot_gantt_dependency_width (Union[int, float, None]): The line width of the dependency arrows.
        plot_gantt_dependency_style (Union[str, None]): The arrow head of the dependency arrows, as a matplotlib arrow style.
        plot_gantt_dependency_zorder (Union[int, float, None]): The zorder of the dependency arrows.
        plot_gantt_dependency_entry (Union[GANTT_ARROW_ENTRY, str, None]): The side of the dependent task a dependency arrow enters ("top" or "left").
        plot_gantt_summary_height (Union[int, float, None]): The height of a group's summary bar under `show_group_headers`, as a fraction of its row.
        plot_gantt_summary_color (Union[str, None]): The color of the summary bars; `None` takes each group's color.
        plot_gantt_group_gap (Union[int, float, None]): The empty space before each group header, in rows.
        plot_gantt_milestone_marker (Union[LINE_MARKER, str, None]): The marker of a milestone, a task whose `start` equals its `end`.
        plot_gantt_milestone_size (Union[int, float, None]): The size of the milestone marker, in points.
        plot_gantt_today_color (Union[str, None]): The color of the today line.
        plot_gantt_today_style (Union[LINE_STYLE, str, None]): The line style of the today line.
        plot_gantt_today_width (Union[int, float, None]): The line width of the today line.
        plot_gantt_today_alpha (Union[float, None]): The alpha value of the today line.

    """

    plot_gantt_bar_height: Union[int, float, None]
    plot_gantt_progress_color: Union[str, None]
    plot_gantt_progress_alpha: Union[float, None]
    plot_gantt_progress_height: Union[int, float, None]
    plot_gantt_dependency_color: Union[str, None]
    plot_gantt_dependency_width: Union[int, float, None]
    plot_gantt_dependency_style: Union[str, None]
    plot_gantt_dependency_zorder: Union[int, float, None]
    plot_gantt_dependency_entry: Union[GANTT_ARROW_ENTRY, str, None]
    plot_gantt_summary_height: Union[int, float, None]
    plot_gantt_summary_color: Union[str, None]
    plot_gantt_group_gap: Union[int, float, None]
    plot_gantt_milestone_marker: Union[LINE_MARKER, str, None]
    plot_gantt_milestone_size: Union[int, float, None]
    plot_gantt_today_color: Union[str, None]
    plot_gantt_today_style: Union[LINE_STYLE, str, None]
    plot_gantt_today_width: Union[int, float, None]
    plot_gantt_today_alpha: Union[float, None]


class DumbbellStyleAttrs(TypedDict):
    """The typing for the dumbbell chart style.

    The value labels take the shared `plot_value_*` keys.

    Attributes:
        plot_dumbbell_start_color (Union[str, None]): The color of the start dots; `None` takes the first color of the `PaperAccent` pair.
        plot_dumbbell_end_color (Union[str, None]): The color of the end dots; `None` takes the second color of the `PaperAccent` pair.
        plot_dumbbell_alpha (Union[float, None]): The alpha value of the dots.
        plot_dumbbell_size (Union[int, float, None]): The size of the dots, in points squared.
        plot_dumbbell_start_marker (Union[LINE_MARKER, str, None]): The marker of the start dots.
        plot_dumbbell_end_marker (Union[LINE_MARKER, str, None]): The marker of the end dots.
        plot_dumbbell_edge_width (Union[int, float, None]): The edge width of the dots.
        plot_dumbbell_edge_color (Union[str, None]): The edge color of the dots.
        plot_dumbbell_zorder (Union[int, float, None]): The zorder of the dots.
        plot_dumbbell_connector_color (Union[str, None]): The color of the connectors.
        plot_dumbbell_connector_width (Union[int, float, None]): The line width of the connectors.
        plot_dumbbell_connector_style (Union[LINE_STYLE, str, None]): The line style of the connectors.
        plot_dumbbell_connector_zorder (Union[int, float, None]): The zorder of the connectors; below the dots by default.
        plot_dumbbell_arrow_color (Union[str, None]): The color of the direction arrows under `show_direction`.
        plot_dumbbell_arrow_width (Union[int, float, None]): The line width of the direction arrows.
        plot_dumbbell_arrow_style (Union[str, None]): The direction arrow head, as a matplotlib arrow style.
        plot_dumbbell_arrow_gap (Union[int, float, None]): The space between a dot's edge and its direction arrow, in points.
        plot_dumbbell_grid_minor (Union[int, None]): The parts each step between labelled values splits into with fainter gridlines, on a gridded linear value axis; 0 or `None` draws none.

    """

    plot_dumbbell_start_color: Union[str, None]
    plot_dumbbell_end_color: Union[str, None]
    plot_dumbbell_alpha: Union[float, None]
    plot_dumbbell_size: Union[int, float, None]
    plot_dumbbell_start_marker: Union[LINE_MARKER, str, None]
    plot_dumbbell_end_marker: Union[LINE_MARKER, str, None]
    plot_dumbbell_edge_width: Union[int, float, None]
    plot_dumbbell_edge_color: Union[str, None]
    plot_dumbbell_zorder: Union[int, float, None]
    plot_dumbbell_connector_color: Union[str, None]
    plot_dumbbell_connector_width: Union[int, float, None]
    plot_dumbbell_connector_style: Union[LINE_STYLE, str, None]
    plot_dumbbell_connector_zorder: Union[int, float, None]
    plot_dumbbell_arrow_color: Union[str, None]
    plot_dumbbell_arrow_width: Union[int, float, None]
    plot_dumbbell_arrow_style: Union[str, None]
    plot_dumbbell_arrow_gap: Union[int, float, None]
    plot_dumbbell_grid_minor: Union[int, None]


class CalendarHeatmapStyleAttrs(TypedDict):
    """The typing for the calendar heatmap style.

    Attributes:
        plot_calendar_heatmap_cmap (Union[str, List[str], colors.LinearSegmentedColormap, None]): The colormap of the day cells (palette name, single color, list of hex colors, or colormap); `None` takes the heatmap colormap.
        plot_calendar_heatmap_cmap_diverging (Union[str, List[str], colors.LinearSegmentedColormap, None]): The colormap the day cells take under a centred `norm`; `None` takes the heatmap diverging colormap.
        plot_calendar_heatmap_alpha (Union[float, None]): The alpha value of the day cells.
        plot_calendar_heatmap_font_size (Union[int, float, str, None]): The font size of the cell values.
        plot_calendar_heatmap_font_color (Union[str, None]): The font color of the cell values.
        plot_calendar_heatmap_font_style (Union[FONT_STYLE, str, None]): The font style of the cell values.
        plot_calendar_heatmap_font_weight (Union[FONT_WEIGHT, str, None]): The font weight of the cell values.
        plot_calendar_heatmap_edge_width (Union[int, float, None]): The width of the borders drawn between the day cells (0 draws none).
        plot_calendar_heatmap_edge_color (Union[str, None]): The color of the borders drawn between the day cells.
        plot_calendar_heatmap_month_line_width (Union[int, float, None]): The width of the separators drawn between months (0 draws none).
        plot_calendar_heatmap_month_line_color (Union[str, None]): The color of the separators drawn between months; `None` takes the heatmap frame color.
        plot_calendar_heatmap_week_start (Union[CALENDAR_WEEKDAY, str, None]): The weekday in the top row of every week, the default of `week_start`.

    """

    plot_calendar_heatmap_cmap: Union[
        str, List[str], colors.LinearSegmentedColormap, None
    ]
    plot_calendar_heatmap_cmap_diverging: Union[
        str, List[str], colors.LinearSegmentedColormap, None
    ]
    plot_calendar_heatmap_alpha: Union[float, None]
    plot_calendar_heatmap_font_size: Union[int, float, str, None]
    plot_calendar_heatmap_font_color: Union[str, None]
    plot_calendar_heatmap_font_style: Union[FONT_STYLE, str, None]
    plot_calendar_heatmap_font_weight: Union[FONT_WEIGHT, str, None]
    plot_calendar_heatmap_edge_width: Union[int, float, None]
    plot_calendar_heatmap_edge_color: Union[str, None]
    plot_calendar_heatmap_month_line_width: Union[int, float, None]
    plot_calendar_heatmap_month_line_color: Union[str, None]
    plot_calendar_heatmap_week_start: Union[CALENDAR_WEEKDAY, str, None]


class ContourStyleAttrs(TypedDict):
    """The typing for the contour chart style.

    Attributes:
        plot_contour_color (Union[str, None]): The color of the iso-lines; `None` takes the panel's color cycle.
        plot_contour_cmap (Union[str, List[str], colors.LinearSegmentedColormap, None]): The colormap of the filled bands (palette name, single color, list of hex colors, or colormap); `None` takes the heatmap colormap. Iso-lines use it only when set.
        plot_contour_line_width (Union[int, float, None]): The width of the iso-lines; `None` takes the line chart width.
        plot_contour_line_style (Union[LINE_STYLE, str, None]): The style of the iso-lines.
        plot_contour_alpha (Union[float, None]): The alpha value of the contour.
        plot_contour_zorder (Union[int, float, None]): The z-order of the contour.
        plot_contour_label_font_size (Union[int, float, None]): The font size of the inline level labels; `None` takes the general font size minus two.
        plot_contour_label_font_color (Union[str, None]): The color of the inline level labels; `None` takes the line color.

    """

    plot_contour_color: Union[str, None]
    plot_contour_cmap: Union[str, List[str], colors.LinearSegmentedColormap, None]
    plot_contour_line_width: Union[int, float, None]
    plot_contour_line_style: Union[LINE_STYLE, str, None]
    plot_contour_alpha: Union[float, None]
    plot_contour_zorder: Union[int, float, None]
    plot_contour_label_font_size: Union[int, float, None]
    plot_contour_label_font_color: Union[str, None]


class HexbinStyleAttrs(TypedDict):
    """The typing for the hexbin chart style.

    Attributes:
        plot_hexbin_cmap (Union[str, List[str], colors.LinearSegmentedColormap, None]): The colormap of the hexagons (palette name, single color, list of hex colors, or colormap); `None` takes the heatmap colormap.
        plot_hexbin_alpha (Union[float, None]): The alpha value of the hexagons.
        plot_hexbin_edge_width (Union[int, float, None]): The width of the hexagon edges; `0` draws none.
        plot_hexbin_edge_color (Union[str, None]): The color of the hexagon edges.
        plot_hexbin_gridsize (Union[int, None]): The number of hexagons across the x-axis when the chart sets no `gridsize`.

    """

    plot_hexbin_cmap: Union[str, List[str], colors.LinearSegmentedColormap, None]
    plot_hexbin_alpha: Union[float, None]
    plot_hexbin_edge_width: Union[int, float, None]
    plot_hexbin_edge_color: Union[str, None]
    plot_hexbin_gridsize: Union[int, None]


class ImageStyleAttrs(TypedDict):
    """The typing for the image chart style.

    Attributes:
        plot_image_alpha (Union[float, None]): The alpha value of the picture; below 1 lets the axes ground show through.
        plot_image_cmap (Union[str, List[str], colors.LinearSegmentedColormap, None]): The colormap a 2-D array is read through (palette name, single color, list of hex colors, or colormap); an RGB(A) picture ignores it.
        plot_image_interpolation (Union[str, None]): How the pixels are resampled to the axes, as matplotlib's `imshow` names it (`"antialiased"`, `"nearest"`, `"bilinear"`, ...).
        plot_image_aspect (Union[str, float, None]): The aspect of the pixels: `"auto"` stretches the picture to fill its extent and leaves the axes shape to the data; `"equal"` keeps the pixels square and reshapes the axes.

    """

    plot_image_alpha: Union[float, None]
    plot_image_cmap: Union[str, List[str], colors.LinearSegmentedColormap, None]
    plot_image_interpolation: Union[str, None]
    plot_image_aspect: Union[str, float, None]


class BasemapStyleAttrs(TypedDict):
    """The typing for the basemap chart style.

    Attributes:
        plot_basemap_land_color (Union[str, None]): The fill color of the land, and of the countries `highlight` leaves out.
        plot_basemap_highlight_color (Union[str, None]): The fill color of the countries `highlight` picks out.
        plot_basemap_highlight_edge_color (Union[str, None]): The color of the outline around the countries `highlight` picks out, coast included.
        plot_basemap_highlight_edge_width (Union[float, None]): The width of that outline, in points; 0 (default) draws none.
        plot_basemap_coastline_color (Union[str, None]): The color of the coastlines.
        plot_basemap_coastline_width (Union[float, None]): The width of the coastlines, in points.
        plot_basemap_border_color (Union[str, None]): The color of the borders between countries.
        plot_basemap_border_width (Union[float, None]): The width of the borders, in points.
        plot_basemap_border_style (Union[LINE_STYLE, str, None]): The line style of the borders. See [`LINE_STYLE`][datachart.constants.LINE_STYLE].
        plot_basemap_lake_color (Union[str, None]): The fill color of the lakes; `None` takes the axes background, so a lake reads as water.
        plot_basemap_river_color (Union[str, None]): The color of the rivers.
        plot_basemap_river_width (Union[float, None]): The width of the rivers, in points.
        plot_basemap_road_color (Union[str, None]): The color of the roads.
        plot_basemap_road_width (Union[float, None]): The width of the roads, in points.

    """

    plot_basemap_land_color: Union[str, None]
    plot_basemap_highlight_color: Union[str, None]
    plot_basemap_highlight_edge_color: Union[str, None]
    plot_basemap_highlight_edge_width: Union[float, None]
    plot_basemap_coastline_color: Union[str, None]
    plot_basemap_coastline_width: Union[float, None]
    plot_basemap_border_color: Union[str, None]
    plot_basemap_border_width: Union[float, None]
    plot_basemap_border_style: Union[LINE_STYLE, str, None]
    plot_basemap_lake_color: Union[str, None]
    plot_basemap_river_color: Union[str, None]
    plot_basemap_river_width: Union[float, None]
    plot_basemap_road_color: Union[str, None]
    plot_basemap_road_width: Union[float, None]


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
        plot_scatter_error_color (Union[str, None]): The color of the error bars;
            `None` takes the color of the point they belong to.
        plot_scatter_error_width (Union[int, float, None]): The error bar line width.
        plot_scatter_error_capsize (Union[int, float, None]): The half-width of the
            cap drawn at each end of an error bar; `0` draws none.

    """

    plot_scatter_color: Union[str, None]
    plot_scatter_alpha: Union[float, None]
    plot_scatter_size: Union[int, float, None]
    plot_scatter_marker: Union[LINE_MARKER, str, None]
    plot_scatter_zorder: Union[int, float, None]
    plot_scatter_edge_width: Union[int, float, None]
    plot_scatter_edge_color: Union[str, None]
    plot_scatter_error_color: Union[str, None]
    plot_scatter_error_width: Union[int, float, None]
    plot_scatter_error_capsize: Union[int, float, None]


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
        plot_box_whisker_color (Union[str, None]): The whisker line color.
        plot_box_whisker_linewidth (Union[int, float, None]): The whisker line width.
        plot_box_cap_color (Union[str, None]): The cap line color.
        plot_box_cap_linewidth (Union[int, float, None]): The cap line width.
        plot_xticks_label_rotate (Union[int, float, None]): The label rotation of the xticks.
        plot_yticks_label_rotate (Union[int, float, None]): The label rotation of the yticks.
        plot_box_hatch (Union[HATCH_STYLE, str, None]): The hatch pattern of the box.
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
    plot_box_whisker_color: Union[str, None]
    plot_box_whisker_linewidth: Union[int, float, None]
    plot_box_cap_color: Union[str, None]
    plot_box_cap_linewidth: Union[int, float, None]
    plot_xticks_label_rotate: Union[int, float, None]
    plot_yticks_label_rotate: Union[int, float, None]
    plot_box_hatch: Union[HATCH_STYLE, str, None]


class SwarmStyleAttrs(TypedDict):
    """The typing for the swarm plot style.

    Attributes:
        plot_swarm_color (Union[str, None]): The point color.
        plot_swarm_alpha (Union[float, None]): The alpha value of the points.
        plot_swarm_size (Union[int, float, None]): The point size.
        plot_swarm_marker (Union[LINE_MARKER, str, None]): The point marker shape.
        plot_swarm_zorder (Union[int, float, None]): The zorder of the points.
        plot_swarm_edge_width (Union[int, float, None]): The edge width of the points.
        plot_swarm_edge_color (Union[str, None]): The edge color of the points.

    """

    plot_swarm_color: Union[str, None]
    plot_swarm_alpha: Union[float, None]
    plot_swarm_size: Union[int, float, None]
    plot_swarm_marker: Union[LINE_MARKER, str, None]
    plot_swarm_zorder: Union[int, float, None]
    plot_swarm_edge_width: Union[int, float, None]
    plot_swarm_edge_color: Union[str, None]


class ViolinStyleAttrs(TypedDict):
    """The typing for the violin plot style.

    Attributes:
        plot_violin_color (Union[str, None]): The violin fill color.
        plot_violin_alpha (Union[float, None]): The alpha value of the violin body.
        plot_violin_linewidth (Union[int, float, None]): The line width of the body edge.
        plot_violin_edgecolor (Union[str, None]): The edge color of the body; defaults to the fill.
        plot_violin_width (Union[int, float, None]): The maximum width of the body.
        plot_violin_inner_color (Union[str, None]): The color of the inner marks; defaults to the font color.
        plot_violin_inner_linewidth (Union[int, float, None]): The line width of the inner marks.
        plot_violin_median_color (Union[str, None]): The color of the median dot.
        plot_violin_median_size (Union[int, float, None]): The size of the median dot.
        plot_violin_hatch (Union[HATCH_STYLE, str, None]): The hatch pattern of the body.
    """

    plot_violin_color: Union[str, None]
    plot_violin_alpha: Union[float, None]
    plot_violin_linewidth: Union[int, float, None]
    plot_violin_edgecolor: Union[str, None]
    plot_violin_width: Union[int, float, None]
    plot_violin_inner_color: Union[str, None]
    plot_violin_inner_linewidth: Union[int, float, None]
    plot_violin_median_color: Union[str, None]
    plot_violin_median_size: Union[int, float, None]
    plot_violin_hatch: Union[HATCH_STYLE, str, None]


class RidgelineStyleAttrs(TypedDict):
    """The typing for the ridgeline plot style.

    Attributes:
        plot_ridgeline_color (Union[str, None]): The ridge fill color; defaults to the palette color.
        plot_ridgeline_alpha (Union[float, None]): The alpha value of the ridge fill.
        plot_ridgeline_linewidth (Union[int, float, None]): The line width of the ridge outline.
        plot_ridgeline_edgecolor (Union[str, None]): The color of the ridge outline; defaults to the fill.
        plot_ridgeline_overlap (Union[float, None]): How far a peak rises into the row above, in `[0, 1]`.
        plot_ridgeline_inner_color (Union[str, None]): The color of the inner marks; defaults to the font color.
        plot_ridgeline_inner_linewidth (Union[int, float, None]): The line width of the inner marks.
        plot_ridgeline_hatch (Union[HATCH_STYLE, str, None]): The hatch pattern of the ridge fill.

    """

    plot_ridgeline_color: Union[str, None]
    plot_ridgeline_alpha: Union[float, None]
    plot_ridgeline_linewidth: Union[int, float, None]
    plot_ridgeline_edgecolor: Union[str, None]
    plot_ridgeline_overlap: Union[float, None]
    plot_ridgeline_inner_color: Union[str, None]
    plot_ridgeline_inner_linewidth: Union[int, float, None]
    plot_ridgeline_hatch: Union[HATCH_STYLE, str, None]


class RaincloudStyleAttrs(ViolinStyleAttrs, SwarmStyleAttrs, BoxStyleAttrs):
    """The typing for the raincloud plot style.

    The union of the violin (cloud), swarm (rain), and box style keys; each
    key styles its own part of the raincloud.

    """


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
        plot_parallel_tick_label_bg_color (Union[str, None]): The tick label background color; `None` draws no box and strokes the label with the value halo instead.
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


class ScatterMatrixStyleAttrs(TypedDict):
    """The typing for the scatter matrix style.

    The cells take the scatter, histogram and plot text keys; these keys
    style what the matrix adds on top of them.

    Attributes:
        plot_scatter_matrix_regression_color (Union[str, None]): The color of the regression lines under `show_regression`; `None` takes each hue group's color.
        plot_scatter_matrix_regression_width (Union[int, float, None]): The line width of the regression lines.
        plot_scatter_matrix_regression_style (Union[LINE_STYLE, str, None]): The line style of the regression lines.
        plot_scatter_matrix_correlation_size (Union[int, float, None]): The font size of the correlation text under `show_correlation`.
        plot_scatter_matrix_correlation_weight (Union[FONT_WEIGHT, str, None]): The font weight of the correlation text.
        plot_scatter_matrix_kde_width (Union[int, float, None]): The line width of the diagonal density curves.
        plot_scatter_matrix_kde_alpha (Union[float, None]): The alpha value of the fill under the diagonal density curves; 0 draws no fill.
        plot_scatter_matrix_diagonal_alpha (Union[float, None]): The alpha value of the diagonal histograms, overlaid per hue group.

    """

    plot_scatter_matrix_regression_color: Union[str, None]
    plot_scatter_matrix_regression_width: Union[int, float, None]
    plot_scatter_matrix_regression_style: Union[LINE_STYLE, str, None]
    plot_scatter_matrix_correlation_size: Union[int, float, None]
    plot_scatter_matrix_correlation_weight: Union[FONT_WEIGHT, str, None]
    plot_scatter_matrix_kde_width: Union[int, float, None]
    plot_scatter_matrix_kde_alpha: Union[float, None]
    plot_scatter_matrix_diagonal_alpha: Union[float, None]


class ThemeDefaultAttrs(TypedDict):
    """The typing for theme-driven defaults and cycles.

    Attributes:
        chart_default_show_grid (Union[SHOW_GRID, str, None]): The theme default
            for `show_grid`, applied when a chart call leaves it unset. Never
            applies to heatmaps. `None` means the theme has no opinion.
        chart_default_show_values (Union[bool, None]): The theme default for
            `show_values`, applied to every chart that takes it when the chart
            call leaves it unset. `None` means the theme has no opinion.
        chart_default_node_label_position (Union[NETWORK_LABEL_POSITION, str, None]):
            The theme default for the network chart's `label_position`, applied
            when the chart call leaves it unset. `None` means the theme has no
            opinion.
        plot_hatch_cycle (Union[List[str], None]): The hatch patterns assigned
            per bar/histogram series, parallel to the color cycle; with
            `plot_etch` on, line area fills and stacked areas take them too. An
            explicit per-chart hatch style wins. `None` disables the cycle.
        plot_linestyle_cycle (Union[List[Union[LINE_STYLE, str]], None]): The
            line styles assigned per line, bump and radial line series, parallel
            to the color cycle. An explicit per-chart line style wins. `None`
            disables the cycle.
        plot_marker_cycle (Union[List[Union[LINE_MARKER, str, Dict[str, Union[str, bool]]]], None]):
            The markers assigned per scatter and radial scatter series,
            parallel to the color cycle, and per network node group: a marker,
            or `{"marker": ..., "hollow": True}` to draw it as an outline. An
            explicit per-chart marker wins.
            `None` disables the cycle.
    """

    chart_default_show_grid: Union[SHOW_GRID, str, None]
    chart_default_show_values: Union[bool, None]
    chart_default_node_label_position: Union[NETWORK_LABEL_POSITION, str, None]
    plot_hatch_cycle: Union[List[str], None]
    plot_linestyle_cycle: Union[List[Union[LINE_STYLE, str]], None]
    plot_marker_cycle: Union[
        List[Union[LINE_MARKER, str, Dict[str, Union[str, bool]]]], None
    ]


class SketchStyleAttrs(TypedDict):
    """The typing for the sketch attributes: the theme's render-scoped rc-level
    look (path wobble, halo stroke). The panel snapshots the wobble at build
    time and applies it inside a scoped matplotlib rc context, so no global rc
    setting changes; the halo resolves like any style key, so a chart's `style`
    can override it. Composition keeps the look of the figures it was built from.

    Attributes:
        plot_sketch_params (Union[List[float], None]): The path wobble as
            matplotlib sketch parameters `[scale, length, randomness]`;
            `plt.xkcd()` uses `[1, 100, 2]`. `None` draws clean paths.
        plot_sketch_halo_width (Union[float, None]): The extra width, added to
            the line width, of the halo (in the axes face color) stroked under series lines (line,
            radial, regression), so crossing lines read as cut-outs; marks, text
            and patches stay clean. `None` or `0` draws no halo.

    """

    plot_sketch_params: Union[List[float], None]
    plot_sketch_halo_width: Union[float, None]


class InkStyleAttrs(TypedDict):
    """The typing for the ink attributes: marks drawn as a quill and an etching
    needle would draw them. Every attribute resolves when the chart is built and
    rides on its artists, so composition keeps the look; `None` turns it off.

    Attributes:
        plot_ink_stroke (Union[Dict[str, float], None]): The broad-nib pen the
            series lines (line, bump, radial, regression) are drawn with, as a
            filled ribbon whose width varies along the line. Keys:
            `width_scale` (the nib width over the line width), `nib_angle`
            (degrees), `nib_floor` (the hairline width as a share of the nib),
            `wobble` (the ink wobble amplitude), `taper` (the end taper, in
            pixels). `None` draws plain lines.
        plot_etch (Union[Dict[str, Union[float, str, None]], None]): The
            etching that replaces the hatch tile of a hatched fill with
            hand-drawn lines clipped to its outline; the hatch pattern still
            picks the lines and `.` stipples. Keys: `spacing` (points between
            lines), `jitter` (the spacing jitter as a share of it),
            `angle_jitter` (degrees), `line_width` (points), `wash` (the share
            of the face color laid over the axes face under the lines; fills
            under lines take none), `color` (the etch ink). `None` keeps
            matplotlib's hatch.
        plot_value_etch (Union[Dict[str, List[str]], None]): The steps a value
            scale draws in when `plot_etch` is on: `washes` (one fill color per
            step, lightest first) and `hatches` (one pattern per step, sparsest
            first). Heatmap, calendar heatmap and hexbin cells and filled
            contour bands take the step their value falls in, a filled contour
            draws its level lines and labels over the bands, and a legend of
            the steps replaces the colorbar. `None` keeps the colormap.

    """

    plot_ink_stroke: Union[Dict[str, float], None]
    plot_etch: Union[Dict[str, Union[float, str, None]], None]
    plot_value_etch: Union[Dict[str, List[str]], None]


class StyleAttrs(
    ColorStyleAttrs,
    FontStyleAttrs,
    AxesStyleAttrs,
    LegendStyleAttrs,
    AreaStyleAttrs,
    GridStyleAttrs,
    LineStyleAttrs,
    StackedAreaStyleAttrs,
    BumpStyleAttrs,
    SankeyStyleAttrs,
    TreemapStyleAttrs,
    NetworkStyleAttrs,
    BarStyleAttrs,
    ValueLabelStyleAttrs,
    HistStyleAttrs,
    VLineStyleAttrs,
    HLineStyleAttrs,
    DLineStyleAttrs,
    BracketStyleAttrs,
    VSpanStyleAttrs,
    HSpanStyleAttrs,
    TextStyleAttrs,
    HeatmapStyleAttrs,
    CalendarHeatmapStyleAttrs,
    GanttStyleAttrs,
    DumbbellStyleAttrs,
    ContourStyleAttrs,
    HexbinStyleAttrs,
    ImageStyleAttrs,
    BasemapStyleAttrs,
    ScatterStyleAttrs,
    RegressionStyleAttrs,
    BoxStyleAttrs,
    SwarmStyleAttrs,
    ViolinStyleAttrs,
    RidgelineStyleAttrs,
    ParallelCoordsStyleAttrs,
    ScatterMatrixStyleAttrs,
    ThemeDefaultAttrs,
    SketchStyleAttrs,
    InkStyleAttrs,
):
    """The style attributes. Combines all style typings."""

    pass


# ================================================
# Reference Line Attributes
# ================================================


class VLineSettingAttrs(TypedDict):
    """The vertical reference line setting, passed to a chart front as `vlines`.

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


class HLineSettingAttrs(TypedDict):
    """The horizontal reference line setting, passed to a chart front as `hlines`.

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


class DLineSettingAttrs(TypedDict):
    """The diagonal reference line setting, passed to a chart front as `dlines`.

    The line is straight in data coordinates, so it curves on a log axis,
    where it is drawn between the axis limits. On linear axes, and without
    `xmin` and `xmax`, it spans the axes and follows the zoom.

    Attributes:
        slope (Union[int, float, None]): The slope of the line. Defaults to 1.
        intercept (Union[int, float, None]): The y-axis value of the line at x = 0. Defaults to 0.
        xmin (Union[int, float, None]): The x-axis position the line starts at.
        xmax (Union[int, float, None]): The x-axis position the line ends at.
        style (Union[DLineStyleAttrs, None]): The diagonal line style attributes.
        label (Union[str, None]): The label of the diagonal line.

    """

    slope: Union[int, float, None]
    intercept: Union[int, float, None]
    xmin: Union[int, float, None]
    xmax: Union[int, float, None]
    style: Union[DLineStyleAttrs, None]
    label: Union[str, None]


# `from` is a keyword, so the bracket setting is declared functionally
BracketSettingAttrs = TypedDict(
    "BracketSettingAttrs",
    {
        "from": Union[str, int, float],
        "to": Union[str, int, float],
        "text": Union[str, None],
        "y": Union[int, float, None],
        "style": Union[BracketStyleAttrs, None],
    },
    total=False,
)
BracketSettingAttrs.__doc__ = """The pairwise comparison bracket setting, passed to a chart front as `brackets`.

A bracket spans two categories of the category axis, with a tick at each end
pointing toward the data and its text centred beyond the span. Without `y` it
sits above the data within its span, and brackets that overlap stack without
covering each other; the value axis then grows to fit them, unless the chart
sets its own limit. A chart whose marks carry no position of their own, such
as a histogram, has no data inside the span to read, so the bracket clears
the whole chart instead.

Attributes:
    from (Union[str, int, float]): The category the bracket starts at: its label, or a position on the category axis.
    to (Union[str, int, float]): The category the bracket ends at: its label, or a position on the category axis.
    text (Union[str, None]): The text drawn beyond the span, such as a p-value.
    y (Union[int, float, None]): The value-axis position of the bracket line; on a horizontal chart, the x position.
    style (Union[BracketStyleAttrs, None]): The bracket style attributes.

"""


# ================================================
# Vertical and Horizontal Band Attributes
# ================================================


class VSpanSettingAttrs(TypedDict):
    """The vertical reference band setting, passed to a chart front as `vspans`.

    A vertical band shades the region between two x-axis positions over the
    full height of the axes. On a radial chart the bounds are angles in
    degrees and the band is a wedge over the full radius.

    Attributes:
        xmin (Union[int, float, None]): The lower x-axis bound. Defaults to the axis minimum.
        xmax (Union[int, float, None]): The upper x-axis bound. Defaults to the axis maximum.
        style (Union[VSpanStyleAttrs, None]): The vertical band style attributes.
        label (Union[str, None]): The label of the band (shown in the legend).

    """

    xmin: Union[int, float, None]
    xmax: Union[int, float, None]
    style: Union[VSpanStyleAttrs, None]
    label: Union[str, None]


class HSpanSettingAttrs(TypedDict):
    """The horizontal reference band setting, passed to a chart front as `hspans`.

    A horizontal band shades the region between two y-axis positions over the
    full width of the axes. On a radial chart the bounds are radii and the
    band is an annulus over the full circle.

    Attributes:
        ymin (Union[int, float, None]): The lower y-axis bound. Defaults to the axis minimum.
        ymax (Union[int, float, None]): The upper y-axis bound. Defaults to the axis maximum.
        style (Union[HSpanStyleAttrs, None]): The horizontal band style attributes.
        label (Union[str, None]): The label of the band (shown in the legend).

    """

    ymin: Union[int, float, None]
    ymax: Union[int, float, None]
    style: Union[HSpanStyleAttrs, None]
    label: Union[str, None]


# ================================================
# Text Annotation Attributes
# ================================================


class LegendSettingAttrs(TypedDict):
    """The per-figure legend setting, passed to a chart front as `legend`.

    Every field is optional; a `None` field falls back to the theme's
    `plot_legend_*` attribute of the same name.

    Attributes:
        title (Union[str, None]): The legend title; an empty string draws none.
        location (Union[LEGEND_LOCATION, str, None]): The legend location. An
            outside member places the legend beside the axes.
        ncols (Union[int, None]): The number of legend columns.
        alignment (Union[LEGEND_ALIGN, str, None]): The legend alignment.

    """

    title: Union[str, None]
    location: Union[LEGEND_LOCATION, str, None]
    ncols: Union[int, None]
    alignment: Union[LEGEND_ALIGN, str, None]


class EmphasisRuleAttrs(TypedDict):
    """The emphasis rule setting, passed to a chart front as `emphasis_rule`.

    Exactly one comparison key: a unit matching it is highlighted and every
    other unit muted. Each front selects its own unit — a bar, leaf, node,
    row, cell or bin reads its one value; a group or series reads a summary
    of its values, chosen by `by`. A unit's explicit `emphasis` role wins.

    Attributes:
        above (Union[int, float]): Highlight values strictly above this.
        below (Union[int, float]): Highlight values strictly below this.
        between (Tuple[Union[int, float], Union[int, float]]): Highlight
            values within `(lo, hi)`, both bounds inclusive.
        top (int): Highlight the `n` largest values; ties keep input order.
        bottom (int): Highlight the `n` smallest values; ties keep input order.
        by (Literal["mean", "median", "min", "max", "sum"]): The summary a
            group or series is read by. Groups default to `"median"`, series
            to `"mean"`; a front reading one value per unit rejects it.

    """

    above: Union[int, float]
    below: Union[int, float]
    between: Tuple[Union[int, float], Union[int, float]]
    top: int
    bottom: int
    by: Literal["mean", "median", "min", "max", "sum"]


class TextSettingAttrs(TypedDict):
    """The text annotation setting, passed to a chart front as `texts`.

    Attributes:
        text (str): The annotation text.
        x (Union[int, float]): The x-axis position of the text.
        y (Union[int, float]): The y-axis position of the text.
        coords (Union[str, None]): The coordinate system of the text position:
            `"data"` (default) or `"axes"` (axes fraction, `0`–`1`).
        target (Union[Tuple[Union[int, float], Union[int, float]], None]): The
            data point the connector points to, always in data coordinates.
            When present, a connector is drawn from the text to the target.
        style (Union[TextStyleAttrs, None]): The per-text style attributes.
        subplot (Union[int, None]): The 0-based index, in render order, of the
            subplot the text lands in. Read only by `Annotate` on a
            multi-subplot figure, where every text must name one; chart fronts
            target subplots with a list of lists instead.
    """

    text: str
    x: Union[int, float]
    y: Union[int, float]
    coords: Union[str, None]
    target: Union[Tuple[Union[int, float], Union[int, float]], None]
    style: Union[TextStyleAttrs, None]
    subplot: Union[int, None]


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
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
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

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    x: Union[str, None]  # the name of the x attribute in data (default: "x")
    y: Union[str, None]  # the name of the y attribute in data (default: "y")
    yerr: Union[str, None]  # the name of the yerr attribute in data (default: "yerr")


# ================================================
# Stacked Area Chart Attributes
# ================================================


class StackedAreaSingleChartAttrs(TypedDict):
    """The single chart attributes for the stacked area chart.

    Attributes:
        data (List[LineDataPointAttrs]): The list of data points defining one series; every series shares the same `x` values.
        subtitle (Union[str, None]): The subtitle of the series. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the chart.
        ylabel (Union[str, None]): The ylabel of the chart.
        style (Union[StackedAreaStyleAttrs, None]): The style of the series.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        x (Union[str, None]): The key name in `data` that contains the x-axis value. Defaults to `"x"`.
        y (Union[str, None]): The key name in `data` that contains the y-axis value. Defaults to `"y"`.

    """

    data: List[LineDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[StackedAreaStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    x: Union[str, None]
    y: Union[str, None]


# ================================================
# Bump Chart Attributes
# ================================================


class BumpSingleChartAttrs(TypedDict):
    """The single chart attributes for the bump chart.

    Attributes:
        data (List[LineDataPointAttrs]): The list of data points defining one series; `y` is a value ranked per period, or the rank itself.
        subtitle (Union[str, None]): The subtitle of the series. Also used as its end label and legend label.
        xlabel (Union[str, None]): The xlabel of the chart.
        ylabel (Union[str, None]): The ylabel of the chart.
        style (Union[BumpStyleAttrs, None]): The style of the series.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        x (Union[str, None]): The key name in `data` that contains the x-axis value. Defaults to `"x"`.
        y (Union[str, None]): The key name in `data` that contains the y-axis value. Defaults to `"y"`.

    """

    data: List[LineDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[BumpStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    x: Union[str, None]
    y: Union[str, None]


# ================================================
# Sankey Chart Attributes
# ================================================


class SankeyLinkAttrs(TypedDict):
    """The link record attributes for the Sankey chart.

    Attributes:
        source (str): The node the flow leaves.
        target (str): The node the flow enters.
        value (Union[int, float]): The size of the flow; must be greater than 0.

    """

    source: str
    target: str
    value: Union[int, float]


class SankeySingleChartAttrs(TypedDict):
    """The single chart attributes for the Sankey chart.

    Attributes:
        links (List[SankeyLinkAttrs]): The flows; a node is the string that names it.
        subtitle (Union[str, None]): The subtitle of the chart.
        style (Union[SankeyStyleAttrs, None]): The style of the chart.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    links: List[SankeyLinkAttrs]
    subtitle: Union[str, None]
    style: Union[SankeyStyleAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Treemap Attributes
# ================================================


class TreemapRecordAttrs(TypedDict):
    """The record attributes for the treemap.

    Attributes:
        label (str): The drawn label of the tile or group.
        value (Union[int, float, None]): The size of the tile; must be greater than 0. A group omits it or carries its children's sum.
        children (Union[List["TreemapRecordAttrs"], None]): The records of a group, nesting up to four levels deep.
        emphasis (Union[EMPHASIS, str, None]): The emphasis role of the record and its subtree; a descendant's own role overrides it.

    """

    label: str
    value: Union[int, float, None]
    children: Union[List["TreemapRecordAttrs"], None]
    emphasis: Union[EMPHASIS, str, None]


class TreemapSingleChartAttrs(TypedDict):
    """The single chart attributes for the treemap.

    Attributes:
        data (List[TreemapRecordAttrs]): The records to tile.
        subtitle (Union[str, None]): The subtitle of the chart.
        style (Union[TreemapStyleAttrs, None]): The style of the chart.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: List[TreemapRecordAttrs]
    subtitle: Union[str, None]
    style: Union[TreemapStyleAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Network Chart Attributes
# ================================================


class NetworkNodeAttrs(TypedDict):
    """The node record attributes for the network chart.

    Attributes:
        id (str): The node identifier the edges refer to; unique within a chart.
        label (Union[str, None]): The drawn label; defaults to `id`. An empty string draws nothing.
        size (Union[int, float, None]): The node size, mapped by square root to marker area; must be greater than 0.
        group (Union[str, None]): The group the node is colored by.
        emphasis (Union[EMPHASIS, str, None]): The emphasis role of the node.
        x (Union[float, None]): The node's horizontal position in the 0–1 layout space; `NETWORK_LAYOUT.FIXED` only.
        y (Union[float, None]): The node's vertical position in the 0–1 layout space; `NETWORK_LAYOUT.FIXED` only.

    """

    id: str
    label: Union[str, None]
    size: Union[int, float, None]
    group: Union[str, None]
    emphasis: Union[EMPHASIS, str, None]
    x: Union[float, None]
    y: Union[float, None]


class NetworkEdgeAttrs(TypedDict):
    """The edge record attributes for the network chart.

    Attributes:
        source (str): The id of the node the edge leaves.
        target (str): The id of the node the edge enters.
        weight (Union[int, float, None]): The edge weight, mapped to its width and, under the weighted layouts, its pull; must be greater than 0.

    """

    source: str
    target: str
    weight: Union[int, float, None]


class NetworkSingleChartAttrs(TypedDict):
    """The single chart attributes for the network chart.

    Attributes:
        nodes (Union[List[NetworkNodeAttrs], None]): The nodes; inferred from the edges when omitted.
        edges (List[NetworkEdgeAttrs]): The edges.
        subtitle (Union[str, None]): The subtitle of the chart.
        style (Union[NetworkStyleAttrs, None]): The style of the chart.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    nodes: Union[List[NetworkNodeAttrs], None]
    edges: List[NetworkEdgeAttrs]
    subtitle: Union[str, None]
    style: Union[NetworkStyleAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Bar Chart Attributes
# ================================================


class BarDataPointAttrs(TypedDict):
    """The data point attributes for the bar chart.

    Attributes:
        label (str): The label.
        y (Union[int, float]): The y-axis value.
        yerr (Optional[Union[int, float]]): The y-axis error value.
        emphasis (Optional[Union[EMPHASIS, str]]): The bar's own emphasis role
            ("background" or "highlight"); wins over the chart's `emphasis_rule`.

    """

    # the default attributes, could be anything
    label: str
    y: Union[int, float]
    yerr: Optional[Union[int, float]]
    emphasis: Optional[Union[EMPHASIS, str]]


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
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
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

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    y: Union[str, None]  # the name of the y attribute in data
    yerr: Union[str, None]  # the name of the yerr attribute in data


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
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
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

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    x: Union[str, None]  # the name of the x attribute in data


# ================================================
# Heatmap Chart Attributes
# ================================================


class ColorbarSettingAttrs(TypedDict):
    """The per-figure colorbar setting, passed to a chart front as `colorbar`.

    Every field is optional. `location` is the control: it places the bar on
    any edge of the chart. With no `location`, `orientation` derives the edge:
    vertical means right, horizontal means top. When both are given `location`
    wins.

    Attributes:
        label (Union[str, None]): The caption beside the bar, reading along
            it; drawn in the `font_ylabel_*` theme font.
        location (Union[COLORBAR_LOCATION, str, None]): The chart edge the
            bar sits on.
        format (Union[VALUE_FORMAT, str, None]): The format of the bar's tick
            labels, with the value named `x` (e.g. `"{x:.0f}"`). On a hexbin
            chart, `value_format` still applies when this is unset.
        ticks (Union[List[Union[int, float]], None]): Explicit tick positions
            on the bar; positions outside the mapped value range are not drawn.
        orientation (Union[ORIENTATION, str, None]): The orientation; derives
            the edge when `location` is unset.

    """

    label: Union[str, None]
    location: Union[COLORBAR_LOCATION, str, None]
    format: Union[VALUE_FORMAT, str, None]
    ticks: Union[List[Union[int, float]], None]
    orientation: Union[ORIENTATION, str, None]


class HeatmapDataAttrs(TypedDict):
    """The data attributes for the heatmap chart.

    Attributes:
        x (Union[List[Union[str, int, float]], None]): The column labels, one per column of `z`. Defaults to the column indices.
        y (Union[List[Union[str, int, float]], None]): The row labels, one per row of `z`. Defaults to the row indices.
        z (List[List[Union[int, float, None]]]): The 2-D grid of cell values, one row per `y` and one column per `x`.
        emphasis (Union[List[List[Union[EMPHASIS, str, None]]], None]): The per-cell emphasis roles, aligned with `z` ("background" or "highlight"); wins over the chart's `emphasis_rule`.

    """

    x: Union[List[Union[str, int, float]], None]
    y: Union[List[Union[str, int, float]], None]
    z: List[List[Union[int, float, None]]]
    emphasis: Union[List[List[Union[EMPHASIS, str, None]]], None]


class HeatmapSingleChartAttrs(TypedDict):
    """The single chart attributes for the heatmap chart.

    Attributes:
        data (HeatmapDataAttrs): The labelled grid defining the heatmap chart.
        subtitle (Union[str, None]): The subtitle of the heatmap chart. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the heatmap chart.
        ylabel (Union[str, None]): The ylabel of the heatmap chart.
        style (Union[HeatmapStyleAttrs, None]): The style of the heatmap chart.

        norm (Union[COLOR_NORM, str, None]): The value normalization.
        vmin (Union[str, None]): The minimum value to normalize the data points.
        vmax (Union[str, None]): The maximum value to normalize the data points.

        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.

        colorbar (Union[ColorbarSettingAttrs, None]): The colorbar setting of the heatmap.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: HeatmapDataAttrs
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

    colorbar: Union[ColorbarSettingAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Calendar Heatmap Attributes
# ================================================


class CalendarHeatmapDataAttrs(TypedDict):
    """The data attributes for the calendar heatmap.

    Attributes:
        date (List[Union[date, datetime]]): One temporal object per day: a `date`, `datetime`, `numpy.datetime64`, or pandas `Timestamp`. Date strings are never parsed, and every date appears once.
        value (List[Union[int, float, None]]): The value of each day, one per date; `None` leaves the day blank.

    """

    date: List[Union[date, datetime]]
    value: List[Union[int, float, None]]


class CalendarHeatmapSingleChartAttrs(TypedDict):
    """The single chart attributes for the calendar heatmap.

    Attributes:
        data (CalendarHeatmapDataAttrs): The dated values defining the calendar.
        subtitle (Union[str, None]): The subtitle of the calendar; a multi-year calendar appends the year to it.
        style (Union[CalendarHeatmapStyleAttrs, None]): The style of the calendar.

        norm (Union[COLOR_NORM, str, None]): The value normalization.
        vmin (Union[float, None]): The minimum value to normalize the data points.
        vmax (Union[float, None]): The maximum value to normalize the data points.

        colorbar (Union[ColorbarSettingAttrs, None]): The colorbar setting of the calendar.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: CalendarHeatmapDataAttrs
    subtitle: Union[str, None]
    style: Union[CalendarHeatmapStyleAttrs, None]

    norm: Union[str, None]
    vmin: Union[float, None]
    vmax: Union[float, None]

    colorbar: Union[ColorbarSettingAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Gantt Chart Attributes
# ================================================


class GanttTaskAttrs(TypedDict):
    """The task record attributes for the gantt chart.

    Attributes:
        task (str): The task name, unique within the chart; the label of its row.
        start (Union[date, datetime]): When the task starts: a `date`, `datetime`, `numpy.datetime64`, or pandas `Timestamp`. Date strings are never parsed.
        end (Union[date, datetime]): When the task ends, of the same temporal types; never before `start`. A task ending when it starts is a milestone, drawn as a marker.
        group (Optional[str]): The task group; tasks of one group share a color and a legend entry.
        progress (Optional[Union[int, float]]): The fraction of the task done, in `[0, 1]`; drawn as an inner bar.
        depends_on (Optional[List[str]]): The names of the tasks this task depends on.
        emphasis (Optional[Union[EMPHASIS, str]]): The task's own emphasis role ("background" or "highlight"); wins over the chart's `emphasis_rule`.

    """

    task: str
    start: Union[date, datetime]
    end: Union[date, datetime]
    group: Optional[str]
    progress: Optional[Union[int, float]]
    depends_on: Optional[List[str]]
    emphasis: Optional[Union[EMPHASIS, str]]


class GanttSingleChartAttrs(TypedDict):
    """The single chart attributes for the gantt chart.

    Attributes:
        data (List[GanttTaskAttrs]): The task records defining one schedule.
        subtitle (Union[str, None]): The subtitle of the schedule.
        style (Union[GanttStyleAttrs, None]): The style of the schedule.
        xtickrotate (Union[int, None]): The xtick rotation value.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: List[GanttTaskAttrs]
    subtitle: Union[str, None]
    style: Union[GanttStyleAttrs, None]

    xtickrotate: Union[int, None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Dumbbell Chart Attributes
# ================================================


class DumbbellRecordAttrs(TypedDict):
    """The record attributes for the dumbbell chart.

    Attributes:
        label (str): The category, unique within the chart; the label of its row (or column).
        start (Union[int, float]): The value of the start endpoint.
        end (Union[int, float]): The value of the end endpoint.
        emphasis (Optional[Union[EMPHASIS, str]]): The record's own emphasis role ("background" or "highlight"); wins over the chart's `emphasis_rule`.

    """

    label: str
    start: Union[int, float]
    end: Union[int, float]
    emphasis: Optional[Union[EMPHASIS, str]]


class DumbbellSingleChartAttrs(TypedDict):
    """The single chart attributes for the dumbbell chart.

    Attributes:
        data (List[DumbbellRecordAttrs]): The records defining one set of dumbbells.
        subtitle (Union[str, None]): The subtitle of the set.
        style (Union[DumbbellStyleAttrs, None]): The style of the set.
        xtickrotate (Union[int, None]): The xtick rotation value.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: List[DumbbellRecordAttrs]
    subtitle: Union[str, None]
    style: Union[DumbbellStyleAttrs, None]

    xtickrotate: Union[int, None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Contour Chart Attributes
# ================================================


class ContourDataAttrs(TypedDict):
    """The data attributes for the contour chart.

    Attributes:
        x (Union[List[Union[int, float]], None]): The x-axis values, one per column of `z`. Defaults to the column indices.
        y (Union[List[Union[int, float]], None]): The y-axis values, one per row of `z`. Defaults to the row indices.
        z (List[List[Union[int, float]]]): The 2-D grid of surface values, one row per `y` and one column per `x`.

    """

    x: Union[List[Union[int, float]], None]
    y: Union[List[Union[int, float]], None]
    z: List[List[Union[int, float]]]


class ContourSingleChartAttrs(TypedDict):
    """The single chart attributes for the contour chart.

    Attributes:
        data (ContourDataAttrs): The gridded surface defining the contour chart.
        subtitle (Union[str, None]): The subtitle of the contour chart. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the contour chart.
        ylabel (Union[str, None]): The ylabel of the contour chart.
        style (Union[ContourStyleAttrs, None]): The style of the contour chart.

        norm (Union[COLOR_NORM, str, None]): The value normalization of the filled bands.
        vmin (Union[float, None]): The minimum value to normalize the surface values.
        vmax (Union[float, None]): The maximum value to normalize the surface values.
        vcenter (Union[float, None]): The value a centred norm holds mid-colormap.
        value_format (Union[VALUE_FORMAT, str, None]): The format of the inline level labels.

        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.

        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        colorbar (Union[ColorbarSettingAttrs, None]): The colorbar setting of a filled contour.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: ContourDataAttrs
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[ContourStyleAttrs, None]

    norm: Union[str, None]
    vmin: Union[float, None]
    vmax: Union[float, None]
    vcenter: Union[float, None]
    value_format: Union[str, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    colorbar: Union[ColorbarSettingAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Hexbin Chart Attributes
# ================================================


class HexbinDataAttrs(TypedDict):
    """The data attributes for the hexbin chart.

    Attributes:
        x (List[Union[int, float]]): The x values of the points.
        y (List[Union[int, float]]): The y values of the points, one per `x`.
        c (Union[List[Union[int, float]], None]): The value of each point, one per `x`; when given, every hexagon shows their `reduce` aggregate instead of its point count.

    """

    x: List[Union[int, float]]
    y: List[Union[int, float]]
    c: Union[List[Union[int, float]], None]


class HexbinSingleChartAttrs(TypedDict):
    """The single chart attributes for the hexbin chart.

    Attributes:
        data (HexbinDataAttrs): The points binned by the hexbin chart.
        subtitle (Union[str, None]): The subtitle of the hexbin chart.
        xlabel (Union[str, None]): The xlabel of the hexbin chart.
        ylabel (Union[str, None]): The ylabel of the hexbin chart.
        style (Union[HexbinStyleAttrs, None]): The style of the hexbin chart.

        gridsize (Union[int, None]): The number of hexagons across the x-axis; `None` takes the `plot_hexbin_gridsize` config value.
        reduce (Union[HEXBIN_REDUCE, str, None]): The aggregation of the `c` values in a hexagon; `None` takes the mean. Ignored without `c`.
        mincnt (Union[int, None]): The point count below which a hexagon stays blank; `None` draws every hexagon.
        norm (Union[COLOR_NORM, str, None]): The value normalization of the hexagon colors.
        vmin (Union[float, None]): The minimum value to normalize the hexagon values.
        vmax (Union[float, None]): The maximum value to normalize the hexagon values.
        vcenter (Union[float, None]): The value a centred norm holds mid-colormap.
        value_format (Union[VALUE_FORMAT, str, None]): The format of the colorbar tick labels when the colorbar setting names none.

        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): the ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.

        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        colorbar (Union[ColorbarSettingAttrs, None]): The colorbar setting.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: HexbinDataAttrs
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[HexbinStyleAttrs, None]

    gridsize: Union[int, None]
    reduce: Union[HEXBIN_REDUCE, str, None]
    mincnt: Union[int, None]
    norm: Union[str, None]
    vmin: Union[float, None]
    vmax: Union[float, None]
    vcenter: Union[float, None]
    value_format: Union[str, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    colorbar: Union[ColorbarSettingAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Image Chart Attributes
# ================================================


class ImageDataAttrs(TypedDict):
    """The data attributes for the image chart.

    Attributes:
        image (Union[str, os.PathLike, PILImage, np.ndarray]): The picture: a path to an image file, a PIL image, an RGB(A) array of shape `(rows, columns, 3 or 4)`, or a 2-D array read through the `plot_image_cmap` colormap. The first row is the top edge.
        extent (Tuple[float, float, float, float]): The data-space rectangle the pixels stretch to fill, as `(xmin, xmax, ymin, ymax)`: four finite numbers, `xmin` different from `xmax` and `ymin` from `ymax`. A reversed pair flips the picture.

    """

    image: Union[str, os.PathLike, PILImage, np.ndarray]
    extent: Tuple[float, float, float, float]


# ================================================
# Basemap Chart Attributes
# ================================================


class BasemapDataAttrs(TypedDict):
    """The geometry attributes for the basemap chart.

    Attributes:
        lon (List[float]): The longitudes of the outlines, drawn on the x-axis. A `NaN` separates one outline from the next.
        lat (List[float]): The latitudes of the outlines, drawn on the y-axis; as long as `lon`, with its `NaN` at the same places.
        feature (Optional[Union[BASEMAP_FEATURE, str]]): How the outlines are drawn and styled: `"coastline"` (default) or `"borders"` as lines, `"land"` or `"lakes"` as filled areas; `"countries"` needs Natural Earth's country codes and is not accepted here. See [`BASEMAP_FEATURE`][datachart.constants.BASEMAP_FEATURE].

    """

    lon: List[float]
    lat: List[float]
    feature: Optional[Union[BASEMAP_FEATURE, str]]


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
        annotation (Optional[str]): The text drawn beside the point.
        emphasis (Optional[Union[EMPHASIS, str]]): The point's own emphasis role
            ("background" or "highlight"); wins over the chart's `emphasis` and
            `emphasis_rule`.
        xerr (Optional[Union[float, Tuple[float, float]]]): The x-axis error, as a
            distance from the point: one number reaches the same distance both
            ways, a `(low, high)` pair reaches `low` left and `high` right.
        yerr (Optional[Union[float, Tuple[float, float]]]): The y-axis error, as a
            distance from the point, read like `xerr`.

    """

    x: Union[int, float]
    y: Union[int, float]
    size: Optional[Union[int, float]]
    hue: Optional[str]
    annotation: Optional[str]
    emphasis: Optional[Union[EMPHASIS, str]]
    xerr: Optional[Union[float, Tuple[float, float]]]
    yerr: Optional[Union[float, Tuple[float, float]]]


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
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        x (Union[str, None]): The key name in `data` that contains the x-axis value. Defaults to `"x"`.
        y (Union[str, None]): The key name in `data` that contains the y-axis value. Defaults to `"y"`.
        size (Union[str, None]): The key name in `data` that contains the marker size value.
        hue (Union[str, None]): The key name in `data` that contains the hue/category value.
        annotation (Union[str, None]): The key name in `data` that contains the point annotation.
        xerr (Union[str, None]): The key name in `data` that contains the x-axis error. Defaults to `"xerr"`.
        yerr (Union[str, None]): The key name in `data` that contains the y-axis error. Defaults to `"yerr"`.

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

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    x: Union[str, None]
    y: Union[str, None]
    size: Union[str, None]
    hue: Union[str, None]
    annotation: Union[str, None]
    xerr: Union[str, None]
    yerr: Union[str, None]


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
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
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

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    value: Union[str, None]  # the name of the value attribute in data


# ================================================
# Swarm Plot Attributes
# ================================================


class SwarmDataPointAttrs(TypedDict):
    """The data point attributes for the swarm plot.

    Attributes:
        label (str): The category label.
        value (Union[int, float]): The numeric value.
        emphasis (Optional[Union[EMPHASIS, str]]): The point's own emphasis role
            ("background" or "highlight"); wins over its group's `emphasis` and
            the chart's `emphasis_rule`.

    """

    label: str
    value: Union[int, float]
    emphasis: Optional[Union[EMPHASIS, str]]


class SwarmSingleChartAttrs(TypedDict):
    """The single chart attributes for the swarm plot.

    Attributes:
        data (List[SwarmDataPointAttrs]): The list of data points defining the swarm plot.
        subtitle (Union[str, None]): The subtitle of the swarm plot. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the swarm plot.
        ylabel (Union[str, None]): The ylabel of the swarm plot.
        style (Union[SwarmStyleAttrs, None]): The style of the swarm plot.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): The ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        label (Union[str, None]): The key name in `data` that contains the label value. Defaults to `"label"`.
        value (Union[str, None]): The key name in `data` that contains the value. Defaults to `"value"`.

    """

    data: List[SwarmDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[SwarmStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    value: Union[str, None]  # the name of the value attribute in data


# Violin Plot Attributes
# ================================================


class ViolinDataPointAttrs(TypedDict):
    """The data point attributes for the violin plot.

    Attributes:
        label (str): The category label.
        value (Union[int, float]): The numeric value.

    """

    label: str
    value: Union[int, float]


class ViolinSingleChartAttrs(TypedDict):
    """The single chart attributes for the violin plot.

    Attributes:
        data (List[ViolinDataPointAttrs]): The list of data points defining the violin plot.
        subtitle (Union[str, None]): The subtitle of the violin plot. Also used as the label in the legend.
        xlabel (Union[str, None]): The xlabel of the violin plot.
        ylabel (Union[str, None]): The ylabel of the violin plot.
        style (Union[ViolinStyleAttrs, None]): The style of the violin plot.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): The ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        label (Union[str, None]): The key name in `data` that contains the label value. Defaults to `"label"`.
        value (Union[str, None]): The key name in `data` that contains the value. Defaults to `"value"`.

    """

    data: List[ViolinDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[ViolinStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    value: Union[str, None]  # the name of the value attribute in data


# ================================================
# Ridgeline Plot Attributes
# ================================================


class RidgelineDataPointAttrs(TypedDict):
    """The data point attributes for the ridgeline plot.

    Attributes:
        label (str): The category label; one ridge per label.
        value (Union[int, float]): The numeric value.

    """

    label: str
    value: Union[int, float]


class RidgelineSingleChartAttrs(TypedDict):
    """The single chart attributes for the ridgeline plot.

    Attributes:
        data (List[RidgelineDataPointAttrs]): The list of data points defining the ridgeline plot.
        subtitle (Union[str, None]): The subtitle of the ridgeline plot.
        xlabel (Union[str, None]): The xlabel of the ridgeline plot.
        ylabel (Union[str, None]): The ylabel of the ridgeline plot.
        style (Union[RidgelineStyleAttrs, None]): The style of the ridgeline plot.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): The ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        label (Union[str, None]): The key name in `data` that contains the label value. Defaults to `"label"`.
        value (Union[str, None]): The key name in `data` that contains the value. Defaults to `"value"`.

    """

    data: List[RidgelineDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[RidgelineStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    value: Union[str, None]  # the name of the value attribute in data


# ================================================
# Raincloud Plot Attributes
# ================================================


class RaincloudDataPointAttrs(TypedDict):
    """The data point attributes for the raincloud plot.

    Attributes:
        label (str): The category label.
        value (Union[int, float]): The numeric value.

    """

    label: str
    value: Union[int, float]


class RaincloudSingleChartAttrs(TypedDict):
    """The single chart attributes for the raincloud plot.

    Attributes:
        data (List[RaincloudDataPointAttrs]): The list of data points defining the raincloud plot.
        subtitle (Union[str, None]): The subtitle of the raincloud plot.
        xlabel (Union[str, None]): The xlabel of the raincloud plot.
        ylabel (Union[str, None]): The ylabel of the raincloud plot.
        style (Union[RaincloudStyleAttrs, None]): The style of the raincloud plot.
        xticks (Union[int, float, None]): The xtick positions list.
        xticklabels (Union[List[str], None]): The xtick labels.
        xtickrotate (Union[int, None]): The xtick rotation value.
        yticks (Union[int, float, None]): The ytick position list.
        yticklabels (Union[List[str], None]): The ytick labels.
        ytickrotate (Union[int, None]): The ytick rotation value.
        vlines (Union[VLineSettingAttrs, List[VLineSettingAttrs], None]): The vertical lines to be plot.
        hlines (Union[HLineSettingAttrs, List[HLineSettingAttrs], None]): The horizontal lines to be plot.
        dlines (Union[DLineSettingAttrs, List[DLineSettingAttrs], None]): The diagonal lines to be plot.
        brackets (Union[BracketSettingAttrs, List[BracketSettingAttrs], None]): The pairwise comparison brackets to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The vertical reference bands to be plot.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The horizontal reference bands to be plot.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        label (Union[str, None]): The key name in `data` that contains the label value. Defaults to `"label"`.
        value (Union[str, None]): The key name in `data` that contains the value. Defaults to `"value"`.

    """

    data: List[RaincloudDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[RaincloudStyleAttrs, None]

    xticks: Union[int, float, None]
    xticklabels: Union[List[str], None]
    xtickrotate: Union[int, None]
    yticks: Union[int, float, None]
    yticklabels: Union[List[str], None]
    ytickrotate: Union[int, None]

    vlines: Union[VLineSettingAttrs, List[VLineSettingAttrs]]
    hlines: Union[HLineSettingAttrs, List[HLineSettingAttrs]]
    dlines: Union[DLineSettingAttrs, List[DLineSettingAttrs]]
    brackets: Union[BracketSettingAttrs, List[BracketSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]

    label: Union[str, None]  # the name of the label attribute in data
    value: Union[str, None]  # the name of the value attribute in data


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
        xlabel (Union[str, None]): The xlabel of the chart.
        ylabel (Union[str, None]): The ylabel of the chart.
        style (Union[ParallelCoordsStyleAttrs, None]): The style of the chart.
        dimensions (Union[List[str], None]): The dimensions to include and their order.
        hue (Union[str, None]): The key name in `data` for categorical coloring.
        category_orders (Union[Dict[str, List[str]], None]): Custom order for categorical dimensions.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.

    """

    data: List[ParallelCoordsDataPointAttrs]
    subtitle: Union[str, None]
    xlabel: Union[str, None]
    ylabel: Union[str, None]
    style: Union[ParallelCoordsStyleAttrs, None]
    dimensions: Union[List[str], None]
    hue: Union[str, None]
    category_orders: Union[Dict[str, List[str]], None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]


# ================================================
# Scatter Matrix Attributes
# ================================================


class ScatterMatrixDataPointAttrs(TypedDict):
    """The record attributes for the scatter matrix.

    A dictionary where keys are column names: numeric columns become
    dimensions, and one categorical column may be named as the `hue`. The
    same columns can be passed as one dictionary of lists instead.

    Attributes:
        hue (Optional[str]): The category for color grouping, under the
            column name the `hue` setting names.

    """

    hue: Optional[str]


# ================================================
# Radial Chart Attributes
# ================================================


class RadialDataPointAttrs(TypedDict):
    """The data point attributes for the radial chart.

    The line, bar, and scatter visuals take `label`/`y` points whose labels
    are placed evenly around the circle; the histogram visual takes numeric
    `x` observations in degrees.

    Attributes:
        label (str): The category label (line, bar, and scatter visuals).
        y (Union[int, float]): The radial value (line, bar, and scatter visuals).
        yerr (Optional[Union[int, float]]): The radial error value.
        x (Optional[Union[int, float]]): The angular observation in degrees (histogram visual).
        emphasis (Optional[Union[EMPHASIS, str]]): The bar's own emphasis role
            ("background" or "highlight"); wins over the chart's `emphasis_rule`
            (bar visual).

    """

    label: str
    y: Union[int, float]
    yerr: Optional[Union[int, float]]
    x: Optional[Union[int, float]]


class RadialSingleChartAttrs(TypedDict):
    """The single chart attributes for the radial chart.

    Attributes:
        data (List[RadialDataPointAttrs]): The list of data points defining the radial chart.
        subtitle (Union[str, None]): The subtitle of the radial chart. Also used as the label in the legend.
        style (Union[LineStyleAttrs, BarStyleAttrs, HistStyleAttrs, ScatterStyleAttrs, None]): The style of the radial chart, matching its visual.
        texts (Union[TextSettingAttrs, List[TextSettingAttrs], None]): The text annotations to be drawn.
        vspans (Union[VSpanSettingAttrs, List[VSpanSettingAttrs], None]): The angular wedges to be plot, bounded in degrees.
        hspans (Union[HSpanSettingAttrs, List[HSpanSettingAttrs], None]): The annuli to be plot, bounded in radius.
        label (Union[str, None]): The key name in `data` that contains the category label. Defaults to `"label"`.
        x (Union[str, None]): The key name in `data` that contains the angular observation. Defaults to `"x"`.
        y (Union[str, None]): The key name in `data` that contains the radial value. Defaults to `"y"`.
        yerr (Union[str, None]): The key name in `data` that contains the radial error value. Defaults to `"yerr"`.

    """

    data: List[RadialDataPointAttrs]
    subtitle: Union[str, None]
    style: Union[LineStyleAttrs, BarStyleAttrs, HistStyleAttrs, ScatterStyleAttrs, None]
    texts: Union[TextSettingAttrs, List[TextSettingAttrs]]
    vspans: Union[VSpanSettingAttrs, List[VSpanSettingAttrs]]
    hspans: Union[HSpanSettingAttrs, List[HSpanSettingAttrs]]

    label: Union[str, None]
    x: Union[str, None]
    y: Union[str, None]
    yerr: Union[str, None]


# ================================================
# Deprecated Names
# ================================================

# old name -> new name; removed one release after it ships (ADR 0043)
# None: no public replacement; the type is kept privately as `_<old name>`
_DEPRECATED_ALIASES = {}


def __getattr__(name):
    if name in _DEPRECATED_ALIASES:
        new_name = _DEPRECATED_ALIASES[name]
        hint = f"use `{new_name}` instead" if new_name else "it has no replacement"
        warnings.warn(
            f"`{name}` is deprecated and will be removed in the next release; "
            f"{hint}.",
            DeprecationWarning,
            stacklevel=2,
        )
        return globals()[new_name or f"_{name}"]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
