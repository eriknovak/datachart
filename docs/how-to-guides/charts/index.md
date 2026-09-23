---
title: Charts
---

# Charts

The [datachart.charts](../../references/charts/index.md) module of the `datachart` package provides various chart types to create data visualizations. The module is designed to be highly customizable and easy to use.

The charts are grouped by the question they answer. Each card names a chart, says what it is for, and links to its how-to guide. The chips under the name say how the chart composes with the other charts through the [composition](../composition/index.md) functions:

- <span class="chip">Panel</span> — the chart can be overlaid with other charts in one coordinate space through [Panel](../utility/panel.ipynb). A chart that owns its whole axes (the heatmap, Sankey chart, treemap, network chart, calendar heatmap, and scatter matrix) or draws a mirrored or task axis (the pyramid and gantt charts) cannot, and shows <span class="chip chip-no">Panel</span>. The box, violin, raincloud, and ridgeline plots overlay with other kinds of charts, but a panel holds one dataset of each of these kinds.
- <span class="chip">Grid</span> — the chart can take a cell of a combined figure through [Grid](../utility/grid.ipynb). Every chart can.

A finished chart goes further through the [composition](../composition/index.md) guides, the [styling](../styling/index.md) guides, and the [utility](../utility/index.md) guides.

## Trends and Comparisons

Values along an axis or across categories: how a quantity moves and how the categories compare.

<div class="grid cards card-gallery" markdown>

-   [Line Chart](linechart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    How a value moves along a continuous axis, and how the trajectories of several series compare.

    ![A line chart of three series over nine years](../../assets/imgs/gallery-line.png)

-   [Stacked Area Chart](stackedareachart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    How a total splits into parts along an axis: the top edge traces the total, the bands its composition.

    ![A stacked area chart of three device types over nine years](../../assets/imgs/gallery-stackedarea.png)

-   [Bump Chart](bumpchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Rank over time: who leads and who overtakes whom, with each series named at the end of its line.

    ![A bump chart ranking four cities over five seasons](../../assets/imgs/gallery-bump.png)

-   [Bar Chart](barchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    A numeric value across a few categories; several series can be grouped, stacked, or overlaid.

    ![A grouped bar chart of three regions over four quarters](../../assets/imgs/gallery-bar.png)

-   [Pyramid Chart](pyramidchart.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    Two groups mirrored over the same ordered categories, such as an age-sex population pyramid.

    ![A population pyramid of men and women by age band](../../assets/imgs/gallery-pyramid.png)

-   [Radial Chart](radialchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Series on polar axes: a radar profile over several metrics, or bars over cyclic categories.

    ![A radar chart comparing two cars on six metrics](../../assets/imgs/gallery-radial.png)

-   [Calendar Heatmap](calendarheatmap.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    One cell per day, weeks as columns, for a daily series with a weekly or seasonal rhythm.

    ![A calendar heatmap of daily commits over six months](../../assets/imgs/gallery-calendarheatmap.png)

-   [Gantt Chart](ganttchart.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    A schedule: one bar per task over a date axis, with groups, progress, milestones, and dependencies.

    ![A gantt chart of five tasks in two groups with dependency arrows](../../assets/imgs/gallery-gantt.png)

-   [Dumbbell Chart](dumbbellchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Two values per category and the gap between them: before and after, or a minimum and a maximum.

    ![A dumbbell chart of life expectancy in five countries in 2000 and 2019](../../assets/imgs/gallery-dumbbell.png)

</div>

## Distributions

The spread of the values within each group, from a binned summary to every observation.

<div class="grid cards card-gallery" markdown>

-   [Histogram](histogram.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    The shape of one numeric variable, binned into counts; a few distributions can be overlaid.

    ![A histogram of two overlaid score distributions](../../assets/imgs/gallery-histogram.png)

-   [Box Plot](boxplot.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    The median, quartiles, whiskers, and outliers per group, for comparing many groups compactly.

    ![A box plot of three treatment groups](../../assets/imgs/gallery-box.png)

-   [Violin Plot](violinplot.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    The density profile of each group, showing the skew and the modes that a box plot hides.

    ![A violin plot of three treatment groups](../../assets/imgs/gallery-violin.png)

-   [Swarm Plot](swarmplot.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Every observation as a point at its group, spread so that none hide; for small to medium samples.

    ![A swarm plot of three treatment groups](../../assets/imgs/gallery-swarm.png)

-   [Raincloud Plot](raincloudplot.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    The density, the raw observations, and the quartile box of each group, side by side in one view.

    ![A raincloud plot of three treatment groups](../../assets/imgs/gallery-raincloud.png)

-   [Ridgeline Plot](ridgelineplot.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    One density ridge per group, stacked and overlapping: how a distribution shifts across many groups.

    ![A ridgeline plot of temperatures across six months](../../assets/imgs/gallery-ridgeline.png)

</div>

## Relationships

How two or more variables relate to each other.

<div class="grid cards card-gallery" markdown>

-   [Scatter Chart](scatterchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Two numeric variables per observation, with an optional regression line and correlation coefficient.

    ![A scatter chart of engine size against efficiency with a regression line](../../assets/imgs/gallery-scatter.png)

-   [Heatmap](heatmap.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    Every cell of a matrix as a color: correlations, confusion matrices, feature-by-time tables.

    ![A heatmap of a correlation matrix with the values printed](../../assets/imgs/gallery-heatmap.png)

-   [Contour Chart](contourchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    A surface sampled on a grid, as iso-lines or filled bands: densities, loss landscapes, terrain.

    ![A filled contour chart of a two-peaked density](../../assets/imgs/gallery-contour.png)

-   [Hexbin Chart](hexbinchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Point density on hexagonal tiles, where a scatter chart would turn into an opaque blob.

    ![A hexbin chart of two clusters with a colorbar](../../assets/imgs/gallery-hexbin.png)

-   [Parallel Coordinates](parallelcoords.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Each record as a polyline across one axis per dimension, colored by group to compare the groups.

    ![A parallel coordinates chart of car classes over four dimensions](../../assets/imgs/gallery-parallelcoords.png)

-   [Network Chart](networkchart.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    Relational data as a node-link diagram: edge weight sets the width, node group sets the color.

    ![A network chart of nine services in three groups](../../assets/imgs/gallery-network.png)

-   [Scatter Matrix](scattermatrix.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    A scatter chart for every pair of dimensions, with each dimension's distribution on the diagonal.

    ![A scatter matrix of three measurements split by species](../../assets/imgs/gallery-scattermatrix.png)

-   [Image Chart](imagechart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    A picture in data coordinates, under or over another chart: a map, a floor plan, a microscope image.

    ![Stations scattered over a shaded relief](../../assets/imgs/gallery-image.png)

-   [Basemap Chart](basemapchart.ipynb)

    [Panel](../utility/panel.ipynb){ .chip } [Grid](../utility/grid.ipynb){ .chip }

    Coastlines, land, borders, lakes, rivers and roads under a chart of longitude and latitude, from Natural Earth.

    ![Epicentres over the land and borders of the Aegean and Anatolia](../../assets/imgs/gallery-basemap.png)

</div>

## Flows

How a quantity moves between categories: where it comes from and where it goes.

<div class="grid cards card-gallery" markdown>

-   [Sankey Chart](sankeychart.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    Weighted flows between categories through ordered stages: funnels, label transitions, energy budgets.

    ![A Sankey chart of a signup funnel from three sources](../../assets/imgs/gallery-sankey.png)

</div>

## Part of a Whole

How a whole splits into parts, and parts into smaller parts.

<div class="grid cards card-gallery" markdown>

-   [Treemap](treemap.ipynb)

    <span class="chip chip-no">Panel</span> [Grid](../utility/grid.ipynb){ .chip }

    Part-of-whole data as nested rectangles whose area is the value, up to four levels deep.

    ![A treemap of world population by continent and country](../../assets/imgs/gallery-treemap.png)

</div>

## Across Charts

The options every chart shares, worth a guide of their own.

<div class="grid cards card-gallery" markdown>

-   [Highlighting](../styling/highlighting.ipynb)

    Emphasizing and muting data series with the `emphasis` option, by role or by rule, on any chart.

    ![A line chart with one series highlighted and the rest muted](../../assets/imgs/gallery-highlighting.png)

</div>
