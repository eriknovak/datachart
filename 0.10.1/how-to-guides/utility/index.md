# Utility

The utilities of the [datachart.utils](https://eriknovak.github.io/datachart/0.10.1/references/utils/index.md) module around a figure: the numbers behind the charts, getting a figure out to where it is read, and inspecting it while it is still on screen. Each card names a guide, says what it is for, and links to it.

- [Statistics](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/utility/stats/index.md)

  The numbers behind the charts, in [datachart.utils.stats](https://eriknovak.github.io/datachart/0.10.1/references/utils/stats/index.md): centers, spreads, correlations, fits, intervals, smoothers and densities, each shown feeding back into a chart's title, error bars, or an overlaid series.

- [Saving Figures](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/utility/saving/index.md)

  Writes a figure to disk through [datachart.utils.save_figure](https://eriknovak.github.io/datachart/0.10.1/references/utils/#datachart.utils.save_figure): the format, resolution and background for a manuscript, a slide, and a web page, in one call or several at once.

- [Interactive Figures](https://eriknovak.github.io/datachart/0.10.1/how-to-guides/utility/interactive/index.md)

  Shows a figure with zoom, pan, and hover over its marks through the `interactive` flag of every figure's `show()` method, to read the point behind an outlier or check a value without labelling it.
