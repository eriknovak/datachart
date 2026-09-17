---
title: Utility
---

# Utility

The utilities of the [datachart.utils](../../references/utils/index.md) module around a figure: the numbers behind the charts, getting a figure out to where it is read, and inspecting it while it is still on screen. Each card names a guide, says what it is for, and links to it.

<div class="grid cards card-gallery" markdown>

-   [Statistics](stats.ipynb)

    The numbers behind the charts, in [datachart.utils.stats](../../references/utils/stats.md): centers, spreads, correlations, fits, intervals, smoothers and densities, each shown feeding back into a chart's title, error bars, or an overlaid series.

    <p class="card-icon" markdown="span">:material-sigma:</p>

-   [Saving Figures](saving.md)

    Writes a figure to disk through [datachart.utils.save_figure](../../references/utils/index.md#datachart.utils.save_figure): the format, resolution and background for a manuscript, a slide, and a web page, in one call or several at once.

    <p class="card-icon" markdown="span">:material-content-save-outline:</p>

-   [Interactive Figures](interactive.md)

    Shows a figure with zoom, pan, and hover over its marks through the `interactive` flag of every figure's `show()` method, to read the point behind an outlier or check a value without labelling it.

    ![A line chart with a hovered point showing its values](../../assets/imgs/hover-line.png)

</div>
