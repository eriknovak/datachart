# Charts

The [datachart.charts](https://eriknovak.github.io/datachart/dev/references/charts/index.md) module of the `datachart` package provides various chart types to create data visualizations. The module is designed to be highly customizable and easy to use.

The charts are grouped by the question they answer. Each card names a chart, says what it is for, and links to its how-to guide. The chips under the name say how the chart composes with the other charts through the [composition](https://eriknovak.github.io/datachart/dev/how-to-guides/composition/index.md) functions:

- Panel — the chart can be overlaid with other charts in one coordinate space through [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md). A chart that owns its whole axes (the heatmap, Sankey chart, treemap, network chart, calendar heatmap, and scatter matrix) or draws a mirrored or task axis (the pyramid and gantt charts) cannot, and shows Panel. The box, violin, raincloud, and ridgeline plots overlay with other kinds of charts, but a panel holds one dataset of each of these kinds.
- Grid — the chart can take a cell of a combined figure through [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md). Every chart can.

A finished chart goes further through the [composition](https://eriknovak.github.io/datachart/dev/how-to-guides/composition/index.md) guides, the [styling](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/index.md) guides, and the [utility](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/index.md) guides.

## Trends and Comparisons

Values along an axis or across categories: how a quantity moves and how the categories compare.

- [Line Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  How a value moves along a continuous axis, and how the trajectories of several series compare.

- [Stacked Area Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/stackedareachart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  How a total splits into parts along an axis: the top edge traces the total, the bands its composition.

- [Bump Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/bumpchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Rank over time: who leads and who overtakes whom, with each series named at the end of its line.

- [Bar Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/barchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  A numeric value across a few categories; several series can be grouped, stacked, or overlaid.

- [Pyramid Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/pyramidchart/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Two groups mirrored over the same ordered categories, such as an age-sex population pyramid.

- [Radial Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/radialchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Series on polar axes: a radar profile over several metrics, or bars over cyclic categories.

- [Calendar Heatmap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/calendarheatmap/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  One cell per day, weeks as columns, for a daily series with a weekly or seasonal rhythm.

- [Gantt Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/ganttchart/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  A schedule: one bar per task over a date axis, with groups, progress, milestones, and dependencies.

- [Dumbbell Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/dumbbellchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Two values per category and the gap between them: before and after, or a minimum and a maximum.

## Distributions

The spread of the values within each group, from a binned summary to every observation.

- [Histogram](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/histogram/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  The shape of one numeric variable, binned into counts; a few distributions can be overlaid.

- [Box Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/boxplot/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  The median, quartiles, whiskers, and outliers per group, for comparing many groups compactly.

- [Violin Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/violinplot/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  The density profile of each group, showing the skew and the modes that a box plot hides.

- [Swarm Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/swarmplot/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Every observation as a point at its group, spread so that none hide; for small to medium samples.

- [Raincloud Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/raincloudplot/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  The density, the raw observations, and the quartile box of each group, side by side in one view.

- [Ridgeline Plot](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/ridgelineplot/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  One density ridge per group, stacked and overlapping: how a distribution shifts across many groups.

## Relationships

How two or more variables relate to each other.

- [Scatter Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scatterchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Two numeric variables per observation, with an optional regression line and correlation coefficient.

- [Heatmap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/heatmap/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Every cell of a matrix as a color: correlations, confusion matrices, feature-by-time tables.

- [Contour Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/contourchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  A surface sampled on a grid, as iso-lines or filled bands: densities, loss landscapes, terrain.

- [Hexbin Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/hexbinchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Point density on hexagonal tiles, where a scatter chart would turn into an opaque blob.

- [Parallel Coordinates](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/parallelcoords/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Each record as a polyline across one axis per dimension, colored by group to compare the groups.

- [Network Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/networkchart/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Relational data as a node-link diagram: edge weight sets the width, node group sets the color.

- [Scatter Matrix](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/scattermatrix/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  A scatter chart for every pair of dimensions, with each dimension's distribution on the diagonal.

- [Image Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/imagechart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  A picture in data coordinates, under or over another chart: a map, a floor plan, a microscope image.

- [Basemap Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/basemapchart/index.md)

  [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Coastlines, land, borders and lakes under a chart of longitude and latitude, bundled with the package.

## Flows

How a quantity moves between categories: where it comes from and where it goes.

- [Sankey Chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/sankeychart/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Weighted flows between categories through ordered stages: funnels, label transitions, energy budgets.

## Part of a Whole

How a whole splits into parts, and parts into smaller parts.

- [Treemap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/treemap/index.md)

  Panel [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md)

  Part-of-whole data as nested rectangles whose area is the value, up to four levels deep.

## Across Charts

The options every chart shares, worth a guide of their own.

- [Highlighting](https://eriknovak.github.io/datachart/dev/how-to-guides/styling/highlighting/index.md)

  Emphasizing and muting data series with the `emphasis` option, by role or by rule, on any chart.
