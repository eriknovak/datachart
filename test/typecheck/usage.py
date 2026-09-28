"""What an installed `datachart` looks like to a type checker (ADR 0087).

Never imported by the unit tests: pyright checks it in CI, so the public
figure type and the composition item dicts must stay well-typed for users.
"""

from datachart.charts import BarChart, LineChart
from datachart.typings import (
    BarRecordAttrs,
    GridItemSettingAttrs,
    LayoutSpecSettingAttrs,
    LineRecordAttrs,
    PanelItemSettingAttrs,
)
from datachart.utils import Annotate, DatachartFigure, Grid, Panel, save_figure

bars: list[BarRecordAttrs] = [{"label": "A", "y": 1.0}, {"label": "B", "y": 2.0}]
points: list[LineRecordAttrs] = [{"x": 0, "y": 1.0}, {"x": 1, "y": 2.0}]

bar_figure: DatachartFigure = BarChart(bars)
line_figure: DatachartFigure = LineChart(points, title="Trend")

left: PanelItemSettingAttrs = {"figure": bar_figure, "y_axis": "left"}
right: PanelItemSettingAttrs = {"figure": line_figure, "y_axis": "right"}
panel: DatachartFigure = Panel([left, right], ylabel_left="Count")

spec: LayoutSpecSettingAttrs = {"row": 0, "col": 0, "rowspan": 2, "colspan": 1}
tall: GridItemSettingAttrs = {"figure": bar_figure, "layout_spec": spec}
grid: DatachartFigure = Grid([tall, {"figure": line_figure}])

annotated: DatachartFigure = Annotate(panel, [{"text": "peak", "x": 1, "y": 2.0}])
annotated.show(interactive=True)
paths: list[str] = save_figure(grid, "out", fmt=["png"])
