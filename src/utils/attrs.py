import math
from typing import Union, Tuple, Dict, List

from config import config, Config


# ================================================
# Helper Functions
# ================================================


def get_attr_value(
    attr: str, obj: dict, default: Union[Config, dict, bool, int, float, str, None]
):
    """Retrieves the value of the specified attribute from the given object.

    Args:
        attr (str): The name of the attribute.
        obj (dict): The object.
        default (Union[Config, bool, int, float, str, None]): The default value to return if the attribute is not found.
    Returns:
        The value of the attribute, or the default value if the attribute is not found.

    """
    if isinstance(default, Config) or isinstance(default, dict):
        return obj.get(attr, default[attr])
    return obj.get(attr, default)


def create_config_dict(
    styles: Dict[str, str], attrs: List[Tuple[str, str]]
) -> Dict[str, str]:
    """
    Create a configuration dictionary based on the given styles and attributes.

    Args:
        styles (dict): A dictionary containing the styles.
        attrs (list): A list of tuples representing the attributes.

    Returns:
        dict: The configuration dictionary.

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
    as_subplots: bool, n_charts: int, max_cols: int
) -> dict[str, int]:
    """
    Calculate the configuration for subplots in a figure.
    Args:
        as_subplots (bool): Whether to show subplots separately.
        n_charts (int): The number of subplots.
        max_cols (int): The maximum number of columns for the subplots.
    Returns:
        dict[str, int]: A dictionary containing the configuration for subplots,
            including the number of rows (nrows) and the number of columns (ncols).
    """

    nrows = 1
    ncols = 1

    if as_subplots:
        # there are more subplots
        nrows = math.ceil(n_charts / max_cols)
        ncols = max_cols if n_charts >= max_cols else n_charts % max_cols

    return {"nrows": nrows, "ncols": ncols}


# -------------------------------------
# Text Configuration
# -------------------------------------


def get_text_style(text_type: str = "") -> dict:
    """Get the text configuration

    Args:
        config (Config): The configuration.
        text_type (str): The text type (default: "").

    Returns:
        dict: The text configuration dict.

    """
    config_attrs = [
        ("fontsize", "font.{type}.size"),
        ("fontweight", "font.{type}.weight"),
        ("color", "font.{type}.color"),
        ("style", "font.{type}.style"),
        ("family", "font.{type}.family"),
    ]

    return {
        key: config.get(
            attr.format(type=text_type),
            config.get(attr.format(type="general")),
        )
        for key, attr in config_attrs
    }


# -------------------------------------
# Line Configuration
# -------------------------------------


def get_line_style(chart_style: dict) -> dict:
    """Get the line configuration

    Args:
        chart_style (dict): The chart style dictionary.

    Returns:
        dict: The line configuration dict.

    """
    config_attrs = [
        ("color", "plot.line.color"),
        ("alpha", "plot.line.alpha"),
        ("linewidth", "plot.line.width"),
        ("linestyle", "plot.line.style"),
        ("marker", "plot.line.marker"),
        ("drawstyle", "plot.line.drawstyle"),
        ("zorder", "plot.line.zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Bar Configuration
# -------------------------------------


def get_bar_style(chart_style: dict, is_horizontal: bool = False) -> dict:
    """Get the bar configuration

    Args:
        chart_style (dict): The chart style dictionary.
        horizontal_flag (bool): Whether the bar is horizontal or not.

    Returns:
        dict: The bar configuration dict.

    """
    config_attrs = [
        ("color", "plot.bar.color"),
        ("alpha", "plot.bar.alpha"),
        ("height" if is_horizontal else "width", "plot.bar.width"),
        ("hatch", "plot.bar.hatch"),
        ("linewidth", "plot.bar.edge.width"),
        ("edgecolor", "plot.bar.edge.color"),
        ("ecolor", "plot.bar.error.color"),
        ("zorder", "plot.bar.zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Hist Configuration
# -------------------------------------


def get_hist_style(chart_style: dict) -> dict:
    """Get the hist configuration

    Args:
        chart_style (dict): The chart style dictionary.

    Returns:
        dict: The hist configuration dict.

    """
    config_attrs = [
        ("color", "plot.hist.color"),
        ("alpha", "plot.hist.alpha"),
        ("zorder", "plot.hist.zorder"),
        ("histtype", "plot.hist.type"),
        ("align", "plot.hist.align"),
        ("linewidth", "plot.hist.edge.width"),
        ("edgecolor", "plot.hist.edge.color"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Area Configuration
# -------------------------------------


def get_area_style(chart_style: dict) -> dict:
    """Get the area configuration

    Args:
        chart_style (dict): The chart style dictionary.

    Returns:
        dict: The area configuration dict.

    """

    config_attrs = [
        ("alpha", "plot.area.alpha"),
        ("color", "plot.area.color"),
        ("linewidth", "plot.area.linewidth"),
        ("zorder", "plot.area.zorder"),
    ]

    return create_config_dict(chart_style, config_attrs)


# -------------------------------------
# Grid Configuration
# -------------------------------------


def get_grid_style(chart_style: dict) -> dict:
    """Get the grid configuration

    Args:
        chart_style (dict): The chart style dictionary.

    Returns:
        dict: The grid configuration dict.

    """
    config_attrs = [
        ("alpha", "plot.grid.alpha"),
        ("color", "plot.grid.color"),
        ("linewidth", "plot.grid.line.width"),
        ("linestyle", "plot.grid.line.style"),
        ("zorder", "plot.grid.zorder"),
    ]
    return create_config_dict(chart_style, config_attrs)


# ================================================
# Chart Configurations
# ================================================


def configure_axes_spines(ax):
    """
    Configure axes spines.

    Args:
        ax (Axes): The axes.
    """
    # Turn on the axes
    ax.axis("on")

    # Loop through each axis and configure spines
    for axis in ["top", "bottom", "left", "right"]:
        # Set the linewidth and visibility of the spine
        ax.spines[axis].set(
            linewidth=config["axes.spines.width"],
            visible=config[f"axes.spines.{axis}.visible"],
            zorder=config["axes.spines.zorder"],
        )


def configure_axis_ticks(ax, axis_type: str):
    """Configure axis ticks.

    Args:
        ax (Axes): The axes.
        axis_type (str): The axis type. Options: "xaxis", "yaxis".

    """
    # Set tick parameters for major ticks
    getattr(ax, axis_type).set_tick_params(
        which="major",
        width=config["axes.spines.width"],
        length=config["axes.ticks.length"],
        labelsize=config["axes.ticks.label.size"],
    )


def configure_labels(settings: dict, actions: list):
    """Configure chart labels.

    Args:
        actions (dict): The axes.
        chart (dict): The chart dictionary.
    """
    for label, action in actions:
        if label in settings:
            action(settings[label], **get_text_style(label))
