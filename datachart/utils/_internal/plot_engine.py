"""Figure assembly for the chart fronts.

`render_chart` turns a chart front's charts structure and settings into a
rendered figure: it builds the layers (resolving style at construction),
assembles one panel per coordinate space, renders them, and stores the
metadata transport (`figure._chart_metadata`) that composition functions
consume.
"""

import warnings
from typing import Dict, List, Union

import matplotlib.pyplot as plt

from .config_helpers import get_subplot_config, configure_labels
from .figures import new_figure
from .layers import (
    Panel,
    LayerGroup,
    build_layers,
    group_from_chart,
    build_chart_panel_settings,
)
from ...constants import FIG_SIZE, ORIENTATION

# ================================================
# Chart Rendering
# ================================================


def render_chart(
    chart_type: str,
    charts: Union[Dict, List[Dict]],
    settings: dict,
) -> plt.Figure:
    """Render a chart front's charts and settings into a figure via the Layer/Panel seam.

    Args:
        chart_type: The chart type, e.g. `"linechart"`.
        charts: The charts structure built by `build_charts_structure`.
        settings: The figure-level settings forwarded by the chart front;
            values may be `None`, in which case defaults apply at point of use.

    Returns:
        The rendered figure.

    """

    if not isinstance(charts, (dict, list)):
        raise ValueError("Parameter `charts` is not correctly structured")

    charts = charts if isinstance(charts, list) else [charts]

    # build the layers; style is resolved against the config here, once
    layers = build_layers(chart_type, charts, settings)

    max_cols = settings.get("max_cols")
    subplot_config = get_subplot_config(
        chart_type,
        settings.get("subplots"),
        n_charts=len(charts),
        max_cols=4 if max_cols is None else max_cols,
    )
    figsize = settings.get("figsize")
    sharex = settings.get("sharex")
    sharey = settings.get("sharey")
    figure = new_figure(figsize=FIG_SIZE.DEFAULT if figsize is None else figsize)
    axes = figure.subplots(
        sharex=False if sharex is None else sharex,
        sharey=False if sharey is None else sharey,
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
        if settings.get("show_legend") and chart_type != "heatmap":
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
    # grid cells keep the figure title; single-chart subtitles are the fallback
    composition_settings["title"] = (
        settings.get("title")
        if settings.get("title") is not None
        else charts[0].get("subtitle", None)
    )
    figure._chart_metadata = {
        "type": chart_type,
        "panel": Panel(
            [group_from_chart(layers, settings, mode="multiple")], composition_settings
        ),
    }

    # multi-subplot figures also carry one panel per subplot, so grids can
    # rebuild the subplot arrangement inside a cell
    if not is_single_plot:
        subplot_panels = []
        for layer in layers:
            sub_settings = build_chart_panel_settings(
                chart_type, settings, "composition", layer.style
            )
            sub_settings["show_legend"] = False
            sub_settings["bar_slotting"] = False
            sub_settings["bar_ticks"] = "subplot"
            sub_settings["hist_bins_override"] = hist_bins
            sub_settings["title"] = layer.chart.get("subtitle")
            xlabel, ylabel = layer.chart.get("xlabel"), layer.chart.get("ylabel")
            if is_horizontal_bar:
                xlabel, ylabel = ylabel, xlabel
            sub_settings["xlabel"] = xlabel
            sub_settings["ylabel"] = ylabel
            subplot_panels.append(
                Panel(
                    [group_from_chart([layer], settings, mode="singular")], sub_settings
                )
            )
        figure._chart_metadata["panels"] = subplot_panels
        figure._chart_metadata["shape"] = (
            subplot_config["nrows"],
            subplot_config["ncols"],
        )

    return figure
