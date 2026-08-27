# Themes Module

## datachart.themes

The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize the plots. Themes are named for their visual trait, never for a use case or audience.

| ATTRIBUTE         | DESCRIPTION                                                                            |
| ----------------- | -------------------------------------------------------------------------------------- |
| `DEFAULT_THEME`   | The default theme style. **TYPE:** `StyleAttrs`                                        |
| `GREYSCALE_THEME` | The greyscale theme style. **TYPE:** `StyleAttrs`                                      |
| `INK_THEME`       | The ink theme style (dark-ink accents, print-ready). **TYPE:** `StyleAttrs`            |
| `HATCH_THEME`     | The hatch theme style (hatch cycle, value labels, dotted grid). **TYPE:** `StyleAttrs` |
| `MINIMAL_THEME`   | The minimal theme style (accent blue, no spines, flat bars). **TYPE:** `StyleAttrs`    |
| `MATERIAL_THEME`  | The material theme style (Google palette, light grid). **TYPE:** `StyleAttrs`          |

## Themes

### datachart.themes.DEFAULT_THEME

```
DEFAULT_THEME: StyleAttrs = make_theme({})
```

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
        "plot_hist_edge_color": "#000000",
        "plot_vline_color": "#5D6D7E",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": "#5D6D7E",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_text_box_edgecolor": "#B0B0B0",
        "plot_text_arrow_color": "#5D6D7E",
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_frame_color": "#000000",
        "plot_regression_color": "#34495E",
        "plot_box_median_color": "#000000",
        "plot_violin_edgecolor": "#000000",
        "plot_violin_inner_color": "#000000",
    }
)
```

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
            "DejaVu Sans",
        ],
        "plot_grid_color": "#DDE3E8",
        "plot_bar_edge_width": 1.0,
        "plot_bar_edge_color": "#0B1F44",
        "plot_hist_edge_color": "#0B1F44",
        "plot_vline_color": "#7F8C8D",
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": "#7F8C8D",
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_text_box_edgecolor": "#000000",
        "plot_text_arrow_color": "#000000",
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
        "plot_violin_inner_color": "#34495E",
    }
)
```

### datachart.themes.HATCH_THEME

```
HATCH_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#5B84C4",
            "#C85450",
            "#8C8C8C",
            "#6C9A78",
            "#A8C4E8",
            "#C9A227",
        ],
        "color_parallel_hue_continuous": [
            "#D3DEF0",
            "#A8C4E8",
            "#5B84C4",
            "#2E4E8F",
        ],
        "font_general_sansserif": [
            "Helvetica",
            "Arial",
            "DejaVu Sans",
        ],
        "chart_default_show_values": True,
        "plot_hatch_cycle": ["", "//", ".."],
        "plot_grid_color": "#D0D0D0",
        "plot_grid_linestyle": LINE_STYLE.DOTTED,
        "plot_grid_alpha": 0.8,
        "plot_bar_edge_color": "#000000",
        "plot_bar_edge_width": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_hist_edge_color": "#000000",
        "plot_scatter_edge_color": "#000000",
        "plot_scatter_edge_width": 0.6,
        "plot_swarm_edge_color": "#000000",
        "plot_swarm_edge_width": 0.6,
        "plot_text_box_edgecolor": "#000000",
        "plot_text_arrow_color": "#000000",
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_frame_color": "#000000",
        "plot_violin_edgecolor": "#000000",
    }
)
```

### datachart.themes.MINIMAL_THEME

```
MINIMAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#2B7FFF",
            "#A9B4BE",
            "#7C8894",
            "#525C66",
            "#2E3740",
        ],
        "color_parallel_hue_continuous": [
            "#D9D9D9",
            "#A9B4BE",
            "#6FA0F5",
            "#2B7FFF",
        ],
        "font_general_color": "#1F1F1F",
        "font_title_color": "#1F1F1F",
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "axes_spines_bottom_visible": False,
        "axes_ticks_length": 0,
        "chart_default_show_values": True,
        "plot_grid_color": "#EFEFEF",
        "plot_grid_alpha": 1.0,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_bar_value_fontsize": 9,
        "plot_bar_value_color": "#1F1F1F",
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_scatter_edge_color": "#FFFFFF",
        "plot_swarm_edge_color": "#FFFFFF",
        "plot_text_box_edgecolor": "#CFD8DC",
        "plot_text_arrow_color": "#9AA4AE",
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_frame_color": "#9AA4AE",
    }
)
```

### datachart.themes.MATERIAL_THEME

```
MATERIAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#4285F4",
            "#FBBC04",
            "#34A853",
            "#EA4335",
            "#7BAAF7",
            "#46BDC6",
        ],
        "color_parallel_hue_continuous": [
            "#C6DAFC",
            "#7BAAF7",
            "#4285F4",
            "#1B5FD9",
        ],
        "font_general_sansserif": [
            "Roboto",
            "Arial",
            "Helvetica",
        ],
        "axes_spines_top_visible": False,
        "axes_spines_right_visible": False,
        "axes_spines_left_visible": False,
        "chart_default_show_values": True,
        "plot_grid_color": "#E0E0E0",
        "plot_grid_alpha": 1.0,
        "plot_grid_linewidth": 0.8,
        "plot_bar_alpha": 1.0,
        "plot_bar_edge_width": 0,
        "plot_hist_edge_width": 0,
        "plot_line_width": 2.0,
        "plot_text_box_edgecolor": "#757575",
        "plot_text_arrow_color": "#757575",
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_frame_color": "#000000",
    }
)
```
