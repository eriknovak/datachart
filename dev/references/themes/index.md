# Themes Module

## datachart.themes

The module containing the `themes`.

The `themes` module contains the predefined style themes that are used to visualize the plots. Themes are named for their look, never for a use case or audience; each is a complete `StyleAttrs` dictionary that `config.set_theme` applies.

## Choosing a Theme

Every theme is a complete [`StyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.StyleAttrs) dictionary, named for its look and listed here by where it works best. Apply one with [`config.set_theme`](https://eriknovak.github.io/datachart/dev/references/config/#datachart.config.Config.set_theme) and the member of [`THEME`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME) in the last column; the [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md) shows each on six charts, and the [Themes guide](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/themes/index.md) shows how to adjust one or build your own. [`derive_theme`](#datachart.themes.derive_theme) rebuilds any theme's palettes from a lead, keeps its furniture, and composes [`TRAIT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.TRAIT) members on top; the harbor, muted, contrast, hatch, muted-hatch and slate-hatch themes are built that way from the default theme, a named `COLORS` lead and one or two traits. [`score_palette`](#datachart.themes.score_palette) reports how a series palette holds up for colour-blind readers; every predefined theme passes its gate.

| Theme                                                    | Look                                                                            | Apply with         |
| -------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------ |
| **Screen and presentations**                             |                                                                                 |                    |
| [`DEFAULT_THEME`](#datachart.themes.DEFAULT_THEME)       | softened Okabe–Ito palette, colour-blind safe, baseline furniture               | `THEME.DEFAULT`    |
| [`MATERIAL_THEME`](#datachart.themes.MATERIAL_THEME)     | the Google hues re-stepped for deutan readers, light grid                       | `THEME.MATERIAL`   |
| [`MINIMAL_THEME`](#datachart.themes.MINIMAL_THEME)       | accent violet and five stepped greys, no spines, flat bars                      | `THEME.MINIMAL`    |
| [`HARBOR_THEME`](#datachart.themes.HARBOR_THEME)         | navy and amber in lightness steps, colour-blind safe                            | `THEME.HARBOR`     |
| [`DARK_THEME`](#datachart.themes.DARK_THEME)             | bright marks on a near-black page, light furniture, Viridis value scale         | `THEME.DARK`       |
| **Print and black-and-white**                            |                                                                                 |                    |
| [`GREYSCALE_THEME`](#datachart.themes.GREYSCALE_THEME)   | five greys with hatch, dash and marker cycles, for print without color          | `THEME.GREYSCALE`  |
| [`INK_THEME`](#datachart.themes.INK_THEME)               | lightness-stepped blues and greens, navy ink edges, print-ready                 | `THEME.INK`        |
| [`HATCH_THEME`](#datachart.themes.HATCH_THEME)           | a six-entry hatch cycle, black edges, dotted grid                               | `THEME.HATCH`      |
| [`MUTED_THEME`](#datachart.themes.MUTED_THEME)           | Tol's muted colours, dash and marker cycles, colour-blind safe                  | `THEME.MUTED`      |
| [`CONTRAST_THEME`](#datachart.themes.CONTRAST_THEME)     | lightness-stepped colours plus hatches, print-safe                              | `THEME.CONTRAST`   |
| [`MUTEDHATCH_THEME`](#datachart.themes.MUTEDHATCH_THEME) | Tol's muted colours under hatches, BuPu value scale                             | `THEME.MUTEDHATCH` |
| [`SLATEHATCH_THEME`](#datachart.themes.SLATEHATCH_THEME) | the hatch theme without rust, slate blue first, PuBu value scale                | `THEME.SLATEHATCH` |
| **Illustrative**                                         |                                                                                 |                    |
| [`SKETCH_THEME`](#datachart.themes.SKETCH_THEME)         | hand-drawn: xkcd-style wobble and halo, Comic Neue font                         | `THEME.SKETCH`     |
| [`QUILL_THEME`](#datachart.themes.QUILL_THEME)           | black ink on white paper, pen-stroked lines, etched fills, IM Fell English font | `THEME.QUILL`      |

## Deriving a Theme

### datachart.themes.derive_theme

```
derive_theme(
    base: str | StyleAttrs,
    lead: Lead,
    traits: Sequence[TRAIT | str] | None = None,
    **overrides: Any
) -> StyleAttrs
```

Build a theme variant: the base's furniture with palettes rebuilt from the lead.

A sequential lead becomes the value scale (`color_general_singular`, `plot_heatmap_cmap`); the series palette is six of its colors in lightness steps, interleaved dark and light, the parallel coords ramp four of them from light to dark, and the dumbbell pair its lightest and darkest sample. A categorical lead becomes the series palette, its first color the singular one, and the base keeps its value scale, ramp, and dumbbell pair. Each trait then sets its mark keys, in the order given, so a later trait wins a shared key; fonts, spines and rendering attributes are never touched. The result is a plain theme dictionary: apply it with `register_theme` or `override`; `TRAIT` lists the traits and the predefined themes built this way.

Examples:

```
>>> from datachart.config import config
>>> from datachart.constants import COLORS, THEME
>>> from datachart.themes import derive_theme
>>> forest = derive_theme(THEME.MINIMAL, lead=COLORS.Greens)
>>> config.register_theme("forest", forest)
>>> config.set_theme("forest")
```

| PARAMETER     | DESCRIPTION                                                                                                                                                                 |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `base`        | A THEME constant, a registered theme name, or a theme dictionary; a partial dictionary is completed from the default theme, as register_theme completes it. **TYPE:** \`str |
| `lead`        | A COLORS constant, a pypalettes palette name, or a list of colors. A diverging map is not a lead; it is read as categorical. **TYPE:** `Lead`                               |
| `traits`      | TRAIT members applied in order after the lead; an unknown name raises. **TYPE:** \`Sequence\[TRAIT                                                                          |
| `**overrides` | Style attributes set on the result; an unknown name raises. **TYPE:** `Any` **DEFAULT:** `{}`                                                                               |

| RETURNS      | DESCRIPTION        |
| ------------ | ------------------ |
| `StyleAttrs` | The derived theme. |

## Scoring a Palette

### datachart.themes.score_palette

```
score_palette(
    colors: str | list[str], face: str | None = None
) -> PaletteScore
```

Score a series palette for colour-blind readers.

Every pair of colours is compared, since any two series may sit side by side; each colour is passed through the Machado, Oliveira and Fernandes (2009) simulation of deuteranopia, protanopia and tritanopia at full severity and the distance measured in OKLab (ΔE ×100).

Examples:

```
>>> from datachart.themes import DEFAULT_THEME, score_palette
>>> score = score_palette(DEFAULT_THEME["color_general_multiple"])
>>> score.verdict
'pass'
```

| PARAMETER | DESCRIPTION                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------ |
| `colors`  | The palette: a list of colours, a COLORS constant, or a pypalettes palette name. **TYPE:** \`str |
| `face`    | The colour the marks sit on, for the contrast count; None counts nothing. **TYPE:** \`str        |

| RETURNS        | DESCRIPTION |
| -------------- | ----------- |
| `PaletteScore` | The score.  |

| RAISES       | DESCRIPTION                                    |
| ------------ | ---------------------------------------------- |
| `ValueError` | When the palette holds fewer than two colours. |

### datachart.themes.PaletteScore

How far apart a palette's two closest colours are, per kind of vision.

Every distance is the palette's worst pair in OKLab ΔE ×100, `grey_gap` the smallest lightness step between two colours once printed without colour, `low_contrast` how many colours sit under 3:1 against the face, `worst_kind` whichever of deutan and protan scores lower and `worst_pair` the pair behind it. `verdict` is `"pass"` when deutan and protan reach 8 and normal reaches 15, `"weak"` when deutan and protan stay between 6 and 8 with normal at 15, and `"fail"` otherwise. `colors` is the palette scored; a notebook shows it as a swatch strip over the summary line.

## Themes

### datachart.themes.DEFAULT_THEME

```
DEFAULT_THEME: StyleAttrs = make_theme({})
```

The default theme: the package's baseline palette and furniture.

The palette is a softened Okabe–Ito set closed with charcoal, so every pair of series stays apart for deutan, protan and tritan readers.

### datachart.themes.MATERIAL_THEME

```
MATERIAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Blues,
        "color_general_multiple": [
            "#1A73E8",
            "#BC261D",
            "#EFB04E",
            "#269F47",
            "#19ACC1",
            "#7C48B5",
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
        "plot_dumbbell_start_color": "#EFB04E",
        "plot_dumbbell_end_color": "#1A73E8",
        "plot_dumbbell_edge_width": 0,
        "plot_heatmap_cmap": COLORS.Blues,
        "plot_heatmap_cmap_diverging": COLORS.PuOr,
        "plot_heatmap_frame_color": "#000000",
    }
)
```

The material theme: Google palette, light grid.

### datachart.themes.MINIMAL_THEME

```
MINIMAL_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.Purples,
        "color_general_multiple": [
            "#7048E8",
            "#1B242C",
            "#A2AEB9",
            "#414C58",
            "#D3E0EA",
            "#6D7983",
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
        "plot_dumbbell_start_color": "#A2AEB9",
        "plot_dumbbell_end_color": "#7048E8",
        "plot_dumbbell_connector_color": "#DDE3E8",
        "plot_text_box_edgecolor": "#CFD8DC",
        "plot_text_arrow_color": "#9AA4AE",
        "plot_heatmap_cmap": COLORS.Purples,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
        "plot_heatmap_frame_color": "#9AA4AE",
    }
)
```

The minimal theme: accent violet, no spines, flat bars.

### datachart.themes.HARBOR_THEME

```
HARBOR_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Harbor,
    traits=[TRAIT.FLAT],
    color_general_singular=COLORS.Cividis,
    color_parallel_hue_continuous=[
        "#BCAE6C",
        "#7D7C78",
        "#434E6C",
        "#00224E",
    ],
    plot_dumbbell_start_color="#EFC98C",
    plot_dumbbell_end_color="#1F4E79",
    plot_heatmap_cmap=COLORS.Cividis,
    plot_heatmap_cmap_diverging=COLORS.RdBu,
)
```

The harbor theme: navy and amber in lightness steps, colour-blind safe.

The `Harbor` lead, two hue families, navy to sky and amber to sand, with taupe and near-black closing the set; lightness does the separating, so every pair of series stays apart for deutan, protan and tritan readers. The flat trait gives edgeless opaque bars and 2 pt lines; the value scale is Cividis.

### datachart.themes.DARK_THEME

```
DARK_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": [
            "#007094",
            "#009C95",
            "#00BE7D",
            "#98D84A",
            "#FDE333",
        ],
        "color_general_multiple": [
            "#63A6DE",
            "#CFA23A",
            "#4FE49B",
            "#DC5470",
            "#A35CE8",
            "#E6E9F2",
        ],
        "color_parallel_hue_continuous": [
            "#009C95",
            "#00BE7D",
            "#98D84A",
            "#FDE333",
        ],
        "muted_color": "#4A515B",
        "font_general_color": TEXT,
        "font_title_color": BRIGHT,
        "font_subtitle_color": DIM,
        "font_xlabel_color": TEXT,
        "font_ylabel_color": TEXT,
        "figure_facecolor": PAGE,
        "axes_facecolor": AXES_FACE,
        "axes_spines_color": RULE,
        "axes_ticks_color": RULE,
        "plot_grid_color": GRID,
        "plot_grid_alpha": 1.0,
        "plot_legend_label_color": TEXT,
        "plot_legend_edge_color": EDGE,
        "plot_legend_face_color": AXES_FACE,
        "plot_stackedarea_edge_color": PAGE,
        "plot_sankey_node_edge_color": PAGE,
        "plot_treemap_edge_color": PAGE,
        "plot_network_node_edge_color": PAGE,
        "plot_network_edge_color": DIM,
        "plot_bar_edge_color": PAGE,
        "plot_bar_error_color": TEXT,
        "plot_hist_edge_color": PAGE,
        "plot_hexbin_edge_color": PAGE,
        "plot_basemap_land_color": "#262B33",
        "plot_basemap_highlight_color": "#434B57",
        "plot_basemap_highlight_edge_color": TEXT,
        "plot_basemap_coastline_color": "#59626E",
        "plot_basemap_border_color": EDGE,
        "plot_basemap_river_color": "#4B6178",
        "plot_basemap_road_color": "#5E5850",
        "plot_scatter_edge_color": PAGE,
        "plot_swarm_edge_color": PAGE,
        "plot_gantt_dependency_color": DIM,
        "plot_gantt_today_color": "#FF6B6B",
        "plot_dumbbell_start_color": "#CFA23A",
        "plot_dumbbell_end_color": "#63A6DE",
        "plot_dumbbell_edge_color": PAGE,
        "plot_dumbbell_connector_color": "#6E7681",
        "plot_dumbbell_arrow_color": DIM,
        "plot_value_color": BRIGHT,
        "plot_text_color": BRIGHT,
        "plot_text_box_facecolor": "#242A33",
        "plot_text_box_edgecolor": EDGE,
        "plot_text_arrow_color": DIM,
        "plot_heatmap_cmap": COLORS.Viridis,
        "plot_heatmap_cmap_diverging": COLORS.Coolwarm,
        "plot_heatmap_frame_color": TEXT,
        "plot_heatmap_edge_color": PAGE,
        "plot_calendar_heatmap_edge_color": PAGE,
        "plot_calendar_heatmap_month_line_color": TEXT,
        "plot_parallel_axis_color": TEXT,
        "plot_parallel_tick_color": TEXT,
        "plot_parallel_tick_label_color": BRIGHT,
        "plot_parallel_tick_label_bg_color": AXES_FACE,
        "plot_parallel_dim_label_color": TEXT,
        "plot_box_edgecolor": TEXT,
        "plot_box_median_color": BRIGHT,
        "plot_box_whisker_color": TEXT,
        "plot_box_cap_color": TEXT,
        "plot_box_outlier_color": AXES_FACE,
        "plot_box_outlier_edge_color": TEXT,
    }
)
```

The dark theme: bright marks on a near-black page.

The page is near-black and the plotting area a step lighter, so the axes read as a card on it. Every furniture colour — spines, ticks, fonts, grid, legend frame, value labels, annotation boxes, heatmap frame and separators — carries a light counterpart, and the marks take a six-colour bright palette over the Viridis value scale.

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
        "plot_hatch_cycle": ["", "//", "..", "xx", "\\"],
        "plot_linestyle_cycle": ["-", "--", "-.", ":", "-"],
        "plot_marker_cycle": ["o", "s", "^", "D", "v"],
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
        "plot_dline_color": "#5D6D7E",
        "plot_dline_style": LINE_STYLE.DASHED,
        "plot_bracket_color": "#5D6D7E",
        "plot_vspan_color": "#5D6D7E",
        "plot_hspan_color": "#5D6D7E",
        "plot_text_box_edgecolor": "#B0B0B0",
        "plot_text_arrow_color": "#5D6D7E",
        "plot_gantt_dependency_color": "#2C3E50",
        "plot_gantt_today_color": "#2C3E50",
        "plot_dumbbell_start_color": "#9EA9B4",
        "plot_dumbbell_end_color": "#1A232B",
        "plot_dumbbell_edge_color": "#000000",
        "plot_dumbbell_connector_color": "#85929E",
        "plot_dumbbell_arrow_color": "#5D6D7E",
        "plot_heatmap_cmap": COLORS.Greys,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
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

The greyscale theme: five slate greys, hatches, dashes and markers, for print.

The greys sit 0.16 apart in lightness, so every pair reads apart on paper and for every colour-blind reader alike; bars carry a hatch cycle, lines a dash cycle and scatter points a marker cycle, so a sixth series still differs.

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
        "plot_dline_color": "#7F8C8D",
        "plot_dline_style": LINE_STYLE.DASHED,
        "plot_bracket_color": "#7F8C8D",
        "plot_vspan_color": "#7F8C8D",
        "plot_hspan_color": "#7F8C8D",
        "plot_text_box_edgecolor": "#000000",
        "plot_text_arrow_color": "#000000",
        "plot_gantt_dependency_color": "#0B1F44",
        "plot_gantt_today_color": "#0B1F44",
        "plot_dumbbell_start_color": "#85CFBA",
        "plot_dumbbell_end_color": "#2165AB",
        "plot_dumbbell_edge_color": "#0B1F44",
        "plot_dumbbell_connector_color": "#7F8C8D",
        "plot_dumbbell_arrow_color": "#34495E",
        "plot_heatmap_cmap": COLORS.YlGnBu,
        "plot_heatmap_cmap_diverging": COLORS.PuOr,
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
HATCH_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Rust,
    traits=[TRAIT.HATCHED, TRAIT.OUTLINED],
    color_general_singular=COLORS.YlOrBr,
    color_parallel_hue_continuous=[
        "#F3E0C3",
        "#E0AE6A",
        "#B5563A",
        "#6B2E1A",
    ],
    plot_dumbbell_start_color="#5A6F86",
    plot_dumbbell_end_color="#B5563A",
    plot_heatmap_cmap=COLORS.YlOrBr,
    plot_heatmap_cmap_diverging=COLORS.RdBu,
    **HATCH_FURNITURE
)
```

The hatch theme: hatch cycle, black edges, dotted grid.

The `Rust` lead, muted print tones with rust first and the green deep enough to stay apart from rust for deutan readers; the hatched trait gives every bar series its own hatch under black edges, the outlined trait black outlines on every other mark, and the grid is dotted. The value scale is YlOrBr.

### datachart.themes.MUTED_THEME

```
MUTED_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.TolMuted,
    traits=[TRAIT.PATTERNED, TRAIT.EDGED],
    color_general_singular=COLORS.YlOrBr,
    color_parallel_hue_continuous=[
        "#FEE391",
        "#FE9929",
        "#CC4C02",
        "#662506",
    ],
    plot_heatmap_cmap=COLORS.YlOrBr,
    **MUTED_FURNITURE,
    plot_heatmap_cmap_diverging=COLORS.RdBu
)
```

The muted theme: Tol's muted colours, dashes and markers, colour-blind safe.

The `TolMuted` lead, indigo, cyan, sand, rose and wine from Paul Tol's muted scheme, every pair distinct for deutan, protan and tritan readers. The patterned trait gives lines a dash and scatter points a marker, the edged trait black bar edges, and the grid is dotted, so a figure survives a greyscale print. The value scale is YlOrBr.

### datachart.themes.CONTRAST_THEME

```
CONTRAST_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Contrast,
    traits=[TRAIT.PATTERNED, TRAIT.HATCHED],
    color_general_singular=COLORS.Cividis,
    color_parallel_hue_continuous=[
        "#BCAE6C",
        "#7D7C78",
        "#434E6C",
        "#00224E",
    ],
    plot_line_width=1.4,
    plot_grid_color="#C8C8C8",
    plot_dumbbell_start_color="#D4B24C",
    plot_dumbbell_end_color="#1F4E79",
    plot_heatmap_cmap=COLORS.Cividis,
    plot_heatmap_cmap_diverging=COLORS.RdBu,
)
```

The contrast theme: lightness-stepped colours plus hatches, print-safe.

The `Contrast` lead, navy, straw, dusty rose, charcoal and grey, each a clear lightness step from the next, so a greyscale print or photocopy still tells the series apart, and every pair stays distinct for deutan, protan and tritan readers. The hatched trait gives bars a hatch cycle and black edges, the patterned trait lines a dash cycle and scatter points a marker cycle. The value scale is Cividis.

### datachart.themes.MUTEDHATCH_THEME

```
MUTEDHATCH_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.TolMuted,
    traits=[TRAIT.PATTERNED, TRAIT.HATCHED],
    color_general_singular=COLORS.BuPu,
    color_parallel_hue_continuous=[
        "#EDF8FB",
        "#9EBCDA",
        "#8856A7",
        "#4D004B",
    ],
    plot_heatmap_cmap=COLORS.BuPu,
    plot_heatmap_cmap_diverging=COLORS.BrBG,
    **MUTED_FURNITURE
)
```

The muted-hatch theme: Tol's muted colours under hatches.

The muted theme with the hatched trait in place of the edged one: indigo, cyan, sand, rose and wine bars take the hatch cycle and black edges, lines keep the muted dashes and markers. The value scale is BuPu.

### datachart.themes.SLATEHATCH_THEME

```
SLATEHATCH_THEME: StyleAttrs = derive_theme(
    DEFAULT_THEME,
    lead=COLORS.Slate,
    traits=[TRAIT.HATCHED, TRAIT.OUTLINED],
    color_general_singular=COLORS.PuBu,
    color_parallel_hue_continuous=[
        "#F1EEF6",
        "#A6BDDB",
        "#3690C0",
        "#023858",
    ],
    plot_dumbbell_start_color="#4F6D8F",
    plot_dumbbell_end_color="#743538",
    plot_heatmap_cmap=COLORS.PuBu,
    plot_heatmap_cmap_diverging=COLORS.BrBG,
    **HATCH_FURNITURE
)
```

The slate-hatch theme: the hatch theme without rust.

The `Slate` lead, slate blue, sand, wine, green, orchid and sky blue, under the hatch theme's hatched and outlined traits and dotted grid; every pair stays apart for deutan and protan readers. The value scale is PuBu.

### datachart.themes.SKETCH_THEME

```
SKETCH_THEME: StyleAttrs = make_theme(
    {
        "color_general_singular": COLORS.YlOrRd,
        "color_general_multiple": [
            "#E4572E",
            "#3F84A3",
            "#F4BA2D",
            "#784AAD",
            "#90B376",
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
        "plot_dumbbell_start_color": "#3F84A3",
        "plot_dumbbell_end_color": "#E4572E",
        "plot_dumbbell_edge_color": "#222222",
        "plot_dumbbell_connector_color": "#8A8A8A",
        "plot_heatmap_cmap": COLORS.YlOrRd,
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
        "plot_treemap_group_edge_width": 0,
        "plot_sketch_params": [0.5, 100, 2],
        "plot_sketch_halo_width": 1.5,
    }
)
```

The sketch theme: hand-drawn, xkcd-style wobble and halo, Comic Neue font.

Paths wobble, lines carry a white halo, spines and lines are thick, the grid is off, and text is set in Comic Neue, downloaded on first use; Humor Sans and Comic Sans MS are the fallbacks should the download fail.

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
        "chart_default_network_label_position": NETWORK_LABEL_POSITION.ABOVE,
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
        "plot_value_tab": {
            "facecolor": PAPER,
            "edgecolor": INK,
            "line_width": 0.6,
            "pad": 0.16,
            "rounding": 0.1,
        },
        "plot_hist_alpha": 1.0,
        "plot_hist_edge_width": 1.0,
        "plot_hist_edge_color": INK,
        "plot_vline_color": INK,
        "plot_vline_style": LINE_STYLE.DASHED,
        "plot_hline_color": INK,
        "plot_hline_style": LINE_STYLE.DASHED,
        "plot_dline_color": INK,
        "plot_dline_style": LINE_STYLE.DASHED,
        "plot_bracket_color": INK,
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
        "plot_heatmap_cmap_diverging": COLORS.RdBu,
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
        "plot_network_node_edge_width": 1.2,
        "plot_network_node_size": 70,
        "plot_network_node_alpha": 1.0,
        "plot_network_edge_color": FADED_INK,
        "plot_network_edge_alpha": 0.6,
        "plot_network_edge_style": ARROW_STYLE.STRAIGHT,
        "plot_network_edge_curve": 0.0,
        "plot_network_edge_width_min": 0.5,
        "plot_network_edge_width_max": 1.3,
        "plot_network_edge_ink_stroke": {
            "width_scale": 1.0,
            "nib_floor": 1.0,
            "wobble": 0.0,
            "swell": 0.0,
            "noise": 0.05,
        },
        "plot_network_label_family": "IM FELL English SC",
        "plot_network_label_halo_width": 5,
        "plot_network_group_linestyle": LINE_STYLE.DOTTED,
    }
)
```

The quill theme: black ink on white paper, as a quill and an etching needle draw.

One ink only: series differ by line style, marker and etching, never by color. Series lines are broad-nib pen strokes whose width varies along the line, bars, areas and bodies are etched by hand instead of hatched, the furniture wobbles, and text is set in IM Fell English, downloaded on first use, titles in its italic.
