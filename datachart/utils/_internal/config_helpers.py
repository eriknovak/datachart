import math
import warnings
from functools import lru_cache
from typing import Union, Tuple, Dict, List

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt

from ...config import config, Config
from ...config.charts import CHART_CONFIGS
from ...constants import ARROW_STYLE

# ================================================
# Helper Functions
# ================================================


def get_attr_value(
    attr: str, obj: dict, default: Union[Config, dict, bool, int, float, str, None]
):
    """Retrieves the value of the specified attribute from the given object.

    Args:
        attr: The name of the attribute.
        obj: The object.
        default: The default value to return if the attribute is not found.

    Returns:
        The value of the attribute, or the default value if the attribute is not found.

    """
    if isinstance(default, Config) or isinstance(default, dict):
        return obj.get(attr, default[attr])
    return obj.get(attr, default)


def create_config_dict(
    styles: Dict[str, str], attrs: List[Tuple[str, str]]
) -> Dict[str, str]:
    """Create a configuration dictionary based on the given styles and attributes.

    Args:
        styles: A dictionary containing the styles.
        attrs: A list of tuples representing the attributes.

    Returns:
        The configuration dictionary.

    """

    # Create a dictionary comprehension that maps each key to the attribute value
    return {
        key: get_attr_value(attr, styles, config)
        for key, attr in attrs
        if get_attr_value(attr, styles, config) is not None
    }


# ================================================
# Configuration Constructors
# ================================================


# -------------------------------------
# Subplot Configuration
# -------------------------------------


def get_subplot_config(
    chart_type: str, subplots: bool, n_charts: int = 1, max_cols: int = 1
) -> Dict[str, int]:
    """Calculate the configuration for subplots in a figure.

    Args:
        subplots: Whether to show subplots.
        n_charts: The number of charts.
        max_cols: The maximum number of columns.

    Returns:
        The configuration for subplots, including the number of rows (nrows) and
        the number of columns (ncols).
    """

    nrows = 1
    ncols = 1

    chart_config = CHART_CONFIGS[chart_type]
    if subplots and not chart_config["subplots"]:
        warnings.warn(
            f"Chart type '{chart_type}' does not support subplots. Setting subplots to False..."
        )
        subplots = False

    if subplots or not chart_config["multiplot"]:
        if not isinstance(n_charts, int):
            raise TypeError("The number of charts is not an integer.")
        if n_charts <= 0:
            raise ValueError("The number of charts must be greater than 0.")
        if not isinstance(max_cols, int):
            raise TypeError("The maximum number of columns is not an integer.")
        if max_cols <= 0:
            raise ValueError("The maximum number of columns must be greater than 0.")
        # there are more subplots
        nrows = math.ceil(n_charts / max_cols)
        ncols = max_cols if n_charts >= max_cols else n_charts % max_cols

    return {"nrows": nrows, "ncols": ncols}


# -------------------------------------
# Text Style
# -------------------------------------


@lru_cache(maxsize=None)
def _font_available(name: str) -> bool:
    """Whether the font is installed; missing names would make matplotlib warn."""

    try:
        font_manager.findfont(
            font_manager.FontProperties(family=name), fallback_to_default=False
        )
        return True
    except ValueError:
        return False


def resolve_font_family(family: Union[str, None] = None) -> Union[str, List[str]]:
    """Resolve a generic font family into the theme's concrete font stack.

    Args:
        family: The font family; falls back to `font_general_family`.

    Returns:
        The theme's font stack (ending in the generic family as a fallback),
        or the family itself when the theme defines no stack for it.

    """

    family = family if family is not None else config.get("font_general_family")
    family = family or "sans-serif"
    if family == "serif":
        stack = config.get("font_general_serif")
    elif family == "sans-serif":
        stack = config.get("font_general_sansserif")
    else:
        stack = None
    if stack:
        # drop fonts not installed here; they would only trigger findfont warnings
        stack = [name for name in stack if _font_available(name)]
    return list(stack) + [family] if stack else family


def get_text_style(text_type: str = "") -> dict:
    """Get the text style.

    Args:
        text_type: The text type.

    Returns:
        The text style setting.

    """

    config_attrs = [
        ("fontsize", "font_{type}_size"),
        ("fontweight", "font_{type}_weight"),
        ("color", "font_{type}_color"),
        ("style", "font_{type}_style"),
        ("family", "font_{type}_family"),
    ]

    style = {
        key: config.get(
            attr.format(type=text_type),
            config.get(attr.format(type="general")),
        )
        for key, attr in config_attrs
    }
    style["family"] = resolve_font_family(style.get("family"))
    return style


# -------------------------------------
# Line Style
# -------------------------------------


def get_line_style(chart_style: dict) -> dict:
    """Get the line chart style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The line style setting.

    """

    config_attrs = [
        ("color", "plot_line_color"),
        ("alpha", "plot_line_alpha"),
        ("linewidth", "plot_line_width"),
        ("linestyle", "plot_line_style"),
        ("marker", "plot_line_marker"),
        ("drawstyle", "plot_line_drawstyle"),
        ("zorder", "plot_line_zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Bar Style
# -------------------------------------


def get_bar_style(chart_style: dict, is_horizontal: bool = False) -> dict:
    """Get the bar chart style.

    Args:
        chart_style: The chart style dictionary.
        is_horizontal: Whether the bar is horizontal or not.

    Returns:
        The bar style setting.

    """

    config_attrs = [
        ("color", "plot_bar_color"),
        ("alpha", "plot_bar_alpha"),
        ("height" if is_horizontal else "width", "plot_bar_width"),
        ("hatch", "plot_bar_hatch"),
        ("linewidth", "plot_bar_edge_width"),
        ("edgecolor", "plot_bar_edge_color"),
        ("ecolor", "plot_bar_error_color"),
        ("zorder", "plot_bar_zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Hist Style
# -------------------------------------


def get_hist_style(chart_style: dict) -> dict:
    """Get the histogram chart style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The histogram style setting.

    """

    config_attrs = [
        ("color", "plot_hist_color"),
        ("alpha", "plot_hist_alpha"),
        ("fill", "plot_hist_fill"),
        ("hatch", "plot_hist_hatch"),
        ("zorder", "plot_hist_zorder"),
        ("histtype", "plot_hist_type"),
        ("align", "plot_hist_align"),
        ("linewidth", "plot_hist_edge_width"),
        ("edgecolor", "plot_hist_edge_color"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Area Style
# -------------------------------------


def get_area_style(chart_style: dict) -> dict:
    """Get the area chart style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The area style setting.

    """

    config_attrs = [
        ("alpha", "plot_area_alpha"),
        ("color", "plot_area_color"),
        ("linewidth", "plot_area_linewidth"),
        ("hatch", "plot_area_hatch"),
        ("zorder", "plot_area_zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Grid Style
# -------------------------------------


def get_grid_style(chart_style: dict) -> dict:
    """Get the grid chart style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The grid style setting.

    """

    config_attrs = [
        ("alpha", "plot_grid_alpha"),
        ("color", "plot_grid_color"),
        ("linewidth", "plot_grid_linewidth"),
        ("linestyle", "plot_grid_linestyle"),
        ("zorder", "plot_grid_zorder"),
    ]
    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Vertical Line Style
# -------------------------------------


def get_vline_style(vline_style: dict) -> dict:
    """Get the vertical line chart style.

    Args:
        vline_style: The vertical line style dictionary.

    Returns:
        The vertical line style setting.

    """

    config_attrs = [
        ("color", "plot_vline_color"),
        ("linestyle", "plot_vline_style"),
        ("linewidth", "plot_vline_width"),
        ("alpha", "plot_vline_alpha"),
    ]

    return create_config_dict(vline_style, config_attrs)


# -------------------------------------
# Horizontal Line Style
# -------------------------------------


def get_hline_style(hline_style: dict) -> dict:
    """Get the horizontal line chart style.

    Args:
        hline_style: The horizontal line style dictionary.

    Returns:
        The horizontal line style setting.

    """

    config_attrs = [
        ("color", "plot_hline_color"),
        ("linestyle", "plot_hline_style"),
        ("linewidth", "plot_hline_width"),
        ("alpha", "plot_hline_alpha"),
    ]

    return create_config_dict(hline_style, config_attrs)


# -------------------------------------
# Text Annotation Style
# -------------------------------------


# each connector look expands to (arrow style, curvature, text-side gap in points)
TEXT_ARROW_TEXT_GAP = 6.0
ARROW_STYLE_PRESETS = {
    ARROW_STYLE.CURVE: ("-", 0.2, TEXT_ARROW_TEXT_GAP),
    ARROW_STYLE.CURVE_ARROW: ("->", 0.2, TEXT_ARROW_TEXT_GAP),
    ARROW_STYLE.TOUCHING: ("-", 0.0, 0.0),
    ARROW_STYLE.ARROW: ("->", 0.0, TEXT_ARROW_TEXT_GAP),
}
# the connector always stops short of the target point (points)
TEXT_ARROW_TARGET_GAP = 5.0


def get_plot_text_style(text_style: dict) -> dict:
    """Get the text annotation font style.

    Args:
        text_style: The text style dictionary.

    Returns:
        The text font style setting, as `ax.annotate` keyword arguments.

    """

    config_attrs = [
        ("fontsize", "plot_text_size"),
        ("fontweight", "plot_text_weight"),
        ("color", "plot_text_color"),
        ("ha", "plot_text_halign"),
        ("va", "plot_text_valign"),
        ("alpha", "plot_text_alpha"),
    ]

    style = create_config_dict(text_style, config_attrs)
    if "color" not in style:
        style["color"] = config.get("font_general_color")
    style["family"] = resolve_font_family()
    return style


def get_plot_text_box_style(text_style: dict) -> Union[dict, None]:
    """Get the text annotation background box style.

    Args:
        text_style: The text style dictionary.

    Returns:
        The box style setting for the annotation `bbox`, or `None` when the
        box is hidden.

    """

    visible = get_attr_value("plot_text_box_visible", text_style, config)
    if not visible:
        return None

    config_attrs = [
        ("boxstyle", "plot_text_box_style"),
        ("facecolor", "plot_text_box_facecolor"),
        ("edgecolor", "plot_text_box_edgecolor"),
        ("linewidth", "plot_text_box_edge_width"),
        ("alpha", "plot_text_box_alpha"),
    ]

    return create_config_dict(text_style, config_attrs)


def get_plot_text_arrow_style(text_style: dict) -> dict:
    """Get the text annotation connector style.

    The `plot_text_arrow_style` look (see `ARROW_STYLE`) expands to the arrow
    style, curvature, and text-side gap; individual `plot_text_arrow_*` keys
    override single properties. A raw matplotlib arrow style passes through.

    The curvature is returned as `curve` with a `curve_pinned` flag rather
    than a finished `connectionstyle`: for a curved look left on its default,
    the panel picks the bow side and depth against the data at draw time,
    while an explicit `plot_text_arrow_curve` pins the bow exactly.

    Args:
        text_style: The text style dictionary.

    Returns:
        The connector style setting; `curve`/`curve_pinned` plus annotation
        `arrowprops` entries.

    """

    look = get_attr_value("plot_text_arrow_style", text_style, config)
    arrowstyle, curve, text_gap = ARROW_STYLE_PRESETS.get(
        look, (look, 0.0, TEXT_ARROW_TEXT_GAP)
    )
    curve_override = get_attr_value("plot_text_arrow_curve", text_style, config)
    pinned = curve_override is not None
    if pinned:
        curve = curve_override

    return {
        "arrowstyle": arrowstyle,
        "curve": curve,
        "curve_pinned": pinned,
        "color": get_attr_value("plot_text_arrow_color", text_style, config),
        "linewidth": get_attr_value("plot_text_arrow_width", text_style, config),
        "shrinkA": text_gap,
        "shrinkB": TEXT_ARROW_TARGET_GAP,
    }


# -------------------------------------
# Heatmap Style
# -------------------------------------


def get_heatmap_style(heatmap_style: dict) -> dict:
    """Get the heatmap style.

    Args:
        heatmap_style: The heatmap style dictionary.

    Returns:
        The heatmap style setting.

    """

    config_attrs = [
        ("cmap", "plot_heatmap_cmap"),
        ("alpha", "plot_heatmap_alpha"),
    ]

    return create_config_dict(heatmap_style, config_attrs)


def get_heatmap_font_style(heatmap_style: dict) -> dict:
    """Get the heatmap font style.

    Args:
        heatmap_style: The heatmap font style dictionary.

    Returns:
        The heatmap font style setting.

    """

    config_attrs = [
        ("size", "plot_heatmap_font_size"),
        ("color", "plot_heatmap_font_color"),
        ("style", "plot_heatmap_font_style"),
        ("weight", "plot_heatmap_font_weight"),
    ]

    return create_config_dict(heatmap_style, config_attrs)


def get_heatmap_edge_style(heatmap_style: dict) -> dict:
    """Get the style of the borders drawn between heatmap cells.

    Args:
        heatmap_style: The heatmap style dictionary.

    Returns:
        The cell border style setting.

    """

    config_attrs = [
        ("linewidth", "plot_heatmap_edge_width"),
        ("color", "plot_heatmap_edge_color"),
    ]

    return create_config_dict(heatmap_style, config_attrs)


# -------------------------------------
# Contour Style
# -------------------------------------

# inline level labels sit this much below the general font size
CONTOUR_LABEL_SIZE_STEP = 2


def get_contour_style(chart_style: dict) -> dict:
    """Get the contour chart style.

    The `cmap` falls back to the heatmap colormap and the `linewidths` to the
    line chart width when the contour keys leave them unset.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The contour style setting.

    """

    config_attrs = [
        ("color", "plot_contour_color"),
        ("cmap", "plot_contour_cmap"),
        ("linewidths", "plot_contour_line_width"),
        ("linestyles", "plot_contour_line_style"),
        ("alpha", "plot_contour_alpha"),
        ("zorder", "plot_contour_zorder"),
    ]

    style = create_config_dict(chart_style, config_attrs)
    style.setdefault("cmap", get_attr_value("plot_heatmap_cmap", chart_style, config))
    style.setdefault(
        "linewidths", get_attr_value("plot_line_width", chart_style, config)
    )
    return style


def get_contour_label_style(chart_style: dict) -> dict:
    """Get the style of the inline contour level labels.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The label style setting; `colors` is absent when the labels follow
        the line color.

    """

    config_attrs = [
        ("fontsize", "plot_contour_label_font_size"),
        ("colors", "plot_contour_label_font_color"),
    ]

    style = create_config_dict(chart_style, config_attrs)
    style.setdefault(
        "fontsize", config["font_general_size"] - CONTOUR_LABEL_SIZE_STEP
    )
    return style


# -------------------------------------
# Scatter Style
# -------------------------------------


def get_scatter_style(chart_style: dict) -> dict:
    """Get the scatter chart style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The scatter style setting.

    """

    config_attrs = [
        ("c", "plot_scatter_color"),
        ("alpha", "plot_scatter_alpha"),
        ("s", "plot_scatter_size"),
        ("marker", "plot_scatter_marker"),
        ("zorder", "plot_scatter_zorder"),
        ("linewidths", "plot_scatter_edge_width"),
        ("edgecolors", "plot_scatter_edge_color"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_swarm_style(chart_style: dict) -> dict:
    """Get the swarm plot style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The swarm style setting.

    """

    config_attrs = [
        ("c", "plot_swarm_color"),
        ("alpha", "plot_swarm_alpha"),
        ("s", "plot_swarm_size"),
        ("marker", "plot_swarm_marker"),
        ("zorder", "plot_swarm_zorder"),
        ("linewidths", "plot_swarm_edge_width"),
        ("edgecolors", "plot_swarm_edge_color"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Regression Style
# -------------------------------------


def get_regression_style(chart_style: dict) -> dict:
    """Get the regression line style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The regression line style setting.

    """

    config_attrs = [
        ("color", "plot_regression_color"),
        ("alpha", "plot_regression_alpha"),
        ("linewidth", "plot_regression_width"),
        ("linestyle", "plot_regression_style"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Box Plot Style
# -------------------------------------


def get_box_style(chart_style: dict) -> dict:
    """Get the box plot style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The box plot style setting.

    """

    config_attrs = [
        ("facecolor", "plot_box_color"),
        ("alpha", "plot_box_alpha"),
        ("linewidth", "plot_box_linewidth"),
        ("edgecolor", "plot_box_edgecolor"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_box_outlier_style(chart_style: dict) -> dict:
    """Get the box plot outlier style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The outlier style setting.

    """

    config_attrs = [
        ("marker", "plot_box_outlier_marker"),
        ("markersize", "plot_box_outlier_size"),
        ("markerfacecolor", "plot_box_outlier_color"),
        ("markeredgecolor", "plot_box_outlier_edge_color"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_box_median_style(chart_style: dict) -> dict:
    """Get the box plot median line style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The median line style setting.

    """

    config_attrs = [
        ("color", "plot_box_median_color"),
        ("linewidth", "plot_box_median_linewidth"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_box_whisker_style(chart_style: dict) -> dict:
    """Get the box plot whisker style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The whisker style setting.

    """

    config_attrs = [
        ("color", "plot_box_whisker_color"),
        ("linewidth", "plot_box_whisker_linewidth"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_box_cap_style(chart_style: dict) -> dict:
    """Get the box plot cap style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The cap style setting.

    """

    config_attrs = [
        ("color", "plot_box_cap_color"),
        ("linewidth", "plot_box_cap_linewidth"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Violin Plot Style
# -------------------------------------


def get_violin_style(chart_style: dict) -> dict:
    """Get the violin body style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The violin body style setting.

    """

    config_attrs = [
        ("facecolor", "plot_violin_color"),
        ("alpha", "plot_violin_alpha"),
        ("linewidth", "plot_violin_linewidth"),
        ("edgecolor", "plot_violin_edgecolor"),
        ("width", "plot_violin_width"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_violin_inner_style(chart_style: dict) -> dict:
    """Get the violin inner marks style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The inner marks style setting; `color` falls back to the font color.

    """

    config_attrs = [
        ("color", "plot_violin_inner_color"),
        ("linewidth", "plot_violin_inner_linewidth"),
        ("median_color", "plot_violin_median_color"),
        ("median_size", "plot_violin_median_size"),
    ]

    style = create_config_dict(chart_style, config_attrs)
    if style.get("color") is None:
        style["color"] = get_attr_value("font_general_color", chart_style, config)
    return style


# -------------------------------------
# Parallel Coordinates Style
# -------------------------------------


def get_parallel_coords_style(chart_style: dict) -> dict:
    """Get the parallel coordinates chart style for data lines.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The parallel coordinates style setting.

    """

    config_attrs = [
        ("color", "plot_parallel_color"),
        ("alpha", "plot_parallel_alpha"),
        ("linewidth", "plot_parallel_width"),
        ("linestyle", "plot_parallel_style"),
        ("marker", "plot_parallel_marker"),
        ("zorder", "plot_parallel_zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_parallel_axis_style(chart_style: dict) -> dict:
    """Get the parallel coordinates vertical axis line style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The vertical axis line style setting.

    """

    config_attrs = [
        ("color", "plot_parallel_axis_color"),
        ("linewidth", "plot_parallel_axis_width"),
        ("zorder", "plot_parallel_axis_zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_parallel_tick_style(chart_style: dict) -> dict:
    """Get the parallel coordinates tick mark style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The tick mark style setting.

    """

    config_attrs = [
        ("color", "plot_parallel_tick_color"),
        ("linewidth", "plot_parallel_tick_width"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_parallel_tick_length(chart_style: dict) -> float:
    """Get the parallel coordinates tick mark length.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The tick mark length.

    """

    return chart_style.get(
        "plot_parallel_tick_length", config["plot_parallel_tick_length"]
    )


def get_parallel_tick_label_style(chart_style: dict) -> dict:
    """Get the parallel coordinates tick label style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The tick label style setting.

    """

    config_attrs = [
        ("fontsize", "plot_parallel_tick_label_size"),
        ("color", "plot_parallel_tick_label_color"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_parallel_tick_label_bbox(chart_style: dict) -> dict:
    """Get the parallel coordinates tick label background box style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The tick label background box style setting.

    """

    bg_color = chart_style.get(
        "plot_parallel_tick_label_bg_color", config["plot_parallel_tick_label_bg_color"]
    )
    bg_alpha = chart_style.get(
        "plot_parallel_tick_label_bg_alpha", config["plot_parallel_tick_label_bg_alpha"]
    )

    return dict(
        boxstyle="round,pad=0.15",
        facecolor=bg_color,
        alpha=bg_alpha,
        edgecolor="none",
    )


def get_parallel_dim_label_style(chart_style: dict) -> dict:
    """Get the parallel coordinates dimension label style.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The dimension label style setting.

    """

    config_attrs = [
        ("fontsize", "plot_parallel_dim_label_size"),
        ("color", "plot_parallel_dim_label_color"),
    ]

    return create_config_dict(chart_style, config_attrs)


def get_parallel_dim_label_rotation(chart_style: dict) -> float:
    """Get the parallel coordinates dimension label rotation.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The dimension label rotation.

    """

    return chart_style.get(
        "plot_parallel_dim_label_rotation", config["plot_parallel_dim_label_rotation"]
    )


def get_parallel_dim_label_pad(chart_style: dict) -> float:
    """Get the parallel coordinates dimension label padding.

    Args:
        chart_style: The chart style dictionary.

    Returns:
        The dimension label padding.

    """

    return chart_style.get(
        "plot_parallel_dim_label_pad", config["plot_parallel_dim_label_pad"]
    )


# -------------------------------------
# Legend Style
# -------------------------------------


def get_legend_style() -> dict:
    """Get the legend style.

    Returns:
        The legend style setting.

    """

    config_attrs = [
        ("shadow", "plot_legend_shadow"),
        ("frameon", "plot_legend_frameon"),
        ("fontsize", "plot_legend_font_size"),
        ("alignment", "plot_legend_alignment"),
        ("loc", "plot_legend_location"),
        ("title_fontsize", "plot_legend_title_size"),
        ("labelcolor", "plot_legend_label_color"),
    ]
    return create_config_dict({}, config_attrs)


# ================================================
# Chart Configurations
# ================================================


def configure_axis_ticks_position(ax: plt.Axes, chart: dict):
    """Configure axis ticks position.

    Args:
        ax: The axes.
        chart: The chart style.

    """

    tick_attrs = [
        ("xticks", "xticklabels", "xtickrotate", "xaxis"),
        ("yticks", "yticklabels", "ytickrotate", "yaxis"),
    ]
    for attrs in tick_attrs:
        ticks = chart.get(attrs[0], None)
        labels = chart.get(attrs[1], None)
        rotation = chart.get(attrs[2], 0)

        if attrs[3] == "xaxis":
            ha = "center" if rotation == 0 else "right"
            va = "top" if rotation == 0 else "center"
        if attrs[3] == "yaxis":
            ha = "right"
            va = "center"

        set_ticks = getattr(ax, attrs[3]).set_ticks

        if ticks is None and labels is None:
            continue
        if ticks is None and labels is not None:
            warnings.warn(
                f"Please provide the `{attrs[0]}` values. Ignoring `{attrs[1]}` values..."
            )
            continue
        elif ticks is not None and labels is None:
            set_ticks(
                ticks,
                labels=ticks,
                rotation=rotation,
                rotation_mode="anchor",
                ha=ha,
                va=va,
            )
        elif ticks is not None and labels is not None:
            if len(ticks) != len(labels):
                warnings.warn(
                    f"The values of `{attrs[0]}` and `{attrs[1]}` are of different lengths. "
                    + f"Please provide the same number of values. Ignoring `{attrs[1]}` values..."
                )
                # draw only the ticks
                set_ticks(
                    ticks,
                    labels=ticks,
                    rotation=rotation,
                    rotation_mode="anchor",
                    ha=ha,
                    va=va,
                )
            else:
                # draw both the ticks and the labels
                set_ticks(
                    ticks,
                    labels=labels,
                    rotation=rotation,
                    rotation_mode="anchor",
                    ha=ha,
                    va=va,
                )


def configure_axis_limits(ax: plt.Axes, settings: dict):
    """Configure axis limits.

    Args:
        ax: The axes.
        settings: The settings.

    """

    if settings["xmin"] is not None or settings["xmax"] is not None:
        xmin, xmax = ax.get_xlim()
        xmin = settings["xmin"] if settings["xmin"] is not None else xmin
        xmax = settings["xmax"] if settings["xmax"] is not None else xmax
        ax.set_xlim(xmin=xmin, xmax=xmax)

    if settings["ymin"] is not None or settings["ymax"] is not None:
        ymin, ymax = ax.get_ylim()
        ymin = settings["ymin"] if settings["ymin"] is not None else ymin
        ymax = settings["ymax"] if settings["ymax"] is not None else ymax
        ax.set_ylim(ymin=ymin, ymax=ymax)


def configure_labels(settings: dict, actions: List[Tuple[str, callable]]):
    """Configure chart labels.

    Args:
        settings: The chart settings.
        actions: The actions.

    """

    for label, action in actions:
        if label in settings:
            action(settings[label], **get_text_style(label))
