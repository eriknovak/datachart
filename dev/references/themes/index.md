# Themes Module

## datachart.themes

The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize the plots. Themes are named for their visual trait, never for a use case or audience; each is a complete `StyleAttrs` dictionary that `config.set_theme` applies.

## Choosing a Theme

Every theme is a complete [`StyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.StyleAttrs) dictionary, named for its visual trait. Apply one with [`config.set_theme`](https://eriknovak.github.io/datachart/dev/references/config/#datachart.config.Config.set_theme) and the member of [`THEME`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME) in the last column; the [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md) shows each on six charts, and the [Themes guide](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) shows how to adjust one or build your own.

| Theme                                                  | Look                                                                            | Apply with        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------- | ----------------- |
| [`DEFAULT_THEME`](#datachart.themes.DEFAULT_THEME)     | the package's baseline palette and furniture                                    | `THEME.DEFAULT`   |
| [`GREYSCALE_THEME`](#datachart.themes.GREYSCALE_THEME) | greys only, for print without color                                             | `THEME.GREYSCALE` |
| [`INK_THEME`](#datachart.themes.INK_THEME)             | dark-ink accents, print-ready                                                   | `THEME.INK`       |
| [`HATCH_THEME`](#datachart.themes.HATCH_THEME)         | a hatch cycle, black edges, dotted grid                                         | `THEME.HATCH`     |
| [`MINIMAL_THEME`](#datachart.themes.MINIMAL_THEME)     | accent violet, no spines, flat bars                                             | `THEME.MINIMAL`   |
| [`MATERIAL_THEME`](#datachart.themes.MATERIAL_THEME)   | the Google palette, light grid                                                  | `THEME.MATERIAL`  |
| [`SKETCH_THEME`](#datachart.themes.SKETCH_THEME)       | hand-drawn: xkcd-style wobble and halo, Comic Neue font                         | `THEME.SKETCH`    |
| [`QUILL_THEME`](#datachart.themes.QUILL_THEME)         | black ink on white paper, pen-stroked lines, etched fills, IM Fell English font | `THEME.QUILL`     |

## Themes

### datachart.themes.DEFAULT_THEME

```
DEFAULT_THEME: StyleAttrs = make_theme({})
```

The default theme: the package's baseline palette and furniture.

### datachart.themes.GREYSCALE_THEME

```
GREYSCALE_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Greys,
        "color_general_multiple": GREYS,
        "color_parallel_hue": GREYS,
        "color_parallel_hue_continuous": [
            "#D9D9D9",
            "#969696",
            "#525252",
            "#000000",
        ],
        "plot_bar_edge_width": 0.8,
        "plot_bar_edge_color": "#000000",
        "plot_stackedarea_edge_color": "#000000",
        "plot_sankey_node_edge_color": "#000000",
        "plot_treemap_edge_color": "#000000",
        "plot_network_node_edge_color": "#000000",
        "plot_hist_edge_color": "#000000",
        "plot_vline_color": "#5D6D7E",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": "#5D6D7E",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_vspan_color": "#5D6D7E",
        "plot_hspan_color": "#5D6D7E",
        "plot_text_box_edgecolor": "#B0B0B0",
        "plot_text_arrow_color": "#5D6D7E",
        "plot_gantt_dependency_color": "#2C3E50",
        "plot_gantt_today_color": "#2C3E50",
        "plot_dumbbell_start_color": "#ABB2B9",
        "plot_dumbbell_end_color": "#2C3E50",
        "plot_dumbbell_edge_color": "#000000",
        "plot_dumbbell_connector_color": "#85929E",
        "plot_dumbbell_arrow_color": "#5D6D7E",
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_frame_color": "#000000",
        "plot_regression_color": "#34495E",
        "plot_box_median_color": "#000000",
        "plot_violin_edgecolor": "#000000",
        "plot_violin_inner_color": "#000000",
        "plot_ridgeline_edgecolor": "#000000",
        "plot_ridgeline_inner_color": "#000000",
    }
)
```

The greyscale theme: shades of grey for print or colorblind-safe output.

### datachart.themes.INK_THEME

```
INK_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": COLORS.PaperYlGnBu,
        "color_parallel_hue": COLORS.PaperYlGnBu,
        "color_parallel_hue_continuous": [
            "#C7E9B4",
            "#7FCDBB",
            "#41B6C4",
            "#225EA8",
        ],
        "font_general_sansserif": [
            "Helvetica",
            "Arial",
            "Liberation Sans",
            "DejaVu Sans",
        ],
        "plot_grid_color": "#DDE3E8",
        "plot_bar_edge_width": 1.0,
        "plot_bar_edge_color": "#0B1F44",
        "plot_stackedarea_edge_color": "#0B1F44",
        "plot_sankey_node_edge_color": "#0B1F44",
        "plot_treemap_edge_color": "#0B1F44",
        "plot_network_node_edge_color": "#0B1F44",
        "plot_hist_edge_color": "#0B1F44",
        "plot_vline_color": "#7F8C8D",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": "#7F8C8D",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_vspan_color": "#7F8C8D",
        "plot_hspan_color": "#7F8C8D",
        "plot_text_box_edgecolor": "#000000",
        "plot_text_arrow_color": "#000000",
        "plot_gantt_dependency_color": "#0B1F44",
        "plot_gantt_today_color": "#0B1F44",
        "plot_dumbbell_start_color": "#7FCDBB",
        "plot_dumbbell_end_color": "#225EA8",
        "plot_dumbbell_edge_color": "#0B1F44",
        "plot_dumbbell_connector_color": "#7F8C8D",
        "plot_dumbbell_arrow_color": "#34495E",
        "plot_heatmap_cmap": COLORS.YlGnBu,
        "plot_heatmap_frame_color": "#0B1F44",
        "plot_scatter_edge_width": 0.6,
        "plot_scatter_edge_color": "#0B1F44",
        "plot_swarm_edge_width": 0.6,
        "plot_swarm_edge_color": "#0B1F44",
        "plot_regression_color": "#34495E",
        "plot_parallel_axis_color": "#34495E",
        "plot_parallel_tick_color": "#34495E",
        "plot_parallel_tick_label_color": "#34495E",
        "plot_parallel_dim_label_color": "#34495E",
        "plot_box_edgecolor": "#34495E",
        "plot_box_median_color": "#34495E",
        "plot_violin_edgecolor": "#34495E",
        "plot_ridgeline_edgecolor": "#34495E",
    }
)
```

The ink theme: dark-ink accents, print-ready.

### datachart.themes.HATCH_THEME

```
HATCH_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.YlOrBr,
        "color_general_multiple": [
            "#B5563A",
            "#4F6D8F",
            "#D4A64A",
            "#4E7A5A",
            "#A6A6A6",
            "#7B5EA7",
        ],
        "color_parallel_hue_continuous": [
            "#F3E0C3",
            "#E0AE6A",
            "#B5563A",
            "#6B2E1A",
        ],
        "font_general_sansserif": [
            "Helvetica",
            "Arial",
            "Liberation Sans",
            "DejaVu Sans",
        ],
        "plot_hatch_cycle": ["", "//", ".."],
        "plot_grid_color": "#D0D0D0",
        "plot_grid_linestyle": LINE_STYLE.DOTTED,
        "plot_grid_alpha": 0.8,
        "plot_bar_edge_color": "#000000",
        "plot_stackedarea_edge_color": "#000000",
        "plot_sankey_node_edge_color": "#000000",
        "plot_treemap_edge_color": "#000000",
        "plot_network_node_edge_color": "#000000",
        "plot_bar_edge_width": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_hist_edge_color": "#000000",
        "plot_scatter_edge_color": "#000000",
        "plot_scatter_edge_width": 0.6,
        "plot_swarm_edge_color": "#000000",
        "plot_swarm_edge_width": 0.6,
        "plot_text_box_edgecolor": "#000000",
        "plot_text_arrow_color": "#000000",
        "plot_gantt_dependency_color": "#000000",
        "plot_gantt_today_color": "#000000",
        "plot_dumbbell_start_color": "#4F6D8F",
        "plot_dumbbell_end_color": "#B5563A",
        "plot_dumbbell_edge_color": "#000000",
        "plot_dumbbell_connector_color": "#8C8C8C",
        "plot_dumbbell_arrow_color": "#000000",
        "plot_heatmap_cmap": COLORS.YlOrBr,
        "plot_heatmap_frame_color": "#000000",
        "plot_violin_edgecolor": "#000000",
        "plot_ridgeline_edgecolor": "#000000",
    }
)
```

The hatch theme: hatch cycle, black edges, dotted grid.

### datachart.themes.MINIMAL_THEME

```
MINIMAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Purples,
        "color_general_multiple": [
            "#7048E8",
            "#1F2933",
            "#8A97A3",
            "#C5CDD4",
        ],
        "color_parallel_hue_continuous": [
            "#DCD3F7",
            "#A796EE",
            "#7048E8",
            "#3B1E9E",
        ],
        "font_general_color": "#1F1F1F",
        "font_title_color": "#1F1F1F",
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "axes_spines_bottom_visible": False,
        "axes_ticks_length": 0,
        "plot_grid_color": "#EFEFEF",
        "plot_grid_alpha": 1.0,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_stackedarea_edge_width": 0,
        "plot_value_fontsize": 9,
        "plot_value_color": "#1F1F1F",
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_scatter_edge_color": "#FFFFFF",
        "plot_swarm_edge_color": "#FFFFFF",
        "plot_dumbbell_start_color": "#C5CDD4",
        "plot_dumbbell_end_color": "#7048E8",
        "plot_dumbbell_connector_color": "#DDE3E8",
        "plot_text_box_edgecolor": "#CFD8DC",
        "plot_text_arrow_color": "#9AA4AE",
        "plot_heatmap_cmap": COLORS.Purples,
        "plot_heatmap_frame_color": "#9AA4AE",
    }
)
```

The minimal theme: accent violet, no spines, flat bars.

### datachart.themes.MATERIAL_THEME

```
MATERIAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#1A73E8",
            "#D93025",
            "#F9AB00",
            "#1E8E3E",
            "#12B5CB",
            "#9334E6",
        ],
        "color_parallel_hue_continuous": [
            "#C6DAFC",
            "#7BAAF7",
            "#1A73E8",
            "#174EA6",
        ],
        "font_general_sansserif": [
            "Roboto",
            "Arial",
            "Helvetica",
            "Liberation Sans",
        ],
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "plot_grid_color": "#E0E0E0",
        "plot_grid_alpha": 1.0,
        "plot_grid_linewidth": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_stackedarea_edge_width": 0,
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_text_box_edgecolor": "#757575",
        "plot_text_arrow_color": "#757575",
        "plot_dumbbell_start_color": "#F9AB00",
        "plot_dumbbell_end_color": "#1A73E8",
        "plot_dumbbell_edge_width": 0,
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_frame_color": "#000000",
    }
)
```

The material theme: Google palette, light grid.

### datachart.themes.SKETCH_THEME

```
SKETCH_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.YlOrRd,
        "color_general_multiple": [
            "#E4572E",
            "#2E86AB",
            "#F5B700",
            "#7E5AAB",
            "#76B041",
        ],
        "color_parallel_hue_continuous": [
            "#FDD49E",
            "#FC8D59",
            "#E4572E",
            "#99000D",
        ],
        "font_general_family": "sans-serif",
        "font_general_sansserif": [
            "Comic Neue",
            "Humor Sans",
            "Comic Sans MS",
        ],
        "font_general_size": 11,
        "font_general_color": "#222222",
        "font_title_size": 15,
        "font_title_color": "#222222",
        "font_title_weight": FONT_WEIGHT.BOLD,
        "axes_spines_width": 1.6,
        "axes_ticks_length": 5,
        "chart_default_show_grid": None,
        "plot_line_width": 2.5,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 1.0,
        "plot_hist_edge_width": 1.0,
        "plot_scatter_edge_color": "#222222",
        "plot_dumbbell_start_color": "#2E86AB",
        "plot_dumbbell_end_color": "#E4572E",
        "plot_dumbbell_edge_color": "#222222",
        "plot_dumbbell_connector_color": "#8A8A8A",
        "plot_heatmap_cmap": COLORS.YlOrRd,
        "plot_treemap_group_edge_width": 0,
        "plot_sketch_params": [0.5, 100, 2],
        "plot_sketch_halo_width": 1.5,
    }
)
```

The sketch theme: hand-drawn, xkcd-style wobble and halo, Comic Neue font.

Paths wobble, lines carry a white halo, spines and lines are thick, the grid is off, and text is set in Comic Neue, which ships with the package; Humor Sans and Comic Sans MS are the fallbacks should the bundled face fail to register.

### datachart.themes.QUILL_THEME

```
QUILL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Greys,
        "color_general_multiple": [INK],
        "color_parallel_hue": [INK],
        "color_parallel_hue_continuous": [
            "#D9CCAA",
            "#8C7E5E",
            "#4A3C2A",
            INK,
        ],
        "muted_color": "#C9B892",
        "font_general_family": "serif",
        "font_general_serif": [
            "IM FELL English",
            "IM FELL English SC",
            "Georgia",
        ],
        "font_general_size": 11,
        "font_general_color": INK,
        "font_title_size": 16,
        "font_title_color": INK,
        "font_title_style": FONT_STYLE.ITALIC,
        "font_title_weight": FONT_WEIGHT.NORMAL,
        "font_subtitle_color": INK,
        "font_xlabel_color": INK,
        "font_ylabel_color": INK,
        "axes_spines_color": INK,
        "axes_ticks_color": INK,
        "axes_spines_width": 1.4,
        "axes_ticks_length": 5,
        "axes_ticks_label_size": 9,
        "chart_default_show_grid": None,
        "chart_default_node_label_position": NETWORK_LABEL_POSITION.ABOVE,
        "plot_hatch_cycle": ["/", ".", "\\", "x", "-", "|"],
        "plot_linestyle_cycle": [
            "-",
            "--",
            ":",
            "-.",
            [0, [7, 2, 1, 2, 1, 2]],
            [0, [2, 2]],
        ],
        "plot_marker_cycle": [
            "o",
            {"marker": "s", "hollow": True},
            "^",
            {"marker": "D", "hollow": True},
            "v",
            {"marker": "P", "hollow": True},
        ],
        "plot_sketch_params": [0.7, 90, 2],
        "plot_ink_stroke": {
            "width_scale": 1.6,
            "nib_angle": 32,
            "nib_floor": 0.35,
            "wobble": 0.22,
            "taper": 7,
        },
        "plot_etch": {
            "spacing": 4.2,
            "jitter": 0.3,
            "angle_jitter": 2.5,
            "line_width": 0.6,
            "wash": 0.1,
            "color": INK,
        },
        "plot_value_etch": {
            "washes": [PAPER] * 5,
            "hatches": ["", ".", "..", "//", "xx"],
        },
        "plot_legend_label_color": INK,
        "plot_legend_font_size": 9,
        "plot_legend_title_size": 10,
        "plot_legend_edge_color": INK,
        "plot_line_width": 2.2,
        "plot_area_alpha": 1.0,
        "plot_area_linewidth": 0.8,
        "plot_stackedarea_alpha": 1.0,
        "plot_stackedarea_outline": True,
        "plot_stackedarea_edge_color": INK,
        "plot_stackedarea_edge_width": 0.9,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 1.0,
        "plot_bar_edge_color": INK,
        "plot_bar_error_color": INK,
        "plot_value_color": INK,
        "plot_value_halo_width": 5,
        "plot_hist_alpha": 1.0,
        "plot_hist_edge_width": 1.0,
        "plot_hist_edge_color": INK,
        "plot_vline_color": INK,
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": INK,
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_vspan_color": INK,
        "plot_hspan_color": INK,
        "plot_vspan_alpha": 1.0,
        "plot_hspan_alpha": 1.0,
        "plot_vspan_hatch": ".",
        "plot_hspan_hatch": ".",
        "plot_vspan_edge_color": INK,
        "plot_hspan_edge_color": INK,
        "plot_text_color": INK,
        "plot_text_box_facecolor": PAPER,
        "plot_text_box_edgecolor": INK,
        "plot_text_box_style": "round,pad=0.4,rounding_size=0.2",
        "plot_text_arrow_color": INK,
        "plot_gantt_dependency_color": INK,
        "plot_gantt_today_color": INK,
        "plot_dumbbell_start_color": PAPER,
        "plot_dumbbell_end_color": INK,
        "plot_dumbbell_edge_color": INK,
        "plot_dumbbell_edge_width": 0.8,
        "plot_dumbbell_connector_color": INK,
        "plot_dumbbell_arrow_color": INK,
        "plot_dumbbell_connector_width": 1.2,
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_frame_color": INK,
        "plot_heatmap_font_color": INK,
        "plot_heatmap_font_size": 10,
        "plot_calendar_heatmap_font_size": 8,
        "plot_heatmap_edge_width": 0.6,
        "plot_heatmap_edge_color": INK,
        "plot_calendar_heatmap_edge_color": PAPER,
        "plot_calendar_heatmap_month_line_color": INK,
        "plot_contour_color": INK,
        "plot_contour_line_width": 1.8,
        "plot_hexbin_edge_width": 0.3,
        "plot_hexbin_edge_color": INK,
        "plot_scatter_edge_width": 0.8,
        "plot_scatter_edge_color": INK,
        "plot_scatter_alpha": 0.8,
        "plot_swarm_edge_width": 0.6,
        "plot_swarm_edge_color": INK,
        "plot_swarm_alpha": 0.9,
        "plot_regression_color": INK,
        "plot_regression_ci_alpha": 0.12,
        "plot_parallel_color": INK,
        "plot_parallel_alpha": 0.35,
        "plot_parallel_axis_color": INK,
        "plot_parallel_tick_color": INK,
        "plot_parallel_tick_label_color": INK,
        "plot_parallel_tick_label_size": 9,
        "plot_parallel_tick_label_bg_color": None,
        "plot_parallel_dim_label_color": INK,
        "plot_box_edgecolor": INK,
        "plot_box_linewidth": 1.2,
        "plot_box_hatch": "/",
        "plot_box_median_color": INK,
        "plot_box_median_linewidth": 2.5,
        "plot_box_whisker_color": INK,
        "plot_box_whisker_linewidth": 1.2,
        "plot_box_cap_color": INK,
        "plot_box_cap_linewidth": 1.2,
        "plot_box_outlier_color": PAPER,
        "plot_box_outlier_edge_color": INK,
        "plot_box_alpha": 1.0,
        "plot_violin_edgecolor": INK,
        "plot_violin_linewidth": 1.2,
        "plot_violin_alpha": 1.0,
        "plot_violin_hatch": "\\",
        "plot_violin_inner_color": INK,
        "plot_violin_median_color": PAPER,
        "plot_ridgeline_edgecolor": INK,
        "plot_ridgeline_linewidth": 1.2,
        "plot_ridgeline_alpha": 1.0,
        "plot_ridgeline_hatch": "/",
        "plot_ridgeline_inner_color": INK,
        "plot_sankey_link_alpha": 0.25,
        "plot_sankey_node_edge_color": INK,
        "plot_sankey_node_edge_width": 1.0,
        "plot_sankey_node_fill": False,
        "plot_treemap_edge_color": INK,
        "plot_treemap_edge_width": 1.0,
        "plot_treemap_level_shade": 0.55,
        "plot_treemap_etch_density": [3, 1, 0],
        "plot_network_node_edge_color": INK,
        "plot_network_node_edge_width": 1.6,
        "plot_network_node_alpha": 1.0,
        "plot_network_edge_color": INK,
        "plot_network_edge_alpha": 0.9,
        "plot_network_edge_style": ARROW_STYLE.STRAIGHT,
        "plot_network_edge_curve": 0.0,
        "plot_network_edge_width_min": 2.0,
        "plot_network_edge_width_max": 2.8,
        "plot_network_edge_ink_stroke": {
            "width_scale": 1.4,
            "nib_floor": 1.0,
            "wobble": 0.0,
            "swell": 0.5,
            "noise": 0.12,
        },
        "plot_network_group_linestyle": LINE_STYLE.DOTTED,
    }
)
```

The quill theme: black ink on white paper, as a quill and an etching needle draw.

One ink only: series differ by line style, marker and etching, never by color. Series lines are broad-nib pen strokes whose width varies along the line, bars, areas and bodies are etched by hand instead of hatched, the furniture wobbles, and text is set in IM Fell English, which ships with the package, titles in its italic.
