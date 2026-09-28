import matplotlib
matplotlib.use("Agg")
from datachart.charts import BarChart, LineChart
from datachart.utils import Panel

for val in [100, 150, 170, 178, 195, 200]:
    bars = BarChart(data=[{"label": str(i), "y": val + 5*(i%2)} for i in range(12)], subtitle="A")
    line = LineChart(data=[{"x": i, "y": 30 - abs(i-6)*4} for i in range(12)], subtitle="B")
    fig = Panel([{"figure": bars, "y_axis":"left"}, {"figure": line, "y_axis":"right"}], show_legend=True)
    host, twin = fig.axes
    before = (host.get_ylim()[1], twin.get_ylim()[1])
    fig.canvas.draw()
    legend = twin.get_legend()
    renderer = fig.canvas.get_renderer()
    box = legend.get_window_extent(renderer)
    loc = legend._loc
    grew = host.get_ylim()[1] > before[0] and twin.get_ylim()[1] > before[1]
    overlap = any(box.overlaps(a.get_window_extent(renderer)) for ax in (host,twin) for a in ax.patches+ax.lines)
    print(val, "loc!=0:", loc!=0, "grew:", grew, "overlap:", overlap)
