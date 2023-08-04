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
    "font.general.size": 12,
    "font.general.style": FontStyle.NORMAL,
    "font.general.weight": FontWeight.NORMAL,
    # title size configuration
    "font.title.size": 16,
    "font.title.color": "#000000",
    "font.title.style": FontStyle.NORMAL,
    "font.title.weight": FontWeight.NORMAL,
    # subtitle size configuration
    "font.subtitle.size": 14,
    "font.subtitle.color": "#000000",
    "font.subtitle.style": FontStyle.NORMAL,
    "font.subtitle.weight": FontWeight.NORMAL,
    # xlabel size configuration
    "font.xlabel.size": 12,
    "font.xlabel.color": "#000000",
    "font.xlabel.style": FontStyle.NORMAL,
    "font.xlabel.weight": FontWeight.NORMAL,
    # ylabel size configuration
    "font.ylabel.size": 12,
    "font.ylabel.color": "#000000",
    "font.ylabel.style": FontStyle.NORMAL,
    "font.ylabel.weight": FontWeight.NORMAL,
    # axes configuration
    "axes.spines.top.visible": True,
    "axes.spines.right.visible": True,
    "axes.spines.bottom.visible": True,
    "axes.spines.left.visible": True,
    "axes.spines.width": 0.5,
    "axes.ticks.length": 2,
    "axes.ticks.label.size": 10,
    # plot line configuration
    "plot.line.color": "#000000",
    "plot.line.style": LineStyle.SOLID,
    "plot.line.marker": None,
    "plot.line.width": 1,
    "plot.line.alpha": 1.0,
    "plot.line.drawstyle": LineDrawStyle.DEFAULT,
    # plot area configuration
    "plot.area.alpha": 0.3,
    "plot.area.color": "#E6E6E6",
    "plot.area.linewidth": 0,
    # plot grid configuration
    "plot.grid.alpha": 1,
    "plot.grid.color": "#E6E6E6",
    "plot.grid.line.width": 0.5,
    "plot.grid.line.style": LineStyle.SOLID,
    # TODO: plot bar configuration
    # TODO: plot heatmap configuration
}
