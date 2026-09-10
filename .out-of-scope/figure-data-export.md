# Figure data export

datachart does not provide a way to read the plotted values back out of a
rendered figure. There is no `figure_data`, no `save_data`, and no `data()`
hook on `Layer`. A figure is an image; the data behind it stays with the
caller who passed it in.

## Why this is out of scope

For most chart types the request is a round trip. `LineChart`,
`ScatterChart`, `BarChart`, and `StackedAreaChart` draw the columns they were
handed, so a record per layer would return the caller's own input to them:

```python
data = [{"x": xs, "y": ys}]
figure = LineChart({"charts": data})
# figure_data(figure) would hand back xs and ys, which the caller still holds
```

The values datachart genuinely derives are mostly public already. Bin edges
and counts, density curves, fits, quantiles, and smoothing all live in
`datachart.utils.stats` as `histogram`, `kde1d`, `kde2d`, `linear_fit`,
`quantile`, `iqr`, `loess`, `rolling_mean`, and `ewma`. A user who wants the
numbers behind a histogram or a violin calls the same function the chart
calls, on the same input, and gets the same answer.

What would remain is a thin residue: layout geometry a chart invents for
itself, such as treemap tile rectangles, Sankey node boxes, and network node
coordinates, plus the settings a chart resolved on the caller's behalf, such
as a bin count it picked or the bins a `Panel` shared across its layers.
That residue is not worth a public API and 22 `Layer` hooks to maintain, and
exposing tile rectangles or node coordinates would freeze layout internals
into the public surface, where a layout improvement becomes a breaking
change.

The design questions the export raises have no cheap answers either. A flat
record list loses which grid cell a record came from; a long-format CSV has
no shared column set across a heatmap grid, a Sankey edge list, and a network
node set; and every layer would need a data vocabulary parallel to the hover
datums it already builds for `show(interactive=True)` (ADR 0031), against
ADR 0001's single drawing seam.

Users who need the CSV behind a paper figure should save the data they
plotted, at the point they plot it. It is the same data.

## Prior requests

- #127 — "feat(utils): export the data behind a figure"
