import math
import warnings
from typing import Union, Tuple, Dict, List

import matplotlib.pyplot as plt

from ..config import config, Config
from ..config.charts import CHART_CONFIGS


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
        assert n_charts > 0, "The number of charts must be greater than 0."
        assert max_cols > 0, "The maximum number of columns must be greater than 0."
        # there are more subplots
        nrows = math.ceil(n_charts / max_cols)
        ncols = max_cols if n_charts >= max_cols else n_charts % max_cols

    return {"nrows": nrows, "ncols": ncols}


# -------------------------------------
# Text Style
# -------------------------------------


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

    return {
        key: config.get(
            attr.format(type=text_type),
            config.get(attr.format(type="general")),
        )
        for key, attr in config_attrs
    }


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
        ("colors", "plot_hline_color"),
        ("linestyle", "plot_hline_style"),
        ("linewidth", "plot_hline_width"),
        ("alpha", "plot_hline_alpha"),
    ]

    return create_config_dict(hline_style, config_attrs)


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
        ("title_fontsize", "plot_legend_title_size"),
        ("labelcolor", "plot_legend_label_color"),
    ]
    return create_config_dict({}, config_attrs)


# ================================================
# Chart Configurations
# ================================================


def configure_axes_spines(ax: plt.Axes):
    """Configure axes spines.

    Args:
        ax: The axes.

    """

    # Turn on the axes
    ax.axis("on")

    # Loop through each axis and configure spines
    for axis in ["top", "bottom", "left", "right"]:
        # Set the linewidth and visibility of the spine
        ax.spines[axis].set(
            linewidth=config["axes_spines_width"],
            visible=config[f"axes_spines_{axis}_visible"],
            zorder=config["axes_spines_zorder"],
        )


def configure_axis_ticks_style(ax: plt.Axes, axis_type: str):
    """Configure axis ticks.

    Args:
        ax: The axes.
        axis_type: The axis type. Options: "xaxis", "yaxis".

    """

    # Set tick parameters for major ticks
    getattr(ax, axis_type).set_tick_params(
        which="major",
        width=config["axes_spines_width"],
        length=config["axes_ticks_length"],
        labelsize=config["axes_ticks_label_size"],
    )


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
