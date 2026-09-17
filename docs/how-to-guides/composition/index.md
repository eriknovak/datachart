---
title: Composition
---

# Composition

The composition functions of the [datachart.utils](../../references/utils/index.md) module take figures already drawn by the chart functions and draw them again: overlaid in one coordinate space, side by side in a grid, or with annotations added. Each card names a guide, says what it is for, and links to it.

<div class="grid cards card-gallery" markdown>

-   [Panel](../utility/panel.ipynb)

    Overlays several charts in one coordinate space, with a shared x-axis and up to two y-axes, through [datachart.utils.Panel](../../references/utils/index.md#datachart.utils.Panel).

    ![A bar chart and a line chart overlaid on two y-axes](../../assets/imgs/gallery-panel.png)

-   [Grid Layout](../utility/grid.ipynb)

    Arranges several charts in the cells of one figure, with nested rows for the layout, through [datachart.utils.Grid](../../references/utils/index.md#datachart.utils.Grid).

    ![Four charts arranged in a two-by-two grid](../../assets/imgs/gallery-grid.png)

-   [Text Annotations](../utility/annotations.ipynb)

    Attaches text, boxes, and connectors to a chart through its `texts` parameter, or to a finished figure through [datachart.utils.Annotate](../../references/utils/index.md#datachart.utils.Annotate).

    ![A line chart with two annotations pointing at data points](../../assets/imgs/gallery-annotate.png)

</div>
