"""Point labels sit beside their markers and steer clear of the other marks."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from matplotlib.text import Annotation

from datachart.charts import ScatterChart
from datachart.config import config
from datachart.utils import Grid, Panel

POINTS = [
    {"x": 1, "y": 1, "label": "a"},
    {"x": 5, "y": 5, "label": "b"},
    {"x": 9, "y": 2, "label": "c"},
]


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")
    config.reset_config()


def _labels(ax):
    return [
        artist
        for artist in ax.texts
        if isinstance(artist, Annotation) and artist.get_text() != ""
    ]


def _overlap(a, b):
    return max(0.0, min(a.x1, b.x1) - max(a.x0, b.x0)) * max(
        0.0, min(a.y1, b.y1) - max(a.y0, b.y0)
    )


def test_labels_drawn_from_default_key():
    fig = ScatterChart(data=POINTS)
    labels = _labels(fig.axes[0])
    assert [t.get_text() for t in labels] == ["a", "b", "c"]


def test_label_parameter_names_the_key():
    data = [{"x": p["x"], "y": p["y"], "name": p["label"]} for p in POINTS]
    fig = ScatterChart(data=data, label="name")
    assert [t.get_text() for t in _labels(fig.axes[0])] == ["a", "b", "c"]


def test_no_labels_without_the_key():
    fig = ScatterChart(data=[{"x": 1, "y": 1}, {"x": 2, "y": 2}])
    assert _labels(fig.axes[0]) == []


def test_missing_label_skips_the_point():
    data = [{"x": 1, "y": 1, "label": "a"}, {"x": 2, "y": 2}]
    fig = ScatterChart(data=data)
    assert [t.get_text() for t in _labels(fig.axes[0])] == ["a"]


def test_per_chart_none_leaves_the_series_unlabelled():
    fig = ScatterChart(data=[POINTS, POINTS], label=[None, "label"])
    assert [t.get_text() for t in _labels(fig.axes[0])] == ["a", "b", "c"]


def test_labels_take_the_text_font():
    fig = ScatterChart(data=POINTS)
    label = _labels(fig.axes[0])[0]
    assert label.get_fontsize() == config["plot_text_size"]
    assert label.get_color() == config["font_general_color"]


def test_background_labels_are_muted():
    fig = ScatterChart(data=[POINTS, POINTS], emphasis=["background", None])
    colors = {t.get_color() for t in _labels(fig.axes[0])}
    assert config["muted_color"] in colors
    assert config["font_general_color"] in colors


def test_labels_clear_markers_and_each_other():
    # neighbours whose obvious right-hand spots collide with the next point
    data = [
        {"x": 1.0, "y": 1.0, "label": "left point"},
        {"x": 1.15, "y": 1.0, "label": "right point"},
        {"x": 1.3, "y": 1.02, "label": "far point"},
    ]
    fig = ScatterChart(data=data, figsize=(6, 4))
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax = fig.axes[0]
    boxes = [t.get_window_extent(renderer) for t in _labels(ax)]
    centers = ax.transData.transform(ax.collections[0].get_offsets())
    for i, box in enumerate(boxes):
        for other in boxes[i + 1 :]:
            assert _overlap(box, other) == 0.0
        for px, py in centers:
            assert not box.contains(px, py)


def test_hue_groups_keep_their_labels():
    data = [{**p, "hue": "g" + str(i % 2)} for i, p in enumerate(POINTS)]
    fig = ScatterChart(data=data, hue="hue")
    assert sorted(t.get_text() for t in _labels(fig.axes[0])) == ["a", "b", "c"]


def test_labels_survive_panel_and_grid():
    other = [{"x": 2, "y": 6, "label": "d"}]
    panel = Panel([ScatterChart(data=POINTS), ScatterChart(data=other)])
    assert sorted(t.get_text() for t in _labels(panel.axes[0])) == [
        "a",
        "b",
        "c",
        "d",
    ]
    grid = Grid([[ScatterChart(data=POINTS), ScatterChart(data=other)]])
    assert [t.get_text() for t in _labels(grid.axes[0])] == ["a", "b", "c"]
    assert [t.get_text() for t in _labels(grid.axes[1])] == ["d"]


def test_panel_labels_clear_the_other_figure_markers():
    # each figure's right-hand spot lands on the other figure's marker
    left = [{"x": 1.0, "y": 1.0, "label": "left point"}]
    right = [{"x": 1.15, "y": 1.0, "label": "right point"}]
    fig = Panel([ScatterChart(data=left), ScatterChart(data=right)], figsize=(6, 4))
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax = fig.axes[0]
    boxes = [t.get_window_extent(renderer) for t in _labels(ax)]
    centers = [ax.transData.transform(c.get_offsets())[0] for c in ax.collections]
    assert len(boxes) == 2 and len(centers) == 2
    assert _overlap(*boxes) == 0.0
    for box in boxes:
        for px, py in centers:
            assert not box.contains(px, py)


def test_log_scale_places_labels():
    data = [{"x": 10**i, "y": 10**i, "label": str(i)} for i in range(1, 4)]
    fig = ScatterChart(data=data, scalex="log", scaley="log")
    assert len(_labels(fig.axes[0])) == 3
