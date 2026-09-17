---
title: Utils Module
---

# Utils Module

::: datachart.utils
    options:
        members: False
        heading_level: 2

## Choosing a Utility

Everything here takes or returns the figure a chart function returns: three ways to compose finished figures, one to save them, and the statistics behind them.

| I want to…                                                        | Use                                              | Guide |
| :---------------------------------------------------------------- | :----------------------------------------------- | :---- |
| draw several charts in one coordinate space, with a second value axis | [`Panel`](#datachart.utils.Panel)            | [Panel](../../how-to-guides/utility/panel.ipynb) |
| lay charts out side by side or in rows                            | [`Grid`](#datachart.utils.Grid)                  | [Grid](../../how-to-guides/utility/grid.ipynb) |
| add notes to a figure that is already drawn                       | [`Annotate`](#datachart.utils.Annotate)          | [Text Annotations](../../how-to-guides/utility/annotations.ipynb) |
| write a figure to disk, in one format or several                  | [`save_figure`](#datachart.utils.save_figure)    | [Saving Figures](../../how-to-guides/utility/saving.md) |
| compute the number a chart shows                                  | [`stats`](stats.md)                              | [Statistics](../../how-to-guides/utility/stats.ipynb) |

## Composition

::: datachart.utils.Panel

::: datachart.utils.Grid

::: datachart.utils.Annotate

## Output

::: datachart.utils.save_figure
