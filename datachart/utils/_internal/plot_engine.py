"""Figure assembly for the chart fronts.

`render_chart` turns a chart front's attrs dict into a rendered figure: it
builds the layers (resolving style at construction), assembles one panel per
coordinate space, renders them, and stores the metadata transport
(`figure._chart_metadata`) that composition functions consume.
"""

import warnings
from typing import List

import matplotlib.pyplot as plt

from .config_helpers import get_subplot_config, configure_labels
from .layers import (
    Panel,
    LayerGroup,
    build_layers,
    group_from_chart,
    build_chart_panel_settings,
)
from ...constants import FIG_SIZE, ASPECT_RATIO, ORIENTATION
from ...typings import ChartAttrs

# ------------------------------------------------
# Settings Mapping and Helpers
# ------------------------------------------------


settings_attr_mapping = [
    # common attributes
    {"name": "type", "default": None},
    {"name": "title", "default": None},
    {"name": "xlabel", "default": None},
    {"name": "ylabel", "default": None},
    {"name": "figsize", "default": FIG_SIZE.DEFAULT},
    {"name": "xmin", "default": None},
    {"name": "xmax", "default": None},
    {"name": "ymin", "default": None},
    {"name": "ymax", "default": None},
    {"name": "aspect_ratio", "default": ASPECT_RATIO.AUTO},
    {"name": "subplots", "default": None},
    {"name": "max_cols", "default": 4},
    {"name": "sharex", "default": False},
    {"name": "sharey", "default": False},
    # visibility attributes
    {"name": "show_legend", "default": None},
    {"name": "show_grid", "default": None},
    {"name": "show_yerr", "default": None},
    {"name": "show_values", "default": None},
    {"name": "show_area", "default": None},
    {"name": "show_density", "default": None},
    {"name": "show_cumulative", "default": None},
    {"name": "show_colorbars", "default": None},
    {"name": "show_heatmap_values", "default": None},
    {"name": "show_regression", "default": None},
    {"name": "show_ci", "default": None},
    {"name": "show_correlation", "default": None},
    {"name": "show_outliers", "default": None},
    {"name": "show_notch", "default": None},
    # chart specific attributes
    {"name": "orientation", "default": None},
    {"name": "scalex", "default": None},
    {"name": "scaley", "default": None},
    {"name": "num_bins", "default": None},
    {"name": "ci_level", "default": None},
    {"name": "size_range", "default": None},
    {"name": "value_format", "default": None},
    {"name": "bar_mode", "default": None},
]

settings_chart_mapping = [
    "aspect_ratio",
    "xmin",
    "xmax",
    "ymin",
    "ymax",
    "show_legend",
    "show_grid",
    "show_yerr",
    "show_values",
    "show_area",
    "show_density",
    "show_cumulative",
    "show_colorbars",
    "show_heatmap_values",
    "show_regression",
    "show_ci",
    "show_correlation",
    "show_outliers",
    "show_notch",
    "orientation",
    "scalex",
    "scaley",
    "num_bins",
    "ci_level",
    "size_range",
    "value_format",
    "bar_mode",
]

SUPPORTED_SETTINGS = {
    "linechart": [
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "aspect_ratio",
        "show_legend",
        "show_grid",
        "show_yerr",
        "show_area",
        "scalex",
        "scaley",
    ],
    "barchart": [
        "aspect_ratio",
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "show_legend",
        "show_grid",
        "show_yerr",
        "show_values",
        "value_format",
        "orientation",
        "scalex",
        "scaley",
        "bar_mode",
    ],
    "histogram": [
        "aspect_ratio",
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "show_legend",
        "show_grid",
        "show_density",
        "show_cumulative",
        "num_bins",
        "orientation",
        "scalex",
        "scaley",
    ],
    "heatmap": [
        "aspect_ratio",
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "show_grid",
        "show_colorbars",
        "show_heatmap_values",
    ],
    "scatterchart": [
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "aspect_ratio",
        "show_legend",
        "show_grid",
        "show_regression",
        "show_ci",
        "ci_level",
        "show_correlation",
        "scalex",
        "scaley",
        "size_range",
    ],
    "boxplot": [
        "aspect_ratio",
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "show_legend",
        "show_grid",
        "show_outliers",
        "show_notch",
        "orientation",
        "scaley",
    ],
    "parallelcoords": [
        "aspect_ratio",
        "show_legend",
        "show_grid",
    ],
}


def get_settings(attrs: dict) -> dict:
    """Get the chart settings.

    Args:
        attrs: The attributes.

    Returns:
        The chart settings.

    """

    return {
        attr["name"]: attrs.get(attr["name"], attr["default"])
        for attr in settings_attr_mapping
    }


def get_chart_settings(settings: dict) -> dict:
    """Get the chart settings.

    Args:
        settings: The chart settings.

    Returns:
        The chart settings without the `None` values.

    """

    return {key: val for key, val in settings.items() if key in settings_chart_mapping}


def assert_chart_settings(settings: dict, supported_settings: List[str]) -> None:
    """Assert that the chart config is supported.

    Args:
        settings: The chart settings.
        supported_settings: The supported settings.

    """

    for key, val in settings.items():
        if key not in supported_settings and val:
            warnings.warn(
                f"Settings['{key}'] is present but is not supported. Ignoring flag..."
            )


# ================================================
# Chart Rendering
# ================================================


def render_chart(attrs: ChartAttrs) -> plt.Figure:
    """Render a chart front's attrs dict into a figure via the Layer/Panel seam.

    Args:
        attrs: The chart attributes.

    Returns:
        The rendered figure.

    """

    if not isinstance(attrs["charts"], dict) and not isinstance(attrs["charts"], list):
        raise ValueError("Parameter `attrs['charts']` is not correctly structured")

    settings = get_settings(attrs)
    chart_type = settings["type"]

    assert_chart_settings(
        settings=get_chart_settings(settings),
        supported_settings=SUPPORTED_SETTINGS[chart_type],
    )

    charts = attrs.get("charts")
    charts = charts if isinstance(charts, list) else [charts]

    # build the layers; style is resolved against the config here, once
    layers = build_layers(chart_type, charts, settings)

    subplot_config = get_subplot_config(
        chart_type,
        settings["subplots"],
        n_charts=len(charts),
        max_cols=settings["max_cols"],
    )
    figure, axes = plt.subplots(
        figsize=settings["figsize"],
        sharex=settings["sharex"],
        sharey=settings["sharey"],
        constrained_layout=True,
        squeeze=False,
        **subplot_config,
    )

    is_single_plot = subplot_config["nrows"] == 1 and subplot_config["ncols"] == 1
    axes = axes.flatten()

    for ax in axes:
        ax.axis("off")

    first_style = charts[0].get("style", {}) or {}

    if is_single_plot:
        panel = Panel(
            [group_from_chart(layers, settings, mode="multiple")],
            build_chart_panel_settings(chart_type, settings, "single", first_style),
        )
        panel.render(axes[0])
    else:
        if settings["show_legend"] and chart_type != "heatmap":
            warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")

        # histograms share bin edges across all subplots
        hist_bins = None
        if chart_type == "histogram":
            hist_bins = LayerGroup(
                layers, num_bins=settings.get("num_bins")
            ).hist_bins()

        is_horizontal_bar = (
            chart_type == "barchart"
            and settings.get("orientation") == ORIENTATION.HORIZONTAL
        )

        for layer, ax in zip(layers, axes):
            configure_labels(
                layer.chart,
                [
                    ("subtitle", ax.set_title),
                    (
                        "xlabel",
                        ax.set_xlabel if not is_horizontal_bar else ax.set_ylabel,
                    ),
                    (
                        "ylabel",
                        ax.set_ylabel if not is_horizontal_bar else ax.set_xlabel,
                    ),
                ],
            )
            panel_settings = build_chart_panel_settings(
                chart_type, settings, "subplot", layer.style
            )
            panel_settings["hist_bins_override"] = hist_bins
            panel = Panel(
                [group_from_chart([layer], settings, mode="singular")],
                panel_settings,
            )
            panel.render(ax)

    # global figure labels
    configure_labels(
        settings,
        [
            ("title", figure.suptitle),
            ("xlabel", figure.supxlabel),
            ("ylabel", figure.supylabel),
        ],
    )

    # metadata transport: the layers and panel settings compositions consume
    composition_settings = build_chart_panel_settings(
        chart_type, settings, "composition", first_style
    )
    composition_settings["title"] = charts[0].get("subtitle", None)
    figure._chart_metadata = {
        "type": chart_type,
        "panel": Panel(
            [group_from_chart(layers, settings, mode="multiple")], composition_settings
        ),
    }

    return figure
