from ...schema.definitions import ConfigAttrs
from ...schema.constants import (
    LineStyle,
    FontStyle,
    FontWeight,
    LineDrawStyle,
    Colors,
)

DEFAULT_THEME: ConfigAttrs = {
    # general color style
    "color.general.singular": Colors.Blue,
    "color.general.multiple": Colors.Spectral,
    # general font style
    "font.general.family": "sans-serif",
    "font.general.sans-serif": ["Helvetica", "Arial"],
    "font.general.color": "#000000",
    "font.general.size": 11,
    "font.general.style": FontStyle.NORMAL,
    "font.general.weight": FontWeight.NORMAL,
    # title size style
    "font.title.size": 12,
    "font.title.color": "#000000",
    "font.title.style": FontStyle.NORMAL,
    "font.title.weight": FontWeight.NORMAL,
    # subtitle size style
    "font.subtitle.size": 11,
    "font.subtitle.color": "#000000",
    "font.subtitle.style": FontStyle.NORMAL,
    "font.subtitle.weight": FontWeight.NORMAL,
    # xlabel size style
    "font.xlabel.size": 10,
    "font.xlabel.color": "#000000",
    "font.xlabel.style": FontStyle.NORMAL,
    "font.xlabel.weight": FontWeight.NORMAL,
    # ylabel size style
    "font.ylabel.size": 10,
    "font.ylabel.color": "#000000",
    "font.ylabel.style": FontStyle.NORMAL,
    "font.ylabel.weight": FontWeight.NORMAL,
    # plot axes style
    "axes.spines.top.visible": True,
    "axes.spines.right.visible": True,
    "axes.spines.bottom.visible": True,
    "axes.spines.left.visible": True,
    "axes.spines.width": 0.5,
    "axes.spines.zorder": 100,
    "axes.ticks.length": 2,
    "axes.ticks.label.size": 9,
    # plot legend style
    "plot.legend.shadow": False,
    "plot.legend.frameon": True,
    "plot.legend.alignment": "left",
    "plot.legend.font.size": 9,
    "plot.legend.title.size": 10,
    "plot.legend.label.color": "#000000",
    # plot area style
    "plot.area.alpha": 0.3,
    "plot.area.color": None,
    "plot.area.line.width": 0,
    "plot.area.hatch": None,
    "plot.area.zorder": 3,
    # plot grid style
    "plot.grid.alpha": 1,
    "plot.grid.color": "#E6E6E6",
    "plot.grid.line.width": 0.5,
    "plot.grid.line.style": LineStyle.SOLID,
    "plot.grid.zorder": 0,
    # plot line style
    "plot.line.color": None,
    "plot.line.style": LineStyle.SOLID,
    "plot.line.marker": None,
    "plot.line.width": 1,
    "plot.line.alpha": 1.0,
    "plot.line.drawstyle": LineDrawStyle.DEFAULT,
    "plot.line.zorder": 3,
    # plot bar style
    "plot.bar.color": None,
    "plot.bar.alpha": 1.0,
    "plot.bar.width": 0.8,
    "plot.bar.zorder": 3,
    "plot.bar.hatch": None,
    "plot.bar.edge.width": 0.5,
    "plot.bar.edge.color": "#000000",
    "plot.bar.error.color": "#000000",
    # plot hist style
    "plot.hist.color": None,
    "plot.hist.alpha": 1.0,
    "plot.hist.zorder": 3,
    "plot.hist.fill": None,
    "plot.hist.hatch": None,
    "plot.hist.type": "bar",
    "plot.hist.align": "mid",
    "plot.hist.edge.width": 0.5,
    "plot.hist.edge.color": "#000000",
}
