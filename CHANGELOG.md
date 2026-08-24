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