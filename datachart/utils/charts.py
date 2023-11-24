import json
import warnings
from typing import List, Union

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from ..utils.colors import create_color_cycle, get_colormap
from ..utils.stats import get_min_max_values
from ..utils.attrs import (
    get_subplot_config,
    get_attr_value,
    get_area_style,
    get_grid_style,
    get_line_style,
    get_bar_style,
    get_hist_style,
    get_legend_style,
    get_vline_style,
    get_hline_style,
    get_heatmap_style,
    get_heatmap_font_style,
    configure_axes_spines,
    configure_axis_ticks_style,
    configure_axis_ticks_position,
    configure_axis_limits,
    configure_labels,
)

from ..definitions import (
    LineDataAttrs,
    BarDataAttrs,
    HistDataAttrs,
    HeatmapChartAttrs,
    UnionChartAttrs,
    HLineAttrs,
    VLineAttrs,
)
from ..constants import FIG_SIZE, ORIENTATION, VALFMT
from ..config import config

# ================================================
# Defaults
# ================================================

DEFAULT_NUM_BINS = 20
DEFAULT_ORIENTATION = ORIENTATION.VERTICAL
DEFAULT_VALFMT = VALFMT.DEFAULT


# ================================================
# Helper Functions
# ================================================


def get_chart_data(attr: str, chart: dict) -> np.array:
    """Generate a numpy array of data from a given chart dictionary.

    Parameters
    ----------
    attr : str
        The attribute to extract from the chart data.
    chart : dict
        The chart dictionary containing the data.

    Returns
    -------
    np.array
        An array of values extracted from the chart data, or None if no values are found.
    """

    attr_label = get_attr_value(attr, chart, attr)

    if isinstance(chart["data"], dict):
        return chart["data"][attr_label] if attr_label in chart["data"] else None

    if isinstance(chart["data"], list):
        data = np.array([d[attr_label] for d in chart["data"] if attr_label in d])
        return data if len(data) > 0 else None

    return None


def custom_color_cycle(has_multi_subplots: bool, n_charts: int):
    """Create a custom color cycle.

    Parameters
    ----------
    has_multi_subplots : bool
        True if there are multiple subplots, False otherwise.
    n_charts : int
        The number of charts.

    Returns
    -------
    list
        The custom color cycle.
    """

    color_type = "singular" if has_multi_subplots else "multiple"
    color_attr = config[f"color.general.{color_type}"]
    max_colors = 1 if has_multi_subplots else n_charts
    return create_color_cycle(color_attr, max_colors)


def has_multiple_subplots(axes: list) -> bool:
    """Check if there are multiple subplots.

    Parameters
    ----------
    axes : list
        The axes list.

    Returns
    -------
    bool
        True if there are multiple subplots, False otherwise.
    """

    return not all([ax == axes[0] for ax in axes])


def get_chart_hash(chart: dict) -> str:
    """Get a hash of the chart.

    Parameters
    ----------
    chart : dict
        The chart dictionary.

    Returns
    -------
    str
        The hash of the chart.
    """

    return hash(json.dumps(chart, sort_keys=True))


# ------------------------------------------------
# Settings Mapping and Helpers
# ------------------------------------------------


settings_attr_mapping = [
    # common attributes
    {"name": "type", "default": None},
    {"name": "title", "default": None},
    {"name": "xlabel", "default": None},
    {"name": "ylabel", "default": None},
    {"name": "sharex", "default": False},
    {"name": "sharey", "default": False},
    {"name": "subplots", "default": None},
    {"name": "aspect_ratio", "default": "auto"},
    {"name": "figsize", "default": FIG_SIZE.DEFAULT},
    {"name": "max_cols", "default": 4},
    {"name": "xmin", "default": None},
    {"name": "xmax", "default": None},
    {"name": "ymin", "default": None},
    {"name": "ymax", "default": None},
    # visibility attributes
    {"name": "show_legend", "default": None},
    {"name": "show_grid", "default": None},
    {"name": "show_yerr", "default": None},
    {"name": "show_area", "default": None},
    {"name": "show_density", "default": None},
    {"name": "show_cumulative", "default": None},
    {"name": "show_colorbars", "default": None},
    {"name": "show_heatmap_vals", "default": None},
    # chart specific attributes
    {"name": "orientation", "default": None},
    {"name": "log_scale", "default": None},
    {"name": "num_bins", "default": None},
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
    "show_area",
    "show_density",
    "show_cumulative",
    "show_colorbars",
    "show_heatmap_vals",
    "orientation",
    "log_scale",
    "num_bins",
]


def get_settings(attrs: dict) -> dict:
    """Get the chart settings.

    Parameters
    ----------
    attrs : dict
        The attributes.

    Returns
    -------
    dict
        The chart settings.
    """

    return {
        attr["name"]: attrs.get(attr["name"], attr["default"])
        for attr in settings_attr_mapping
    }


def get_chart_settings(settings: dict) -> dict:
    """Get the chart settings.

    Parameters
    ----------
    settings : dict
        The chart settings.

    Returns
    -------
    dict
        The chart settings without the None values.
    """

    return {key: val for key, val in settings.items() if key in settings_chart_mapping}


def assert_chart_settings(settings: dict, supported_settings: List[str]) -> None:
    """Assert that the chart config is supported.

    Parameters
    ----------
    settings : dict
        The chart settings.
    supported_settings : List[str]
        The supported settings.
    """

    for key, val in settings.items():
        if key not in supported_settings and val:
            warnings.warn(
                f"Settings['{key}'] is present but is not supported. Ignoring flag..."
            )


# ================================================
# Main Chart Wrapper Definition
# ================================================


def chart_wrapper(func: callable) -> callable:
    def wrapper_func(attrs: UnionChartAttrs) -> None:
        # check how many data point are there
        if not isinstance(attrs["charts"], dict) and not isinstance(
            attrs["charts"], list
        ):
            raise ValueError("Parameter `attrs['charts']` is not correctly structured")

        # get chart settings
        settings = get_settings(attrs)

        # format the data into a 1D array
        charts = attrs.get("charts")
        charts = charts if isinstance(charts, list) else [charts]
        charts = np.array(charts)

        # get the number of rows and columns of the chart
        subplot_config = get_subplot_config(
            settings["type"],
            settings["subplots"],
            n_charts=charts.shape[0],
            max_cols=settings["max_cols"],
        )
        # define the canvas
        figure, axes = plt.subplots(
            figsize=settings["figsize"],
            sharex=settings["sharex"],
            sharey=settings["sharey"],
            constrained_layout=True,
            squeeze=False,
            **subplot_config,
        )

        is_single_plot = subplot_config["nrows"] == 1 and subplot_config["ncols"] == 1
        # prepare the axes based on the draw type
        axes = (
            [axes[0, 0] for _ in range(charts.shape[0])]
            if is_single_plot
            else axes.flatten()
        )

        # hide all axes
        for ax in axes:
            ax.axis("off")

        for chart, ax in zip(charts, axes):
            # configure the local chart spines and ticks
            configure_axes_spines(ax)
            configure_axis_ticks_style(ax, "xaxis")
            configure_axis_ticks_style(ax, "yaxis")
            # configure the local chart labels
            if not is_single_plot:
                configure_labels(
                    chart,
                    [
                        ("subtitle", ax.set_title),
                        ("xlabel", ax.set_xlabel),
                        ("ylabel", ax.set_ylabel),
                    ],
                )

        func(figure, axes, charts, settings=get_chart_settings(settings))
        # configure the global figure labels
        configure_labels(
            settings,
            [
                ("title", figure.suptitle),
                ("xlabel", figure.supxlabel),
                ("ylabel", figure.supylabel),
            ],
        )

        return figure

    return wrapper_func


# ================================================
# Draw Line Chart
# ================================================


def draw_line_chart(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[LineDataAttrs],
    settings: dict,
) -> None:
    """Draw a line chart

    Parameters
    ----------
    figure: plt.Figure
        The figure.
    axes : List[plt.Axes]
        The axes list.
    charts : List[LineDataAttrs]
        The charts data.
    settings : dict
        The general settings.
    """

    # assert the configuration
    assert_chart_settings(
        settings=settings,
        supported_settings=[
            "xmin",
            "xmax",
            "ymin",
            "ymax",
            "aspect_ratio",
            "show_legend",
            "show_grid",
            "show_yerr",
            "show_area",
            "log_scale",
        ],
    )

    has_multi_subplots = has_multiple_subplots(axes)

    # get the color cycle
    color_cycle = custom_color_cycle(has_multi_subplots, charts.shape[0])

    for chart, ax in zip(charts, axes):
        # retrieve the chart data points
        x = get_chart_data("x", chart)
        y = get_chart_data("y", chart)
        yerr = get_chart_data("yerr", chart)

        # get the chart style attributes
        style = chart.get("style", {})

        # validate the drawing flags
        draw_yerr_flag = (
            settings["show_yerr"]
            and isinstance(yerr, np.ndarray)
            and len(yerr) == len(y)
        )
        draw_area_flag = settings["show_area"]

        if draw_yerr_flag and draw_area_flag:
            warnings.warn(
                "Both the `show_yerr` and `show_area` will be used. "
                + "Only one of them should be True."
            )

        # get style configuration
        chart_hash = get_chart_hash(chart)
        line_style = {**color_cycle[chart_hash], **get_line_style(style)}
        area_style = {**color_cycle[chart_hash], **get_area_style(style)}

        if draw_yerr_flag:
            # draw the confidence interval around the line
            ymin = y - yerr
            ymax = y + yerr
            ax.fill_between(x, ymin, ymax, **area_style)

        if draw_area_flag:
            # draw the area under the curve
            step = (
                line_style["drawstyle"].split("-")[1]
                if "steps-" in line_style["drawstyle"]
                else None
            )
            ax.fill_between(x, y, step=step, **area_style)

        # draw the line chart
        subtitle = chart.get("subtitle", None)
        ax.plot(x, y, **line_style, label=subtitle)

        if settings["log_scale"]:
            ax.set_yscale("log")

        if settings["show_grid"]:
            ax.grid(axis=settings["show_grid"], **get_grid_style(style))

        # set the x-axis limit
        xmin, xmax = get_min_max_values(x)
        ax.set_xlim(xmin=xmin, xmax=xmax)

        # override axis limits
        configure_axis_ticks_position(ax, chart)
        configure_axis_limits(ax, settings)

        if "vlines" in chart:
            # draw vertical lines
            draw_vlines(ax, chart["vlines"])

        if "hlines" in chart:
            # draw horizontal lines
            draw_hlines(ax, chart["hlines"])

        # set the aspect ratio of the chart
        if settings["aspect_ratio"]:
            ax.set(adjustable="box", aspect=settings["aspect_ratio"])

    # show the legend in the last subplot
    if has_multi_subplots and settings["show_legend"]:
        warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")

    if not has_multi_subplots and settings["show_legend"]:
        axes[0].legend(title="Legend", **get_legend_style())


# ================================================
# Draw Bar Chart
# ================================================


def draw_bar_chart(
    figure: plt.Figure, axes: List[plt.Axes], charts: List[BarDataAttrs], settings: dict
) -> None:
    """Draw a bar chart

    Parameters
    ----------
    figure: plt.Figure
        The figure.
    axes : List[plt.Axes]
        The axes list.
    charts : List[BarDataAttrs]
        The charts data.
    settings : dict
        The general settings.
    """

    # assert the configuration
    assert_chart_settings(
        settings=settings,
        supported_settings=[
            "aspect_ratio",
            "xmin",
            "xmax",
            "ymin",
            "ymax",
            "show_legend",
            "show_grid",
            "show_yerr",
            "orientation",
            "log_scale",
        ],
    )

    has_multi_subplots = has_multiple_subplots(axes)
    is_horizontal = (
        settings.get("orientation", DEFAULT_ORIENTATION) == ORIENTATION.HORIZONTAL
    )

    color_cycle = custom_color_cycle(has_multi_subplots, charts.shape[0])
    if not has_multi_subplots and charts.shape[0] > 5:
        warnings.warn(
            "The number of charts is greater than 5. "
            + "Please consider using a different plotting method or create subplots."
        )

    # prepare the bar chart position variables
    x_start = np.arange(max([len(get_chart_data("label", chart)) for chart in charts]))
    x_width = config["plot.bar.width"] / charts.shape[0]  # the width of the bar
    x_offset = 0

    for idx, (chart, ax) in enumerate(zip(charts, axes)):
        # get the chart style attributes
        style = chart.get("style", {})

        # retrieve the chart data points
        y = get_chart_data("y", chart)
        yerr = get_chart_data("yerr", chart) if settings["show_yerr"] else None
        labels = get_chart_data("label", chart)

        x = np.arange(labels.shape[0])

        chart_hash = get_chart_hash(chart)
        bar_style = {**color_cycle[chart_hash], **get_bar_style(style, is_horizontal)}

        if not has_multi_subplots:
            # update the bar chart style
            tmp_attr = "height" if is_horizontal else "width"
            bar_style[tmp_attr] = x_width
            x_offset = idx * x_width

        tmp_attr = "xerr" if is_horizontal else "yerr"
        error_range = {tmp_attr: yerr}

        # draw the bar chart
        subtitle = chart.get("subtitle", None)
        draw_func = ax.barh if is_horizontal else ax.bar
        draw_func(
            x + x_offset,
            y + (1 if settings["log_scale"] else 0),
            log=settings["log_scale"],
            label=subtitle,
            **error_range,
            **bar_style,
        )

        if settings["show_grid"]:
            ax.grid(axis=settings["show_grid"], **get_grid_style(style))

        # ---------------------------------------
        # Update the tick position
        # ---------------------------------------

        def get_rotation_degrees(n_labels: int):
            """Rotate the bar labels based on the number of labels."""
            if has_multi_subplots:
                # rotate based on the number of labels
                return 90 if n_labels >= 7 else (45 if n_labels >= 4 else 0)
            # do not rotate the labels
            return 0

        def position_group_labels(ticks_loc: List[float], labels: List[str], axis: str):
            """Update the group bar labels on the specified axis."""
            if axis == "xaxis":
                ax.set_xticks(ticks_loc, labels)
                ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
                ax.set_xticklabels(
                    labels, rotation=get_rotation_degrees(labels.shape[0])
                )
            elif axis == "yaxis":
                ax.set_yticks(ticks_loc, labels)
                ax.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))

        # position the ticks in the middle of the group
        ticks_loc = x_start + (charts.shape[0] - 1) / 2 * x_width
        ticks_loc = ticks_loc if not has_multi_subplots else x
        label_axis = "yaxis" if is_horizontal else "xaxis"
        position_group_labels(ticks_loc, labels, axis=label_axis)

        if has_multi_subplots:
            # overwrite the label positions
            configure_labels(
                chart,
                [
                    ("subtitle", ax.set_title),
                    ("xlabel", ax.set_xlabel if not is_horizontal else ax.set_ylabel),
                    ("ylabel", ax.set_ylabel if not is_horizontal else ax.set_xlabel),
                ],
            )

        if "vlines" in chart:
            # draw vertical lines
            draw_vlines(ax, chart["vlines"])

        if "hlines" in chart:
            # draw horizontal lines
            draw_hlines(ax, chart["hlines"])

        # set the tick positions
        configure_axis_ticks_position(ax, chart)
        configure_axis_limits(ax, settings)

        # set the aspect ratio of the chart
        if settings["aspect_ratio"]:
            ax.set(adjustable="box", aspect=settings["aspect_ratio"])

    # show the legend in the last subplot
    if has_multi_subplots and settings["show_legend"]:
        warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")

    if not has_multi_subplots and settings["show_legend"]:
        axes[0].legend(title="Legend", **get_legend_style())


# ================================================
# Draw Histogram Chart
# ================================================


def draw_histogram(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[HistDataAttrs],
    settings: dict,
) -> None:
    """Draw a bar chart

    Parameters
    ----------
    figure: plt.Figure
        The figure.
    axes : List[plt.Axes]
        The axes list.
    charts : List[HistDataAttrs]
        The charts data.
    settings : dict
        The general settings.
    """

    # assert the configuration
    assert_chart_settings(
        settings=settings,
        supported_settings=[
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
            "log_scale",
        ],
    )

    has_multi_subplots = has_multiple_subplots(axes)
    num_bins = settings["num_bins"] if settings["num_bins"] else DEFAULT_NUM_BINS
    orientation = (
        settings["orientation"] if settings["orientation"] else DEFAULT_ORIENTATION
    )

    color_cycle = custom_color_cycle(has_multi_subplots, charts.shape[0])

    # normalize the bin size for all charts
    xall = [get_chart_data("x", chart) for chart in charts]
    bins = np.histogram(np.hstack(tuple(xall)), bins=num_bins)[1]

    if not has_multi_subplots:
        # visualize all charts in a common subplot
        labels = []
        tmp_styles = []
        style = charts[0].get("style", {})
        for chart in charts:
            chart_hash = get_chart_hash(chart)
            tmp_styles.append({**color_cycle[chart_hash], **get_hist_style(style)})
            labels.append(chart.get("subtitle", None))

        colors = [c["color"] for c in tmp_styles]

        hist_style = {
            **tmp_styles[0],
            "color": colors if colors.count(None) == 0 else None,
        }

        # draw the histogram chart
        axes[0].hist(
            xall,
            bins=bins,
            label=labels,
            stacked=True,
            log=settings["log_scale"],
            density=settings["show_density"],
            cumulative=settings["show_cumulative"],
            orientation=orientation,
            **hist_style,
        )

        if "vlines" in chart:
            # draw vertical lines
            draw_vlines(axes[0], chart["vlines"])

        if "hlines" in chart:
            # draw horizontal lines
            draw_hlines(axes[0], chart["hlines"])

        # override the axis limits
        configure_axis_ticks_position(axes[0], charts[0])
        configure_axis_limits(axes[0], settings)

        if settings["show_grid"]:
            # show the chart grid
            axes[0].grid(axis=settings["show_grid"], **get_grid_style(style))

        # set the aspect ratio of the chart
        if settings["aspect_ratio"]:
            axes[0].set(adjustable="box", aspect=settings["aspect_ratio"])

        if settings["show_legend"]:
            axes[0].legend(title="Legend", **get_legend_style())

    else:
        # visualize each chart in a separate subplot
        for chart, ax in zip(charts, axes):
            # get the chart style attributes
            style = chart.get("style", {})

            # retrieve the chart data points
            x = get_chart_data("x", chart)

            chart_hash = get_chart_hash(chart)
            hist_style = {**color_cycle[chart_hash], **get_hist_style(style)}
            label = chart.get("subtitle", None)
            # draw the histogram chart
            ax.hist(
                x,
                bins=bins,
                label=label,
                log=settings["log_scale"],
                density=settings["show_density"],
                cumulative=settings["show_cumulative"],
                orientation=orientation,
                **hist_style,
            )

            if "vlines" in chart:
                # draw vertical lines
                draw_vlines(ax, chart["vlines"])

            if "hlines" in chart:
                # draw horizontal lines
                draw_hlines(ax, chart["hlines"])

            # override the axis limits
            configure_axis_ticks_position(ax, chart)
            configure_axis_limits(ax, settings)

            if settings["show_grid"]:
                # show the chart grid
                ax.grid(axis=settings["show_grid"], **get_grid_style(style))

            # set the aspect ratio of the chart
            if settings["aspect_ratio"]:
                ax.set(adjustable="box", aspect=settings["aspect_ratio"])

        # show the legend in the last subplot
        if settings["show_legend"]:
            warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")


# ================================================
# Draw Vertical Lines
# ================================================


def draw_vlines(ax: plt.Axes, vlines: Union[VLineAttrs, List[VLineAttrs]]):
    """Draws vertical lines.

    Parameters
    ----------
    ax : plt.Axes
        The axes.

    vlines : Union[VLineAttrs, List[VLineAttrs]]
        The configuration of the vertical lines.
    """

    vlines = vlines if isinstance(vlines, list) else [vlines]
    ymin, ymax = ax.get_ylim()
    for vline in vlines:
        x = vline.get("x")
        ymin = vline.get("ymin", ymin)
        ymax = vline.get("ymax", ymax)
        label = vline.get("label", "")
        style = get_vline_style(vline.get("style", {}))

        if x is None:
            warnings.warn(
                "The attribute `x` is not specified. Please provide the `x` value."
            )
            continue

        ax.vlines(x=x, ymin=ymin, ymax=ymax, label=label, **style)


# ================================================
# Draw Horizontal Lines
# ================================================


def draw_hlines(ax: plt.Axes, hlines: Union[HLineAttrs, List[HLineAttrs]]):
    """Draws horizontal lines.

    Parameters
    ----------
    ax : plt.Axes
        The axes.

    hlines : Union[HLineAttrs, List[HLineAttrs]]
        The configuration of the horizontal lines.
    """

    hlines = hlines if isinstance(hlines, list) else [hlines]

    xmin, xmax = ax.get_xlim()

    for hline in hlines:
        y = hline.get("y")
        xmin = hline.get("xmin", xmin)
        xmax = hline.get("xmax", xmax)
        label = hline.get("label", "")
        style = get_hline_style(hline.get("style", {}))

        if y is None:
            warnings.warn(
                "The attribute `y` is not specified. Please provide the `y` value."
            )
            continue

        ax.hlines(y=y, xmin=xmin, xmax=xmax, label=label, **style)


# ================================================
# Draw Bar Chart
# ================================================


def draw_heatmap(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[HeatmapChartAttrs],
    settings: dict,
) -> None:
    """Draw a heatmap chart

    Parameters
    ----------
    figure: plt.Figure
        The figure.
    axes : List[plt.Axes]
        The axes list.
    charts : List[HeatmapChartAttrs]
        The charts data.
    settings : dict
        The general settings.
    """

    # assert the configuration
    assert_chart_settings(
        settings=settings,
        supported_settings=[
            "aspect_ratio",
            "show_colorbars",
            "show_heatmap_vals",
        ],
    )

    for chart, ax in zip(charts, axes):
        # get the chart style attributes
        style = chart.get("style", {})

        # retrieve the chart data points
        data = np.array(chart.get("data"))
        assert len(data.shape) == 2, "The `data` attribute is not a 2-dimensional array"

        data = [[(np.nan if item == None else item) for item in row] for row in data]
        norm = chart.get("norm", None)
        vmin = chart.get("vmin", None)
        vmax = chart.get("vmax", None)
        valfmt = chart.get("valfmt", DEFAULT_VALFMT)
        colorbar = chart.get("colorbar", {})

        # get the heatmap style
        heatmap_style = get_heatmap_style(style)
        heatmap_style["cmap"] = get_colormap(heatmap_style["cmap"])

        # draw the heatmap
        im = ax.imshow(data, norm=norm, vmin=vmin, vmax=vmax, **heatmap_style)

        # set the tick positions
        configure_axis_ticks_position(ax, chart)

        if settings["show_heatmap_vals"]:
            if isinstance(valfmt, str):
                valfmt = mticker.StrMethodFormatter(valfmt)

            text_style = get_heatmap_font_style(style)
            for i in range(len(data)):
                for j in range(len(data[i])):
                    ax.text(
                        j,
                        i,
                        valfmt(data[i][j], None),
                        ha="center",
                        va="center",
                        **text_style,
                    )

        if settings["show_colorbars"]:
            # draw the colorbar
            orientation = colorbar.get("orientation", DEFAULT_ORIENTATION)
            location = "right" if orientation == ORIENTATION.VERTICAL else "top"
            figure.colorbar(
                im,
                ax=ax,
                orientation=orientation,
                location=location,
                fraction=0.1,
                pad=0.05,
            )
