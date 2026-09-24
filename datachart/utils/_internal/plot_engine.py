"""Figure assembly for the chart fronts.

`render_chart` turns a chart front's charts structure and settings into a
rendered figure: it builds the layers (resolving style at construction),
assembles one panel per coordinate space, renders them, and stores the
metadata transport (`figure._chart_metadata`) that composition functions
consume.
"""

import warnings
from typing import Dict, List, Optional, Union

import matplotlib.pyplot as plt

from .config_helpers import get_subplot_config, configure_labels
from .figures import new_figure
from .chart_builder import build_charts_structure
from .chart_kinds import (
    ChartKind,
    build_chart_panel_settings,
    build_layers,
    chart_kind,
    check_domains,
    splits_datasets,
)
from .layers import Layer, Panel, LayerGroup, group_from_chart, layers_per_chart
from ...themes._base import warn_aliases
from ...constants import COLORBAR_LOCATION, FIG_SIZE, ORIENTATION

# ================================================
# Chart Rendering
# ================================================

# the figure-level settings a subplots figure carries into a grid cell
SUBPLOT_FURNITURE_KEYS = ("title", "xlabel", "ylabel", "sharex", "sharey")


def single_plot_axes_labels(kind: ChartKind, layers: List[Layer]) -> tuple:
    """The axis labels a single plot carries on its axes, not the figure.

    A figure-level label sits at the figure edge: far from a polar circle,
    and past a left or bottom colorbar, where it reads as the bar's caption.
    """

    if kind.projection == "polar":
        return ("xlabel", "ylabel")
    edges = {layer.colorbar_edge for layer in layers}
    return tuple(
        key
        for key, edge in [
            ("xlabel", COLORBAR_LOCATION.BOTTOM),
            ("ylabel", COLORBAR_LOCATION.LEFT),
        ]
        if edge in edges
    )


def composition_panel(
    chart_type: str,
    charts: List[Dict],
    settings: dict,
    layers: Optional[List[Layer]] = None,
) -> Panel:
    """The panel a chart front's figure carries for composition.

    Args:
        chart_type: The chart type, e.g. `"linechart"`.
        charts: The charts structure built by `build_charts_structure`.
        settings: The figure-level settings forwarded by the chart front.
        layers: The layers already built from `charts`; built here when None.

    Returns:
        One panel holding every layer, with the composition settings.

    """

    if layers is None:
        layers = build_layers(chart_type, charts, settings)
    first_style = charts[0].get("style", {}) or {}
    composition_settings = build_chart_panel_settings(
        chart_type, settings, "composition", first_style
    )
    # grid cells keep the figure title; a single chart's subtitle is the
    # fallback, while several subtitles name series, not the figure
    title = settings.get("title")
    if title is None and len(charts) == 1:
        title = charts[0].get("subtitle", None)
    composition_settings["title"] = title
    return Panel([group_from_chart(layers, settings)], composition_settings)


def rename_deprecated(kind: ChartKind, params: dict) -> dict:
    """The front's arguments with each deprecated name moved to its new one.

    Warns once per deprecated name the caller set, pointing at the front's
    caller; raises `ValueError` when both names are set.
    """

    params = dict(params)
    for old, new in kind.renamed.items():
        value = params.pop(old, None)
        if value is None:
            continue
        # this function, `render`, the front, then the caller
        warnings.warn(
            f"`{old}` is deprecated and will be removed in the next release; "
            f"use `{new}` instead.",
            DeprecationWarning,
            stacklevel=4,
        )
        if params.get(new) is not None:
            raise ValueError(f"Pass `{new}` only; `{old}` is its deprecated name.")
        params[new] = value
    return params


def render(chart_type: str, params: dict) -> plt.Figure:
    """Render a chart front's arguments, split by its row (ADR 0066).

    Deprecated names move to their new ones, rejected parameters raise, and
    every constant-typed value is checked against its class (ADR 0068).
    Per-chart keys are indexed against the charts; every other argument is a
    figure-level setting, with the row's defaults filling what was left unset.

    Args:
        chart_type: The chart type, e.g. `"linechart"`.
        params: The front's arguments by name, `data` among them.

    Returns:
        The rendered figure.

    """

    kind = chart_kind(chart_type)
    params = rename_deprecated(kind, params)
    for name, reason in kind.rejects.items():
        if params.get(name) is not None:
            raise ValueError(reason)
    check_domains(params, kind.domains)
    styles = params.get("style")
    for style in styles if isinstance(styles, list) else [styles]:
        # `render`, the front, then the caller
        warn_aliases(style or {}, stacklevel=3)
    chart_keys = kind.per_chart_keys
    per_chart = {k: v for k, v in params.items() if k in chart_keys}
    settings = {k: v for k, v in params.items() if k not in chart_keys and k != "data"}
    for key, value in kind.defaults.items():
        if settings.get(key) is None:
            settings[key] = value

    charts = build_charts_structure(chart_type, params["data"], **per_chart)
    if kind.check_records is not None:
        kind.check_records(charts, settings)
    if kind.expand is not None:
        charts, settings = kind.expand(charts, settings)
    if kind.legend_default is not None and settings.get("show_legend") is None:
        settings["show_legend"] = kind.legend_default(charts, settings)
    return render_chart(chart_type, charts, settings)


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
    kind = chart_kind(chart_type)
    split = splits_datasets(kind, len(charts), settings.get("subplots"))

    # build the layers; style is resolved against the config here, once
    layers = build_layers(chart_type, charts, settings)

    max_cols = settings.get("max_cols")
    subplot_config = get_subplot_config(
        split,
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
        subplot_kw=(
            None if kind.projection is None else {"projection": kind.projection}
        ),
        **subplot_config,
    )

    is_single_plot = subplot_config["nrows"] == 1 and subplot_config["ncols"] == 1
    axes = axes.flatten()

    for ax in axes:
        ax.axis("off")

    # square polar axes leave slack in wide grid slots; anchor the outer
    # rows/columns toward the center so the circles read as one figure
    if kind.projection == "polar" and not is_single_plot:
        nrows, ncols = subplot_config["nrows"], subplot_config["ncols"]
        for idx, ax in enumerate(axes):
            row, col = divmod(idx, ncols)
            vert = (
                "S" if row < (nrows - 1) / 2 else "N" if row > (nrows - 1) / 2 else ""
            )
            horiz = (
                "E" if col < (ncols - 1) / 2 else "W" if col > (ncols - 1) / 2 else ""
            )
            ax.set_anchor(vert + horiz or "C")

    first_style = charts[0].get("style", {}) or {}

    if is_single_plot:
        panel_settings = build_chart_panel_settings(
            chart_type, settings, "single", first_style
        )
        axes_labels = single_plot_axes_labels(kind, layers)
        for key in axes_labels:
            panel_settings[key] = settings.get(key)
        panel_settings["label_styles"] = Panel.snapshot_label_styles()
        panel = Panel([group_from_chart(layers, settings)], panel_settings)
        panel.render(axes[0])
    else:
        if settings.get("show_legend") and kind.warns_subplot_legend:
            warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")

        hist_bins = None
        if kind.shared_bins:
            hist_bins = LayerGroup(
                layers, num_bins=settings.get("num_bins")
            ).hist_bins()

        is_horizontal_bar = (
            kind.swaps_horizontal_labels
            and settings.get("orientation") == ORIENTATION.HORIZONTAL
        )

        # one dataset per axes; a raincloud dataset is three layers
        for chart_layers, ax in zip(layers_per_chart(layers), axes):
            layer = chart_layers[0]
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
                [group_from_chart(chart_layers, settings)],
                panel_settings,
            )
            panel.render(ax)

    # global figure labels, less those a single plot carries on its axes
    figure_labels = [
        ("title", figure.suptitle),
        ("xlabel", figure.supxlabel),
        ("ylabel", figure.supylabel),
    ]
    if is_single_plot:
        figure_labels = [(k, a) for k, a in figure_labels if k not in axes_labels]
    configure_labels(settings, figure_labels)

    # metadata transport: the layers and panel settings compositions consume
    figure._chart_metadata = {
        "type": chart_type,
        "panel": composition_panel(chart_type, charts, settings, layers),
    }

    # multi-subplot figures also carry one panel per subplot, so grids can
    # rebuild the subplot arrangement inside a cell
    if not is_single_plot:
        subplot_panels = []
        for chart_layers in layers_per_chart(layers):
            layer = chart_layers[0]
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
                    [group_from_chart(chart_layers, settings)],
                    sub_settings,
                )
            )
        figure._chart_metadata["panels"] = subplot_panels
        figure._chart_metadata["shape"] = (
            subplot_config["nrows"],
            subplot_config["ncols"],
        )
        # a grid cell rebuilds the figure-level furniture too (ADR 0006)
        for key in SUBPLOT_FURNITURE_KEYS:
            figure._chart_metadata[key] = settings.get(key)

    return figure
