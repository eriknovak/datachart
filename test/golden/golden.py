"""Golden-image regression harness for the Layer/Panel drawing seam (ADR 0001).

Usage:
    python test/golden/golden.py baseline   # render all cases into baseline/
    python test/golden/golden.py candidate  # render into candidate/ and diff vs baseline/
"""

import sys
import os
import hashlib
import warnings
from datetime import date, datetime, timedelta

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

from datachart.charts import (
    LineChart,
    CalendarHeatmap,
    BarChart,
    Histogram,
    ScatterChart,
    Heatmap,
    BoxPlot,
    SwarmPlot,
    ParallelCoords,
    PyramidChart,
    RadialChart,
    RaincloudPlot,
    RidgelinePlot,
    ViolinPlot,
    ContourChart,
    HexbinChart,
    StackedAreaChart,
    BumpChart,
    GanttChart,
    DumbbellChart,
    ScatterMatrix,
    SankeyChart,
    Treemap,
    NetworkChart,
    ImageChart,
    BasemapChart,
)
from datachart.utils import Panel, Grid, Annotate
from datachart.config import config
from datachart.constants import (
    ARROW_STYLE,
    ASPECT_RATIO,
    BASEMAP_FEATURE,
    BASEMAP_RESOLUTION,
    BUMP_LABEL_POSITION,
    BUMP_RANK,
    CALENDAR_WEEKDAY,
    COLORBAR_LOCATION,
    COLORS,
    CONTOUR_LEVELS,
    DATE_FORMAT,
    HEXBIN_REDUCE,
    HISTOGRAM_TYPE,
    DRAW_POSITION,
    LEGEND_LOCATION,
    NETWORK_LABEL_POSITION,
    NETWORK_LAYOUT,
    COLOR_NORM,
    AXIS_SCALE,
    SCATTER_MATRIX_DIAGONAL,
    SORT,
    STACKED_AREA_BASELINE,
    THEME,
    VALUE_FORMAT,
)
from datachart.utils.stats import kde1d, kde2d

# Cases whose output intentionally changed since the last published baseline.
EXPECTED_CHANGES = {
    # new basemap rivers and roads cases (ADR 0062)
    "basemap_rivers",
    "basemap_roads",
    # new basemap chart cases (ADR 0062)
    "basemap_default",
    "basemap_borders_lakes",
    "basemap_geometry",
    "basemap_geographic_aspect",
    "basemap_under_hexbin_in_grid",
    "basemap_countries_highlight",
    # new image chart cases (ADR 0060)
    "image_below_scatter",
    "image_above_line",
    "image_field_cmap",
    "image_panel_in_grid",
    # new pairwise bracket cases (#258)
    "raincloud_brackets_stacked",
    "box_horizontal_bracket",
    "panel_brackets_two_sources",
    # DEFAULT palette: softened Okabe–Ito, colour-blind safe on every pair
    "bar_horizontal",
    "bar_single",
    "bar_yerr_limits",
    "box_basic",
    "box_horizontal_notch",
    "grid_custom_layout",
    "grid_uniform_mixed",
    "hist_horizontal_density",
    "hist_single",
    "line_log",
    "line_single",
    "line_ticks",
    "line_yerr",
    "scatter_labels",
    "scatter_single",
    # new colour-blind-safe themes
    "theme_harbor_line",
    "theme_harbor_bar",
    "theme_muted_line",
    "theme_contrast_bar",
    "theme_mutedhatch_bar",
    "theme_slatehatch_bar",
    # new dark theme cases (ADR 0058)
    "theme_dark_line",
    "theme_dark_bar",
    "theme_dark_scatter",
    "theme_dark_heatmap",
    # new derived theme case (#245)
    "theme_derived_minimal_greens_bar",
    # palettes re-stepped so every predefined theme passes the gate (ADR 0073)
    "theme_greyscale_bar",
    # one lead hue per theme: DEFAULT reordered, PaperYlGnBu navy first, SKETCH vermilion first
    "line_multi",
    "bar_multi_grouped",
    "hist_multi_stacked",
    "scatter_hue_size",
    "overlay_zorder_grid",
    # theme renames: PUBLICATION -> INK (same style, new case name)
    "theme_ink_line",
    # new emphasis cases (ADR 0009)
    "emphasis_line_walks",
    "emphasis_line_walks_material",
    "emphasis_scatter_cohort",
    "emphasis_parallel_rows",
    "emphasis_parallel_composed",
    "emphasis_hist_reference",
    "emphasis_box_labels",
    "emphasis_panel_cross_type",
    # parallel tick labels take the theme font, then snap to round values (#211)
    "parallel_basic",
    # new quill theme cases (ADR 0048)
    "theme_quill_line",
    "theme_quill_bar_scatter",
    "theme_quill_heatmap_steps",
    "theme_quill_contour_relief",
    "theme_quill_network_treemap",
    # show_area now fills down to the axis floor instead of y=0
    "line_area_styled",
    # new panel axis-scale case (ADR 0041)
    "overlay_bar_linear_line_log",
    # new horizontal panel cases (ADR 0012)
    "overlay_horizontal_bar_line_dual",
    "overlay_horizontal_bar_bar_line",
    # new radial chart cases (ADR 0015)
    "radial_line",
    "radial_line_area_donut",
    "radial_bar",
    "radial_bar_stacked",
    "radial_scatter",
    "radial_hist_rose",
    "radial_panel_two",
    "radial_grid_mixed",
    "radial_bar_tip_labels",
    "radial_line_values",
    # new pyramid chart cases (ADR 0017)
    "pyramid_basic",
    "pyramid_values_xmax",
    "pyramid_styled_ticks",
    "pyramid_grid_pair",
    # nested/subplot grid cells now align their axes with the host columns
    "grid_with_overlay",
    "grid_subplot_figure",
    "grid_mixed_panel_and_grid",
    "grid_theme_mutation",
    # new text annotation cases (ADR 0018)
    "line_texts_annotated",
    "overlay_annotated",
    # new subplot-targeted Annotate case (#125)
    "subplots_annotated",
    # the scatter correlation box now wears the plot_text_* family (ADR 0018)
    "scatter_regression",
    # new swarm plot cases (ADR 0020)
    "swarm_vertical",
    "strip_horizontal",
    "box_swarm_overlay",
    "swarm_emphasis",
    # new violin plot cases (ADR 0019)
    "violin_basic",
    "violin_split_quartiles",
    "violin_horizontal_median",
    "violin_panel_box",
    # new raincloud plot cases (ADR 0021); the rain drops are too small for
    # the theme edge and draw solid
    "raincloud_vertical",
    "raincloud_horizontal",
    "raincloud_emphasis",
    # new ridgeline plot cases (ADR 0047)
    "ridgeline_basic",
    "ridgeline_sorted_overlap",
    "ridgeline_common",
    "ridgeline_vertical",
    "ridgeline_panel_swarm",
    # colorbars are placed by the layout engine instead of an inset (ADR 0022)
    "heatmap_basic",
    # new temporal axis cases (ADR 0037)
    "date_axis_daily_monthly_yearly",
    "date_axis_labels_and_references",
    # new heatmap label case (ADR 0023)
    "heatmap_labels",
    # new contour cases (ADR 0022)
    "contour_lines",
    "contour_filled_colorbar",
    "contour_labels",
    "contour_overlay",
    "contour_subplots",
    "contour_panel_scatter",
    "contour_grid",
    # new kernel density cases (ADR 0022)
    "contour_kde2d",
    "hist_kde1d",
    # new hexbin cases (ADR 0024)
    "hexbin_counts",
    "hexbin_log",
    "hexbin_c_mean",
    "hexbin_edges",
    "hexbin_subplots",
    "hexbin_panel_scatter",
    "hexbin_grid",
    # new stacked area cases (ADR 0025)
    "stackedarea_zero",
    "stackedarea_percent",
    "stackedarea_sym",
    "stackedarea_wiggle",
    "stackedarea_outline",
    "stackedarea_subplots",
    "stackedarea_panel_line",
    "stackedarea_grid",
    # new sankey cases (ADR 0026)
    "sankey_default",
    "sankey_explicit_nodes",
    "sankey_link_target",
    "sankey_subplots",
    "sankey_grid",
    "sankey_values_labels",
    # new treemap cases (ADR 0028); groups inset their children by the
    # gutter and records nest to four levels (ADR 0032)
    "treemap_flat",
    "treemap_nested",
    "treemap_emphasis",
    "treemap_values",
    "treemap_grid",
    "treemap_deep",
    # line-only panels hug the data range like line charts (ADR 0025)
    "overlay_line_line",
    "overlay_theme_snapshot",
    # panel grids sit below the marks, like single-chart grids
    "overlay_line_bar_dual",
    "overlay_auto_assign",
    "overlay_nested_panel",
    "overlay_hist_line",
    "overlay_bar_bar",
    "overlay_bar_bar_line",
    "overlay_hist_hist",
    # nested gridspecs size their parent cell (ADR 0007, issue #86)
    "grid_nested_grid",
    # new sketch theme cases (ADR 0027)
    "theme_sketch_line",
    "theme_sketch_bar",
    "grid_sketch_panel_twin",
    # new network cases (ADR 0029)
    "network_default",
    "network_directed_values",
    "network_grouped_legend",
    "network_straight",
    "network_circular_emphasis",
    "network_grid",
    # new network layouts (ADR 0030)
    "network_weighted",
    "network_grouped",
    # ARROW_STYLE.STRAIGHT annotation connector (ADR 0029)
    "annotate_arrow_straight",
    # new value label cases (ADR 0033); the labelling themes now label lines
    "values_line",
    "values_scatter_hue",
    "values_hist_stacked",
    "values_stackedarea",
    "values_box_horizontal",
    "values_violin_split",
    "values_panel_line_scatter",
    "values_theme_minimal_grid",
    "emphasis_line_walks_material",
    # every value label now wears the plot_value_halo_width stroke
    "bar_values",
    # new per-figure legend cases (ADR 0034)
    "legend_title",
    "legend_outside_right",
    "legend_multi_column",
    # new per-figure colorbar cases (ADR 0035)
    "colorbar_left_label",
    "colorbar_bottom_format",
    "colorbar_top_locked",
    "colorbar_right_ticks",
    "colorbar_grid_label",
    # new reference band cases (ADR 0036)
    "band_line_vspans_hspans",
    "band_bar_vspans_hspans",
    "band_labelled",
    "band_hatched",
    "band_half_open",
    "band_theme_ink",
    "band_radial_wedge",
    "band_radial_annulus",
    "band_grid_composed",
    # new category sort and emphasis rule cases (ADR 0042)
    "bar_sorted_grouped",
    "bar_rule_top3",
    # a blank heatmap cell no longer prints "nan" as its value (ADR 0044)
    "heatmap_blank_cells",
    # new calendar heatmap cases (ADR 0044)
    "calendar_single_year",
    "calendar_multi_year",
    "calendar_sunday_start",
    "calendar_grid",
    # new emphasis rule cases on every front (ADR 0045)
    "line_rule_by_max",
    "box_rule_median",
    "treemap_rule_top",
    "parallel_rule_hue",
    "heatmap_rule_above",
    "hexbin_rule_top",
    # new swarm and raincloud value label cases (#136)
    "values_swarm_vertical",
    "values_swarm_horizontal_strip",
    "values_raincloud",
    "values_theme_minimal_swarm_raincloud",
    # new bump chart cases (ADR 0046)
    "bump_default",
    "bump_given",
    "bump_both_curve",
    "bump_rule_top",
    "bump_panel",
    # new gantt chart cases (ADR 0049)
    "gantt_basic",
    "gantt_grouped_progress",
    "gantt_dependencies_today",
    "gantt_grid",
    "gantt_week_headers_milestone",
    "gantt_month_left_arrows",
    # new dumbbell chart cases (ADR 0050)
    "dumbbell_basic",
    "dumbbell_vertical_delta_sorted",
    "dumbbell_panel_two",
    "dumbbell_grid_themes",
    "dumbbell_direction_mixed",
    # new scatter matrix cases (ADR 0051)
    "matrix_default",
    "matrix_hue",
    "matrix_lower_only",
    "matrix_kde_correlation_regression",
    "matrix_blank_diagonal_grid",
    # reference lines draw over the marks (ADR 0054)
    "line_vlines_hlines",
    # diagonal reference lines (ADR 0055)
    "line_dlines",
    "panel_dlines_two_sources",
    # new filled-surface cases: log hexbin, level overflow, surface order
    "hexbin_log_scales",
    "contour_levels_overflow",
    "contour_filled_panel_line_ref",
    # layout fronts: shared dimensions, fixed inset, packed components
    "parallel_sets_dimensions",
    "network_fixed_inset",
    "network_spring_components",
    # colorbar fixes: tight-bbox locked bar, axis label beside its ticks
    "calendar_narrow_colorbar",
    "hexbin_bottom_bar_xlabel",
    # legend fixes: matrix legend edge, grid-cell title over the legend
    "matrix_legend_bottom",
    "grid_panel_title_outside_top_legend",
    # subplots draw from the series palette, like a single chart (#183)
    "line_multi_subplots",
    "bar_multi_subplots",
    "hist_multi_subplots",
    "scatter_multi_subplots",
    "stackedarea_subplots",
    # new step outline cases: the drops to zero that state nothing are gone
    # (#199, #198)
    "hist_step_log",
    "hist_step_cumulative",
    # new centred norm cases (ADR 0056)
    "heatmap_centered",
    "heatmap_twoslope",
    "calendar_centered",
    # new scatter error bar case (ADR 0057)
    "scatter_error_bars",
}


def _reset():
    np.random.seed(42)
    config.set_theme(THEME.DEFAULT)


LINE1 = [{"x": i, "y": i**2} for i in range(10)]
LINE2 = [{"x": i, "y": 5 * i + 3} for i in range(10)]
BAR1 = [{"label": c, "y": v} for c, v in zip("ABCDE", [10, 24, 17, 30, 22])]
BAR2 = [{"label": c, "y": v} for c, v in zip("ABCDE", [14, 18, 25, 12, 28])]
SCAT1 = [{"x": i, "y": 2 * i + ((i * 7) % 5) - 2} for i in range(20)]


def hist_data(n=200, mu=0.0, sigma=1.0):
    rng = np.random.RandomState(7)
    return [{"x": float(v)} for v in rng.randn(n) * sigma + mu]


CASES = {}


def case(fn):
    CASES[fn.__name__] = fn
    return fn


# ----- per-figure legend settings (ADR 0034) -----


@case
def legend_title():
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["sq", "lin"],
        show_legend=True,
        title="Legend title",
        legend={"title": "Series"},
    )


@case
def legend_outside_right():
    return BarChart(
        data=[BAR1, BAR2],
        subtitle=["a", "b"],
        show_legend=True,
        xlabel="x",
        ylabel="y",
        title="Legend outside right",
        legend={"location": LEGEND_LOCATION.OUTSIDE_RIGHT, "title": ""},
    )


@case
def legend_multi_column():
    return LineChart(
        data=[LINE1, LINE2, SCAT1, [{"x": i, "y": 40 - 3 * i} for i in range(10)]],
        subtitle=["sq", "lin", "saw", "fall"],
        show_legend=True,
        xlabel="x",
        ylabel="y",
        title="Legend multi-column",
        legend={"location": LEGEND_LOCATION.OUTSIDE_BOTTOM, "ncols": 4},
    )


# ----- single charts -----


@case
def line_single():
    return LineChart(data=LINE1, title="Line", xlabel="x", ylabel="y")


@case
def line_multi():
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["sq", "lin"],
        show_legend=True,
        show_grid="both",
        title="Lines",
    )


@case
def line_multi_subplots():
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["sq", "lin"],
        subplots=True,
        max_cols=2,
        title="Line subplots",
    )


@case
def line_yerr():
    data = [{"x": i, "y": i * 2, "yerr": 1 + 0.3 * i} for i in range(10)]
    return LineChart(data=data, show_yerr=True)


@case
def line_area_styled():
    style = {"plot_line_color": "#aa3355", "plot_line_style": "--"}
    return LineChart(data=LINE1, show_area=True, style=style)


@case
def line_vlines_hlines():
    return LineChart(
        data=LINE1,
        vlines={"x": 4, "label": "v"},
        hlines={"y": 40, "label": "h"},
        show_legend=True,
    )


@case
def line_dlines():
    return LineChart(
        data=LINE2,
        dlines=[
            {"label": "parity"},
            {"slope": 3, "intercept": 5, "xmin": 2, "xmax": 6, "label": "clipped"},
        ],
        show_legend=True,
        title="Unclipped and clipped diagonals",
    )


@case
def panel_dlines_two_sources():
    first = ScatterChart(
        data=SCAT1,
        subtitle="measured",
        dlines={"label": "parity"},
    )
    second = ScatterChart(
        data=[{"x": i, "y": 3 * i - 4} for i in range(20)],
        subtitle="modelled",
        dlines={"slope": 3, "intercept": -4, "label": "fit"},
    )
    return Panel([first, second], show_legend=True, title="Two sources, two diagonals")


@case
def line_log():
    data = [{"x": i, "y": 10**i} for i in range(1, 6)]
    return LineChart(data=data, scaley="log")


@case
def line_ticks():
    return LineChart(
        data=LINE1,
        xticks=[0, 3, 6, 9],
        xticklabels=["a", "b", "c", "d"],
        xtickrotate=45,
    )


@case
def bar_single():
    return BarChart(data=BAR1, title="Bar", show_grid="y")


@case
def bar_multi_grouped():
    return BarChart(
        data=[BAR1, BAR2], subtitle=["s1", "s2"], show_legend=True, title="Grouped"
    )


@case
def bar_multi_subplots():
    return BarChart(data=[BAR1, BAR2], subtitle=["s1", "s2"], subplots=True, max_cols=2)


@case
def bar_horizontal():
    return BarChart(data=BAR1, orientation="horizontal")


@case
def bar_values():
    return BarChart(data=BAR1, show_values=True, value_format="{:.0f}")


@case
def bar_sorted_grouped():
    return BarChart(
        data=[BAR1, BAR2],
        subtitle=["s1", "s2"],
        sort=SORT.DESCENDING,
        sort_by="s2",
        show_legend=True,
        title="Sorted by s2",
    )


@case
def bar_rule_top3():
    return BarChart(
        data=BAR1,
        emphasis_rule={"top": 3},
        show_values=True,
        value_format="{:.0f}",
        title="Top 3",
    )


@case
def bar_yerr_limits():
    data = [{"label": c, "y": v, "yerr": 2} for c, v in zip("ABC", [5, 9, 7])]
    return BarChart(data=data, show_yerr=True, ymin=0, ymax=12)


@case
def hist_single():
    return Histogram(data=hist_data(), num_bins=15)


@case
def hist_multi_stacked():
    return Histogram(
        data=[hist_data(150, 0.0), hist_data(150, 2.5)],
        subtitle=["a", "b"],
        num_bins=12,
        show_legend=True,
    )


@case
def hist_multi_subplots():
    return Histogram(
        data=[hist_data(150, 0.0), hist_data(150, 2.5)],
        subplots=True,
        max_cols=2,
        num_bins=12,
    )


@case
def hist_horizontal_density():
    return Histogram(
        data=hist_data(), orientation="horizontal", show_density=True, num_bins=10
    )


@case
def hist_step_log():
    # Gutenberg-Richter magnitudes: the tail leaves empty bins, and on a log
    # count axis the outline breaks over them instead of spiking to the floor
    rng = np.random.RandomState(42)
    data = [{"x": float(2.5 + m)} for m in rng.exponential(1 / np.log(10), 5000)]
    return Histogram(
        data=data,
        num_bins=40,
        scaley=AXIS_SCALE.LOG,
        style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
    )


@case
def hist_step_cumulative():
    # the running share ends at 1, with no drop back to zero
    return Histogram(
        data=hist_data(),
        num_bins=15,
        show_cumulative=True,
        show_density=True,
        style={"plot_hist_type": HISTOGRAM_TYPE.STEP},
    )


@case
def scatter_single():
    return ScatterChart(data=SCAT1, title="Scatter")


@case
def scatter_hue_size():
    data = [
        {"x": i, "y": (i * 3) % 11, "size": 10 + i, "hue": "grp" + str(i % 3)}
        for i in range(30)
    ]
    return ScatterChart(data=data, show_legend=True)


@case
def scatter_error_bars():
    # every second point carries an asymmetric y error, the rest a symmetric
    # one; the appended point carries none
    data = [
        {
            "x": i,
            "y": (i * 3) % 11,
            "hue": "grp" + str(i % 3),
            "xerr": 0.3,
            **({"yerr": [0.4, 1.6]} if i % 2 else {"yerr": 0.8}),
        }
        for i in range(12)
    ]
    data.append({"x": 12, "y": 5, "hue": "grp0"})
    return ScatterChart(data=data, show_legend=True, title="Scores with intervals")


@case
def scatter_regression():
    return ScatterChart(
        data=SCAT1, show_regression=True, show_ci=True, show_correlation=True
    )


@case
def scatter_labels():
    # neighbours crowd the right-hand spots, so labels must move around
    data = [
        {"x": i % 5 + (i // 5) * 0.35, "y": i // 5, "name": f"point {i}"}
        for i in range(15)
    ]
    return ScatterChart(
        data=data, label="name", show_regression=True, show_correlation=True
    )


@case
def scatter_multi_subplots():
    return ScatterChart(data=[SCAT1, LINE1], subplots=True, max_cols=2)


@case
def heatmap_basic():
    data = {"z": [[(i * j) % 7 for j in range(5)] for i in range(4)]}
    return Heatmap(data=data, show_values=True, show_colorbars=True)


@case
def heatmap_multi():
    d1 = [[(i + j) % 4 for j in range(4)] for i in range(4)]
    d2 = [[(i * j) % 5 for j in range(4)] for i in range(4)]
    return Heatmap(data=[{"z": d1}, {"z": d2}], subtitle=["m1", "m2"], max_cols=2)


@case
def heatmap_labels():
    data = {
        "x": ["mon", "tue", "wed", "thu", "fri"],
        "y": ["q1", "q2", "q3", "q4"],
        "z": [[(i * j) % 7 for j in range(5)] for i in range(4)],
    }
    return Heatmap(data=data, show_values=True, xtickrotate=45)


@case
def heatmap_blank_cells():
    data = {"z": [[1, None, 3], [None, 5, 6]]}
    return Heatmap(data=data, show_values=True, show_colorbars=True)


def signed_matrix():
    """A signed 5x5 matrix: a difference table running either side of zero."""
    rng = np.random.RandomState(11)
    return (rng.rand(5, 5) * 8 - 3).round(1).tolist()


@case
def heatmap_centered():
    data = {"z": signed_matrix()}
    return Heatmap(
        data=data,
        norm=COLOR_NORM.CENTERED,
        show_values=True,
        show_colorbars=True,
        title="Centred on zero",
    )


@case
def heatmap_twoslope():
    data = {"z": signed_matrix()}
    return Heatmap(
        data=data,
        norm=COLOR_NORM.TWOSLOPE,
        vmin=-3,
        vmax=5,
        show_values=True,
        show_colorbars=True,
        title="Two slopes about zero",
    )


@case
def box_basic():
    rng = np.random.RandomState(3)
    data = [
        {"label": lab, "value": float(v)}
        for lab in ["A", "B", "C"]
        for v in rng.randn(30) + {"A": 0, "B": 2, "C": 1}[lab]
    ]
    return BoxPlot(data=data, show_outliers=True)


def violin_data(seed=5, split=False):
    rng = np.random.RandomState(seed)
    data = []
    for lab, off in [("A", 0), ("B", 2), ("C", 1)]:
        for j, v in enumerate(rng.randn(40) + off):
            point = {"label": lab, "value": float(v)}
            if split:
                point["sex"] = "F" if j % 2 else "M"
            data.append(point)
    return data


@case
def violin_basic():
    return ViolinPlot(data=violin_data(), show_grid="y")


@case
def violin_split_quartiles():
    return ViolinPlot(
        data=violin_data(split=True),
        split="sex",
        inner="quartiles",
        show_legend=True,
        emphasis=["background", None, "highlight"],
    )


@case
def violin_horizontal_median():
    return ViolinPlot(
        data=violin_data(seed=6),
        orientation="horizontal",
        inner="median",
        bandwidth=0.3,
    )


@case
def violin_panel_box():
    data = violin_data(seed=7)
    return Panel(
        [ViolinPlot(data=data, inner=None), BoxPlot(data=data, show_outliers=False)],
        title="Violin + box",
    )


def ridgeline_data(seed=5):
    rng = np.random.RandomState(seed)
    return [
        {"label": month, "value": float(v)}
        for i, month in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
        for v in rng.randn(60) * (1.5 + i % 3) + 8 * np.sin(i / 2)
    ]


@case
def ridgeline_basic():
    return RidgelinePlot(data=ridgeline_data(), inner="median", title="Ridges")


@case
def ridgeline_sorted_overlap():
    return RidgelinePlot(
        data=ridgeline_data(seed=6),
        sort=SORT.DESCENDING,
        overlap=1.0,
        inner="quartiles",
        emphasis=["background", None, None, "highlight", None, None],
    )


@case
def ridgeline_common():
    return RidgelinePlot(
        data=ridgeline_data(seed=7),
        ridge_scale="common",
        fill=False,
        bandwidth=0.3,
    )


@case
def ridgeline_vertical():
    return RidgelinePlot(
        data=ridgeline_data(seed=8), orientation="vertical", show_outline=False
    )


@case
def ridgeline_panel_swarm():
    data = ridgeline_data(seed=9)
    return Panel(
        [RidgelinePlot(data=data), SwarmPlot(data=data, orientation="horizontal")],
        title="Ridges + swarm",
    )


@case
def box_horizontal_notch():
    rng = np.random.RandomState(4)
    data = [
        {"label": lab, "value": float(v)}
        for lab in ["A", "B"]
        for v in rng.randn(40) + {"A": 0, "B": 3}[lab]
    ]
    return BoxPlot(data=data, orientation="horizontal", show_notch=True)


def swarm_data(seed=5, n=45):
    rng = np.random.RandomState(seed)
    return [
        {"label": lab, "value": float(v)}
        for lab in ["A", "B", "C"]
        for v in rng.randn(n) * 2 + {"A": 10, "B": 12, "C": 16}[lab]
    ]


@case
def swarm_vertical():
    return SwarmPlot(data=swarm_data(), title="swarm", show_grid="y")


@case
def strip_horizontal():
    return SwarmPlot(data=swarm_data(), mode="strip", orientation="horizontal")


@case
def box_swarm_overlay():
    data = swarm_data()
    return Panel(
        [BoxPlot(data=data, show_outliers=False), SwarmPlot(data=data)],
        title="box + swarm",
    )


@case
def raincloud_vertical():
    return RaincloudPlot(data=swarm_data(), title="raincloud", show_legend=True)


@case
def raincloud_horizontal():
    return RaincloudPlot(
        data=swarm_data(seed=6), orientation="horizontal", mode="strip", show_grid="x"
    )


@case
def raincloud_emphasis():
    return RaincloudPlot(
        data=swarm_data(), emphasis=["background", None, "highlight"], bandwidth=0.3
    )


@case
def raincloud_brackets_stacked():
    return RaincloudPlot(
        data=swarm_data(),
        title="Pairwise comparisons",
        brackets=[
            {"from": "A", "to": "B", "text": "p = .03"},
            {"from": "B", "to": "C", "text": "p < .001"},
            {"from": "A", "to": "C", "text": "p < .001"},
        ],
    )


@case
def box_horizontal_bracket():
    return BoxPlot(
        data=swarm_data(seed=7),
        orientation="horizontal",
        brackets={"from": "A", "to": "C", "text": "ns"},
    )


@case
def panel_brackets_two_sources():
    data = swarm_data()
    return Panel(
        [
            BoxPlot(
                data=data,
                show_outliers=False,
                brackets={"from": "A", "to": "B", "text": "*"},
            ),
            SwarmPlot(data=data, brackets={"from": "B", "to": "C", "text": "**"}),
        ],
        title="box + swarm, bracketed",
    )


@case
def swarm_emphasis():
    return SwarmPlot(
        data=swarm_data(), emphasis=["background", None, "highlight"], subtitle="obs"
    )


@case
def parallel_sets_dimensions():
    rng = np.random.RandomState(6)
    sets = [
        [
            {"alpha": float(rng.rand() * 10), "beta": float(rng.rand()), "gamma": k}
            for _ in range(8)
        ]
        for k in range(2)
    ]
    return ParallelCoords(
        data=sets,
        dimensions=["gamma", "beta", "alpha"],
        style=[{"plot_parallel_color": "#c0c0c0"}, {"plot_parallel_color": "#0f7173"}],
    )


@case
def parallel_basic():
    rng = np.random.RandomState(5)
    data = [
        {
            "alpha": float(rng.rand() * 10),
            "beta": float(rng.rand() * 100),
            "cat": ["low", "mid", "high"][i % 3],
            "hue": "g" + str(i % 2),
        }
        for i in range(20)
    ]
    return ParallelCoords(
        data=data, dimensions=["alpha", "beta", "cat"], hue="hue", show_legend=True
    )


# ----- text annotations (ADR 0018) -----


@case
def line_texts_annotated():
    return LineChart(
        data=LINE1,
        title="Annotated",
        texts=[
            {"text": "curve look", "x": 1, "y": 55, "target": (6, 36)},
            {
                "text": "arrow look",
                "x": 0.55,
                "y": 0.2,
                "coords": "axes",
                "target": (8, 64),
                "style": {"plot_text_arrow_style": ARROW_STYLE.ARROW},
            },
            {
                "text": "boxless",
                "x": 0.05,
                "y": 0.9,
                "coords": "axes",
                "style": {"plot_text_box_visible": False},
            },
        ],
    )


@case
def overlay_annotated():
    fb = BarChart(data=BAR1)
    fl = LineChart(data=LINE2)
    panel = Panel([fb, fl], title="Annotated panel", show_legend=True)
    return Annotate(
        panel,
        {"text": "peak", "x": 0.75, "y": 0.85, "coords": "axes", "target": (3, 30)},
    )


@case
def subplots_annotated():
    figure = LineChart(
        data=[LINE1, LINE2, SCAT1],
        subtitle=["sq", "lin", "saw"],
        subplots=True,
        title="Annotated subplots",
        xlabel="x",
        ylabel="y",
    )
    return Annotate(
        figure,
        [
            {"text": "third only", "x": 0.05, "y": 0.9, "coords": "axes", "subplot": 2},
            {"text": "steep", "x": 1, "y": 60, "target": (8, 64), "subplot": 0},
        ],
    )


# ----- themes -----


@case
def theme_ink_line():
    config.set_theme(THEME.INK)
    return LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)


@case
def theme_greyscale_bar():
    config.set_theme(THEME.GREYSCALE)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


@case
def theme_sketch_line():
    config.set_theme(THEME.SKETCH)
    return LineChart(
        data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True, show_area=True
    )


@case
def theme_sketch_bar():
    config.set_theme(THEME.SKETCH)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


@case
def theme_harbor_line():
    config.set_theme(THEME.HARBOR)
    return LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)


@case
def theme_harbor_bar():
    config.set_theme(THEME.HARBOR)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


@case
def theme_muted_line():
    config.set_theme(THEME.MUTED)
    return LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)


@case
def theme_contrast_bar():
    config.set_theme(THEME.CONTRAST)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


@case
def theme_mutedhatch_bar():
    config.set_theme(THEME.MUTEDHATCH)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


@case
def theme_slatehatch_bar():
    config.set_theme(THEME.SLATEHATCH)
    return BarChart(data=[BAR1, BAR2], show_legend=True)


@case
def theme_quill_line():
    config.set_theme(THEME.QUILL)
    return LineChart(
        data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True, show_area=True
    )


@case
def theme_quill_bar_scatter():
    config.set_theme(THEME.QUILL)
    bars = BarChart(data=[BAR1, BAR2], subtitle=["a", "b"], show_legend=True)
    shifted = [{"x": p["x"], "y": p["y"] + 2} for p in SCAT1]
    scatter = ScatterChart(data=[SCAT1, shifted], subtitle=["c", "d"], show_legend=True)
    return Grid([[bars, scatter]], figsize=(9, 4))


@case
def theme_quill_heatmap_steps():
    config.set_theme(THEME.QUILL)
    data = {"z": [[(i * j) % 7 for j in range(5)] for i in range(4)]}
    return Heatmap(
        data=data,
        show_values=True,
        show_colorbars=True,
        colorbar={"label": "value"},
    )


@case
def theme_quill_contour_relief():
    config.set_theme(THEME.QUILL)
    grid = np.linspace(-2, 2, 40)
    z = [
        [
            float(np.exp(-(a * a + b * b)) - 0.5 * np.exp(-((a - 1) ** 2 + b * b)))
            for a in grid
        ]
        for b in grid
    ]
    return ContourChart(
        data={"x": list(grid), "y": list(grid), "z": z},
        filled=True,
        show_colorbars=True,
    )


@case
def theme_quill_network_treemap():
    config.set_theme(THEME.QUILL)
    network = NetworkChart(
        data={
            "nodes": [
                {"id": n, "group": g}
                for n, g in (("a", "x"), ("b", "x"), ("c", "y"), ("d", "y"))
            ],
            "edges": [
                {"source": s, "target": t, "weight": w}
                for s, t, w in (("a", "b", 3), ("b", "c", 1), ("c", "d", 2))
            ],
        },
        directed=True,
        layout=NETWORK_LAYOUT.GROUPED,
        show_legend=True,
    )
    treemap = Treemap(
        data={
            "data": [
                {
                    "label": "Asia",
                    "children": [
                        {"label": "India", "value": 14},
                        {"label": "China", "value": 14},
                    ],
                },
                {"label": "Africa", "value": 15},
            ]
        },
        show_legend=True,
    )
    return Grid([[network, treemap]], figsize=(9, 4))


@case
def theme_dark_line():
    config.set_theme(THEME.DARK)
    return LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)


@case
def theme_dark_bar():
    config.set_theme(THEME.DARK)
    return BarChart(data=[BAR1, BAR2], show_legend=True, show_values=True)


@case
def theme_dark_scatter():
    config.set_theme(THEME.DARK)
    shifted = [{"x": p["x"], "y": p["y"] + 4} for p in SCAT1]
    return ScatterChart(data=[SCAT1, shifted], show_legend=True)


@case
def theme_dark_heatmap():
    """The frame, separators and colorbar invert; a light cell keeps dark text."""
    config.set_theme(THEME.DARK)
    data = {"z": [[(i * j) % 7 for j in range(5)] for i in range(4)]}
    return Heatmap(
        data=data,
        show_values=True,
        show_colorbars=True,
        colorbar={"label": "value"},
    )


@case
def theme_derived_minimal_greens_bar():
    """MINIMAL furniture under a Greens lead: stepped series, Greens value scale."""
    from datachart.themes import derive_theme

    config.register_theme("forest", derive_theme(THEME.MINIMAL, lead=COLORS.Greens))
    config.set_theme("forest")
    return BarChart(data=[BAR1, BAR2], show_legend=True, show_values=True)


@case
def grid_sketch_panel_twin():
    """A sketch twin-axis panel keeps its look inside a grid built under DEFAULT."""
    config.set_theme(THEME.SKETCH)
    bars = BarChart(data=BAR1, subtitle="bars")
    line = LineChart(
        data=[{"x": i, "y": 1000 * (i + 1)} for i in range(5)], subtitle="line"
    )
    panel = Panel([bars, line], auto_secondary_axis=1, show_legend=True)
    scatter = ScatterChart(data=SCAT1, title="scatter")
    config.set_theme(THEME.DEFAULT)
    return Grid([[panel, scatter]], figsize=(9, 4))


# ----- emphasis (ADR 0009) -----


def walk_data(seed, n=40):
    rng = np.random.RandomState(seed)
    return [{"x": i, "y": float(v)} for i, v in enumerate(np.cumsum(rng.randn(n)))]


def _emphasis_walks():
    walks = [walk_data(seed) for seed in range(6)]
    return LineChart(
        data=walks,
        subtitle=[f"run {i}" for i in range(6)],
        emphasis=["background"] * 3 + [None, "highlight", "background"],
        show_legend=True,
        title="One walk among many",
    )


@case
def emphasis_line_walks():
    return _emphasis_walks()


@case
def emphasis_line_walks_material():
    config.set_theme(THEME.MATERIAL)
    return _emphasis_walks()


@case
def emphasis_scatter_cohort():
    cohort = [{"x": i, "y": 2 * i + (i * 3) % 5} for i in range(25)]
    rest = [{"x": i, "y": i + (i * 7) % 9} for i in range(25)]
    return ScatterChart(
        data=[rest, cohort],
        subtitle=["all points", "cohort"],
        emphasis=["background", "highlight"],
        show_legend=True,
    )


@case
def emphasis_parallel_rows():
    rng = np.random.RandomState(11)
    data = [
        {
            "speed": float(rng.rand() * 10),
            "cost": float(rng.rand() * 100),
            "score": float(rng.rand()),
        }
        for _ in range(15)
    ]
    best = [2, 7]
    return ParallelCoords(
        data=data,
        dimensions=["speed", "cost", "score"],
        emphasis=["highlight" if i in best else "background" for i in range(len(data))],
        title="Best runs",
    )


@case
def emphasis_parallel_composed():
    rng = np.random.RandomState(13)
    ctx = [{"a": float(rng.rand() * 5), "b": float(rng.rand() * 20)} for _ in range(12)]
    runs = [{"a": float(2 + i), "b": float(60 + 5 * i)} for i in range(3)]
    f1 = ParallelCoords(data=ctx, dimensions=["a", "b"])
    f2 = ParallelCoords(data=runs, dimensions=["a", "b"])
    return Panel(
        [{"figure": f1, "emphasis": "background"}, {"figure": f2}],
        title="Composed parallel",
    )


@case
def emphasis_hist_reference():
    return Histogram(
        data=[hist_data(300, 0.5, 1.4), hist_data(150, 2.0, 0.8)],
        subtitle=["reference", "cohort"],
        emphasis=["background", None],
        num_bins=18,
        show_legend=True,
    )


@case
def emphasis_box_labels():
    rng = np.random.RandomState(9)
    data = [
        {"label": lab, "value": float(v)}
        for lab in "ABCD"
        for v in rng.randn(30) + {"A": 0, "B": 2, "C": 1, "D": 3}[lab]
    ]
    return BoxPlot(data=data, emphasis=["background", None, "highlight", "background"])


@case
def emphasis_panel_cross_type():
    fh = Histogram(data=hist_data(), num_bins=20, subtitle="observations")
    xs = np.linspace(-3, 3, 50)
    fl = LineChart(
        data=[{"x": float(x), "y": float(30 * np.exp(-x * x / 2))} for x in xs],
        subtitle="trend",
    )
    return Panel(
        [
            {"figure": fh, "emphasis": "background"},
            {"figure": fl, "emphasis": "highlight"},
        ],
        title="Trend over observations",
        show_legend=True,
    )


# ----- value labels (ADR 0033) -----


@case
def values_line():
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["square", "linear"],
        show_values=True,
        value_format=VALUE_FORMAT.INTEGER,
        show_legend=True,
    )


@case
def values_scatter_hue():
    data = [
        {"x": p["x"], "y": p["y"], "hue": "even" if i % 2 == 0 else "odd"}
        for i, p in enumerate(SCAT1)
    ]
    return ScatterChart(data=data, hue="hue", show_values=True, value_step=2)


@case
def values_hist_stacked():
    return Histogram(
        data=[hist_data(), hist_data(mu=2.0)],
        subtitle=["a", "b"],
        num_bins=12,
        show_values=True,
        show_legend=True,
    )


@case
def values_stackedarea():
    return StackedAreaChart(
        data=stack_series(),
        subtitle=["a", "b", "c"],
        show_values=True,
        value_format=VALUE_FORMAT.DECIMAL,
        show_legend=True,
    )


@case
def values_box_horizontal():
    rng = np.random.RandomState(3)
    data = [
        {"label": lab, "value": float(v)}
        for lab in ["A", "B", "C"]
        for v in rng.randn(30) * 10 + {"A": 40, "B": 60, "C": 50}[lab]
    ]
    return BoxPlot(
        data=data,
        orientation="horizontal",
        show_values=True,
        value_format=VALUE_FORMAT.DECIMAL,
    )


@case
def values_violin_split():
    return ViolinPlot(
        data=violin_data(split=True),
        split="sex",
        show_values=True,
        value_format=VALUE_FORMAT.DECIMAL_2,
        show_legend=True,
    )


@case
def values_panel_line_scatter():
    line = LineChart(data=LINE2, show_values=True, value_format=VALUE_FORMAT.INTEGER)
    scatter = ScatterChart(data=SCAT1, show_values=True, value_step=3)
    return Panel([line, scatter], title="composed value labels")


@case
def values_theme_minimal_grid():
    config.set_theme(THEME.MINIMAL)
    line = LineChart(data=LINE2, title="line")
    hist = Histogram(data=hist_data(), num_bins=10, title="histogram")
    box = BoxPlot(
        data=[{"label": lab, "value": v} for lab in "AB" for v in range(1, 8)],
        title="box",
    )
    area = StackedAreaChart(data=stack_series(), title="area")
    return Grid([[line, hist], [box, area]], figsize=(10, 7))


@case
def values_swarm_vertical():
    return SwarmPlot(
        data=swarm_data(), show_values=True, value_format=VALUE_FORMAT.DECIMAL
    )


@case
def values_swarm_horizontal_strip():
    return SwarmPlot(
        data=swarm_data(seed=6),
        mode="strip",
        orientation="horizontal",
        show_values=True,
        value_format=VALUE_FORMAT.DECIMAL,
    )


@case
def values_raincloud():
    return RaincloudPlot(
        data=swarm_data(), show_values=True, value_format=VALUE_FORMAT.DECIMAL
    )


@case
def values_theme_minimal_swarm_raincloud():
    config.set_theme(THEME.MINIMAL)
    swarm = SwarmPlot(data=swarm_data(), title="swarm")
    rain = RaincloudPlot(data=swarm_data(), title="raincloud")
    return Grid([[swarm, rain]], figsize=(10, 4))


# ----- overlays -----


@case
def overlay_line_line():
    f1 = LineChart(data=LINE1, subtitle="sq")
    f2 = LineChart(data=LINE2, subtitle="lin")
    return Panel(
        charts=[{"figure": f1}, {"figure": f2}], title="Two lines", show_legend=True
    )


@case
def overlay_line_bar_dual():
    fb = BarChart(
        data=[{"label": c, "y": v * 100} for c, v in zip("ABCD", [1, 2, 3, 2])]
    )
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(4)])
    return Panel(
        charts=[
            {"figure": fb, "y_axis": "left"},
            {"figure": fl, "y_axis": "right", "legend_label": "trend"},
        ],
        title="Dual",
        xlabel="cat",
        ylabel_left="count",
        ylabel_right="value",
        show_legend=True,
    )


@case
def overlay_bar_linear_line_log():
    fb = BarChart(
        data=[{"label": c, "y": v} for c, v in zip("ABCD", [12, 30, 21, 26])],
        subtitle="count",
    )
    fl = LineChart(
        data=[{"x": i, "y": v} for i, v in enumerate([2, 40, 900, 15000])],
        subtitle="growth",
    )
    return Panel(
        charts=[{"figure": fb, "y_axis": "left"}, {"figure": fl, "y_axis": "right"}],
        scaley_right=AXIS_SCALE.LOG,
        title="Linear bars, log line",
        ylabel_left="count",
        ylabel_right="growth (log)",
        show_legend=True,
    )


@case
def overlay_auto_assign():
    fb = BarChart(data=[{"label": str(i), "y": i * 1000} for i in range(5)])
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(5)])
    return Panel(charts=[{"figure": fb}, {"figure": fl}], auto_secondary_axis=3.0)


@case
def overlay_nested_panel():
    fb = BarChart(
        data=[{"label": c, "y": v * 100} for c, v in zip("ABCD", [1, 2, 3, 2])]
    )
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(4)])
    inner = Panel(
        [
            {"figure": fb, "y_axis": "left"},
            {"figure": fl, "y_axis": "right", "legend_label": "trend"},
        ]
    )
    f2 = LineChart(data=[{"x": i, "y": i * 3} for i in range(4)], subtitle="extra")
    return Panel(
        [inner, f2],
        title="Nested",
        ylabel_left="count",
        ylabel_right="value",
        show_legend=True,
    )


@case
def overlay_hist_line():
    fh = Histogram(data=hist_data(), num_bins=20)
    xs = np.linspace(-3, 3, 50)
    fl = LineChart(
        data=[{"x": float(x), "y": float(30 * np.exp(-x * x / 2))} for x in xs]
    )
    return Panel(
        charts=[{"figure": fh, "y_axis": "left"}, {"figure": fl, "y_axis": "left"}],
        show_legend=True,
    )


@case
def overlay_zorder_grid():
    f1 = LineChart(data=LINE2, subtitle="l")
    f2 = ScatterChart(data=SCAT1, subtitle="s")
    return Panel(
        charts=[{"figure": f1, "z_order": 3}, {"figure": f2, "z_order": 2}],
        show_grid="both",
        show_legend=True,
        ymin=0,
        ymax=60,
    )


@case
def overlay_theme_snapshot():
    config.set_theme(THEME.INK)
    f1 = LineChart(data=LINE1, subtitle="pub")
    config.set_theme(THEME.DEFAULT)
    f2 = LineChart(data=LINE2, subtitle="def")
    return Panel(charts=[{"figure": f1}, {"figure": f2}], show_legend=True)


@case
def overlay_bar_bar():
    f1 = BarChart(data=BAR1, subtitle="s1")
    f2 = BarChart(data=BAR2, subtitle="s2")
    return Panel(charts=[{"figure": f1}, {"figure": f2}], show_legend=True)


@case
def overlay_bar_bar_line():
    f1 = BarChart(data=BAR1, subtitle="s1")
    f2 = BarChart(data=BAR2, subtitle="s2")
    f3 = LineChart(data=[{"x": i, "y": 20} for i in range(5)], subtitle="ref")
    return Panel(
        charts=[{"figure": f1}, {"figure": f2}, {"figure": f3}],
        bar_mode="stack",
        show_legend=True,
    )


@case
def overlay_horizontal_bar_line_dual():
    fb = BarChart(
        data=[{"label": c, "y": v * 100} for c, v in zip("ABCD", [1, 2, 3, 2])],
        orientation="horizontal",
        subtitle="count",
    )
    fl = LineChart(data=[{"x": i, "y": i * 2} for i in range(4)], subtitle="trend")
    return Panel(
        [{"figure": fb, "y_axis": "left"}, {"figure": fl, "y_axis": "right"}],
        title="Horizontal dual",
        xlabel="cat",
        ylabel_left="count",
        ylabel_right="value",
        ymin=0,
        ymin_right=0,
        show_legend=True,
    )


@case
def overlay_horizontal_bar_bar_line():
    f1 = BarChart(data=BAR1, orientation="horizontal", subtitle="s1")
    f2 = BarChart(data=BAR2, orientation="horizontal", subtitle="s2")
    f3 = LineChart(data=[{"x": i, "y": 20} for i in range(5)], subtitle="ref")
    return Panel([f1, f2, f3], bar_mode="stack", show_legend=True, show_grid="x")


@case
def overlay_hist_hist():
    f1 = Histogram(data=hist_data(150, 0.0), subtitle="a", num_bins=12)
    f2 = Histogram(data=hist_data(150, 2.0), subtitle="b", num_bins=12)
    return Panel(charts=[{"figure": f1}, {"figure": f2}], show_legend=True)


# ----- grids -----


@case
def grid_uniform_mixed():
    f1 = LineChart(data=LINE1, subtitle="line")
    f2 = BarChart(data=BAR1, subtitle="bar")
    f3 = ScatterChart(data=SCAT1, subtitle="scatter")
    f4 = Histogram(data=hist_data(), subtitle="hist", num_bins=10)
    return Grid(
        charts=[{"figure": f} for f in (f1, f2, f3, f4)],
        title="Grid",
        max_cols=2,
        figsize=(10, 8),
    )


@case
def grid_custom_layout():
    f1 = LineChart(data=LINE1)
    f2 = BarChart(data=BAR1)
    f3 = ScatterChart(data=SCAT1)
    return Grid(
        charts=[
            {
                "figure": f1,
                "layout_spec": {"row": 0, "col": 0, "rowspan": 1, "colspan": 2},
            },
            {
                "figure": f2,
                "layout_spec": {"row": 1, "col": 0, "rowspan": 1, "colspan": 1},
            },
            {
                "figure": f3,
                "layout_spec": {"row": 1, "col": 1, "rowspan": 1, "colspan": 1},
            },
        ],
        title="Custom",
        figsize=(10, 8),
    )


@case
def grid_with_overlay():
    fb = BarChart(data=BAR1, title="Bar")
    fl = LineChart(data=LINE2, title="Line")
    fo = Panel(
        charts=[{"figure": fb, "y_axis": "left"}, {"figure": fl, "y_axis": "right"}],
        title="Overlay",
        show_legend=True,
    )
    return Grid(
        charts=[{"figure": fb}, {"figure": fl}, {"figure": fo}],
        title="Grid+Overlay",
        max_cols=2,
        figsize=(10, 8),
    )


@case
def grid_subplot_figure():
    f = LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], subplots=True, max_cols=2)
    g = BarChart(data=BAR1)
    return Grid(charts=[{"figure": f}, {"figure": g}], max_cols=2, figsize=(10, 4))


@case
def grid_nested_grid():
    f1 = LineChart(data=LINE1, subtitle="line")
    f2 = BarChart(data=BAR1, subtitle="bar")
    f3 = ScatterChart(data=SCAT1, subtitle="scatter")
    f4 = Histogram(data=hist_data(), subtitle="hist", num_bins=10)
    inner = Grid([[f1, f2], [f3]], title="Inner", sharex=True)
    return Grid([inner, f4], title="Nested", figsize=(12, 5))


@case
def grid_mixed_panel_and_grid():
    fb = BarChart(data=BAR1, title="Bar")
    fl = LineChart(data=LINE2, title="Line")
    panel = Panel([fb, fl], title="Panel", show_legend=True)
    grid_fig = Grid([LineChart(data=LINE1), ScatterChart(data=SCAT1)], title="Sub")
    return Grid([panel, grid_fig], figsize=(12, 5))


COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
RAD1 = [{"label": d, "y": v} for d, v in zip(COMPASS, [4, 7, 6, 3, 5, 8, 2, 6])]
RAD2 = [{"label": d, "y": v} for d, v in zip(COMPASS, [6, 3, 5, 7, 2, 4, 8, 3])]


def wind_directions(n=200):
    rng = np.random.RandomState(11)
    return [{"x": float(v % 360)} for v in rng.vonmises(np.pi / 4, 2, n) * 180 / np.pi]


@case
def radial_line():
    return RadialChart(
        data=[RAD1, RAD2], subtitle=["a", "b"], show_legend=True, title="Radar"
    )


@case
def radial_line_area_donut():
    return RadialChart(data=RAD1, show_area=True, innerradius=0.25, startangle="E")


@case
def radial_bar():
    return RadialChart(data=RAD1, mark="bar", title="Circular bars", show_grid="both")


@case
def radial_bar_stacked():
    return RadialChart(
        data=[RAD1, RAD2],
        mark="bar",
        bar_mode="stack",
        subtitle=["a", "b"],
        show_legend=True,
    )


@case
def radial_scatter():
    return RadialChart(data=RAD1, mark="scatter", direction="counterclockwise")


@case
def radial_hist_rose():
    return RadialChart(data=wind_directions(), mark="histogram", num_bins=16)


@case
def radial_bar_tip_labels():
    labels = [f"Set {i + 1}" for i in range(16)]
    rng = np.random.RandomState(5)
    s1 = [{"label": l, "y": int(v)} for l, v in zip(labels, rng.randint(20, 80, 16))]
    s2 = [{"label": l, "y": int(v)} for l, v in zip(labels, rng.randint(10, 60, 16))]
    return RadialChart(
        data=[s1, s2],
        mark="bar",
        bar_mode="stack",
        show_tip_labels=True,
        show_border=False,
        innerradius=0.3,
        figsize=(7, 7),
    )


@case
def radial_line_values():
    return RadialChart(data=RAD1, show_values=True, value_format="%.0f")


@case
def radial_panel_two():
    f1 = RadialChart(data=RAD1, subtitle="a")
    f2 = RadialChart(data=RAD2, mark="bar", subtitle="b")
    return Panel([f2, f1], title="Radial panel", show_legend=True)


@case
def radial_grid_mixed():
    fr = RadialChart(data=RAD1, mark="bar", title="Rose")
    fl = LineChart(data=LINE1, title="Line")
    return Grid([fr, fl], max_cols=2, figsize=(10, 4))


def pyr_side(base, boom_age, boom_size, taper, phase):
    """A deterministic single-year age distribution: 80 bands per side."""
    return [
        {
            "label": str(age),
            "y": round(
                max(
                    base
                    - age * taper
                    + boom_size * np.exp(-((age - boom_age) ** 2) / 120)
                    + 55 * np.sin(age / 5.5 + phase),
                    40.0,
                ),
                1,
            ),
        }
        for age in range(80)
    ]


def pyr_bands(side, width=2):
    """Aggregate a single-year side into `width`-year bands."""
    return [
        {
            "label": f"{lo}-{lo + width - 1}",
            "y": round(sum(p["y"] for p in side[lo : lo + width]), 1),
        }
        for lo in range(0, len(side), width)
    ]


PYR1 = pyr_side(base=920, boom_age=31, boom_size=380, taper=6.5, phase=0.4)
PYR2 = pyr_side(base=860, boom_age=42, boom_size=430, taper=5.8, phase=2.1)


@case
def pyramid_basic():
    return PyramidChart(
        data=[PYR1, PYR2],
        subtitle=["Group A", "Group B"],
        title="Pyramid",
        xlabel="Residents",
        ylabel="Age",
        show_legend=True,
        yticks=list(range(0, 80, 10)),
    )


@case
def pyramid_values_xmax():
    return PyramidChart(
        data=[pyr_bands(PYR1), pyr_bands(PYR2)],
        show_values=True,
        value_format="%.0f",
        style={"plot_bar_value_fontsize": 6},
        xmax=2600,
        show_grid="x",
        figsize=(10, 8),
    )


@case
def pyramid_styled_ticks():
    styles = [{"plot_bar_hatch": "//"}, {"plot_bar_edge_color": "#222222"}]
    return PyramidChart(
        data=[pyr_bands(PYR1), pyr_bands(PYR2)],
        style=styles,
        xticks=[0, 1000, 2000],
        xticklabels=["0", "1k", "2k"],
    )


@case
def pyramid_grid_pair():
    fa = PyramidChart(
        data=[PYR1, PYR2],
        subtitle=["A", "B"],
        title="2010",
        yticks=list(range(0, 80, 10)),
    )
    fb = PyramidChart(
        data=[PYR2, PYR1],
        subtitle=["A", "B"],
        title="2020",
        yticks=list(range(0, 80, 10)),
    )
    return Grid([fa, fb], max_cols=2, figsize=(10, 4))


def contour_grid_data(f, lo=-5, hi=5, n=80):
    x = np.linspace(lo, hi, n)
    X, Y = np.meshgrid(x, x)
    return {"x": x, "y": x, "z": f(X, Y)}


def himmelblau(X, Y):
    return (X**2 + Y - 11) ** 2 + (X + Y**2 - 7) ** 2


def peaks(X, Y):
    return (
        3 * (1 - X) ** 2 * np.exp(-(X**2) - (Y + 1) ** 2)
        - 10 * (X / 5 - X**3 - Y**5) * np.exp(-(X**2) - Y**2)
        - np.exp(-((X + 1) ** 2) - Y**2) / 3
    )


def gauss_bump(mx, my, sx=1.2, sy=0.8):
    return lambda X, Y: np.exp(
        -((X - mx) ** 2 / (2 * sx**2) + (Y - my) ** 2 / (2 * sy**2))
    )


@case
def contour_lines():
    return ContourChart(data=contour_grid_data(himmelblau), title="Himmelblau")


@case
def contour_filled_colorbar():
    return ContourChart(
        data=contour_grid_data(peaks, -3, 3),
        filled=True,
        show_colorbars=True,
        levels=CONTOUR_LEVELS.FD,
    )


@case
def contour_labels():
    return ContourChart(
        data=contour_grid_data(himmelblau),
        show_labels=True,
        value_format="{x:.0f}",
        levels=CONTOUR_LEVELS.RICE,
    )


@case
def contour_overlay():
    return ContourChart(
        data=[
            contour_grid_data(gauss_bump(-1.5, -1)),
            contour_grid_data(gauss_bump(1.8, 1.2)),
        ],
        subtitle=["cluster A", "cluster B"],
        levels=6,
        show_legend=True,
        emphasis=[None, "highlight"],
    )


@case
def contour_subplots():
    return ContourChart(
        data=[
            contour_grid_data(himmelblau),
            contour_grid_data(
                lambda X, Y: np.log1p((1 - X) ** 2 + 100 * (Y - X**2) ** 2), -2, 2
            ),
            contour_grid_data(peaks, -3, 3),
        ],
        subtitle=["Himmelblau", "Rosenbrock (log z)", "Peaks"],
        filled=True,
        subplots=True,
        max_cols=3,
        figsize=(12, 4),
    )


@case
def contour_panel_scatter():
    rng = np.random.RandomState(1)
    pts = rng.normal((-1.5, -1), (1.0, 0.7), (200, 2))
    scatter = ScatterChart(
        data=[{"x": float(x), "y": float(y)} for x, y in pts], subtitle="points"
    )
    density = ContourChart(
        data=contour_grid_data(gauss_bump(-1.5, -1, 1.0, 0.7)),
        subtitle="density",
        levels=6,
    )
    return Panel([scatter, density], title="Panel", show_legend=True)


@case
def contour_grid():
    top = ContourChart(
        data=contour_grid_data(peaks, -3, 3),
        filled=True,
        show_colorbars=True,
        title="filled",
    )
    line = LineChart(data=LINE1, title="line")
    lines = ContourChart(
        data=contour_grid_data(himmelblau), show_labels=True, title="lines"
    )
    return Grid([[top], [line, lines]], figsize=(10, 7))


@case
def grid_theme_mutation():
    f1 = LineChart(data=[LINE1, LINE2], subtitle=["a", "b"], show_legend=True)
    config.set_theme(THEME.GREYSCALE)
    grid = Grid(charts=[{"figure": f1}], figsize=(6, 4))
    config.set_theme(THEME.DEFAULT)
    return grid


@case
def contour_kde2d():
    rng = np.random.RandomState(3)
    pts = np.vstack(
        [rng.normal((-1, -1), 0.6, (150, 2)), rng.normal((1.5, 1), 0.8, (100, 2))]
    )
    return ContourChart(
        data=kde2d(pts[:, 0].tolist(), pts[:, 1].tolist(), gridsize=60),
        filled=True,
        show_colorbars=True,
        levels=8,
    )


def hexbin_points(n=4000, seed=5):
    """Two gaussian clusters of unequal weight, as hexbin columns."""

    rng = np.random.RandomState(seed)
    pts = np.vstack(
        [
            rng.normal((-1.5, -1), (1.0, 0.7), (int(n * 0.7), 2)),
            rng.normal((2, 1.5), (0.8, 1.2), (n - int(n * 0.7), 2)),
        ]
    )
    return {"x": pts[:, 0].tolist(), "y": pts[:, 1].tolist()}


@case
def hexbin_counts():
    return HexbinChart(data=hexbin_points(), title="counts")


@case
def hexbin_log():
    return HexbinChart(data=hexbin_points(), norm=COLOR_NORM.LOG, mincnt=1)


@case
def hexbin_c_mean():
    data = hexbin_points()
    data["c"] = [x - y for x, y in zip(data["x"], data["y"])]
    return HexbinChart(
        data=data,
        reduce=HEXBIN_REDUCE.MEAN,
        style={"plot_hexbin_cmap": COLORS.RdBu},
        gridsize=20,
    )


@case
def hexbin_edges():
    return HexbinChart(
        data=hexbin_points(),
        style={"plot_hexbin_edge_width": 0.8, "plot_hexbin_edge_color": "#FFFFFF"},
        gridsize=15,
        show_colorbars=False,
    )


@case
def hexbin_subplots():
    return HexbinChart(
        data=[hexbin_points(seed=1), hexbin_points(seed=2)],
        subtitle=["run 1", "run 2"],
        subplots=True,
        max_cols=2,
        sharex=True,
        sharey=True,
        figsize=(10, 4),
    )


@case
def hexbin_panel_scatter():
    data = hexbin_points(n=1500)
    rng = np.random.RandomState(9)
    sample = rng.choice(len(data["x"]), 40, replace=False)
    scatter = ScatterChart(
        data=[{"x": data["x"][i], "y": data["y"][i]} for i in sample],
        subtitle="sample",
    )
    tiles = HexbinChart(
        data=data,
        style={"plot_hexbin_edge_width": 0.5, "plot_hexbin_edge_color": "#FFFFFF"},
        show_colorbars=False,
    )
    return Panel([tiles, scatter], title="Panel", show_legend=True)


@case
def hexbin_grid():
    top = HexbinChart(data=hexbin_points(), title="counts")
    line = LineChart(data=LINE1, title="line")
    data = hexbin_points()
    data["c"] = [x + y for x, y in zip(data["x"], data["y"])]
    right = HexbinChart(data=data, reduce=HEXBIN_REDUCE.MAX, title="max c")
    return Grid([[top], [line, right]], figsize=(10, 7))


@case
def hexbin_bottom_bar_xlabel():
    return HexbinChart(
        data=hexbin_points(),
        xlabel="Area (m2)",
        ylabel="Rent",
        colorbar={"label": "count", "location": COLORBAR_LOCATION.BOTTOM},
    )


@case
def hexbin_log_scales():
    rng = np.random.RandomState(4)
    xy = np.exp(rng.normal(0, 1, (3000, 2)))
    data = {"x": xy[:, 0].tolist(), "y": xy[:, 1].tolist()}
    return HexbinChart(data=data, scalex="log", scaley="log", gridsize=20)


def contour_bowl(n=40):
    x = np.linspace(-3, 3, n)
    X, Y = np.meshgrid(x, x)
    return {"x": x.tolist(), "y": x.tolist(), "z": (X**2 + Y**2).tolist()}


@case
def contour_levels_overflow():
    return ContourChart(data=contour_bowl(), filled=True, levels=[2, 4, 6, 8])


@case
def contour_filled_panel_line_ref():
    bowl = ContourChart(data=contour_bowl(), filled=True, hlines={"y": 1})
    line = LineChart(data=[{"x": x, "y": x / 2} for x in np.linspace(-3, 3, 13)])
    return Panel([bowl, line], title="surface under the line")


def stack_series(seed=3, n=12, k=3):
    """`k` smooth positive series over the same x, as stacked area input."""

    rng = np.random.RandomState(seed)
    return [
        [
            {"x": i, "y": float(v)}
            for i, v in enumerate(np.abs(rng.randn(n)).cumsum() + 1)
        ]
        for _ in range(k)
    ]


@case
def stackedarea_zero():
    return StackedAreaChart(
        data=stack_series(), subtitle=["a", "b", "c"], title="zero", show_legend=True
    )


@case
def stackedarea_percent():
    return StackedAreaChart(data=stack_series(), baseline=STACKED_AREA_BASELINE.PERCENT)


@case
def stackedarea_sym():
    return StackedAreaChart(data=stack_series(), baseline=STACKED_AREA_BASELINE.SYM)


@case
def stackedarea_wiggle():
    return StackedAreaChart(
        data=stack_series(k=4), baseline=STACKED_AREA_BASELINE.WIGGLE
    )


@case
def stackedarea_outline():
    return StackedAreaChart(
        data=stack_series(),
        style={"plot_stackedarea_outline": True, "plot_stackedarea_alpha": 0.5},
    )


@case
def stackedarea_subplots():
    return StackedAreaChart(
        data=stack_series(),
        subtitle=["a", "b", "c"],
        subplots=True,
        max_cols=3,
        sharey=True,
        figsize=(12, 3.5),
    )


@case
def stackedarea_panel_line():
    data = stack_series()
    total = [{"x": p[0]["x"], "y": sum(pt["y"] for pt in p)} for p in zip(*data)]
    return Panel(
        [
            StackedAreaChart(data=data, subtitle=["a", "b", "c"]),
            LineChart(data=total, subtitle="total"),
        ],
        title="Panel",
        show_legend=True,
    )


@case
def stackedarea_grid():
    top = StackedAreaChart(data=stack_series(), title="zero")
    left = StackedAreaChart(
        data=stack_series(), baseline=STACKED_AREA_BASELINE.PERCENT, title="percent"
    )
    right = LineChart(data=LINE1, title="line")
    return Grid([[top], [left, right]], figsize=(10, 7))


BUMP_NAMES = ["Ljubljana", "Maribor", "Celje", "Koper", "Kranj"]


def bump_series(seed=5, n=8, k=5, gap=True):
    """`k` noisy scores over `n` seasons; the fourth misses one season."""

    rng = np.random.RandomState(seed)
    return [
        [
            {"x": 2017 + i, "y": float(v)}
            for i, v in enumerate(rng.randint(40, 90, n))
            if not (gap and s == 3 and i == 4)
        ]
        for s in range(k)
    ]


@case
def bump_default():
    return BumpChart(
        data=bump_series(), subtitle=BUMP_NAMES, title="League", ylabel="Rank"
    )


@case
def bump_given():
    ranks = [[1, 2, 3, 1], [2, 1, 1, 3], [3, 3, 2, 2]]
    return BumpChart(
        data=[[{"x": i, "y": r} for i, r in enumerate(row)] for row in ranks],
        subtitle=["a", "b", "c"],
        rank_by=BUMP_RANK.GIVEN,
    )


@case
def bump_both_curve():
    return BumpChart(
        data=bump_series(),
        subtitle=BUMP_NAMES,
        label_position=BUMP_LABEL_POSITION.BOTH,
        line_curve=0.8,
        show_values=True,
    )


@case
def bump_rule_top():
    return BumpChart(data=bump_series(), subtitle=BUMP_NAMES, emphasis_rule={"top": 2})


@case
def bump_panel():
    lower = [[4, 5, 5, 4], [5, 4, 4, 5]]
    return Panel(
        [
            BumpChart(data=bump_series(n=4, k=3, gap=False), subtitle=BUMP_NAMES[:3]),
            BumpChart(
                data=[
                    [{"x": 2017 + i, "y": r} for i, r in enumerate(row)]
                    for row in lower
                ],
                subtitle=BUMP_NAMES[3:],
                rank_by=BUMP_RANK.GIVEN,
                line_curve=1,
            ),
        ],
        title="Panel",
    )


GANTT_START = date(2024, 3, 4)


def gantt_tasks(offset=0):
    """A small release plan: (task, group, start day, days, progress, depends_on)."""

    plan = [
        ("Scope", "Plan", 0, 6, 1.0, []),
        ("Design", "Plan", 4, 12, 0.8, ["Scope"]),
        ("Backend", "Build", 14, 24, 0.5, ["Design"]),
        ("Frontend", "Build", 18, 20, 0.3, ["Design"]),
        ("QA", "Ship", 38, 10, None, ["Backend", "Frontend"]),
        ("Launch", "Ship", 48, 3, None, ["QA"]),
    ]
    tasks = []
    for name, group, start, days, progress, depends_on in plan:
        begin = GANTT_START + timedelta(days=start + offset)
        record = {
            "task": name,
            "start": begin,
            "end": begin + timedelta(days=days),
            "group": group,
            "depends_on": depends_on,
        }
        if progress is not None:
            record["progress"] = progress
        tasks.append(record)
    return tasks


def without(records, *keys):
    return [{k: v for k, v in r.items() if k not in keys} for r in records]


@case
def gantt_basic():
    return GanttChart(
        without(gantt_tasks(), "group", "progress", "depends_on"),
        title="Release plan",
        xlabel="Date",
    )


@case
def gantt_grouped_progress():
    return GanttChart(
        without(gantt_tasks(), "depends_on"),
        sort=SORT.ASCENDING,
        sort_by="group",
        show_values=True,
        value_kind="progress",
        title="Grouped with progress",
    )


@case
def gantt_dependencies_today():
    return GanttChart(
        gantt_tasks(),
        show_dependencies=True,
        show_today=True,
        today=date(2024, 3, 30),
        show_values=True,
        value_kind="duration",
        emphasis_rule={"above": 11},
        xticks_format=DATE_FORMAT.ISO,
        xtickrotate=30,
        title="Dependencies and today",
    )


def gantt_with_milestone():
    tasks = gantt_tasks()
    tasks.append(
        {
            "task": "Beta",
            "start": date(2024, 4, 12),
            "end": date(2024, 4, 12),
            "group": "Ship",
            "depends_on": ["QA"],
        }
    )
    return tasks


@case
def gantt_week_headers_milestone():
    return GanttChart(
        gantt_with_milestone(),
        period="week",
        show_group_headers=True,
        show_values=True,
        value_kind="duration",
        show_today=True,
        today=date(2024, 3, 30),
        today_label="Today",
        title="Weeks, headers, milestone",
    )


@case
def gantt_month_left_arrows():
    return GanttChart(
        gantt_with_milestone(),
        period="month",
        show_dependencies=True,
        style={"plot_gantt_dependency_entry": "left"},
        title="Months, arrows from the left",
    )


@case
def gantt_grid():
    return Grid(
        [
            [
                GanttChart(gantt_tasks(), title="Plan"),
                GanttChart(
                    without(gantt_tasks(offset=7), "progress"),
                    show_dependencies=True,
                    title="Actual",
                ),
            ]
        ]
    )


# ----- dumbbell chart (ADR 0050) -----

DUMBBELL_LIFE = [
    ("Norway", 79.8, 83.2),
    ("Chile", 77.1, 81.2),
    ("India", 62.5, 70.9),
    ("Russia", 65.4, 65.4),
    ("Japan", 81.1, 84.4),
    ("Nigeria", 46.3, 54.7),
]


def dumbbell_records(rows=DUMBBELL_LIFE):
    return [{"label": label, "start": start, "end": end} for label, start, end in rows]


@case
def dumbbell_basic():
    return DumbbellChart(
        dumbbell_records(),
        start_name="2000",
        end_name="2019",
        show_values=True,
        value_kind="endpoints",
        xlabel="Life expectancy (years)",
        title="Life expectancy",
    )


@case
def dumbbell_vertical_delta_sorted():
    records = dumbbell_records()
    records[4]["emphasis"] = "highlight"
    return DumbbellChart(
        records,
        orientation="vertical",
        sort=SORT.DESCENDING,
        sort_by="delta",
        show_values=True,
        value_kind="delta",
        value_format="{:+.1f}",
        marker=("s", "o"),
        connector_style="--",
        emphasis_rule={"top": 3},
        title="Gain, largest first",
    )


@case
def dumbbell_direction_mixed():
    # 2019 to 2021: some countries fell, some rose, one held (WHO, rounded)
    rows = [
        ("Japan", 84.5, 84.5),
        ("Norway", 82.7, 82.9),
        ("Germany", 81.0, 80.5),
        ("United States", 78.7, 76.4),
        ("China", 77.3, 77.6),
        ("India", 70.7, 67.3),
    ]
    return Grid(
        [
            [
                DumbbellChart(
                    dumbbell_records(rows),
                    start_name="2019",
                    end_name="2021",
                    show_direction=True,
                    show_values=True,
                    value_kind="delta",
                    value_format="{:+.1f}",
                    title="Horizontal",
                ),
                DumbbellChart(
                    dumbbell_records(rows),
                    orientation="vertical",
                    show_direction=True,
                    show_values=True,
                    value_kind="endpoints",
                    title="Vertical",
                ),
            ]
        ]
    )


@case
def dumbbell_panel_two():
    women = [
        ("Norway", 81.6, 84.9),
        ("Chile", 80.1, 83.5),
        ("Brazil", 74.1, 79.6),
    ]
    return Panel(
        [
            DumbbellChart(
                dumbbell_records(DUMBBELL_LIFE[:3]),
                subtitle="Men",
                start_name="2000",
                end_name="2019",
            ),
            DumbbellChart(
                dumbbell_records(women),
                subtitle="Women",
                start_name="2000",
                end_name="2019",
            ),
        ],
        show_legend=True,
        title="Two dumbbell layers",
    )


@case
def dumbbell_grid_themes():
    figures = []
    for theme in (THEME.GREYSCALE, THEME.QUILL, THEME.SKETCH, THEME.MATERIAL):
        config.set_theme(theme)
        figures.append(
            DumbbellChart(
                dumbbell_records(DUMBBELL_LIFE[:4]),
                start_name="2000",
                end_name="2019",
                show_values=True,
                value_kind="endpoints",
                title=theme,
            )
        )
    config.set_theme(THEME.DEFAULT)
    return Grid([figures[:2], figures[2:]])


SANKEY_LABELS = [
    ("pos (A)", "pos (B)", 40),
    ("pos (A)", "neu (B)", 8),
    ("pos (A)", "neg (B)", 2),
    ("neu (A)", "neu (B)", 25),
    ("neu (A)", "pos (B)", 6),
    ("neu (A)", "neg (B)", 5),
    ("neg (A)", "neg (B)", 30),
    ("neg (A)", "neu (B)", 4),
    ("pos (B)", "pos", 44),
    ("pos (B)", "neu", 2),
    ("neu (B)", "neu", 33),
    ("neu (B)", "pos", 2),
    ("neu (B)", "neg", 2),
    ("neg (B)", "neg", 35),
    ("neg (B)", "neu", 2),
]
SANKEY_FUNNEL = [
    ("Visited", "Signed up", 300),
    ("Visited", "Bounced", 700),
    ("Signed up", "Activated", 180),
    ("Signed up", "Churned", 120),
    ("Activated", "Paid", 90),
    ("Activated", "Free tier", 90),
]


def sankey_links(rows):
    return {"links": [{"source": s, "target": t, "value": v} for s, t, v in rows]}


@case
def sankey_default():
    return SankeyChart(sankey_links(SANKEY_LABELS), title="Label transitions")


@case
def sankey_explicit_nodes():
    return SankeyChart(
        sankey_links(SANKEY_FUNNEL),
        nodes=[
            ["Visited"],
            ["Bounced", "Signed up"],
            ["Churned", "Activated"],
            ["Free tier", "Paid"],
        ],
    )


@case
def sankey_link_target():
    return SankeyChart(
        sankey_links(SANKEY_FUNNEL),
        style={"plot_sankey_link_color": "target", "plot_sankey_link_alpha": 0.6},
    )


@case
def sankey_subplots():
    return SankeyChart(
        [sankey_links(SANKEY_LABELS), sankey_links(SANKEY_FUNNEL)],
        subtitle=["labels", "funnel"],
        subplots=True,
        figsize=(12, 4),
    )


@case
def sankey_values_labels():
    return SankeyChart(
        sankey_links(SANKEY_FUNNEL),
        column_labels=["Visit", "Signup", "Activation", "Plan"],
        show_values=True,
        value_format=VALUE_FORMAT.INTEGER,
        title="Signup funnel",
    )


@case
def sankey_grid():
    left = SankeyChart(sankey_links(SANKEY_FUNNEL), title="funnel")
    right = LineChart(data=LINE1, title="line")
    return Grid([[left, right]], figsize=(10, 4))


TREEMAP_BUDGET = [
    ("Salaries", 520),
    ("Cloud", 180),
    ("Marketing", 140),
    ("Office", 90),
    ("Travel", 45),
    ("Legal", 25),
]
TREEMAP_WORLD = {
    "Asia": [
        ("India", 1429),
        ("China", 1426),
        ("Indonesia", 278),
        ("Pakistan", 240),
        ("Bangladesh", 173),
        ("Japan", 123),
        ("Rest of Asia", 1084),
    ],
    "Africa": [
        ("Nigeria", 224),
        ("Ethiopia", 127),
        ("Egypt", 113),
        ("DR Congo", 102),
        ("Rest of Africa", 895),
    ],
    "Europe": [
        ("Russia", 144),
        ("Germany", 83),
        ("UK", 68),
        ("France", 65),
        ("Rest of Europe", 382),
    ],
    "N. America": [("USA", 340), ("Mexico", 128), ("Rest", 132)],
    "S. America": [("Brazil", 216), ("Rest", 220)],
    "Oceania": [("Australia", 26), ("Rest", 19)],
}


def treemap_records(rows, emphasis=None):
    emphasis = emphasis or {}
    records = []
    for label, value in rows:
        record = {"label": label, "value": value}
        if label in emphasis:
            record["emphasis"] = emphasis[label]
        records.append(record)
    return records


def treemap_world(emphasis=None):
    emphasis = emphasis or {}
    records = []
    for group, rows in TREEMAP_WORLD.items():
        record = {"label": group, "children": treemap_records(rows, emphasis)}
        if group in emphasis:
            record["emphasis"] = emphasis[group]
        records.append(record)
    return {"data": records}


@case
def treemap_flat():
    return Treemap({"data": treemap_records(TREEMAP_BUDGET)}, title="Budget")


@case
def treemap_nested():
    return Treemap(
        treemap_world(),
        title="World population by continent and country",
        figsize=(8, 4.5),
    )


@case
def treemap_emphasis():
    return Treemap(
        treemap_world(
            {"Asia": "background", "India": "highlight", "Europe": "highlight"}
        ),
        show_legend=True,
        figsize=(8, 4.5),
    )


@case
def treemap_values():
    return Treemap(
        treemap_world(),
        show_values=True,
        value_format=VALUE_FORMAT.INTEGER,
        figsize=(8, 4.5),
    )


# a home directory four levels deep, in gigabytes
TREEMAP_HOME = {
    "Projects": {
        "datachart": {"docs": 14, "src": 6, ".venv": 22, "test": 3},
        "thesis": {"figures": 18, "chapters": 4, "data": 31},
        "scratch": {"notes": 3, "tmp": 6},
    },
    "Media": {
        "Photos": {"2024": 38, "2025": 52, "raw": 61},
        "Videos": 47,
        "Music": 12,
    },
    "Library": {"Caches": 28, "Mail": {"Inbox": 3, "Archive": 2}, "Fonts": 2},
    "Downloads": 24,
    "Desktop": 5,
}


def treemap_tree(tree):
    """Nested dicts as treemap records: a number is a leaf, a dict a group."""
    return [
        (
            {"label": label, "value": value}
            if not isinstance(value, dict)
            else {"label": label, "children": treemap_tree(value)}
        )
        for label, value in tree.items()
    ]


@case
def treemap_deep():
    return Treemap(
        {"data": treemap_tree(TREEMAP_HOME)},
        title="Home folder, GB",
        show_values=True,
        value_format=VALUE_FORMAT.INTEGER,
        figsize=(8, 5),
    )


def calendar_days(year, seed):
    """One value per day of `year`: weekday commits with a summer lull."""
    rng = np.random.RandomState(seed)
    first = date(year, 1, 1)
    n_days = (date(year + 1, 1, 1) - first).days
    days = [first + timedelta(days=i) for i in range(n_days)]
    values = [
        int(
            rng.poisson(3.0 if d.weekday() < 5 else 0.7)
            * (0.5 if d.month in (7, 8) else 1)
        )
        for d in days
    ]
    return days, values


@case
def calendar_single_year():
    days, values = calendar_days(2024, seed=4)
    return CalendarHeatmap(
        {"date": days, "value": values},
        title="Commits, 2024",
        show_colorbars=True,
        colorbar={"label": "commits", "location": COLORBAR_LOCATION.BOTTOM},
        figsize=(9, 2.6),
    )


@case
def calendar_multi_year():
    d1, v1 = calendar_days(2023, seed=5)
    d2, v2 = calendar_days(2024, seed=6)
    return CalendarHeatmap(
        {"date": d1 + d2, "value": v1 + v2},
        subtitle="commits",
        title="Two years",
        norm=COLOR_NORM.ASINH,
        figsize=(9, 4.4),
    )


@case
def calendar_sunday_start():
    days, values = calendar_days(2024, seed=4)
    # the first quarter, valued: the values print in the cells
    quarter = [(d, v) for d, v in zip(days, values) if d.month <= 3]
    return CalendarHeatmap(
        {"date": [d for d, _ in quarter], "value": [v for _, v in quarter]},
        week_start=CALENDAR_WEEKDAY.SUNDAY,
        show_values=True,
        style={"plot_calendar_heatmap_cmap": COLORS.Greens},
        title="Q1 2024, weeks from Sunday",
        figsize=(9, 2.6),
    )


@case
def calendar_centered():
    days, values = calendar_days(2024, seed=4)
    # the daily departure from the year's mean: a signed anomaly about zero
    mean = sum(values) / len(values)
    quarter = [(d, round(v - mean, 1)) for d, v in zip(days, values) if d.month <= 3]
    return CalendarHeatmap(
        {"date": [d for d, _ in quarter], "value": [v for _, v in quarter]},
        norm=COLOR_NORM.CENTERED,
        show_colorbars=True,
        title="Q1 2024, daily anomaly",
        figsize=(9, 2.6),
    )


@case
def calendar_grid():
    days, values = calendar_days(2024, seed=4)
    left = CalendarHeatmap({"date": days, "value": values}, title="per day")
    right = LineChart(data=LINE1, title="line")
    return Grid([[left, right]], figsize=(12, 3))


@case
def calendar_narrow_colorbar():
    days, values = calendar_days(2024, seed=4)
    return CalendarHeatmap(
        {"date": days[:60], "value": values[:60]},
        title="Two months",
        show_colorbars=True,
        colorbar={"label": "commits"},
    )


@case
def treemap_grid():
    left = Treemap(treemap_world(), title="population")
    right = LineChart(data=LINE1, title="line")
    return Grid([[left, right]], figsize=(10, 4))


NETWORK_DEPS = [
    ("core", "utils"),
    ("cli", "core"),
    ("api", "core"),
    ("api", "auth"),
    ("auth", "utils"),
    ("web", "api"),
    ("web", "ui"),
    ("ui", "utils"),
    ("tests", "core"),
    ("tests", "api"),
    ("docs", "cli"),
]
NETWORK_FLOWS = [
    ("Alpha", "Beta", 8),
    ("Alpha", "Gamma", 3),
    ("Beta", "Gamma", 5),
    ("Beta", "Delta", 2),
    ("Gamma", "Delta", 7),
    ("Delta", "Alpha", 1),
    ("Gamma", "Epsilon", 4),
    ("Epsilon", "Beta", 2),
]
NETWORK_PEOPLE = {
    "Ana": ("Design", 30),
    "Bo": ("Design", 12),
    "Cy": ("Eng", 45),
    "Di": ("Eng", 20),
    "Ed": ("Eng", 8),
    "Fay": ("Ops", 25),
    "Gus": ("Ops", 10),
    "Hal": ("Design", 18),
}
NETWORK_TIES = [
    ("Ana", "Bo"),
    ("Ana", "Cy"),
    ("Cy", "Di"),
    ("Cy", "Ed"),
    ("Di", "Ed"),
    ("Cy", "Fay"),
    ("Fay", "Gus"),
    ("Ana", "Hal"),
    ("Hal", "Bo"),
    ("Fay", "Di"),
    ("Gus", "Ed"),
]


def network_edges(pairs):
    return [
        {"source": p[0], "target": p[1], **({"weight": p[2]} if len(p) > 2 else {})}
        for p in pairs
    ]


def network_team(emphasis=None):
    return {
        "nodes": [
            {
                "id": k,
                "group": g,
                "size": s,
                **({"emphasis": emphasis[k]} if emphasis and k in emphasis else {}),
            }
            for k, (g, s) in NETWORK_PEOPLE.items()
        ],
        "edges": network_edges(NETWORK_TIES),
    }


@case
def network_default():
    return NetworkChart(
        {"edges": network_edges(NETWORK_DEPS)}, title="Module dependencies"
    )


@case
def network_directed_values():
    return NetworkChart(
        {"edges": network_edges(NETWORK_FLOWS)},
        directed=True,
        show_values=True,
        title="Directed flows",
    )


@case
def network_grouped_legend():
    return NetworkChart(network_team(), show_legend=True, title="Team ties")


@case
def network_weighted():
    return NetworkChart(
        {"edges": network_edges(NETWORK_FLOWS)},
        layout=NETWORK_LAYOUT.WEIGHTED,
        show_values=True,
        title="Weighted pull",
    )


@case
def network_grouped():
    team = network_team()
    # one node without a group: its own cluster, in the edge color
    team["nodes"].append({"id": "Ivy", "size": 15})
    team["edges"].append({"source": "Ivy", "target": "Cy", "weight": 3})
    for record in team["edges"][:4]:
        record["weight"] = 6
    return NetworkChart(
        team, layout=NETWORK_LAYOUT.GROUPED, show_legend=True, title="Grouped"
    )


@case
def network_straight():
    return NetworkChart(
        {"edges": network_edges(NETWORK_FLOWS)},
        directed=True,
        show_values=True,
        style={"plot_network_edge_style": ARROW_STYLE.STRAIGHT},
    )


@case
def network_circular_emphasis():
    return NetworkChart(
        network_team({"Cy": "highlight", "Gus": "background", "Bo": "background"}),
        layout=NETWORK_LAYOUT.CIRCULAR,
        directed=True,
    )


@case
def network_grid():
    left = NetworkChart(network_team(), show_legend=True, title="team")
    right = LineChart(data=LINE1, title="line")
    return Grid([[left, right]], figsize=(10, 4))


@case
def network_fixed_inset():
    corners = {"A": (0, 0), "B": (1, 0), "C": (1, 1), "D": (0, 1), "E": (0.5, 0.5)}
    return NetworkChart(
        {
            "nodes": [{"id": k, "x": x, "y": y} for k, (x, y) in corners.items()],
            "edges": network_edges([("A", "E"), ("B", "E"), ("C", "E"), ("D", "E")]),
        },
        layout=NETWORK_LAYOUT.FIXED,
        label_position=NETWORK_LABEL_POSITION.ABOVE,
        texts={"text": "corner", "x": 0.7, "y": 0.8, "target": (1, 1)},
        title="Fixed corners",
    )


@case
def network_spring_components():
    pairs = NETWORK_TIES + [("P", "Q"), ("Q", "R"), ("R", "P"), ("S", "T")]
    ids = dict.fromkeys([k for pair in pairs for k in pair] + ["Lone", "Solo"])
    data = {"nodes": [{"id": k} for k in ids], "edges": network_edges(pairs)}
    return NetworkChart(data, title="Components and isolates")


@case
def annotate_arrow_straight():
    return LineChart(
        data=LINE1,
        texts={
            "text": "note",
            "x": 0.3,
            "y": 0.8,
            "coords": "axes",
            "target": (6, 36),
            "style": {"plot_text_arrow_style": ARROW_STYLE.STRAIGHT},
        },
    )


@case
def hist_kde1d():
    values = [p["x"] for p in hist_data(300)]
    return Panel(
        [
            Histogram(data=hist_data(300), subtitle="binned", show_density=True),
            LineChart(data=kde1d(values), subtitle="kde", show_area=True),
        ],
        show_legend=True,
    )


# ----- per-figure colorbar settings (ADR 0035) -----


@case
def colorbar_left_label():
    data = {"z": [[(i * j) % 7 for j in range(6)] for i in range(5)]}
    return Heatmap(
        data=data,
        show_colorbars=True,
        colorbar={"label": "Residual", "location": COLORBAR_LOCATION.LEFT},
    )


@case
def colorbar_bottom_format():
    return ContourChart(
        data=contour_grid_data(peaks, -3, 3),
        filled=True,
        show_colorbars=True,
        colorbar={
            "label": "Height",
            "location": COLORBAR_LOCATION.BOTTOM,
            "format": "{x:.1f}",
        },
    )


@case
def colorbar_top_locked():
    return HexbinChart(
        data=hexbin_points(),
        aspect_ratio=ASPECT_RATIO.EQUAL,
        colorbar={"label": "Points", "location": COLORBAR_LOCATION.TOP},
    )


@case
def colorbar_right_ticks():
    data = {"z": [[(i * j) % 7 for j in range(6)] for i in range(5)]}
    return Heatmap(
        data=data,
        show_colorbars=True,
        aspect_ratio=ASPECT_RATIO.EQUAL,
        colorbar={"label": "Residual", "ticks": [0, 3, 6], "format": "{x:.0f}"},
    )


@case
def colorbar_grid_label():
    data = {"z": [[(i * j) % 7 for j in range(6)] for i in range(5)]}
    heatmap = Heatmap(
        data=data,
        show_colorbars=True,
        title="labelled",
        colorbar={"label": "Residual", "location": COLORBAR_LOCATION.BOTTOM},
    )
    line = LineChart(data=LINE1, title="line")
    return Grid([[heatmap, line]], figsize=(10, 4))


# ----- reference bands (ADR 0036) -----


@case
def band_line_vspans_hspans():
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["sq", "lin"],
        vspans={"xmin": 3, "xmax": 5},
        hspans={"ymin": 20, "ymax": 40},
        show_grid="both",
        show_legend=True,
        title="Bands over the grid, under the marks",
    )


@case
def band_bar_vspans_hspans():
    return BarChart(
        data=BAR1,
        vspans={"xmin": 1.5, "xmax": 3.5},
        hspans={"ymin": 15, "ymax": 25, "style": {"plot_hspan_color": "#2A9D8F"}},
        show_grid="y",
        title="Bar bands",
    )


@case
def band_labelled():
    return LineChart(
        data=LINE1,
        subtitle="sq",
        vspans={"xmin": 2, "xmax": 4, "label": "recession"},
        hspans={
            "ymin": 10,
            "ymax": 30,
            "label": "target",
            "style": {"plot_hspan_color": "#E76F51"},
        },
        show_legend=True,
        title="Labelled bands",
    )


@case
def band_hatched():
    return LineChart(
        data=LINE1,
        hspans={
            "ymin": 40,
            "ymax": 60,
            "style": {
                "plot_hspan_hatch": "//",
                "plot_hspan_edge_color": "#264653",
                "plot_hspan_color": "#FFFFFF",
            },
        },
        vspans={
            "xmin": 6,
            "xmax": 8,
            "style": {"plot_vspan_hatch": "..", "plot_vspan_edge_color": "#E76F51"},
        },
        show_grid="both",
        title="Hatched bands",
    )


@case
def band_half_open():
    return LineChart(
        data=LINE1,
        vspans={"xmin": 7},
        hspans={"ymax": 10},
        show_grid="both",
        title="Half-open bands run to the axis limits",
    )


@case
def band_theme_ink():
    config.set_theme(THEME.INK)
    return LineChart(
        data=[LINE1, LINE2],
        subtitle=["sq", "lin"],
        vspans={"xmin": 3, "xmax": 5, "label": "band"},
        hlines={"y": 40, "label": "line"},
        show_grid="both",
        show_legend=True,
        title="Ink band",
    )


@case
def band_radial_wedge():
    return RadialChart(
        data=RAD1,
        vspans={"xmin": 0, "xmax": 90, "label": "NE quadrant"},
        show_legend=True,
        title="Wedge",
    )


@case
def band_radial_annulus():
    return RadialChart(
        data=RAD1,
        mark="bar",
        hspans={"ymin": 3, "ymax": 5, "style": {"plot_hspan_color": "#E76F51"}},
        vspans={"xmin": 300, "xmax": 30},
        innerradius=0.2,
        title="Annulus and a wrapped wedge",
    )


@case
def band_grid_composed():
    banded_line = LineChart(
        data=LINE1, subtitle="sq", vspans={"xmin": 2, "xmax": 4, "label": "band"}
    )
    other_line = LineChart(data=LINE2, subtitle="lin")
    panel = Panel([banded_line, other_line], title="Panel", show_legend=True)
    bar = BarChart(data=BAR1, hspans={"ymin": 15, "ymax": 25}, title="Bar")
    wedge = RadialChart(data=RAD1, vspans={"xmin": 180, "xmax": 270}, title="Wedge")
    return Grid([[panel, bar], [wedge]], figsize=(12, 8))


# ----- temporal axis (ADR 0037) -----


def _walk(n, seed):
    return np.cumsum(np.random.RandomState(seed).randn(n)).round(3).tolist()


DAILY = [
    {"x": datetime(2024, 3, 1) + timedelta(days=i), "y": v}
    for i, v in enumerate(_walk(45, 21))
]
MONTHLY = [
    {"x": date(2022 + m // 12, m % 12 + 1, 1), "y": v}
    for m, v in enumerate(_walk(30, 22))
]
YEARLY = [
    {"x": np.datetime64(f"{year}-01-01"), "y": v}
    for year, v in zip(range(1990, 2025), _walk(35, 23))
]
BAR_MONTHS = [
    {"label": date(2024, m, 1), "y": v} for m, v in zip(range(1, 7), [3, 5, 4, 6, 2, 7])
]


@case
def date_axis_daily_monthly_yearly():
    daily = LineChart(data=DAILY, title="Daily", show_area=True)
    monthly = LineChart(
        data=MONTHLY, title="Monthly", xticks_format=DATE_FORMAT.YEAR_MONTH
    )
    yearly = ScatterChart(data=YEARLY, title="Yearly", show_regression=True)
    return Grid([[daily, monthly], [yearly]], figsize=(12, 8))


@case
def date_axis_labels_and_references():
    line = LineChart(
        data=DAILY,
        title="Ticks, limits, references",
        xticks=[datetime(2024, 3, 10), datetime(2024, 3, 25), datetime(2024, 4, 5)],
        xmin=datetime(2024, 3, 5),
        xmax=datetime(2024, 4, 10),
        vlines={"x": datetime(2024, 3, 20)},
        vspans={"xmin": datetime(2024, 4, 1), "xmax": datetime(2024, 4, 8)},
        yticks_format=VALUE_FORMAT.DECIMAL,
    )
    bars = BarChart(
        data=BAR_MONTHS, title="Date labels", xticks_format=DATE_FORMAT.YEAR_MONTH
    )
    box = BoxPlot(
        data=[{"label": d["label"], "value": v} for d in BAR_MONTHS for v in (1, 2, 4)],
        title="Horizontal date labels",
        orientation="horizontal",
        yticks_format=DATE_FORMAT.MONTH_DAY,
    )
    return Grid([[line], [bars, box]], figsize=(12, 8))


# ----- runner -----


def render_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    results = {}
    for name, fn in CASES.items():
        _reset()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                fig = fn()
                path = os.path.join(outdir, name + ".png")
                fig.savefig(path, dpi=100)
                results[name] = "ok"
            except Exception as e:  # keep going; report at the end
                results[name] = f"ERROR: {type(e).__name__}: {e}"
            finally:
                plt.close("all")
        _reset()
    return results


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def pixel_diff(p1, p2):
    a = plt.imread(p1)
    b = plt.imread(p2)
    if a.shape != b.shape:
        return -1.0
    return float((np.abs(a - b) > 1 / 255).any(axis=-1).mean())


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    outdir = os.path.join(HERE, mode)
    results = render_all(outdir)
    errors = {k: v for k, v in results.items() if v != "ok"}
    print(f"rendered {len(results) - len(errors)}/{len(results)} cases into {mode}/")
    for k, v in errors.items():
        print(f"  RENDER {k}: {v}")

    if mode == "candidate":
        base = os.path.join(HERE, "baseline")
        same, changed, expected = [], [], []
        for name in CASES:
            bp, cp = (os.path.join(d, name + ".png") for d in (base, outdir))
            if not (os.path.exists(bp) and os.path.exists(cp)):
                (expected if name in EXPECTED_CHANGES else changed).append(
                    (name, "missing file")
                )
                continue
            if sha(bp) == sha(cp):
                same.append(name)
            else:
                frac = pixel_diff(bp, cp)
                tag = f"{frac:.4%} px differ" if frac >= 0 else "size mismatch"
                (expected if name in EXPECTED_CHANGES else changed).append((name, tag))
        print(f"\nIDENTICAL: {len(same)}")
        print(f"EXPECTED CHANGES ({len(expected)}):")
        for n, t in expected:
            print(f"  ~ {n}: {t}")
        print(f"UNEXPECTED CHANGES ({len(changed)}):")
        for n, t in changed:
            print(f"  ! {n}: {t}")
        sys.exit(1 if changed or errors else 0)


# ----- emphasis rules on every front (ADR 0045) -----


@case
def line_rule_by_max():
    rng = np.random.RandomState(8)
    walks = [
        [{"x": i, "y": float(v)} for i, v in enumerate(np.cumsum(rng.randn(30)))]
        for _ in range(6)
    ]
    return LineChart(
        data=walks,
        subtitle=[f"w{i}" for i in range(6)],
        emphasis_rule={"top": 2, "by": "max"},
        show_legend=True,
        title="Two highest peaks",
    )


@case
def box_rule_median():
    rng = np.random.RandomState(3)
    data = [
        {"label": lab, "value": float(v)}
        for lab, off in [("A", 0), ("B", 2), ("C", 1), ("D", 3)]
        for v in rng.randn(30) + off
    ]
    return BoxPlot(data=data, emphasis_rule={"above": 1.5}, title="Median above 1.5")


@case
def treemap_rule_top():
    return Treemap(
        treemap_world(), emphasis_rule={"top": 3}, title="Three largest leaves"
    )


@case
def parallel_rule_hue():
    rng = np.random.RandomState(5)
    data = [
        {
            "alpha": float(rng.rand() * 10),
            "beta": float(rng.rand() * 100),
            "gamma": float(rng.rand()),
            "score": float(i),
        }
        for i in range(20)
    ]
    return ParallelCoords(
        data=data,
        dimensions=["alpha", "beta", "gamma"],
        hue="score",
        emphasis_rule={"top": 4},
    )


@case
def heatmap_rule_above():
    data = {"z": [[(i * j) % 7 for j in range(5)] for i in range(4)]}
    data["z"][1][2] = None
    return Heatmap(
        data=data,
        emphasis_rule={"above": 4},
        show_values=True,
        show_colorbars=True,
    )


@case
def hexbin_rule_top():
    return HexbinChart(
        data=hexbin_points(), emphasis_rule={"top": 5}, title="Five densest bins"
    )


# ----- scatter matrix (ADR 0051) -----

# Palmer penguins sample (CC0): bill length, bill depth, flipper, species
MATRIX_PENGUINS = [
    (39.1, 18.7, 181, "Adelie"),
    (39.5, 17.4, 186, "Adelie"),
    (40.3, 18.0, 195, "Adelie"),
    (36.7, 19.3, 193, "Adelie"),
    (37.8, 18.3, 174, "Adelie"),
    (46.5, 17.9, 192, "Chinstrap"),
    (50.0, 19.5, 196, "Chinstrap"),
    (51.3, 19.2, 193, "Chinstrap"),
    (45.4, 18.7, 188, "Chinstrap"),
    (52.7, 19.8, 197, "Chinstrap"),
    (46.1, 13.2, 211, "Gentoo"),
    (50.0, 16.3, 230, "Gentoo"),
    (48.7, 14.1, 210, "Gentoo"),
    (47.6, 14.5, 215, "Gentoo"),
    (46.7, 15.3, 219, "Gentoo"),
]


def matrix_records():
    keys = ("bill length", "bill depth", "flipper", "species")
    return [dict(zip(keys, row)) for row in MATRIX_PENGUINS]


@case
def matrix_default():
    return ScatterMatrix(matrix_records())


@case
def matrix_hue():
    return ScatterMatrix(matrix_records(), hue="species", title="Penguins")


@case
def matrix_lower_only():
    return ScatterMatrix(
        matrix_records(),
        hue="species",
        lower_only=True,
        show_correlation=True,
        legend={"title": "Species"},
    )


@case
def matrix_kde_correlation_regression():
    return ScatterMatrix(
        matrix_records(),
        hue="species",
        diagonal=SCATTER_MATRIX_DIAGONAL.KDE,
        show_correlation=True,
        show_regression=True,
    )


@case
def matrix_blank_diagonal_grid():
    config.set_theme(THEME.INK)
    matrix = ScatterMatrix(
        matrix_records(),
        dimensions=["flipper", "bill length"],
        diagonal=SCATTER_MATRIX_DIAGONAL.BLANK,
        show_regression=True,
        show_grid="both",
        title="Nested",
    )
    bar = BarChart(data=[{"label": "a", "y": 3}, {"label": "b", "y": 5}])
    return Grid([[bar, matrix]])


@case
def matrix_legend_bottom():
    return ScatterMatrix(
        matrix_records(),
        hue="species",
        legend={"location": LEGEND_LOCATION.OUTSIDE_BOTTOM},
        title="Legend below",
    )


@case
def grid_panel_title_outside_top_legend():
    bars = BarChart(data=BAR1, subtitle="bars")
    line = LineChart(data=LINE1[:5], subtitle="line")
    panel = Panel(
        [bars, line],
        title="Title over the legend",
        show_legend=True,
        legend={"location": LEGEND_LOCATION.OUTSIDE_TOP, "ncols": 2},
    )
    return Grid([[panel, LineChart(data=LINE2, title="Neighbour")]])


# ----- image chart (ADR 0060) -----


def image_pixels():
    """A 40 x 60 RGB picture: a warm gradient with a cool square in it."""

    rows, cols = np.mgrid[0:40, 0:60]
    pixels = np.stack(
        [200 + rows, 120 + cols, np.full(rows.shape, 90)], axis=-1
    ).astype(np.uint8)
    pixels[10:25, 20:40] = (60, 110, 190)
    return pixels


def image_field():
    """A 30 x 50 signed surface, a ridge and a basin."""

    y, x = np.mgrid[-1.5:1.5:30j, -2.5:2.5:50j]
    return np.exp(-((x - 1) ** 2) - y**2) - np.exp(-((x + 1) ** 2) - y**2)


@case
def image_below_scatter():
    return Panel(
        [
            ScatterChart(SCAT1, subtitle="stations"),
            ImageChart({"image": image_pixels(), "extent": (-2, 22, -5, 45)}),
        ],
        title="Scatter over a picture; figure order does not decide",
        show_grid="both",
    )


@case
def image_above_line():
    watermark = np.full((20, 20, 4), 70, dtype=np.uint8)
    watermark[..., 3] = 0
    watermark[5:15, 5:15, 3] = 160
    return Panel(
        [
            LineChart(LINE1, subtitle="line", hlines={"y": 45}),
            ImageChart(
                {"image": watermark, "extent": (2, 7, 20, 70)},
                position=DRAW_POSITION.ABOVE,
            ),
        ],
        title="A picture above the marks, under the reference line",
    )


@case
def image_field_cmap():
    return ImageChart(
        {"image": image_field(), "extent": (-2.5, 2.5, -1.5, 1.5)},
        style={"plot_image_cmap": "RdBu_r"},
        vmin=-1,
        vmax=1,
        title="A 2-D array through a colormap",
    )


@case
def image_panel_in_grid():
    under = Panel(
        [
            ImageChart(
                {"image": image_field(), "extent": (-2.5, 2.5, -1.5, 1.5)},
                style={"plot_image_alpha": 0.6},
            ),
            ScatterChart([{"x": 1.0, "y": 0.0}, {"x": -1.0, "y": 0.0}]),
        ],
        title="Composed",
    )
    return Grid(
        [[under, ImageChart({"image": image_pixels(), "extent": (0, 3, 0, 2)})]]
    )


# ----- basemap chart (ADR 0062) -----


@case
def basemap_default():
    return BasemapChart(title="Coastline and land, the world")


@case
def basemap_borders_lakes():
    return BasemapChart(
        [BASEMAP_FEATURE.LAND, BASEMAP_FEATURE.LAKES, BASEMAP_FEATURE.BORDERS],
        title="Borders and lakes around the Great Lakes",
        xmin=-100,
        xmax=-65,
        ymin=35,
        ymax=55,
    )


@case
def basemap_geometry():
    island = {
        "lon": [0, 6, 7, 5, 1, 0, np.nan, 2, 2, 3, 3],
        "lat": [0, 0, 3, 5, 4, 0, np.nan, 1, 2, 2, 1],
        "feature": "land",
    }
    road = {"lon": [0.5, 3.5, 6.5], "lat": [3.5, 2.5, 3.5], "feature": "borders"}
    return BasemapChart(
        geometry=[island, road], title="Caller outlines, a lake as a hole"
    )


@case
def basemap_geographic_aspect():
    return Panel(
        [
            BasemapChart([BASEMAP_FEATURE.LAND, BASEMAP_FEATURE.BORDERS]),
            ScatterChart(
                [
                    {"x": 10.8, "y": 59.9},
                    {"x": 18.1, "y": 59.3},
                    {"x": 24.9, "y": 60.2},
                ],
                subtitle="capitals",
            ),
        ],
        title="Scandinavia at true proportions",
        xmin=0,
        xmax=35,
        ymin=53,
        ymax=72,
        aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
    )


@case
def basemap_under_hexbin_in_grid():
    rng = np.random.default_rng(7)
    lon = np.concatenate([rng.normal(22, 1.5, 300), rng.normal(37, 1.0, 300)])
    lat = np.concatenate([rng.normal(38, 1.0, 300), rng.normal(37.5, 0.6, 300)])
    under = Panel(
        [
            HexbinChart({"x": lon.tolist(), "y": lat.tolist()}, gridsize=20, mincnt=1),
            BasemapChart(),
        ],
        title="Hexbin over the coast",
        aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
    )
    return Grid([[under, LineChart(LINE1, title="Neighbour")]])


@case
def basemap_countries_highlight():
    return BasemapChart(
        [BASEMAP_FEATURE.COUNTRIES, BASEMAP_FEATURE.BORDERS],
        highlight=["SVN", "AUT", "HRV", "HUN", "ITA"],
        style={"plot_basemap_highlight_edge_width": 1.2},
        title="Five countries picked out and outlined",
        xmin=5,
        xmax=25,
        ymin=40,
        ymax=50,
        aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
    )


# ----- basemap rivers and roads (ADR 0062) -----


@case
def basemap_rivers():
    return BasemapChart(
        [
            BASEMAP_FEATURE.LAND,
            BASEMAP_FEATURE.LAKES,
            BASEMAP_FEATURE.RIVERS,
            BASEMAP_FEATURE.BORDERS,
        ],
        resolution=BASEMAP_RESOLUTION.MEDIUM,
        title="The rivers of central Europe at 1:50m",
        xmin=2,
        xmax=30,
        ymin=42,
        ymax=56,
        aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
    )


@case
def basemap_roads():
    return BasemapChart(
        [
            BASEMAP_FEATURE.LAND,
            BASEMAP_FEATURE.RIVERS,
            BASEMAP_FEATURE.ROADS,
            BASEMAP_FEATURE.BORDERS,
            BASEMAP_FEATURE.COASTLINE,
        ],
        resolution=BASEMAP_RESOLUTION.HIGH,
        title="Slovenia's roads and rivers at 1:10m",
        xmin=13,
        xmax=16.8,
        ymin=45.3,
        ymax=47,
        aspect_ratio=ASPECT_RATIO.GEOGRAPHIC,
    )


if __name__ == "__main__":
    main()
