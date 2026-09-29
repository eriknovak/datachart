### datachart-1.0.0 (2026-09-29)

**Breaking Changes**

- Removed every remaining pre-1.0 deprecation shim and alias; starting at 1.0.0 datachart follows SemVer for its programmatic API (not visual output), with future removals going through a one-release deprecation cycle (see `docs/versioning.md`)
- Renamed shared front parameters: `show_heatmap_values`→`show_values`, `valfmt`→`value_format`, `normalize`→`ridge_scale` (RidgelinePlot), `features`→`data` (BasemapChart), `type`→`mark` (RadialChart), `startangle`→`start_angle`, `innerradius`→`inner_radius`, `filled`→`fill`, `mode`→`swarm_mode`, `mincnt`→`min_count`, `gridsize`→`grid_size` (HexbinChart; `kde1d`/`kde2d`'s own `gridsize` is also now `grid_size`), `show_colorbars`→`show_colorbar`
- `ScatterChart`'s per-point `label` parameter and `"label"` record key are renamed to `annotation`
- Renamed constants: `SCALE`→`AXIS_SCALE`, `NORMALIZE`→`COLOR_NORM`, `LINE_MARKER.NONE`→`NO_MARKER`, `LINE_STYLE.NONE`→`NO_LINE`, `SCATTER_MATRIX_DIAGONAL.NONE`→`BLANK`; every constant now validates itself once at the front, and an unrecognised `bar_mode` raises `ValueError` instead of silently falling back to `"group"`
- Renamed theme default keys to one naming rule: `plot_calendar_heatmap_week_start`→`chart_default_calendar_heatmap_week_start`, `plot_ridgeline_overlap`→`chart_default_ridgeline_overlap`, plus a renamed node-label-position key; tick-label rotation keys are unified to `axes_x/yticks_label_rotate`
- Typing renames: record types now end in `RecordAttrs` (`LineRecordAttrs`, `GanttTaskRecordAttrs`, ...); removed 19 unused `*SingleChartAttrs`; added `OverlayStyleAttrs`
- `stats.correlation` is renamed to `stats.pearson`; `kde1d`/`kde2d` return named columns; `Config.update`/`Config.reset` replace `update_config`/`reset_config`; `save_figure(fmt=...)` replaces `format=`
- Every record front now reads its data through the builder's canonical keys; `GanttChart` and `DumbbellChart` gain named keys (`task`/`start`/`end`/`group`/`progress`/`depends_on`, `label`/`start`/`end`) in place of positional dict shapes
- `Panel.show_legend` now defaults to `None` (was `False`); `Panel` gains `emphasis_rule`; `Grid` gains `show_legend`, `legend`, `show_grid`, `xmin`/`xmax`, `ymin`/`ymax`, and `aspect_ratio`
- Bump-chart end labels print in the text colour instead of the series colour, matching the new `show_labels`/`label_position` on `LineChart`/`StackedAreaChart`; the `BUMP_LABEL_POSITION` alias is gone in favour of `LINE_LABEL_POSITION`
- No predefined theme titles its legend by default (`plot_legend_title` is `None` on the base theme); `MUTED`, `MUTEDHATCH`, `HATCH`, and `SLATEHATCH` draw the base theme's solid grid
- Greyscale, hatch, ink, sketch, material, and minimal themes are re-stepped to pass a colour-blindness scoring gate (`score_palette`), changing some of their colours; `register_theme`/`derive_theme` warn when a custom palette fails it
- Malformed record/column data now raises one `ValueError` naming the front, the expected shape, and the offending index, instead of drawing garbage or crashing inside matplotlib/numpy
- `None`, `NaN`, and `inf` values are now uniformly dropped rather than raising or drawing garbage, across `utils.stats` and the bar/histogram/scatter/group/contour layers
- Added validation at previously-silent entry points: `bandwidth`, `Panel`/`Grid` dict keys, legend location, `RadialChart`'s required keys, and `stats.histogram` NaN input
- `__all__` now defines each module's public surface, hiding internal helpers previously visible on `constants`, `typings`, `config`, `utils.stats`, `utils.compose`, and `utils.figure`
- Theme faces (fonts) and the basemap outlines download and cache on first use instead of shipping in the wheel; a smaller install now needs network access the first time those features are used

**New Features**

- Added `BasemapChart`: coastlines, land, borders, lakes, rivers, roads, and country highlighting (`highlight=`) from Natural Earth, downloaded and cached rather than bundled; added the `GEOGRAPHIC` aspect ratio
- Added `ImageChart` for pictures anchored to a data extent
- Added pairwise comparison `brackets`, a fourth reference-mark family alongside `vlines`/`hlines`/`vspans`
- Added diagonal reference lines (`dlines`), a third reference-line family defaulting to the parity line `y = x`
- Added a centred/diverging heatmap norm (`norm="centered"`/`"twoslope"`, `vcenter`) with a diverging colormap on every theme
- Added scatter point error bars (`xerr`/`yerr`, symmetric or `[low, high]`), reported in interactive hover
- Added end labels (`show_labels`, `label_position`) on `LineChart` and `StackedAreaChart`
- Added the `DARK`, `MUTEDHATCH`, and `SLATEHATCH` themes, and `derive_theme` to build a theme variant from a colormap, the basis the six bundled themes are now built from
- Shipped `py.typed`; every front returns the public `DatachartFigure` type; `PanelItem`/`GridItem`/`LayoutSpec` are typed composition settings
- Documentation: a Use Cases section (seven pages walking a real dataset end to end per field), and a stated versioning/deprecation policy with a new CONTRIBUTING.md

**Bug Fixes**

- Raised dependency floors (matplotlib, numpy, scipy, pypalettes, typing-extensions) to versions the code actually needs, and test them in CI at `--resolution lowest-direct`
- Removed the package's private-matplotlib touchpoints bar one, which is guarded by an import-time signature check with a graceful, warned fallback
- Bars, radial marks, and stacks are placed against one shared category index per panel, so series with mismatched label sets or order no longer misplace bars or crash
- Bars, histograms, and areas on twin axes stack per value axis instead of pooling heights across axes
- Fixed six silently-wrong renders: bars/labels drawn at the true value on a log axis, flat mark lists (`vlines`/`hlines`/etc.) applying to every chart instead of scattering across datasets, pypalettes' padded repeats no longer duplicating colors, `hue="label"` no longer force-annotating every scatter point, honest placement of one-value/missing parallel-coordinate cells, and Panel tick formats mapping to the correct axis role
- Previously-crashing valid inputs now render or raise a clear `ValueError`: NaN in groups/histograms/scatter fits, degenerate spread in violin/ridge/KDE, single-dataset per-chart settings, empty dict data, and `CalendarHeatmap`'s flat record lists
- `create_color_cycle` warns once when series, hue levels, groups, or nodes outrun the palette size, instead of silently repeating colors

### datachart-0.10.2 (2026-09-18)

**Breaking Changes**

- Removed the deprecated `VLinePlotAttrs`, `HLinePlotAttrs`, `TextAttrs`, `HeatmapColorbarAttrs`, and `ChartCommonAttrs` names announced in 0.10.0

**Bug Fixes**

- Heatmap value labels turn white on any dark cell, judged per cell, so colormaps with a dark low end such as Cividis stay readable

### datachart-0.10.1 (2026-09-18)

**New Features**

- Added the `HARBOR`, `MUTED`, and `CONTRAST` colour-blind-safe themes
- Made the `DEFAULT` palette colour-blind safe with a softened Okabe–Ito set closed with charcoal
- Gave every theme its own lead hue: `MINIMAL` is violet, and `MATERIAL`, `HATCH`, and `SKETCH` no longer share the default blue
- Added `COLORS.YlOrBr`
- Scored every theme for colour-blindness suitability in the theme gallery

**Bug Fixes**

- `color_parallel_hue` defaults to `None` and takes `color_general_multiple`, so parallel coords hue categories follow the active theme

### datachart-0.10.0 (2026-09-18)

**Breaking Changes**

- Chart-specific constants carry their chart's prefix: `BASELINE` is now `STACKED_AREA_BASELINE` and `DIRECTION` is now `RADIAL_DIRECTION`
- A log axis raises `ValueError` on data at or below zero instead of silently dropping the points
- Box, violin, swarm, and raincloud groups sit at 0-based positions like bars, so reference lines and annotation targets aimed at a group shift by one
- The `MINIMAL`, `MATERIAL`, and `HATCH` themes no longer show value labels by default

**Deprecations**

- `VLinePlotAttrs`, `HLinePlotAttrs`, `TextAttrs`, and `HeatmapColorbarAttrs` are renamed to `VLineSettingAttrs`, `HLineSettingAttrs`, `TextSettingAttrs`, and `ColorbarSettingAttrs`; the old names warn and are removed in the next release
- `ChartCommonAttrs` warns and is removed in the next release

**New Features**

- Added `BumpChart` with the `BUMP_RANK` and `BUMP_LABEL_POSITION` constants
- Added `CalendarHeatmap` with the `CALENDAR_WEEKDAY` constant
- Added `RidgelinePlot` with the `RIDGELINE_SCALE` constant
- Added `GanttChart` with periods, group headers, milestones, dependency arrows, and a today marker, plus the `GANTT_VALUE`, `GANTT_SORT_KEY`, `GANTT_ARROW_ENTRY`, and `GANTT_DATE_PERIOD` constants
- Added `DumbbellChart` with the `DUMBBELL_VALUE` and `DUMBBELL_SORT_KEY` constants
- Added `ScatterMatrix` with the `SCATTER_MATRIX_DIAGONAL` constant
- Added the `QUILL` theme: black ink on white paper with a bundled IM Fell English font, and the ink stroke, etch, hatch cycle, line-style cycle, and marker cycle attributes behind it
- Added `NETWORK_LAYOUT.WEIGHTED` and `NETWORK_LAYOUT.GROUPED`, and the `NETWORK_LABEL_POSITION` constant
- Added `figure.show(interactive=True)` for zoom, pan, and hover-to-inspect on every chart, behind the `datachart[interactive]` extra
- Added value labels (`show_values`, `value_format`) to line, scatter, histogram, stacked area, box, violin, swarm, and raincloud charts, with a halo behind them
- Added scatter point labels
- Added the per-figure `legend` setting (title, location, columns, alignment) and the `LEGEND_LOCATION.OUTSIDE_*` locations
- Added the per-figure `colorbar` setting with label, four-edge location, format, and ticks
- Added reference bands (`vspans`, `hspans`) to every chart that takes reference lines, and to `RadialChart`
- Added a datetime x axis on continuous charts, dated group labels, and the `xticks_format` / `yticks_format` settings with the `DATE_FORMAT` constant
- Added `sort` and `sort_by` to bar, pyramid, radial, box, and violin charts with the `SORT` constant
- Added `emphasis_rule` to every chart and per-record emphasis on bar, scatter, and swarm records
- Added `Panel` axis scales (`scalex`, `scaley`, `scaley_right`)
- Added `Annotate` targeting of a multi-subplot figure's subplots with the `subplot` index
- Added `config.override` and `config.using_theme` context managers, `config.list_themes`, and JSON theme files through `config.save_theme` / `config.load_theme`
- Added `spearman`, `mode`, `skewness`, `kurtosis`, `linear_fit`, `bootstrap_ci`, `histogram`, `rolling_mean`, `ewma`, and `loess` to `utils.stats`; `minimum` and `maximum` accept datetimes and the paired helpers accept a temporal x
- `save_figure` writes several formats in one call and returns the paths written
- `Treemap` nests groups four levels deep, fills a group's box in its own color, and takes one pad for the top-level gap and the gutter
- A plain color string is accepted wherever a palette name is
- Documentation: a landing page, one reference page per chart, chart guides rewritten around real datasets, figures for every constant, and notebooks executed at build time

**Bug Fixes**

- Draw reference lines over marks, and filled surfaces under lines in a `Panel`
- Keep every subplot's data inside shared axes and end an axis on the tick its data sits on
- Keep a subplots figure's title, labels, and sharing in a `Grid` cell
- Draw a subplot in the color a single chart uses
- Hide value labels and marks anchored past a user-set axis limit
- Estimate densities and regressions in log space on a log axis
- Convert text positions through the axis units on a date axis
- Give a covered legend headroom at the value-axis end and draw it over right-axis marks
- Keep an outside-top legend under a grid cell's title and color the legend title like its labels
- List labelled reference lines beside a chart's own legend keys
- Draw one shared reference dict once per axes, and a right-axis figure's references in its own coordinates
- `Panel`: adopt a source figure's bar mode, let a figure with no scale abstain from the axis vote, and raise on a heatmap figure
- Colorbar: reserve room for every aspect-locked bar, keep it in tight saves, keep the axis label beside its ticks, and drop explicit ticks outside the mapped range
- Key treemap and sankey colors by input order
- A single color makes a colormap with both ends; spell `Magma`, `Turbo`, and `OkabeIto_Black` as pypalettes knows them
- Fall back to Liberation Sans where Helvetica and Arial are missing, and take the theme font on heatmap values, contour labels, colorbar ticks, and parallel labels
- Drop the theme edge on markers too small to carry it
- A `plot_bar_value_*` alias wins over a spread theme's canonical key
- Histogram: pool the observations a point holds in a list, break a step outline where a log axis has no zero, and end a cumulative step outline at its total
- Parallel coordinates: snap a numeric dimension to its enclosing ticks, span the hue ramp over every record, and accept a flat dimensions list or a missing per-set entry
- Radial: place the r tick labels between the first two spokes and let `show_grid` select which polar grid set draws
- Pyramid: pin the value axis to a user `xmax` and keep the legend headroom fit symmetric
- Sankey: keep ribbon values off the node bars
- Box and violin: key the subtitle in the legend and raise on a dataset list without subplots
- Swarm: pack overlaid points as one cloud, draw unfilled markers as strokes in the series color, and draw dots whole on an axis end that sits on the data
- Scatter: one bubble size scale per axes
- Contour: fill values beyond an explicit levels list, accept numpy arrays as levels, and explain a filled contour given fewer than two levels
- Hexbin: bin hexagons in the axes' log scale
- Network: lay out disconnected spring graphs component by component and inset the fixed layout by the layout margin
- Annotations: cap the connector's target gap to the mark it names and keep the stub on a connector that still has room

### datachart-0.9.1 (2026-09-07)

**New Features**

- Added `NetworkChart` with the `NETWORK_LAYOUT` constant and `ARROW_STYLE.STRAIGHT`
- Added `Treemap` with squarified tiling and one-level nesting
- Added the `SKETCH` theme: hand-drawn wobble, halo, and a bundled Comic Neue font
- Restructured the README for onboarding with a charts table and rendered examples

**Bug Fixes**

- Clip network arrows at the true marker radius
- Keep the area floor fill unsketched under the sketch theme

### datachart-0.9.0 (2026-08-28)

**Breaking Changes**

- `Heatmap` takes `{x, y, z}` chart dicts
- Removed the deprecated composition fronts (`OverlayChart`, `FigureGridLayout`, `figure_grid_layout`) and the deprecated chart-attrs typing aliases

**New Features**

- Added `ViolinPlot` with inner marks, bandwidth control, and split halves, plus the `BANDWIDTH` constant
- Added `SwarmPlot`, composable with box and violin plots on a shared category index
- Added `RaincloudPlot`
- Added `ContourChart` with `contour_levels` and the `CONTOUR_LEVELS` constant
- Added `HexbinChart` with the `HEXBIN_REDUCE` constant
- Added `StackedAreaChart` with the `BASELINE` constant
- Added `SankeyChart` with column headings and ribbon values
- Added `kde1d` and `kde2d` density estimates to `utils.stats`
- Added figure-level `xlabel`/`ylabel` to `Grid`
- Versioned documentation, grouped chart index, and a theme gallery covering every chart

**Bug Fixes**

- Draw the grid below the marks and hug the data range in line-only panels
- Keep a host row's height when a nested grid sits alone in it
- Place colorbars with the layout engine
- Size the histogram y-range by its view

### datachart-0.8.1 (2026-08-26)

**New Features**

- Added `config.register_theme` for registering custom named themes usable with `set_theme`

### datachart-0.8.0 (2026-08-24)

**Breaking Changes**

- Renamed the themes for their visual trait: `THEME.DEFAULT`, `THEME.GREYSCALE`, `THEME.INK`, `THEME.HATCH`, `THEME.MINIMAL`, `THEME.MATERIAL`; removed `THEME.PUBLICATION` and `THEME.BACKGROUND`
- Replaced the background theme with `EMPHASIS` roles, set per chart or per figure
- `FIG_SIZE` is now an A4-anchored size grid; paper sizes respect print margins and the column gap
- Figures are no longer shown implicitly; showing goes through `Figure.show()` (inline display in Jupyter still works)
- Histogram stacking is now controlled via `bar_mode`

**New Features**

- Added `PyramidChart` for creating population pyramid charts
- Added `RadialChart` for creating radial bar charts
- Added text annotations to every chart and a post-hoc `Annotate` utility, with connectors placed by geometry and data
- Added the public `Panel` and `Grid` composition utilities; `Grid` figures nest recursively inside `Grid`, `Panel` figures flatten losslessly
- Added the `BAR_MODE` constant and support for `VALUE_FORMAT` constants in bar value labels
- Added heatmap cell borders via `plot_heatmap_edge_width` and `plot_heatmap_edge_color`
- Panels infer their orientation and orient the value axis accordingly
- Themes now drive chart defaults and support hatch cycles
- Revamped the documentation: how-to guides built around real-world datasets, a theme gallery, at-a-glance visualizations for all visual constants, and `llms.txt` endpoints generated at build

**Deprecations**

- `OverlayChart`, `FigureGridLayout`, and `figure_grid_layout` are deprecated; use `Panel` and `Grid` instead

**Bug Fixes**

- Center grouped bars, honor a per-chart `plot_bar_width`, and guard category ticks against ragged category counts
- Fill the area under lines down to the axis floor
- Keep bubble chart legend markers at the base marker size
- Apply themed label and tick furniture uniformly across composed figures; align nested grid axes with the host grid's columns
- Skip the legend when no handle carries a label

### datachart-0.7.3 (2025-12-06)

**Bug Fixes**

- Fix input parameter handling in different charts
- Rename `combine_figures` into `figure_grid_layout`

### datachart-0.7.2 (2025-12-05)

**Bug Fixes**

- Updated github workflows
- Fix problems regarding release (v0.7.1 was not created correctly)


### datachart-0.7.1 (2025-12-05)

**New Features**

- Add support for custom layout grids in `combine_figures`


### datachart-0.7.0 (2025-12-05)

**Breaking Change**

- All `chart` input parameters are now provided in a pythonic way (see documentation)
- Changed Python support to version 3.10, 3.11, 3.12, 3.13

**New Features**

- Added `ScatterChart` for creating scatter plots
- Added `BoxPlot` for creating box plots
- Added `ParallelCoords` for creating parallel coordinate plots
- Added `combine_figures` to create a combined grid layout of multiple figures
- Updated existing themes and added `THEME.PUBLICATION` that might be suitable for publication charts
- Added [pypalette](https://github.com/y-sunflower/pypalettes) dependancy; used for selecting colormaps
- Added [scipy](https://scipy.org/) dependancy; used for calculating statistics and regression lines
- Added new examples to the existing documentation


### datachart-0.6.3 (2024-10-17)

**Bug Fixes:**

- Fix `scaley` bug in `Histogram`


### datachart-0.6.2 (2024-08-16)

**Bug Fixes:**

- Fix `BarChart` bar position bug

### datachart-0.6.1 (2024-08-15)

**New Features:**

- Add `scale` support to `LineChart`, `BarChart` and `Histogram`

### datachart-0.6.0 (2024-08-13)

**Breaking Changes:**

- Renaming in the `charts` module
  - Rename the `line_chart` to `LineChart`
  - Rename the `bar_chart` to `BarChart`
  - Rename the `histogram` to `Histogram`
  - Rename the `heatmap` to `Heatmap`
- Renaming the `definitions` module into `typings`
- Renaming of `style` attributes in all modules

**New Features:**

- Complete rework of documentation
- Update project configuration
- Update githooks
- Add favicon

**Bug Fixes:**

- Fix `COLORS` selection

### datachart-0.5.0 (2023-11-24)

**New Features:**

- Add support for WebP output format
- Improve code imports
- Consistent variable naming
- Add code tests

**Bug Fixes:**

- Use consistent naming convention


### datachart-0.4.1 (2023-11-20)

**Bug Fixes:**

- Fix axis label position

### datachart-0.4.0 (2023-11-20)

**New Features:**

- Add heatmap visualization
- Add tick placement, label and rotation support

**Bug Fixes:**

- Fix Consistent attribute naming
- Fix attribute unit tests

### datachart-0.3.0 (2023-11-20)

**New Features:**

- Add vertical and horizontal line support
- Update documentation

### datachart-0.2.6 (2023-11-20)

**New Features:**

- Increase Python support to 3.8 - 3.12

**Bug Fixes:**

- Fix typing documentation

### datachart-0.2.5 (2023-11-20)

**New Features:**

- Add custom tick placement
- Add unit tests and CI/CD
- Add documentation

### datachart-0.1.0 (2023-07-21)

- Initial release

**New Features:**

- Add support for different types of charts: line chart, bar chart, histogram