"""Bar family layers: bar, gantt, histogram, and KDE."""

from collections import defaultdict
from datetime import date
from typing import Callable, List, Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.container import BarContainer
from matplotlib.colors import to_hex, to_rgb
from matplotlib.patches import FancyArrowPatch, Patch
from matplotlib.transforms import Bbox, ScaledTranslation
from ..colors import create_color_cycle
from ..validate import (
    AXIS_TEMPORAL,
    validate_gantt_arrow_entry,
    validate_gantt_sort_by,
    validate_sort_by,
)
from ..config_helpers import (
    get_bar_style,
    get_gantt_style,
    get_hist_style,
    get_kde_style,
    get_vline_style,
)
from ...stats import kde1d
from ....constants import (
    COLORBAR_LOCATION,
    FONT_WEIGHT,
    GANTT_ARROW_ENTRY,
    GANTT_SORT_KEY,
    GANTT_VALUE,
    HISTOGRAM_TYPE,
    ORIENTATION,
    AXIS_SCALE,
    SORT,
    VALUE_FORMAT,
)
from ....config import config
from .base import (
    COLORBAR_FRACTION,
    DEFAULT_NUM_BINS,
    DEFAULT_ORIENTATION,
    EMPHASIS_BACKGROUND,
    HistSlot,
    Layer,
    NO_LEGEND,
    TEXT_ANNOTATION_ZORDER,
    _annotate_value,
    _apply_cycle_hatch,
    _bar_records,
    _category_positions,
    _fill_role,
    _format_value,
    _is_bar_record,
    _point_resolver,
    _present_range,
    _record_emphasis,
    _scalar,
    _span_text,
    _vertex_coordinate,
    get_chart_data,
    get_chart_observations,
    resolve_value_kind,
)
from .ticks import _auto_format, _column_tz, date_labels, to_date_numbers


def _axis_formatter(ax: plt.Axes, which: str) -> Callable:
    """The formatter the axis uses for its own coordinates."""

    return getattr(ax, f"format_{which}data")


class BarLayer(Layer):
    kind = "bar"
    color_style = "bar_style"
    labels_past_mark = True

    def _resolve_style(self):
        orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = orientation == ORIENTATION.HORIZONTAL
        self.is_pyramid = bool(self.settings.get("pyramid"))
        self.bar_style = get_bar_style(self.style, self.is_horizontal)
        self.show_yerr = self.settings.get("show_yerr")
        self.record_roles = _record_emphasis(self.chart)
        self._resolve_value_labels()

    def labels(self) -> Optional[np.ndarray]:
        return get_chart_data("label", self.chart)

    def y_values(self) -> Optional[np.ndarray]:
        return get_chart_data("y", self.chart)

    def value_data(self):
        return self.y_values()

    def y_range(self):
        return _present_range(self.y_values())

    @property
    def bar_width(self) -> float:
        """The layer's resolved `plot_bar_width`, as a fraction of the category width."""
        key = "height" if self.is_horizontal else "width"
        return self.bar_style.get(key, config["plot_bar_width"])

    def draw(self, ax, ctx):
        y = self.y_values()
        labels = self.labels()
        if y is None or labels is None:
            return

        yerr = get_chart_data("yerr", self.chart) if self.show_yerr else None
        # each bar sits at its label's place on the panel's category axis
        x = _category_positions(labels, ctx.category_index)

        bar_style = self._merge_color("color", ctx.color, self.bar_style)
        if ctx.z_order is not None:
            bar_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            bar_style["alpha"] = ctx.alpha
        _apply_cycle_hatch(bar_style, ctx)
        self._apply_emphasis(bar_style, ctx.emphasis)

        slot = ctx.bar_slot
        x_offset = 0.0
        if slot is not None:
            bar_style["height" if self.is_horizontal else "width"] = slot.width
            x_offset = slot.offset
            if slot.bottom is not None:
                bar_style["left" if self.is_horizontal else "bottom"] = slot.bottom
            if not slot.show_yerr:
                yerr = None

        error_range = {("xerr" if self.is_horizontal else "yerr"): yerr}

        draw_func = ax.barh if self.is_horizontal else ax.bar
        bars = draw_func(
            x + x_offset,
            y,
            label=self.label(ctx),
            **error_range,
            **bar_style,
        )
        self._etch(bars.patches)
        roles = self._record_roles(ctx.emphasis, len(bars))
        self._apply_patch_emphasis(bars.patches, roles)
        self._name_legend_patch(bars, roles)
        # each bar reports its category position (the axis names it) and its
        # own value, never the stack total; a pyramid side draws negative
        # values, so they read as passed, like the labels
        self.register_hover(
            bars,
            _point_resolver(
                self.label(ctx),
                x,
                np.abs(y) if self.is_pyramid else y,
                self.is_horizontal,
            ),
        )

        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            # pyramid sides draw as signed data but display positive
            # magnitudes (ADR 0017); a muted bar prints no value
            magnitude = abs if self.is_pyramid else (lambda v: v)
            self._label_bars(
                ax,
                bars,
                labels=[
                    (
                        ""
                        if role == EMPHASIS_BACKGROUND
                        else _format_value(self.value_format, magnitude(v))
                    )
                    for v, role in zip(y, roles)
                ],
                stacked=slot is not None and slot.bottom is not None,
            )


# the gantt value labels print whole days and whole percents by default
GANTT_DURATION_FORMAT = "{x:.0f}d"


GANTT_PROGRESS_FORMAT = VALUE_FORMAT.PERCENT_INT


# the dependency arrow head, in points, and the elbow it bends through
GANTT_ARROW_SCALE = 8


GANTT_ARROW_CONNECTION = "angle,angleA=0,angleB=90,rad=0"


GANTT_ARROW_FROM_LEFT = "angle,angleA=90,angleB=0,rad=0"


# a milestone prints its date as the day and month unless a format is set
GANTT_MILESTONE_FORMAT = "%d %b"


GANTT_MILESTONE_Z_OFFSET = 0.2


# the today label sits this many points off the foot of its line
GANTT_TODAY_LABEL_OFFSET = 3


# the progress bar darkens the task color by this much toward black
GANTT_PROGRESS_DARKEN = 0.35


# the progress bar sits just above its task bar
GANTT_PROGRESS_Z_OFFSET = 0.1


def _darken(color, amount: float) -> str:
    """The color moved `amount` (0–1) of the way to black."""

    return to_hex(tuple(c * (1 - amount) for c in to_rgb(color)))


def gantt_tasks(chart: dict) -> list:
    """The chart's task records, in drawing order."""

    data = chart.get("data")
    if not isinstance(data, list):
        return []
    return [record for record in data if isinstance(record, dict)]


def gantt_durations(tasks: list) -> np.ndarray:
    """Each task's duration in days, from its temporal `start` and `end`."""

    if not tasks:
        return np.array([], dtype=float)
    starts = to_date_numbers([task["start"] for task in tasks])
    ends = to_date_numbers([task["end"] for task in tasks])
    return ends - starts


def _gantt_cluster(tasks: list, index: int):
    """The row cluster of a task: its group, or the task alone without one."""

    group = tasks[index].get("group")
    return ("task", index) if group is None else group


def sort_gantt_charts(charts: List[dict], settings: dict) -> List[dict]:
    """The charts with their task rows in `sort` order by `sort_by` (ADR 0049).

    By start, every row orders by its start; by group, rows cluster by group,
    groups ordered by their earliest start and tasks within a group by start.
    A task without a group forms its own cluster. Ties keep input order.
    """

    sort = settings.get("sort")
    sort_by = validate_gantt_sort_by(sort, settings.get("sort_by"))
    if sort is None:
        return charts

    sign = -1 if sort == SORT.DESCENDING else 1
    sorted_charts = []
    for chart in charts:
        tasks = gantt_tasks(chart)
        if not tasks:
            sorted_charts.append(chart)
            continue
        starts = to_date_numbers([task["start"] for task in tasks])
        if sort_by == GANTT_SORT_KEY.GROUP:
            earliest = {}
            for index in range(len(tasks)):
                key = _gantt_cluster(tasks, index)
                earliest[key] = min(earliest.get(key, starts[index]), starts[index])
            order = sorted(
                range(len(tasks)),
                key=lambda i: (
                    sign * earliest[_gantt_cluster(tasks, i)],
                    sign * starts[i],
                ),
            )
            # a group's rows stay contiguous even when two groups start together
            clusters = {}
            for i in order:
                clusters.setdefault(_gantt_cluster(tasks, i), []).append(i)
            order = [i for cluster in clusters.values() for i in cluster]
        else:
            order = sorted(range(len(tasks)), key=lambda i: sign * starts[i])
        sorted_charts.append(
            {
                **chart,
                "data": [tasks[i] for i in order],
                # colors follow the input order, so a sort never recolors
                "group_order": gantt_groups(tasks),
            }
        )
    return sorted_charts


def gantt_groups(tasks: list) -> list:
    """The task groups in first-seen order; ungrouped tasks name none."""

    groups = []
    for task in tasks:
        if task.get("group") is not None and task["group"] not in groups:
            groups.append(task["group"])
    return groups


class GanttLayer(BarLayer):
    """One range bar per task over a temporal value axis (ADR 0049).

    Draws on the bar layer's geometry: `barh` with each bar's left edge at
    the task start and its width the duration, through the panel's slotting.
    """

    # tasks colour by group from their own cycle, so a bar colour is no series colour
    color_style = None

    kind = "gantt"

    def _resolve_style(self):
        self.is_horizontal = True
        self.is_pyramid = False
        self.show_yerr = False
        self.gantt_style = get_gantt_style(self.style)
        bar_keys = ("color", "alpha", "hatch", "linewidth", "edgecolor", "zorder")
        self.bar_style = {k: v for k, v in self.gantt_style.items() if k in bar_keys}
        self.arrow_entry = validate_gantt_arrow_entry(
            self.gantt_style.get("dependency_entry")
        )
        self.show_headers = bool(self.settings.get("show_group_headers"))
        tasks = gantt_tasks(self.chart)
        if self.show_headers:
            # a header stands over its whole group, so the group's rows cluster
            clusters = {}
            for index in range(len(tasks)):
                clusters.setdefault(_gantt_cluster(tasks, index), []).append(index)
            tasks = [tasks[i] for cluster in clusters.values() for i in cluster]
        self.tasks = tasks
        times = [t["start"] for t in tasks] + [t["end"] for t in tasks]
        self.x_tz = _column_tz(times)
        self.starts = (
            to_date_numbers([t["start"] for t in tasks])
            if tasks
            else np.array([], dtype=float)
        )
        self.durations = gantt_durations(tasks)
        self.milestones = self.durations == 0
        # the front validated the task records, their roles included
        self.record_roles = [t.get("emphasis") for t in tasks]
        # the front validated the kind and filled its default
        self.value_mode = resolve_value_kind(self.settings)
        self._resolve_value_labels()
        self.show_values = self.value_mode is not None
        if self.settings.get("value_format") is None:
            self.value_format = (
                GANTT_PROGRESS_FORMAT
                if self.value_mode == GANTT_VALUE.PROGRESS
                else GANTT_DURATION_FORMAT
            )
        self.milestone_format = self.settings.get("xticks_format")
        if _auto_format(self.milestone_format):
            self.milestone_format = GANTT_MILESTONE_FORMAT
        self.show_dependencies = bool(self.settings.get("show_dependencies"))
        # the bars of the last draw stand for their groups in the legend
        self._task_patches = []

        # the legend lists the groups in row order; one color and hatch per
        # group in input order, so sorting the rows never recolors a group
        self.groups = gantt_groups(tasks)
        groups = self.chart.get("group_order") or self.groups
        cycle = (
            create_color_cycle(config["color_general_multiple"], len(groups), "groups")
            if groups
            else None
        )
        hatches = config.get("plot_hatch_cycle") or []
        self.group_colors = {g: cycle[i]["color"] for i, g in enumerate(groups)}
        self.group_hatches = {
            g: hatches[i % len(hatches)] or None
            for i, g in enumerate(groups)
            if hatches
        }
        self._layout_rows()

        self.today = None
        self.today_label = None
        if self.settings.get("show_today"):
            today = self.settings.get("today") or date.today()
            self.today = float(to_date_numbers([today])[0])
            self.today_label = self.settings.get("today_label")
            line_style = get_vline_style(
                {
                    "plot_vline_color": self.gantt_style.get("today_color"),
                    "plot_vline_style": self.gantt_style.get("today_style"),
                    "plot_vline_width": self.gantt_style.get("today_width"),
                    "plot_vline_alpha": self.gantt_style.get("today_alpha"),
                }
            )
            self.vlines = [({"x": today}, line_style)] + self.vlines

    def _layout_rows(self) -> None:
        """Place the task rows, and under headers each group's header row.

        A header row sits over its group's tasks and a gap of
        `plot_gantt_group_gap` rows opens before every header but the first.
        """

        self.rows = np.arange(len(self.tasks), dtype=float)
        self.header_rows = []
        self.tick_rows = list(self.rows)
        self.tick_labels = [t["task"] for t in self.tasks]
        if not self.show_headers:
            return
        gap = self.gantt_style.get("group_gap", 0.0)
        position = 0.0
        ticks, labels, current = [], [], object()
        for index, task in enumerate(self.tasks):
            group = task.get("group")
            if group is not None and group != current:
                if index > 0:
                    position += gap
                self.header_rows.append((group, position))
                ticks.append(position)
                labels.append(str(group))
                position += 1
            current = group
            self.rows[index] = position
            ticks.append(position)
            labels.append(task["task"])
            position += 1
        self.tick_rows, self.tick_labels = ticks, labels

    def apply_row_ticks(self, ax, rotation: float) -> None:
        """Label the task rows; group header labels print bold."""

        ax.set_yticks(self.tick_rows, self.tick_labels)
        ax.yaxis.set_major_locator(mticker.FixedLocator(self.tick_rows))
        ax.set_yticklabels(self.tick_labels, rotation=rotation)
        headers = {position for _, position in self.header_rows}
        for position, label in zip(self.tick_rows, ax.get_yticklabels()):
            if position in headers:
                label.set_fontweight(FONT_WEIGHT.BOLD)

    def labels(self) -> Optional[np.ndarray]:
        if not self.tasks:
            return None
        return np.array([t["task"] for t in self.tasks], dtype=object)

    def y_values(self) -> Optional[np.ndarray]:
        return self.durations if self.tasks else None

    def value_data(self):
        # time is never on a log scale; durations are derived
        return None

    def value_kind(self) -> Optional[str]:
        return AXIS_TEMPORAL if self.tasks else None

    def y_range(self):
        if not self.tasks:
            return None
        return (
            float(np.min(self.starts)),
            float(np.max(self.starts + self.durations)),
        )

    @property
    def bar_width(self) -> float:
        return self.gantt_style.get("height", config["plot_gantt_bar_height"])

    def task_color(self, task: dict, ctx_color: Optional[str]) -> Optional[str]:
        """The task's fill: an explicit bar color, its group's, or the layer's."""

        if "color" in self.bar_style:
            return self.bar_style["color"]
        return self.group_colors.get(task.get("group"), ctx_color)

    def legend_handles(self):
        """One key per task group; a group whose every task is muted stays out."""

        if not self.groups:
            return None
        handles = []
        for group in self.groups:
            members = [
                (role, patch, milestone)
                for task, role, patch, milestone in zip(
                    self.tasks, self.record_roles, self._task_patches, self.milestones
                )
                if task.get("group") == group
            ]
            if all(role == EMPHASIS_BACKGROUND for role, _, _ in members):
                continue
            # the group's first unmuted bar, so the key shows its hatch and etch
            patch = next(
                (
                    patch
                    for role, patch, milestone in members
                    if role != EMPHASIS_BACKGROUND and not milestone
                ),
                None,
            )
            handle = Patch(facecolor=self.task_color({"group": group}, None))
            if patch is not None:
                handle.update_from(patch)
            handle.set_label(str(group))
            handles.append(handle)
        return handles

    def draw(self, ax, ctx):
        if not self.tasks:
            return

        bar_style = dict(self.bar_style)
        bar_style.pop("color", None)
        if ctx.z_order is not None:
            bar_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            bar_style["alpha"] = ctx.alpha
        if not self.groups:
            _apply_cycle_hatch(bar_style, ctx)
        colors = [self.task_color(task, ctx.color) for task in self.tasks]
        self._apply_emphasis(bar_style, ctx.emphasis)
        if "color" in bar_style:
            colors = [bar_style.pop("color")] * len(self.tasks)

        rows = self.rows
        slot = ctx.bar_slot
        height = self.bar_width
        if slot is not None:
            rows = rows + slot.offset
            height = slot.width if slot.width is not None else height

        bars = ax.barh(
            rows,
            self.durations,
            left=self.starts,
            height=height,
            color=colors,
            label=NO_LEGEND if self.groups else self.label(ctx),
            **bar_style,
        )
        for patch, task, milestone in zip(bars.patches, self.tasks, self.milestones):
            hatch = self.group_hatches.get(task.get("group"))
            if hatch and "hatch" not in bar_style:
                patch.set_hatch(hatch)
            # a milestone is a marker, not a bar; a bar's start pins the axis
            # to it, which would cut a marker at the schedule's end in half
            patch.set_visible(not milestone)
            if milestone:
                patch.sticky_edges.x.clear()
        roles = self._record_roles(ctx.emphasis, len(bars))
        self._task_patches = bars.patches
        self._draw_progress(ax, rows, height, colors, bar_style, roles)
        self._draw_summaries(ax, bar_style, ctx)
        self._draw_milestones(ax, rows, colors, bar_style, roles)
        self._etch(bars.patches)
        self._apply_patch_emphasis(bars.patches, roles)
        self._name_legend_patch(bars, roles)
        self.register_hover(bars, self._task_resolver(self.label(ctx)))

        # date ticks come from the locator, so the rotation applies to the axis
        rotation = self.chart.get("xtickrotate")
        if rotation:
            ax.xaxis.set_tick_params(labelrotation=rotation)

        if self.show_dependencies:
            self._draw_dependencies(ax, rows, height, ctx)
        if self.today_label:
            self._draw_today_label(ax)

        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            self._label_bars(
                ax,
                bars,
                labels=[
                    (
                        ""
                        if role == EMPHASIS_BACKGROUND or milestone
                        else self._value_text(i)
                    )
                    for i, (role, milestone) in enumerate(zip(roles, self.milestones))
                ],
                stacked=False,
            )

    def _draw_progress(self, ax, rows, height, colors, bar_style, roles):
        """The inner bars over each task's done fraction."""

        indices = [
            i
            for i, t in enumerate(self.tasks)
            if t.get("progress") is not None and not self.milestones[i]
        ]
        if not indices:
            return
        style = self.gantt_style
        fraction = np.array([self.tasks[i]["progress"] for i in indices], dtype=float)
        progress_color = style.get("progress_color")
        bars = ax.barh(
            rows[indices],
            self.durations[indices] * fraction,
            left=self.starts[indices],
            height=height
            * style.get("progress_height", config["plot_gantt_progress_height"]),
            color=[
                progress_color or _darken(colors[i], GANTT_PROGRESS_DARKEN)
                for i in indices
            ],
            alpha=style.get("progress_alpha"),
            linewidth=0,
            zorder=bar_style.get("zorder", 0) + GANTT_PROGRESS_Z_OFFSET,
            label=NO_LEGEND,
        )
        # the bar's edge is stroked half inside its outline: the progress
        # starts and ends half a stroke in, flush with the visible border
        for patch, i in zip(bars.patches, indices):
            task = self._task_patches[i]
            inset = task.get_linewidth() / 2 / 72
            shift = lambda dx: ScaledTranslation(dx, 0, ax.figure.dpi_scale_trans)
            patch.set_transform(ax.transData + shift(inset))
            patch.set_clip_path(task.get_path(), task.get_transform() + shift(-inset))
        self._etch(bars.patches)
        self._apply_patch_emphasis(bars.patches, [roles[i] for i in indices])

    def _draw_summaries(self, ax, bar_style, ctx) -> None:
        """A bar over each group header, from the group's first start to its last end."""

        style = self.gantt_style
        for group, position in self.header_rows:
            members = [i for i, t in enumerate(self.tasks) if t.get("group") == group]
            start = float(np.min(self.starts[members]))
            end = float(np.max(self.starts[members] + self.durations[members]))
            muted = ctx.emphasis == EMPHASIS_BACKGROUND or all(
                self.record_roles[i] == EMPHASIS_BACKGROUND for i in members
            )
            color = style.get("summary_color") or self.task_color(
                {"group": group}, None
            )
            ax.barh(
                position,
                end - start,
                left=start,
                height=style.get("summary_height"),
                color=self.muted_color if muted else color,
                alpha=self.muted_alpha if muted else None,
                linewidth=0,
                zorder=bar_style.get("zorder", 0),
                label=NO_LEGEND,
            )

    def _draw_milestones(self, ax, rows, colors, bar_style, roles) -> None:
        """A marker at each milestone; under value labels, its date beside it."""

        style = self.gantt_style
        size = style.get("milestone_size")
        for i in np.flatnonzero(self.milestones):
            muted = roles[i] == EMPHASIS_BACKGROUND
            anchor = (self.starts[i], rows[i])
            (marker,) = ax.plot(
                [self.starts[i]],
                [rows[i]],
                linestyle="none",
                marker=style.get("milestone_marker"),
                markersize=size,
                color=self.muted_color if muted else colors[i],
                markeredgecolor=bar_style.get("edgecolor"),
                markeredgewidth=bar_style.get("linewidth"),
                alpha=self.muted_alpha if muted else None,
                zorder=bar_style.get("zorder", 0) + GANTT_MILESTONE_Z_OFFSET,
                label=NO_LEGEND,
                # a milestone on the view's edge shows whole, over the spine
                clip_on=False,
            )
            self.register_limit_mark(marker, *anchor)
            if self.show_values and not muted:
                label = ax.annotate(
                    date_labels([self.tasks[i]["start"]], self.milestone_format)[0],
                    anchor,
                    xytext=(size / 2 + self.value_padding, 0),
                    textcoords="offset points",
                    ha="left",
                    va="center",
                    zorder=TEXT_ANNOTATION_ZORDER,
                    **self.value_font,
                )
                self.register_limit_mark(label, *anchor)

    def _draw_dependencies(self, ax, rows, height, ctx) -> None:
        """An elbow arrow from each dependency's end to the dependent's start.

        Entering from the top, the arrow runs along the dependency's row and
        turns onto the dependent bar; from the left, it drops from the
        dependency's end and turns into the dependent bar's start.
        """

        style = self.gantt_style
        color = style.get("dependency_color")
        if ctx.emphasis == EMPHASIS_BACKGROUND:
            color = self.muted_color
        # a milestone's marker, not its row centre, is where an arrow stops
        clearance = style.get("milestone_size", 0) / 2
        position = {task["task"]: i for i, task in enumerate(self.tasks)}
        for j, task in enumerate(self.tasks):
            for name in task.get("depends_on") or []:
                i = position[name]
                # with no room before the dependent's start, it enters from the top
                from_left = (
                    self.arrow_entry == GANTT_ARROW_ENTRY.LEFT
                    and self.starts[j] > self.starts[i] + self.durations[i]
                )
                # the facing edge of a bar, toward the other task's row
                toward = height / 2 if rows[j] > rows[i] else -height / 2
                start_edge = 0.0 if self.milestones[i] or not from_left else toward
                end_edge = 0.0 if self.milestones[j] or from_left else -toward
                ax.add_patch(
                    FancyArrowPatch(
                        (self.starts[i] + self.durations[i], rows[i] + start_edge),
                        (self.starts[j], rows[j] + end_edge),
                        arrowstyle=style.get("dependency_style"),
                        connectionstyle=(
                            GANTT_ARROW_FROM_LEFT
                            if from_left
                            else GANTT_ARROW_CONNECTION
                        ),
                        mutation_scale=GANTT_ARROW_SCALE,
                        color=color,
                        linewidth=style.get("dependency_width"),
                        shrinkA=clearance if self.milestones[i] else 0,
                        shrinkB=clearance if self.milestones[j] else 0,
                        zorder=style.get("dependency_zorder"),
                    )
                )

    def _draw_today_label(self, ax) -> None:
        """The today line's label, at the foot of the line."""

        ax.annotate(
            self.today_label,
            (self.today, 0),
            xycoords=ax.get_xaxis_transform(),
            xytext=(GANTT_TODAY_LABEL_OFFSET, GANTT_TODAY_LABEL_OFFSET),
            textcoords="offset points",
            ha="left",
            va="bottom",
            zorder=TEXT_ANNOTATION_ZORDER,
            **{**self.value_font, "color": self.gantt_style.get("today_color")},
        )

    def _value_text(self, index: int) -> str:
        """The bar's value label: its duration in days or its progress."""

        if self.value_mode == GANTT_VALUE.PROGRESS:
            progress = self.tasks[index].get("progress")
            return (
                "" if progress is None else _format_value(self.value_format, progress)
            )
        return _format_value(self.value_format, float(self.durations[index]))

    def _task_resolver(self, label) -> Callable[[int], dict]:
        """The hover datum of a task bar: its name, span, duration and progress."""

        def resolve(index: int) -> dict:
            task = self.tasks[index]
            datum = {
                "label": label,
                "task": task["task"],
                "start": task["start"],
                "end": task["end"],
                "duration": f"{self.durations[index]:g} days",
            }
            if task.get("progress") is not None:
                datum["progress"] = f"{task['progress']:.0%}"
            return datum

        return resolve


class HistogramLayer(Layer):
    kind = "histogram"
    color_style = "hist_style"
    labels_past_mark = True

    def _resolve_style(self):
        self.hist_style = get_hist_style(self.style)
        self.orientation = self.settings.get("orientation") or DEFAULT_ORIENTATION
        self.is_horizontal = self.orientation == ORIENTATION.HORIZONTAL
        self.show_density = self.settings.get("show_density")
        self.show_cumulative = self.settings.get("show_cumulative")
        self.num_bins = self.settings.get("num_bins") or DEFAULT_NUM_BINS
        # step's outline is the series mark: it follows the cycle color and
        # the theme line width unless the chart style pins them (ADR 0014)
        self.step_edge_color_auto = "plot_hist_edge_color" not in self.style
        self.step_edge_width_auto = "plot_hist_edge_width" not in self.style
        self.step_edge_width = config["plot_line_width"]
        self._resolve_value_labels()

    def x_values(self) -> Optional[np.ndarray]:
        return get_chart_observations("x", self.chart)

    def y_range(self):
        x = self.x_values()
        if x is None or len(x) == 0:
            return None
        # the view decides the scale: densities and cumulative shares are not counts
        heights, edges = np.histogram(x, bins=self.num_bins, density=self.show_density)
        if self.show_cumulative:
            heights = np.cumsum(
                heights * np.diff(edges) if self.show_density else heights
            )
        return (float(np.min(heights)), float(np.max(heights)))

    def draw(self, ax, ctx):
        x = self.x_values()
        if x is None:
            return

        hist_style = self._merge_color("color", ctx.color, self.hist_style)
        is_step = hist_style.get("histtype") == HISTOGRAM_TYPE.STEP
        if is_step:
            if ctx.hist_slot is not None:
                # a stack needs area: step stacks as its filled equivalent (ADR 0014)
                hist_style["histtype"] = HISTOGRAM_TYPE.STEP_FILLED
            else:
                if self.step_edge_color_auto:
                    # dropping the theme edge lets `color` drive the outline
                    hist_style.pop("edgecolor", None)
                if self.step_edge_width_auto:
                    hist_style["linewidth"] = self.step_edge_width
        if ctx.z_order is not None:
            hist_style["zorder"] = ctx.z_order
        if ctx.alpha is not None:
            hist_style["alpha"] = ctx.alpha
        _apply_cycle_hatch(hist_style, ctx)
        self._apply_emphasis(hist_style, ctx.emphasis)

        if ctx.hist_slot is not None:
            # weighted bin centers reproduce the precomputed stack heights
            # exactly; density/cumulative are already encoded in them
            slot = ctx.hist_slot
            counts, edges, bars = ax.hist(
                (slot.bins[:-1] + slot.bins[1:]) / 2,
                bins=slot.bins,
                weights=slot.heights,
                bottom=slot.bottom,
                label=self.label(ctx),
                orientation=self.orientation,
                **hist_style,
            )
        else:
            bins = ctx.bins if ctx.bins is not None else self.num_bins
            counts, edges, bars = ax.hist(
                x,
                bins=bins,
                label=self.label(ctx),
                density=self.show_density,
                cumulative=self.show_cumulative,
                orientation=self.orientation,
                **hist_style,
            )
            if is_step:
                self._trim_step_outline(bars[0], ctx)
        self._etch(bars.patches if isinstance(bars, BarContainer) else bars)
        self._register_bins(ax, ctx, bars, edges, counts)
        if self.show_values and ctx.emphasis != EMPHASIS_BACKGROUND:
            self._label_bins(ax, bars, edges, counts, ctx.hist_slot is not None)

    def _trim_step_outline(self, outline, ctx) -> None:
        """Cut the outline's drops to zero that no bin reports (ADR 0014).

        `ax.hist(histtype="step")` draws one open polygon from zero, over the
        bins, and back down to zero. A cumulative total never falls back, so
        its closing drop goes (issue #198); on a log value axis, which has no
        zero, every remaining vertex at zero becomes NaN, and the renderer
        breaks the outline there rather than spiking to the axis floor
        (issue #199).
        """

        value_axis = 0 if self.is_horizontal else 1
        vertices = np.array(outline.get_xy(), dtype=float)
        if self.show_cumulative:
            vertices = vertices[:-1]
        if ctx.value_scale == AXIS_SCALE.LOG:
            vertices[vertices[:, value_axis] == 0, value_axis] = np.nan
        outline.set_xy(vertices)

    def _label_bins(self, ax, bars, edges, counts, stacked: bool) -> None:
        """Print each bin's height at its top; an empty bin stays bare."""

        texts = [_format_value(self.value_format, c) if c else "" for c in counts]
        if isinstance(bars, BarContainer):
            self._label_bars(ax, bars, stacked, labels=texts)
            return
        # a step outline has no bars to label: the bin tops are annotated directly
        centres = (edges[:-1] + edges[1:]) / 2
        for centre, height, text in zip(centres, counts, texts):
            if text:
                _annotate_value(
                    ax,
                    centre,
                    height,
                    text,
                    self.is_horizontal,
                    self.value_padding,
                    self.value_font,
                )

    def _register_bins(self, ax, ctx, bars, edges, counts) -> None:
        """Each bin reports its range on the value axis and its own height."""

        label = self.label(ctx)
        value_axis = "y" if self.is_horizontal else "x"

        def datum(i: int) -> dict:
            span = _span_text(edges[i], edges[i + 1], _axis_formatter(ax, value_axis))
            count = _scalar(counts[i])
            # matplotlib bins into floats; a plain count reads as a whole number
            if not self.show_density and float(count).is_integer():
                count = int(count)
            if self.is_horizontal:
                return {"label": label, "x": count, "y": span}
            return {"label": label, "x": span, "y": count}

        if isinstance(bars, BarContainer):
            self.register_hover(bars, datum)
            return
        # a step outline is one polygon; a picked vertex names its bin
        (outline,) = bars
        axis = 1 if self.is_horizontal else 0

        def resolve(index):
            coordinate = _vertex_coordinate(outline.get_xy(), index, axis)
            i = int(np.searchsorted(edges, coordinate, side="right")) - 1
            return datum(min(max(i, 0), len(counts) - 1))

        self.register_hover(outline, resolve)


class KdeLayer(Layer):
    """A density curve of one chart's `x` values, with a soft fill beneath.

    The scatter matrix draws one per hue group on its diagonal (ADR 0051);
    `kde_xlim` pins the evaluation grid to the column's shared limits.
    """

    overlayable = False

    kind = "kde"

    def _resolve_style(self):
        self.kde_style = get_kde_style(self.style)
        self.xlim = self.settings.get("kde_xlim")

    def x_values(self) -> Optional[np.ndarray]:
        return get_chart_observations("x", self.chart)

    def curve(self) -> Optional[tuple]:
        """The (x, density) samples; None when the values have no spread."""

        # the estimate is fixed once built; the range and the draw share it
        if not hasattr(self, "_curve"):
            x = self.x_values()
            self._curve = None
            if x is not None and len(x) > 1 and np.ptp(x) > 0:
                curve = kde1d(x, xlim=self.xlim)
                self._curve = (np.array(curve["x"]), np.array(curve["y"]))
        return self._curve

    def y_range(self):
        curve = self.curve()
        return None if curve is None else (0.0, float(np.max(curve[1])))

    def draw(self, ax, ctx):
        curve = self.curve()
        if curve is None:
            return
        x, y = curve
        color = self.muted_color if ctx.emphasis == EMPHASIS_BACKGROUND else ctx.color
        line_style = {"color": color, "linewidth": self.kde_style["linewidth"]}
        if ctx.z_order is not None:
            line_style["zorder"] = ctx.z_order
        self._stroke_halo(line_style)
        (line,) = ax.plot(x, y, label=self.label(ctx), **line_style)
        if self.kde_style["alpha"]:
            ax.fill_between(
                x,
                0,
                y,
                color=color,
                alpha=self.kde_style["alpha"],
                linewidth=0,
                zorder=line.get_zorder() - 0.1,
            )
        # a density starts at zero: the autoscale margin stops there
        line.sticky_edges.y.append(0)
        self.register_hover(line, _point_resolver(self.label(ctx), x, y, ctx.transpose))


COLORBAR_DIVIDER_PAD = 0.1


class _LockedBarLocator:
    """Places a bar beside the axes' drawn box, in display space.

    Display space stays valid while a tight-bbox save swaps the figure box,
    which an inch-based divider does not (#192).
    """

    def __init__(self, ax: plt.Axes, location: str):
        self._ax, self._location = ax, location

    def __call__(self, cax: plt.Axes, renderer) -> Bbox:
        ax, location = self._ax, self._location
        ax.apply_aspect()
        box = ax.get_position(original=False).transformed(ax.figure.transSubfigure)
        pad = COLORBAR_DIVIDER_PAD * ax.figure.dpi
        # a left or bottom bar crosses the chart's tick labels: pad past them
        if location == COLORBAR_LOCATION.LEFT:
            ticks = ax.yaxis.get_tightbbox(renderer)
            pad += max(box.x0 - ticks.x0, 0.0) if ticks else 0.0
        elif location == COLORBAR_LOCATION.BOTTOM:
            ticks = ax.xaxis.get_tightbbox(renderer)
            pad += max(box.y0 - ticks.y0, 0.0) if ticks else 0.0
        x0, y0, width, height = box.bounds
        if location in (COLORBAR_LOCATION.LEFT, COLORBAR_LOCATION.RIGHT):
            size = width * COLORBAR_FRACTION
            x0 = x0 - pad - size if location == COLORBAR_LOCATION.LEFT else box.x1 + pad
            bar = Bbox.from_bounds(x0, y0, size, height)
        else:
            size = height * COLORBAR_FRACTION
            y0 = (
                y0 - pad - size
                if location == COLORBAR_LOCATION.BOTTOM
                else box.y1 + pad
            )
            bar = Bbox.from_bounds(x0, y0, width, size)
        return bar.transformed(ax.figure.transSubfigure.inverted())


def _bar_record_values(charts: List[dict], magnitude: bool) -> list:
    """`(label, value)` per drawn record of each chart; magnitudes when asked."""

    columns = []
    for chart in charts:
        if not isinstance(chart.get("data"), list):
            raise ValueError(
                "`sort` and `emphasis_rule` read bar records; pass `data` as a "
                "list of `{label, y}` dicts, not columns."
            )
        columns.append(
            [
                (
                    record.get("label"),
                    abs(record["y"]) if magnitude else record["y"],
                )
                for record in _bar_records(chart)
            ]
        )
    return columns


def sort_bar_charts(charts: List[dict], settings: dict) -> List[dict]:
    """The charts with their records in category order (ADR 0042).

    One order serves every chart: categories sort by their total across the
    charts, or by the value in the one chart `sort_by` names by subtitle;
    categories that chart lacks sort last. Ties keep input order. A pyramid's
    negated left side sorts by magnitude.
    """

    sort, sort_by = settings.get("sort"), settings.get("sort_by")
    magnitude = bool(settings.get("pyramid"))
    validate_sort_by(sort, sort_by, [chart.get("subtitle") for chart in charts])
    if sort is None:
        return charts

    columns = _bar_record_values(charts, magnitude)
    keyed = [
        column
        for chart, column in zip(charts, columns)
        if sort_by is None or chart.get("subtitle") == sort_by
    ]
    totals = defaultdict(float)
    for column in keyed:
        for label, value in column:
            totals[label] += value
    categories = []
    for column in columns:
        for label, _ in column:
            if label not in categories:
                categories.append(label)
    sign = -1 if sort == SORT.DESCENDING else 1
    ordered = sorted(
        categories, key=lambda c: (c not in totals, sign * totals.get(c, 0))
    )
    rank = {label: i for i, label in enumerate(ordered)}

    sorted_charts = []
    for chart in charts:
        data = sorted(
            chart["data"],
            key=lambda r: rank.get(
                r.get("label") if isinstance(r, dict) else None, len(rank)
            ),
        )
        # the category index follows the sort past this chart's gaps (ADR 0079)
        sorted_charts.append({**chart, "data": data, "category_order": ordered})
    return sorted_charts


def bar_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per drawn bar record, reading its own `y` (ADR 0042).

    A pyramid's negated left side reads as magnitudes.
    """

    columns = _bar_record_values(charts, bool(settings.get("pyramid")))
    filled, units = [], []
    for chart, column in zip(charts, columns):
        data = [
            {"emphasis": None, **r} if _is_bar_record(r, "y") else r
            for r in chart["data"]
        ]
        records = [r for r in data if _is_bar_record(r, "y")]
        units += [
            (value, _fill_role(record, "emphasis"))
            for record, (_, value) in zip(records, column)
        ]
        filled.append({**chart, "data": data})
    return filled, units


def gantt_units(charts: List[dict], settings: dict, by) -> tuple:
    """One unit per task record, reading its duration in days (ADR 0049)."""

    filled, units = [], []
    for chart in charts:
        data = [
            {"emphasis": None, **r} if isinstance(r, dict) else r for r in chart["data"]
        ]
        tasks = gantt_tasks({"data": data})
        units += [
            (days, _fill_role(task, "emphasis"))
            for task, days in zip(tasks, gantt_durations(tasks))
        ]
        filled.append({**chart, "data": data})
    return filled, units


def _hist_stack_slots(hist_layers: List[HistogramLayer], bins: np.ndarray) -> dict:
    """Per-layer stacked heights and bottoms on shared bin edges.

    Mirrors matplotlib's stacked-hist math: density normalizes the whole
    stack's area to 1, cumulative accumulates after the density transform.
    """

    first = hist_layers[0]
    density = bool(first.show_density)
    cumulative = bool(first.show_cumulative)
    counts = [
        np.histogram(layer.x_values(), bins=bins)[0].astype(float)
        for layer in hist_layers
    ]
    db = np.diff(bins)
    total = sum(c.sum() for c in counts)

    slots, bottom = {}, np.zeros(len(db))
    for layer, heights in zip(hist_layers, counts):
        if density and total > 0:
            heights = heights / db / total
        if cumulative:
            heights = np.cumsum(heights * db) if density else np.cumsum(heights)
        slots[id(layer)] = HistSlot(bins=bins, heights=heights, bottom=bottom)
        bottom = bottom + heights
    return slots
