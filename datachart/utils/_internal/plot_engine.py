import json
import warnings
from itertools import cycle
from typing import List, Union

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from .colors import create_color_cycle, get_colormap
from ..stats import minimum, maximum
from .config_helpers import (
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
    get_scatter_style,
    get_regression_style,
    get_box_style,
    get_box_outlier_style,
    get_box_median_style,
    get_box_whisker_style,
    get_box_cap_style,
    get_parallel_coords_style,
    get_parallel_axis_style,
    get_parallel_tick_style,
    get_parallel_tick_length,
    get_parallel_tick_label_style,
    get_parallel_tick_label_bbox,
    get_parallel_dim_label_style,
    get_parallel_dim_label_rotation,
    get_parallel_dim_label_pad,
    configure_axes_spines,
    configure_axis_ticks_style,
    configure_axis_ticks_position,
    configure_axis_limits,
    configure_labels,
)

from ...typings import (
    LineChartAttrs,
    BarSingleChartAttrs,
    HistogramSingleChartAttrs,
    HeatmapChartAttrs,
    ScatterSingleChartAttrs,
    BoxSingleChartAttrs,
    ParallelCoordsSingleChartAttrs,
    ChartAttrs,
    HLinePlotAttrs,
    VLinePlotAttrs,
)
from ...constants import FIG_SIZE, ORIENTATION, VALFMT, ASPECT_RATIO, COLORBAR_LOCATION
from ...config import config

# ================================================
# Defaults
# ================================================

DEFAULT_NUM_BINS = 20
DEFAULT_ORIENTATION = ORIENTATION.VERTICAL
DEFAULT_VALFMT = VALFMT.DEFAULT
DEFAULT_CI_LEVEL = 0.95
DEFAULT_SIZE_RANGE = (20, 200)


# ================================================
# Helper Functions
# ================================================


def get_chart_data(attr: str, chart: dict) -> np.array:
    """Generate a numpy array of data from a given chart dictionary.

    Args:
        attr: The attribute to extract from the chart data.
        chart: The chart dictionary containing the data.

    Returns:
        An array of values extracted from the chart data, or `None` if no values are found.

    """

    attr_label = get_attr_value(attr, chart, attr)

    if isinstance(chart["data"], dict):
        return chart["data"][attr_label] if attr_label in chart["data"] else None

    if isinstance(chart["data"], list):
        data = np.array([d[attr_label] for d in chart["data"] if attr_label in d])
        return data if len(data) > 0 else None

    return None


def custom_color_cycle(has_multi_subplots: bool, n_charts: int) -> cycle:
    """Create a custom color cycle.

    Args:
        has_multi_subplots: True if there are multiple subplots, False otherwise.
        n_charts: The number of charts.

    Returns:
        The custom color cycle.

    """

    color_type = "singular" if has_multi_subplots else "multiple"
    color_attr = config[f"color_general_{color_type}"]
    max_colors = 1 if has_multi_subplots else n_charts
    return create_color_cycle(color_attr, max_colors)


def has_multiple_subplots(axes: list) -> bool:
    """Check if there are multiple subplots.

    Args:
        axes: The axes list.

    Returns:
        `True` if there are multiple subplots, `False` otherwise.

    """

    return not all([ax == axes[0] for ax in axes])


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles numpy arrays and types."""

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        return super().default(obj)


def get_chart_hash(chart: dict) -> str:
    """Get a hash of the chart.

    Args:
        chart: The chart dictionary.

    Returns:
        The hash of the chart.

    """

    return hash(json.dumps(chart, sort_keys=True, cls=NumpyEncoder))


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
]


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
# Main Chart Wrapper Definition
# ================================================


def chart_plot_wrapper(func: callable) -> callable:
    """Wraps the chart plot

    Args:
        func: The plot creation function.

    Returns:
        The wrapped function.

    """

    def wrapper_func(attrs: ChartAttrs) -> None:
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

        # Store chart metadata in figure for later use (e.g., combining figures)
        figure._chart_metadata = attrs

        return figure

    return wrapper_func


# ================================================
# Plot Vertical Lines
# ================================================


def plot_vlines(ax: plt.Axes, vlines: Union[VLinePlotAttrs, List[VLinePlotAttrs]]):
    """Plots the vertical lines.

    Args:
        ax: The axes.
        vlines: The configuration of the vertical lines.

    """

    vlines = vlines if isinstance(vlines, list) else [vlines]
    default_ymin, default_ymax = ax.get_ylim()
    for vline in vlines:
        x = vline.get("x")
        line_ymin = vline.get("ymin", default_ymin)
        line_ymax = vline.get("ymax", default_ymax)
        label = vline.get("label", "")
        style = get_vline_style(vline.get("style", {}))

        if x is None:
            warnings.warn(
                "The attribute `x` is not specified. Please provide the `x` value."
            )
            continue

        ax.vlines(x=x, ymin=line_ymin, ymax=line_ymax, label=label, **style)


# ================================================
# Plot Horizontal Lines
# ================================================


def plot_hlines(ax: plt.Axes, hlines: Union[HLinePlotAttrs, List[HLinePlotAttrs]]):
    """Plots the horizontal lines.

    Args:
        ax: The axes.
        hlines: The configuration of the horizontal lines.

    """

    hlines = hlines if isinstance(hlines, list) else [hlines]

    default_xmin, default_xmax = ax.get_xlim()

    for hline in hlines:
        y = hline.get("y")
        line_xmin = hline.get("xmin", default_xmin)
        line_xmax = hline.get("xmax", default_xmax)
        label = hline.get("label", "")
        style = get_hline_style(hline.get("style", {}))

        if y is None:
            warnings.warn(
                "The attribute `y` is not specified. Please provide the `y` value."
            )
            continue

        ax.hlines(y=y, xmin=line_xmin, xmax=line_xmax, label=label, **style)


# ================================================
# Plot Line Chart
# ================================================


def plot_line_chart(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[LineChartAttrs],
    settings: dict,
) -> None:
    """Plot the line chart.

    Args:
        figure: The figure.
        axes: The axes list.
        charts: The charts data.
        settings: The general settings.

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
            "scalex",
            "scaley",
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

        if settings["scalex"]:
            ax.set_xscale(settings["scalex"])

        if settings["scaley"]:
            ax.set_yscale(settings["scaley"])

        if settings["show_grid"]:
            ax.grid(axis=settings["show_grid"], **get_grid_style(style))

        # set the x-axis limit
        xmin, xmax = minimum(x), maximum(x)
        ax.set_xlim(xmin=xmin, xmax=xmax)

        # override axis limits
        configure_axis_ticks_position(ax, chart)
        configure_axis_limits(ax, settings)

        if "vlines" in chart:
            # draw vertical lines
            plot_vlines(ax, chart["vlines"])

        if "hlines" in chart:
            # draw horizontal lines
            plot_hlines(ax, chart["hlines"])

        # set the aspect ratio of the chart
        if settings["aspect_ratio"]:
            ax.set(adjustable="box", aspect=settings["aspect_ratio"])

    # show the legend in the last subplot
    if has_multi_subplots and settings["show_legend"]:
        warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")

    if not has_multi_subplots and settings["show_legend"]:
        axes[0].legend(title="Legend", **get_legend_style())


# ================================================
# Plot Bar Chart
# ================================================


def plot_bar_chart(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[BarSingleChartAttrs],
    settings: dict,
) -> None:
    """Plot the bar chart.

    Args:
        figure: The figure.
        axes: The axes list.
        charts: The charts data.
        settings: The general settings.

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
            "show_values",
            "value_format",
            "orientation",
            "scaley",
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
    x_width = config["plot_bar_width"] / charts.shape[0]  # the width of the bar
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
        bars = draw_func(
            x + x_offset,
            y + (1 if settings["scaley"] == "log" else 0),
            label=subtitle,
            **error_range,
            **bar_style,
        )

        # add bar value labels if enabled
        if settings.get("show_values"):
            value_fmt = settings.get("value_format", "{:.1f}")
            value_padding = style.get(
                "plot_bar_value_padding", config["plot_bar_value_padding"]
            )
            value_fontsize = style.get(
                "plot_bar_value_fontsize", config["plot_bar_value_fontsize"]
            )
            value_color = style.get(
                "plot_bar_value_color", config["plot_bar_value_color"]
            )
            ax.bar_label(
                bars,
                fmt=value_fmt,
                padding=value_padding,
                fontsize=value_fontsize,
                color=value_color,
            )

        if settings["scaley"]:
            ax.set_yscale(settings["scaley"])

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
            plot_vlines(ax, chart["vlines"])

        if "hlines" in chart:
            # draw horizontal lines
            plot_hlines(ax, chart["hlines"])

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
# Plot Histogram Chart
# ================================================


def plot_histogram(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[HistogramSingleChartAttrs],
    settings: dict,
) -> None:
    """Plot the histogram.

    Args:
        figure: The figure.
        axes: The axes list.
        charts: The charts data.
        settings: The general settings.

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
            "scaley",
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
            density=settings["show_density"],
            cumulative=settings["show_cumulative"],
            orientation=orientation,
            **hist_style,
        )

        if settings["scaley"]:
            axes[0].set_yscale(settings["scaley"])

        if "vlines" in chart:
            # draw vertical lines
            plot_vlines(axes[0], chart["vlines"])

        if "hlines" in chart:
            # draw horizontal lines
            plot_hlines(axes[0], chart["hlines"])

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
                density=settings["show_density"],
                cumulative=settings["show_cumulative"],
                orientation=orientation,
                **hist_style,
            )

            if settings["scaley"]:
                ax.set_yscale(settings["scaley"])

            if "vlines" in chart:
                # draw vertical lines
                plot_vlines(ax, chart["vlines"])

            if "hlines" in chart:
                # draw horizontal lines
                plot_hlines(ax, chart["hlines"])

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
# Plot Heatmap
# ================================================


def plot_heatmap(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[HeatmapChartAttrs],
    settings: dict,
) -> None:
    """Plot the heatmap.

    Args:
        figure: The figure.
        axes: The axes list.
        charts: The charts data.
        settings: The general settings.

    """

    # assert the configuration
    assert_chart_settings(
        settings=settings,
        supported_settings=[
            "aspect_ratio",
            "show_colorbars",
            "show_heatmap_values",
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

        if settings["show_heatmap_values"]:
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

            # Use inset_axes for colorbar - works with constrained_layout
            # and ensures colorbar matches chart height
            if orientation == ORIENTATION.VERTICAL:
                # [x, y, width, height] in axes fraction coordinates
                cax = ax.inset_axes([1.05, 0, 0.05, 1])
                figure.colorbar(im, cax=cax, orientation=orientation)
            else:
                cax = ax.inset_axes([0, 1.05, 1, 0.05])
                figure.colorbar(im, cax=cax, orientation=orientation)


# ================================================
# Plot Scatter Chart
# ================================================


def _normalize_sizes(sizes: np.ndarray, size_range: tuple) -> np.ndarray:
    """Normalize size values to the specified range.

    Args:
        sizes: The size values to normalize.
        size_range: The tuple of (min_size, max_size).

    Returns:
        The normalized size values.

    """
    min_size, max_size = size_range
    if sizes.max() == sizes.min():
        return np.full_like(sizes, (min_size + max_size) / 2, dtype=float)
    normalized = (sizes - sizes.min()) / (sizes.max() - sizes.min())
    return normalized * (max_size - min_size) + min_size


def _draw_correlation(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    color: str = None,
    position: str = "top_left",
) -> None:
    """Draw correlation coefficient annotation on the chart.

    Args:
        ax: The axes.
        x: The x-axis data.
        y: The y-axis data.
        color: The color of the annotation text.
        position: Position of the annotation ('top_left', 'top_right', 'bottom_left', 'bottom_right').

    """
    from ..stats import correlation

    r = correlation(x, y)

    # Set position coordinates based on position argument
    pos_map = {
        "top_left": (0.05, 0.95),
        "top_right": (0.95, 0.95),
        "bottom_left": (0.05, 0.05),
        "bottom_right": (0.95, 0.05),
    }
    ha_map = {
        "top_left": "left",
        "top_right": "right",
        "bottom_left": "left",
        "bottom_right": "right",
    }
    va_map = {
        "top_left": "top",
        "top_right": "top",
        "bottom_left": "bottom",
        "bottom_right": "bottom",
    }

    xy = pos_map.get(position, (0.05, 0.95))
    ha = ha_map.get(position, "left")
    va = va_map.get(position, "top")

    text_color = color if color else config.get("plot_text_color", "black")
    fontsize = config.get("plot_annotation_fontsize", 10)

    ax.annotate(
        f"r = {r:.3f}",
        xy=xy,
        xycoords="axes fraction",
        fontsize=fontsize,
        color=text_color,
        ha=ha,
        va=va,
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            edgecolor="gray",
            alpha=0.8,
        ),
    )


def _draw_regression(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    color: str = None,
    show_ci: bool = False,
    ci_level: float = 0.95,
) -> None:
    """Draw regression line with optional confidence interval.

    Args:
        ax: The axes.
        x: The x-axis data.
        y: The y-axis data.
        color: The color of the regression line.
        show_ci: Whether to show the confidence interval.
        ci_level: The confidence interval level.

    """
    from scipy import stats as scipy_stats

    # Check if all x values are identical - cannot calculate regression in this case
    if len(x) == 0 or len(np.unique(x)) <= 1:
        return

    # Fit linear regression
    slope, intercept, r_value, p_value, std_err = scipy_stats.linregress(x, y)

    # Create regression line
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept

    reg_style = get_regression_style({})
    if color is not None:
        reg_style["color"] = color

    ax.plot(x_line, y_line, **reg_style)

    if show_ci:
        # Calculate confidence interval
        n = len(x)
        t_val = scipy_stats.t.ppf((1 + ci_level) / 2, n - 2)

        # Standard error of the estimate
        y_pred = slope * x + intercept
        residuals = y - y_pred
        s_err = np.sqrt(np.sum(residuals**2) / (n - 2))

        # Confidence interval for the line
        x_mean = np.mean(x)
        ss_x = np.sum((x - x_mean) ** 2)

        se_line = s_err * np.sqrt(1 / n + (x_line - x_mean) ** 2 / ss_x)
        ci = t_val * se_line

        ci_alpha = config["plot_regression_ci_alpha"]
        ax.fill_between(
            x_line,
            y_line - ci,
            y_line + ci,
            alpha=ci_alpha,
            color=color,
        )


def plot_scatter_chart(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[ScatterSingleChartAttrs],
    settings: dict,
) -> None:
    """Plot the scatter chart.

    Args:
        figure: The figure.
        axes: The axes list.
        charts: The charts data.
        settings: The general settings.

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
            "show_regression",
            "show_ci",
            "ci_level",
            "show_correlation",
            "scalex",
            "scaley",
            "size_range",
        ],
    )

    has_multi_subplots = has_multiple_subplots(axes)

    for chart, ax in zip(charts, axes):
        # Retrieve chart data
        x_data = get_chart_data("x", chart)
        y_data = get_chart_data("y", chart)
        size_data = get_chart_data("size", chart)
        hue_data = get_chart_data("hue", chart)

        style = chart.get("style", {})
        scatter_style = get_scatter_style(style)

        # Handle hue grouping
        if hue_data is not None:
            unique_hues = np.unique(hue_data)
            n_hues = len(unique_hues)
            color_cycle = custom_color_cycle(False, n_hues)

            for i, hue_val in enumerate(unique_hues):
                mask = hue_data == hue_val
                x_group = x_data[mask]
                y_group = y_data[mask]

                # Get sizes for this group
                if size_data is not None:
                    size_range = settings["size_range"] or DEFAULT_SIZE_RANGE
                    sizes = _normalize_sizes(size_data[mask], size_range)
                else:
                    sizes = scatter_style.get("s", config["plot_scatter_size"])

                group_style = {k: v for k, v in scatter_style.items() if k != "s"}
                group_color = color_cycle[i]["color"]
                group_style["c"] = group_color

                ax.scatter(x_group, y_group, s=sizes, label=str(hue_val), **group_style)
        else:
            # No hue grouping - single scatter
            if size_data is not None:
                size_range = settings["size_range"] or DEFAULT_SIZE_RANGE
                sizes = _normalize_sizes(size_data, size_range)
            else:
                sizes = scatter_style.get("s", config["plot_scatter_size"])

            chart_hash = get_chart_hash(chart)
            color_cycle = custom_color_cycle(has_multi_subplots, charts.shape[0])
            base_style = {k: v for k, v in scatter_style.items() if k != "s"}
            # Use user-specified color (c) if provided, otherwise use color_cycle
            if "c" not in base_style or base_style["c"] is None:
                base_style["c"] = color_cycle[chart_hash]["color"]

            subtitle = chart.get("subtitle", None)
            ax.scatter(x_data, y_data, s=sizes, label=subtitle, **base_style)

            # Draw regression if requested
            if settings["show_regression"]:
                ci_level = settings["ci_level"] or DEFAULT_CI_LEVEL
                _draw_regression(
                    ax,
                    x_data,
                    y_data,
                    color=base_style.get("c", base_style.get("color")),
                    show_ci=settings["show_ci"],
                    ci_level=ci_level,
                )

            # Draw correlation annotation if requested
            if settings["show_correlation"]:
                _draw_correlation(
                    ax,
                    x_data,
                    y_data,
                    color=base_style.get("c", base_style.get("color")),
                )

        # Show overall correlation for hue-grouped data
        if hue_data is not None and settings["show_correlation"]:
            _draw_correlation(ax, x_data, y_data)

        # Show overall regression for hue-grouped data
        if hue_data is not None and settings["show_regression"]:
            ci_level = settings["ci_level"] or DEFAULT_CI_LEVEL
            _draw_regression(
                ax,
                x_data,
                y_data,
                show_ci=settings["show_ci"],
                ci_level=ci_level,
            )

        # Apply scales
        if settings["scalex"]:
            ax.set_xscale(settings["scalex"])
        if settings["scaley"]:
            ax.set_yscale(settings["scaley"])

        # Show grid
        if settings["show_grid"]:
            ax.grid(axis=settings["show_grid"], **get_grid_style(style))

        # Configure axis
        configure_axis_ticks_position(ax, chart)
        configure_axis_limits(ax, settings)

        # Draw vlines/hlines
        if "vlines" in chart:
            plot_vlines(ax, chart["vlines"])
        if "hlines" in chart:
            plot_hlines(ax, chart["hlines"])

        # Set aspect ratio
        if settings["aspect_ratio"]:
            ax.set(adjustable="box", aspect=settings["aspect_ratio"])

    # Show legend
    if has_multi_subplots and settings["show_legend"]:
        warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")

    if not has_multi_subplots and settings["show_legend"]:
        axes[0].legend(title="Legend", **get_legend_style())


# ================================================
# Plot Box Plot
# ================================================


def plot_box_plot(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[BoxSingleChartAttrs],
    settings: dict,
) -> None:
    """Plot the box plot.

    Args:
        figure: The figure.
        axes: The axes list.
        charts: The charts data.
        settings: The general settings.

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
            "show_outliers",
            "show_notch",
            "orientation",
        ],
    )

    has_multi_subplots = has_multiple_subplots(axes)

    # Box plots require subplots=True when multiple datasets are provided
    if charts.shape[0] > 1 and not has_multi_subplots:
        raise ValueError(
            "Multiple box plot datasets require `subplots=True`. "
            "Box plots do not support overlaying multiple datasets on a single axis."
        )

    orientation = settings.get("orientation", DEFAULT_ORIENTATION)
    show_outliers = settings.get("show_outliers", True)
    show_notch = settings.get("show_notch", False)

    color_cycle = custom_color_cycle(has_multi_subplots, charts.shape[0])

    for chart, ax in zip(charts, axes):
        # Get chart style attributes
        style = chart.get("style", {})

        # Retrieve chart data and group by label
        label_attr = get_attr_value("label", chart, "label")
        value_attr = get_attr_value("value", chart, "value")

        data = chart.get("data", [])
        if isinstance(data, list):
            # Group values by label
            grouped_data = {}
            for d in data:
                lbl = d.get(label_attr)
                val = d.get(value_attr)
                if lbl is not None and val is not None:
                    if lbl not in grouped_data:
                        grouped_data[lbl] = []
                    grouped_data[lbl].append(val)

            labels = list(grouped_data.keys())
            values = [grouped_data[lbl] for lbl in labels]
        else:
            labels = []
            values = []

        if len(values) == 0:
            warnings.warn("No data points found for box plot.")
            continue

        # Get style configurations
        chart_hash = get_chart_hash(chart)
        box_color = color_cycle[chart_hash].get("color")
        box_style = get_box_style(style)
        outlier_style = get_box_outlier_style(style)
        median_style = get_box_median_style(style)
        whisker_style = get_box_whisker_style(style)
        cap_style = get_box_cap_style(style)

        # Set default color if not specified
        if "facecolor" not in box_style or box_style.get("facecolor") is None:
            box_style["facecolor"] = box_color

        # Build boxplot props
        boxprops = {k: v for k, v in box_style.items() if v is not None}
        flierprops = {k: v for k, v in outlier_style.items() if v is not None}
        medianprops = {k: v for k, v in median_style.items() if v is not None}
        whiskerprops = {k: v for k, v in whisker_style.items() if v is not None}
        capprops = {k: v for k, v in cap_style.items() if v is not None}

        bp = ax.boxplot(
            values,
            orientation=orientation,
            patch_artist=True,
            showfliers=show_outliers if show_outliers is not None else True,
            notch=show_notch if show_notch is not None else False,
            boxprops=boxprops if boxprops else None,
            flierprops=flierprops if flierprops else None,
            medianprops=medianprops if medianprops else None,
            whiskerprops=whiskerprops if whiskerprops else None,
            capprops=capprops if capprops else None,
        )

        # Apply facecolor and alpha to each box patch
        alpha = box_style.get("alpha", 1.0)
        for patch in bp["boxes"]:
            if box_style.get("facecolor"):
                patch.set_facecolor(box_style["facecolor"])
            if alpha is not None:
                patch.set_alpha(alpha)

        # Set tick labels
        if orientation == ORIENTATION.HORIZONTAL:
            ax.set_yticks(range(1, len(labels) + 1))
            ax.set_yticklabels(labels)
        elif orientation == ORIENTATION.VERTICAL:
            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels)

        if settings["show_grid"]:
            ax.grid(axis=settings["show_grid"], **get_grid_style(style))

        # Draw vlines/hlines
        if "vlines" in chart:
            plot_vlines(ax, chart["vlines"])
        if "hlines" in chart:
            plot_hlines(ax, chart["hlines"])

        # Configure axis
        configure_axis_ticks_position(ax, chart)
        configure_axis_limits(ax, settings)

        # Set the aspect ratio of the chart
        if settings["aspect_ratio"]:
            ax.set(adjustable="box", aspect=settings["aspect_ratio"])

    # Show legend in the last subplot
    if has_multi_subplots and settings["show_legend"]:
        warnings.warn("The `show_legend` flag will be ignored for multi-subplots.")

    if not has_multi_subplots and settings["show_legend"]:
        axes[0].legend(title="Legend", **get_legend_style())


# ================================================
# Plot Parallel Coordinates
# ================================================


def plot_parallel_coords(
    figure: plt.Figure,
    axes: List[plt.Axes],
    charts: List[ParallelCoordsSingleChartAttrs],
    settings: dict,
) -> None:
    """Plots the parallel coordinates chart.

    Args:
        figure: The figure.
        axes: The axes list.
        charts: The charts data.
        settings: The general settings.

    """

    # assert the configuration
    assert_chart_settings(
        settings=settings,
        supported_settings=[
            "aspect_ratio",
            "show_legend",
            "show_grid",
        ],
    )

    # Parallel coordinates always use a single plot
    ax = axes[0]

    # Collect all data from all charts
    all_data = []
    all_hues = []
    all_styles = []

    for chart in charts:
        data = chart.get("data", [])
        hue_attr = chart.get("hue", "hue")
        style = chart.get("style", {})
        dimensions = chart.get("dimensions", None)

        for d in data:
            all_data.append(d)
            all_hues.append(d.get(hue_attr, None))
            all_styles.append(style)

    if len(all_data) == 0:
        warnings.warn("No data points found for parallel coordinates plot.")
        return

    # Determine dimensions from first data point if not specified
    first_chart = charts[0]
    dimensions = first_chart.get("dimensions", None)
    hue_attr = first_chart.get("hue", "hue")

    if dimensions is None:
        # Auto-detect dimensions from first data point (numeric and string, excluding hue)
        sample = all_data[0]
        dimensions = [k for k, v in sample.items() if k != hue_attr and v is not None]

    if len(dimensions) < 2:
        raise ValueError("Parallel coordinates requires at least 2 dimensions.")

    n_dims = len(dimensions)

    # Extract raw values for each dimension and determine if categorical
    dim_values_raw = {dim: [] for dim in dimensions}
    for d in all_data:
        for dim in dimensions:
            val = d.get(dim, None)
            dim_values_raw[dim].append(val)

    # Get category_orders if provided
    category_orders = first_chart.get("category_orders", None) or {}

    # Determine which dimensions are categorical vs numeric
    dim_is_categorical = {}
    dim_categories = {}  # For categorical dims: ordered list of unique values
    dim_category_map = {}  # For categorical dims: value -> normalized position

    for dim in dimensions:
        values = dim_values_raw[dim]
        # Check if any non-None value is a string
        non_none_values = [v for v in values if v is not None]
        if len(non_none_values) > 0 and isinstance(non_none_values[0], str):
            dim_is_categorical[dim] = True
            # Get unique categories
            unique_cats = set(v for v in values if v is not None)

            # Use custom order if provided, otherwise sort alphabetically
            if dim in category_orders:
                # Start with the specified order
                ordered_cats = [c for c in category_orders[dim] if c in unique_cats]
                # Add any remaining categories not in the order (sorted)
                remaining = sorted(unique_cats - set(ordered_cats))
                categories = ordered_cats + remaining
            else:
                categories = sorted(unique_cats)

            dim_categories[dim] = categories
            # Map categories to normalized positions
            if len(categories) == 1:
                dim_category_map[dim] = {categories[0]: 0.5}
            else:
                dim_category_map[dim] = {
                    cat: i / (len(categories) - 1) for i, cat in enumerate(categories)
                }
        else:
            dim_is_categorical[dim] = False

    # Convert values to normalized [0, 1] range
    dim_values = {}
    dim_min = {}
    dim_max = {}
    normalized = {}

    for dim in dimensions:
        if dim_is_categorical[dim]:
            # Map categorical values to normalized positions
            cat_map = dim_category_map[dim]
            normalized[dim] = np.array(
                [
                    cat_map.get(v, np.nan) if v is not None else np.nan
                    for v in dim_values_raw[dim]
                ]
            )
            dim_min[dim] = 0
            dim_max[dim] = len(dim_categories[dim]) - 1
        else:
            # Numeric dimension
            dim_values[dim] = np.array(
                [
                    v if v is not None and isinstance(v, (int, float)) else np.nan
                    for v in dim_values_raw[dim]
                ],
                dtype=float,
            )
            dim_min[dim] = np.nanmin(dim_values[dim])
            dim_max[dim] = np.nanmax(dim_values[dim])
            range_val = dim_max[dim] - dim_min[dim]
            if range_val == 0:
                normalized[dim] = np.zeros_like(dim_values[dim])
            else:
                normalized[dim] = (dim_values[dim] - dim_min[dim]) / range_val

    # Create color mapping for hue categories
    unique_hues = list(set(h for h in all_hues if h is not None))
    unique_hues.sort()

    # Get hue color palette from config
    hue_palette = config.get("color_parallel_hue", "Set1")

    if len(unique_hues) > 0:
        color_cycle = create_color_cycle(hue_palette, len(unique_hues))
        hue_colors = {hue: color_cycle[i]["color"] for i, hue in enumerate(unique_hues)}
        default_color = color_cycle[0]["color"]
    else:
        hue_colors = {}
        singular_cycle = create_color_cycle(hue_palette, 1)
        default_color = singular_cycle[0]["color"]

    # Set up x positions for the vertical axes
    x_positions = np.arange(n_dims)

    # Get shared style from first chart (used for axis, tick, and label styling)
    shared_style = charts[0].get("style", {}) if charts else {}

    # Get style configurations for axis, ticks, and labels
    axis_style = get_parallel_axis_style(shared_style)
    tick_style = get_parallel_tick_style(shared_style)
    tick_length = get_parallel_tick_length(shared_style)
    tick_label_style = get_parallel_tick_label_style(shared_style)
    tick_label_bbox = get_parallel_tick_label_bbox(shared_style)
    dim_label_style = get_parallel_dim_label_style(shared_style)
    dim_label_rotation = get_parallel_dim_label_rotation(shared_style)
    dim_label_pad = get_parallel_dim_label_pad(shared_style)

    # Draw lines for each data point
    for i, (data_point, hue_val, style) in enumerate(
        zip(all_data, all_hues, all_styles)
    ):
        y_vals = [normalized[dim][i] for dim in dimensions]

        # Determine color
        if hue_val is not None and hue_val in hue_colors:
            line_color = hue_colors[hue_val]
        else:
            line_color = default_color

        # Get style configuration
        line_style = get_parallel_coords_style(style)
        if "color" not in line_style or line_style.get("color") is None:
            line_style["color"] = line_color

        # Draw data lines
        ax.plot(x_positions, y_vals, **line_style)

    # Configure x-axis with dimension labels
    ax.set_xticks(x_positions)
    ax.set_xlim(-0.1, n_dims - 0.9)

    # Apply dimension label styling to x-axis tick labels
    ax.set_xticklabels(
        dimensions,
        rotation=dim_label_rotation,
        **dim_label_style,
    )

    # Set y-axis limits with padding to ensure edge tick marks are visible
    ax.set_ylim(-0.02, 1.02)
    ax.set_yticks([])

    # Remove all spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Hide x-axis tick marks but keep labels, apply dimension label padding
    ax.tick_params(axis="x", length=0, pad=dim_label_pad)

    # Draw vertical lines at each dimension position with tick marks
    for i, dim in enumerate(dimensions):
        # Draw vertical line only from 0 to 1 (not full y-axis range)
        ax.plot([i, i], [0, 1], **axis_style)

        # Position labels to the left for first axis, right for others
        is_first_axis = i == 0
        label_x_offset = -0.05 if is_first_axis else 0.05
        label_ha = "right" if is_first_axis else "left"

        def format_number(value):
            """Format number in human-readable way, avoiding scientific notation."""
            if value == 0:
                return "0"
            abs_val = abs(value)
            if abs_val >= 1000:
                return f"{value:,.0f}"
            elif abs_val >= 100:
                return f"{value:.1f}"
            elif abs_val >= 10:
                return f"{value:.1f}"
            elif abs_val >= 1:
                return f"{value:.2f}"
            elif abs_val >= 0.1:
                return f"{value:.2f}"
            else:
                return f"{value:.3f}"

        # Tick marks extend toward the label side
        if is_first_axis:
            tick_start, tick_end = i - tick_length, i
        else:
            tick_start, tick_end = i, i + tick_length

        # Get tick zorder (one above axis zorder)
        tick_zorder = axis_style.get("zorder", 2) + 1

        if dim_is_categorical[dim]:
            # For categorical dimensions, show category labels
            categories = dim_categories[dim]
            cat_map = dim_category_map[dim]

            for cat in categories:
                tick_pos = cat_map[cat]

                # Draw small horizontal tick mark
                ax.plot(
                    [tick_start, tick_end],
                    [tick_pos, tick_pos],
                    zorder=tick_zorder,
                    **tick_style,
                )

                # Add category label
                ax.text(
                    i + label_x_offset,
                    tick_pos,
                    str(cat),
                    ha=label_ha,
                    va="center",
                    bbox=tick_label_bbox,
                    zorder=tick_zorder + 1,
                    **tick_label_style,
                )
        else:
            # For numeric dimensions, show value labels at regular intervals
            tick_positions = [0.0, 0.25, 0.5, 0.75, 1.0]
            dim_range = dim_max[dim] - dim_min[dim]

            for tick_pos in tick_positions:
                # Draw small horizontal tick mark
                ax.plot(
                    [tick_start, tick_end],
                    [tick_pos, tick_pos],
                    zorder=tick_zorder,
                    **tick_style,
                )

                # Calculate actual value at this tick position
                if dim_range != 0:
                    actual_value = dim_min[dim] + tick_pos * dim_range
                else:
                    actual_value = dim_min[dim]

                # Add value label with human-readable format
                ax.text(
                    i + label_x_offset,
                    tick_pos,
                    format_number(actual_value),
                    ha=label_ha,
                    va="center",
                    bbox=tick_label_bbox,
                    zorder=tick_zorder + 1,
                    **tick_label_style,
                )

    if settings["show_grid"]:
        ax.grid(axis="x", **get_grid_style(shared_style))

    # Set the aspect ratio of the chart
    if settings["aspect_ratio"]:
        ax.set(adjustable="box", aspect=settings["aspect_ratio"])

    # Add legend for hue categories
    if settings["show_legend"] and len(unique_hues) > 0:
        legend_handles = [
            plt.Line2D([0], [0], color=hue_colors[hue], linewidth=2, label=hue)
            for hue in unique_hues
        ]
        ax.legend(handles=legend_handles, title="Legend", **get_legend_style())


# ================================================
# Chart Plotter Mapping
# ================================================

CHART_PLOTTERS = {
    "linechart": plot_line_chart,
    "barchart": plot_bar_chart,
    "histogram": plot_histogram,
    "heatmap": plot_heatmap,
    "scatterchart": plot_scatter_chart,
    "boxplot": plot_box_plot,
    "parallelcoords": plot_parallel_coords,
}
