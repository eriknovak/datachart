# Themes

This section showcases the themes found in the [datachart.themes](https://eriknovak.github.io/datachart/dev/references/themes/index.md) module and how to customize them. Six predefined themes are available: `DEFAULT`, `GREYSCALE`, `MINIMAL`, `MATERIAL`, `INK`, and `HATCH` — each named for its visual trait — see the [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md) for every theme rendered across the full range of chart types.

Themes may also carry defaults for chart settings ([ThemeDefaultAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.ThemeDefaultAttrs)): `chart_default_show_grid` supplies the grid when a chart call leaves `show_grid` unset (every predefined theme ships a muted `"y"` grid), `chart_default_show_values` does the same for bar value labels (on in `MINIMAL`, `MATERIAL`, and `HATCH`), and `plot_hatch_cycle` assigns hatch patterns per bar/histogram series (only `HATCH` ships one). An explicit chart setting always wins over the theme default.

Let's start by importing the necessary functions to help us work with the `datachart.themes` module.

```
import random
import numpy as np
from datachart.charts import (
    BarChart,
    LineChart,
    ScatterChart,
)
from datachart.constants import FIG_SIZE, LINE_STYLE, SHOW_GRID
```

```
from datachart.config import config
```

To get the supported themes, you have to load them from the `datachart.themes` module.

```
from datachart.constants import THEME
```

The [datachart.constants.THEME](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.THEME) module contains all the predefined themes.

## Applying a Theme

Applying a theme replaces the whole global configuration, so set it before building the charts it should style:

```
config.set_theme(THEME.MINIMAL)

BarChart(
    data=[{"label": f"cat{idx}", "y": 10 + 5 * idx} for idx in range(5)],
    title="Bar chart under THEME.MINIMAL",
    figsize=FIG_SIZE.FULL_SHORT,
).show()
```

To return to the default theme, reset the configuration:

```
config.reset_config()
```

See the [Theme Gallery](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/theme-gallery/index.md) for every predefined theme rendered across the full range of chart types.

## Creating Your Own Theme

Adding the theme to the `datachart` package

If you think the theme would be useful and would like it to be added to the `datachart` package, please create a pull request to add it.

The user can create their own theme by defining a new dictionary that has the same structure as the [StyleAttrs](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.StyleAttrs) type.

For instance, one can copy the bellow definition of the default theme and modify the values to customize the theme.

```
from datachart.typings import StyleAttrs
from datachart.constants import COLORS, FONT_STYLE, FONT_WEIGHT, LINE_DRAW_STYLE
```

```
CUSTOM_THEME: StyleAttrs = {
    "color_general_singular": COLORS.Blues,
    "color_general_multiple": COLORS.Spectral,
    "font_general_family": "sans-serif",
    "font_general_sansserif": ["Helvetica", "Arial"],
    "font_general_color": "#000000",
    "font_general_size": 11,
    "font_general_style": FONT_STYLE.NORMAL,
    "font_general_weight": FONT_WEIGHT.NORMAL,
    "font_title_size": 12,
    "font_title_color": "#000000",
    "font_title_style": FONT_STYLE.NORMAL,
    "font_title_weight": FONT_WEIGHT.NORMAL,
    "font_subtitle_size": 11,
    "font_subtitle_color": "#000000",
    "font_subtitle_style": FONT_STYLE.NORMAL,
    "font_subtitle_weight": FONT_WEIGHT.NORMAL,
    "font_xlabel_size": 10,
    "font_xlabel_color": "#000000",
    "font_xlabel_style": FONT_STYLE.NORMAL,
    "font_xlabel_weight": FONT_WEIGHT.NORMAL,
    "font_ylabel_size": 10,
    "font_ylabel_color": "#000000",
    "font_ylabel_style": FONT_STYLE.NORMAL,
    "font_ylabel_weight": FONT_WEIGHT.NORMAL,
    "axes_spines_top_visible": True,
    "axes_spines_right_visible": True,
    "axes_spines_bottom_visible": True,
    "axes_spines_left_visible": True,
    "axes_spines_width": 0.5,
    "axes_spines_zorder": 100,
    "axes_ticks_length": 2,
    "axes_ticks_label_size": 9,
    "plot_legend_shadow": False,
    "plot_legend_frameon": True,
    "plot_legend_alignment": "left",
    "plot_legend_font_size": 9,
    "plot_legend_title_size": 10,
    "plot_legend_label_color": "#000000",
    "plot_area_alpha": 0.3,
    "plot_area_color": None,
    "plot_area_linewidth": 0,
    "plot_area_hatch": None,
    "plot_area_zorder": 3,
    "plot_grid_alpha": 1,
    "plot_grid_color": "#E6E6E6",
    "plot_grid_linewidth": 0.5,
    "plot_grid_linestyle": LINE_STYLE.SOLID,
    "plot_grid_zorder": 0,
    "plot_line_color": None,
    "plot_line_style": LINE_STYLE.SOLID,
    "plot_line_marker": None,
    "plot_line_width": 1,
    "plot_line_alpha": 1.0,
    "plot_line_drawstyle": LINE_DRAW_STYLE.DEFAULT,
    "plot_line_zorder": 3,
    "plot_bar_color": None,
    "plot_bar_alpha": 1.0,
    "plot_bar_width": 0.8,
    "plot_bar_zorder": 3,
    "plot_bar_hatch": None,
    "plot_bar_edge_width": 0.5,
    "plot_bar_edge_color": "#000000",
    "plot_bar_error_color": "#000000",
    "plot_hist_color": None,
    "plot_hist_alpha": 1.0,
    "plot_hist_zorder": 3,
    "plot_hist_fill": None,
    "plot_hist_hatch": None,
    "plot_hist_type": "bar",
    "plot_hist_align": "mid",
    "plot_hist_edge_width": 0.5,
    "plot_hist_edge_color": "#000000",
    "plot_vline_color": None,
    "plot_vline_style": LINE_STYLE.SOLID,
    "plot_vline_width": 1,
    "plot_vline_alpha": 1.0,
    "plot_hline_color": None,
    "plot_hline_style": LINE_STYLE.SOLID,
    "plot_hline_width": 1,
    "plot_hline_alpha": 1.0,
    "plot_heatmap_cmap": COLORS.Blues,
    "plot_heatmap_alpha": 1.0,
    "plot_heatmap_font_size": 9,
    "plot_heatmap_font_color": "#000000",
    "plot_heatmap_font_style": FONT_STYLE.NORMAL,
    "plot_heatmap_font_weight": FONT_WEIGHT.NORMAL,
}
```

Once you define the theme, you can use it by updating the `config` module in the following way:

```
from datachart.config import config
```

```
config.update_config(CUSTOM_THEME)
```

Once you do this, all the plots will use the custom theme.

**Bar Chart**

```
BarChart(
    data=[
        {"label": f"xx{id}", "y": 100 * (id + 1) * random.random()}
        for id in range(10)
    ],
    vlines=[{"x": 2 * i} for i in range(1, 4)],
    hlines={"y": 400},
    title="Title",
    xlabel="the global x-axis label",
    ylabel="the global y-axis label",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    xmin=-0.5,
    xmax=9.5,
).show()
```

**Line Chart**

```
LineChart(
    data=[
        [{"x": x / 10, "y": np.cos(x / 2)} for x in range(21)],
        [{"x": x / 10, "y": np.sin(x / 2)} for x in range(21)],
    ],
    subtitle=["cosine", "sine"],
    title="Title",
    xlabel="the global x-axis label",
    ylabel="the global y-axis label",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

**Scatter Chart**

```
chart_data_bubble_hue = [
    {
        "x": random.uniform(0, 10),
        "y": random.uniform(0, 10),
        "population": random.uniform(100, 1000),
        "region": random.choice(["North", "South", "East", "West"])
    }
    for _ in range(50)
]
```

```
ScatterChart(
    data=chart_data_bubble_hue,
    size="population",
    hue="region",
    size_range=(30, 250),
    title="Title",
    xlabel="the global x-axis label",
    ylabel="the global y-axis label",
    figsize=FIG_SIZE.FULL_SHORT,
    show_grid=SHOW_GRID.BOTH,
    show_legend=True,
).show()
```

## Registering a Theme

To make a custom theme switchable by name — like the predefined ones — register it with `config.register_theme`. Missing attributes are filled from the default theme, so a partial override works too:

```
config.register_theme("custom", CUSTOM_THEME)
config.set_theme("custom")
```

This is also how a private companion package can ship its own themes: register them on import and users apply them with `config.set_theme("<name>")`.

```
config.reset_config()
```

Finally, reset the configuration back to the default theme:

```
config.reset_config()
```
