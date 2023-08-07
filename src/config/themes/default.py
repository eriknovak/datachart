from schema.definitions import ConfigAttrs
from schema.constants import (
    LineStyle,
    FontStyle,
    FontWeight,
    LineDrawStyle,
)

DEFAULT_THEME: ConfigAttrs = {
    # general font configuration
    "font.general.family": "sans-serif",
    "font.general.sans-serif": ["Helvetica", "Arial"],
    "font.general.color": "#000000",
    "font.general.size": 11,
    "font.general.style": FontStyle.NORMAL,
    "font.general.weight": FontWeight.NORMAL,
    # title size configuration
    "font.title.size": 14,
    "font.title.color": "#000000",
    "font.title.style": FontStyle.NORMAL,
    "font.title.weight": FontWeight.NORMAL,
    # subtitle size configuration
    "font.subtitle.size": 12,
    "font.subtitle.color": "#000000",
    "font.subtitle.style": FontStyle.NORMAL,
    "font.subtitle.weight": FontWeight.NORMAL,
    # xlabel size configuration
    "font.xlabel.size": 10,
    "font.xlabel.color": "#000000",
    "font.xlabel.style": FontStyle.NORMAL,
    "font.xlabel.weight": FontWeight.NORMAL,
    # ylabel size configuration
    "font.ylabel.size": 10,
    "font.ylabel.color": "#000000",
    "font.ylabel.style": FontStyle.NORMAL,
    "font.ylabel.weight": FontWeight.NORMAL,
    # axes configuration
    "axes.spines.top.visible": True,
    "axes.spines.right.visible": True,
    "axes.spines.bottom.visible": True,
    "axes.spines.left.visible": True,
    "axes.spines.width": 0.5,
    "axes.spines.zorder": 100,
    "axes.ticks.length": 2,
    "axes.ticks.label.size": 11,
    # plot area configuration
    "plot.area.alpha": 0.3,
    "plot.area.color": None,
    "plot.area.linewidth": 0,
    "plot.area.zorder": 3,
    # plot grid configuration
    "plot.grid.alpha": 1,
    "plot.grid.color": "#E6E6E6",
    "plot.grid.line.width": 0.5,
    "plot.grid.line.style": LineStyle.SOLID,
    "plot.grid.zorder": 0,
    # plot line configuration
    "plot.line.color": None,
    "plot.line.style": LineStyle.SOLID,
    "plot.line.marker": None,
    "plot.line.width": 1,
    "plot.line.alpha": 1.0,
    "plot.line.drawstyle": LineDrawStyle.DEFAULT,
    "plot.line.zorder": 3,
    # plot bar configuration
    "plot.bar.color": None,
    "plot.bar.alpha": 1.0,
    "plot.bar.width": 0.8,
    "plot.bar.zorder": 3,
    "plot.bar.hatch": None,
    "plot.bar.edge.width": 0.5,
    "plot.bar.edge.color": "#000000",
    "plot.bar.error.color": "#000000",
    # plot hist configuration
    "plot.hist.color": None,
    "plot.hist.alpha": 1.0,
    "plot.hist.zorder": 3,
    "plot.hist.type": "bar",
    "plot.hist.align": "mid",
    "plot.hist.edge.width": 0.5,
    "plot.hist.edge.color": "#000000",
    # TODO: plot heatmap configuration
}
