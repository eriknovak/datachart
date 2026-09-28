"""Tick locators and formatters for date periods and schedules."""

from datetime import datetime, tzinfo
from typing import List, Optional, Tuple
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as mticker
from ..validate import is_number
from ....constants import DATE_FORMAT, GANTT_DATE_PERIOD
from .base import _format_value, _text_size

# an AUTO date label carries the time only when one of the labels has one
DATE_LABEL_WITH_TIME = "%Y-%m-%d %H:%M"


def _as_datetime(value):
    """A value with `strftime`; numpy scalars convert at microsecond precision."""

    if isinstance(value, np.datetime64):
        return value.astype("datetime64[us]").item()
    return value


def _auto_format(fmt) -> bool:
    """Whether a tick format leaves the labels to the axis."""

    return fmt in (None, DATE_FORMAT.AUTO)


def _column_tz(values) -> Optional[tzinfo]:
    """The zone of the first zone-aware value in a temporal column, else None."""

    return next((v.tzinfo for v in values if getattr(v, "tzinfo", None)), None)


def date_labels(values, fmt=None) -> List[str]:
    """Temporal values as tick text; AUTO prints the date, plus the time when any has one."""

    values = [_as_datetime(v) for v in values]
    if _auto_format(fmt):
        has_time = any(
            isinstance(v, datetime) and (v.hour or v.minute or v.second) for v in values
        )
        fmt = DATE_LABEL_WITH_TIME if has_time else DATE_FORMAT.ISO
    return [v.strftime(fmt) for v in values]


def to_date_numbers(values) -> np.ndarray:
    """Temporal values as matplotlib date numbers, for layers that draw floats."""

    return np.asarray(mdates.date2num(list(values)), dtype=float)


def _tick_formatter(fmt, temporal: bool, locator=None, tz=None):
    """The major formatter a tick format resolves to; None keeps the axis default.

    On a temporal axis the format is a `strftime` pattern, AUTO the concise
    formatter over `locator`. Elsewhere any value-label style string (`{x}`,
    `{}`, or `%`) formats each tick, like the heatmap's `value_format`.
    """

    if temporal:
        if _auto_format(fmt):
            if isinstance(locator, ScheduleTicks):
                return ScheduleDateFormatter(locator, tz=tz)
            return mdates.ConciseDateFormatter(locator, tz=tz)
        return mdates.DateFormatter(fmt, tz=tz)
    if _auto_format(fmt):
        return None
    return mticker.FuncFormatter(lambda value, _pos: _format_value(fmt, value))


# a period's labels, and the enclosing period named in the row beneath
DATE_PERIOD_LABELS = {
    GANTT_DATE_PERIOD.DAY: "%d",
    GANTT_DATE_PERIOD.WEEK: "W%V",
    GANTT_DATE_PERIOD.MONTH: "%b",
    GANTT_DATE_PERIOD.QUARTER: None,
    GANTT_DATE_PERIOD.YEAR: "%Y",
    GANTT_DATE_PERIOD.PROJECT_MONTH: None,
}


# the project year, the row beneath project months; never a period of its own
PROJECT_YEAR = "project_year"


DATE_PERIOD_PARENT = {
    GANTT_DATE_PERIOD.DAY: GANTT_DATE_PERIOD.MONTH,
    GANTT_DATE_PERIOD.WEEK: GANTT_DATE_PERIOD.MONTH,
    GANTT_DATE_PERIOD.MONTH: GANTT_DATE_PERIOD.YEAR,
    GANTT_DATE_PERIOD.QUARTER: GANTT_DATE_PERIOD.YEAR,
    GANTT_DATE_PERIOD.YEAR: None,
    GANTT_DATE_PERIOD.PROJECT_MONTH: PROJECT_YEAR,
}


DATE_PARENT_LABELS = {GANTT_DATE_PERIOD.MONTH: "%b %Y", GANTT_DATE_PERIOD.YEAR: "%Y"}


# the longest period of each kind in days, to reach the edges beyond the view
DATE_PERIOD_SPAN = {
    GANTT_DATE_PERIOD.DAY: 1,
    GANTT_DATE_PERIOD.WEEK: 7,
    GANTT_DATE_PERIOD.MONTH: 31,
    GANTT_DATE_PERIOD.QUARTER: 92,
    GANTT_DATE_PERIOD.YEAR: 366,
    GANTT_DATE_PERIOD.PROJECT_MONTH: 31,
    PROJECT_YEAR: 366,
}


# a period cut to under this share of the widest visible one is unlabelled
DATE_PERIOD_MIN_SHARE = 0.2


# the parent row sits this many label heights below the period row
DATE_PARENT_ROW_SPACING = 1.6


def _months_since(origin, moment) -> int:
    """The whole months from the project origin to `moment`; negative before it."""

    months = (moment.year - origin.year) * 12 + moment.month - origin.month
    if (moment.day, moment.hour, moment.minute) < (
        origin.day,
        origin.hour,
        origin.minute,
    ):
        months -= 1
    return months


class ProjectPeriodEdges(mticker.Locator):
    """Edges every `months` months from the project origin, M1 starting there."""

    def __init__(self, origin, months: int):
        self.origin = origin
        self.months = months

    def tick_values(self, vmin, vmax):
        lo, hi = (v if is_number(v) else mdates.date2num(v) for v in (vmin, vmax))
        first = _months_since(self.origin, mdates.num2date(lo, tz=self.origin.tzinfo))
        # no edge before the origin: the time before M1 is no project period
        k = max(first // self.months - 1, 0)
        edges = []
        while True:
            edge = mdates.date2num(self.origin + relativedelta(months=self.months * k))
            if edge > hi:
                return edges
            edges.append(edge)
            k += 1

    def __call__(self):
        return self.tick_values(*sorted(self.axis.get_view_interval()))


# a schedule's date ticks: at most this many regular steps from the first start
SCHEDULE_TICKS_MAX = 8


# sub-day steps in days: 1, 2, 5, 10, 15, 30 minutes; 1, 2, 3, 4, 6, 12 hours
SCHEDULE_TICK_SUBDAY = tuple(m / 1440 for m in (1, 2, 5, 10, 15, 30)) + tuple(
    h / 24 for h in (1, 2, 3, 4, 6, 12)
)


SCHEDULE_TICK_DAYS = (1, 2, 3, 4, 5, 7, 14, 21, 28)


SCHEDULE_TICK_MONTHS = (1, 2, 3, 4, 6, 12, 24, 60)


class ScheduleTicks(mticker.Locator):
    """Date ticks from a schedule's first start to its last end (ADR 0049).

    Minute, hour, and day steps run regularly from the first start; minutes
    and hours only when the schedule carries times. Month steps fall on the
    first of the calendar months the step divides (quarters, years). The
    first start and the last end are always ticks; a regular tick within
    half a step of either gives way, so they never crowd.
    """

    def __init__(self, start: float, end: float, tz=None, timed: bool = False):
        self.start, self.end, self.tz, self.timed = start, end, tz, timed
        # the month step of the last ticks; None when they step in days or less
        self.months = None

    def tick_values(self, vmin, vmax):
        span = self.end - self.start
        if span <= 0:
            return [self.start]
        steps = (SCHEDULE_TICK_SUBDAY if self.timed else ()) + SCHEDULE_TICK_DAYS
        # the finest step that keeps the count, preferring one that divides
        # the span so the last interval is no shorter than the rest
        fitting = [d for d in steps if span / d <= SCHEDULE_TICKS_MAX]
        even = [d for d in fitting if np.isclose(span / d, round(span / d))]
        step = (even or fitting or [None])[0]
        self.months = None
        if step is not None:
            regular = (self.start + k * step for k in range(1, round(span / step)))
        else:
            months = next(
                (
                    m
                    for m in SCHEDULE_TICK_MONTHS
                    if span / (m * 30.4) <= SCHEDULE_TICKS_MAX
                ),
                SCHEDULE_TICK_MONTHS[-1],
            )
            self.months, step = months, months * 30.4
            regular = self._month_starts(months)
        ticks = [self.start]
        for tick in regular:
            if tick >= self.end - step / 2:
                break
            if tick - self.start >= step / 2:
                ticks.append(tick)
        return ticks + [self.end]

    def _month_starts(self, months: int):
        """The 1sts of every `months`-th calendar month from the start's on."""

        start = mdates.num2date(self.start, tz=self.tz)
        # counted from year 0, so 3 months lands on quarters and 12 on Januaries
        index = -(-(start.year * 12 + start.month - 1) // months) * months
        while True:
            year, month = divmod(index, 12)
            yield mdates.date2num(
                start.replace(
                    year=year,
                    month=month + 1,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
            )
            index += months

    def __call__(self):
        return self.tick_values(*sorted(self.axis.get_view_interval()))


class ScheduleDateFormatter(mdates.ConciseDateFormatter):
    """Concise schedule labels where month-step ticks on January 1 read the year.

    The concise formatter labels at the level the first start and last end
    differ in (days), so it would print every January as "Jan"; the offset
    then names one year only when all ticks fall in it.
    """

    def __init__(self, locator: ScheduleTicks, tz=None):
        super().__init__(locator, tz=tz)
        self.schedule = locator
        self.year_offset = None

    def format_ticks(self, values):
        labels = super().format_ticks(values)
        self.year_offset = None
        if self.schedule.months is None or len(values) < 3:
            return labels
        dates = mdates.num2date(values, tz=self._tz)
        for i in range(1, len(dates) - 1):
            if (dates[i].month, dates[i].day) == (1, 1):
                labels[i] = str(dates[i].year)
        years = {d.year for d in dates}
        self.year_offset = "" if len(years) > 1 else str(dates[0].year)
        return labels

    def get_offset(self):
        if self.year_offset is None:
            return super().get_offset()
        return self.year_offset


def _period_edges(period: str, tz=None, origin=None) -> mticker.Locator:
    """The locator of a period's first instants: its edges on the axis."""

    if period == GANTT_DATE_PERIOD.PROJECT_MONTH:
        return ProjectPeriodEdges(origin, 1)
    if period == PROJECT_YEAR:
        return ProjectPeriodEdges(origin, 12)
    if period == GANTT_DATE_PERIOD.DAY:
        return mdates.DayLocator(tz=tz)
    if period == GANTT_DATE_PERIOD.WEEK:
        return mdates.WeekdayLocator(byweekday=mdates.MO, tz=tz)
    if period == GANTT_DATE_PERIOD.MONTH:
        return mdates.MonthLocator(tz=tz)
    if period == GANTT_DATE_PERIOD.QUARTER:
        return mdates.MonthLocator(bymonth=(1, 4, 7, 10), tz=tz)
    return mdates.YearLocator(tz=tz)


class PeriodCentres(mticker.Locator):
    """Ticks at the centre of each period's visible part, one per period.

    A period cut by the view is centred on what remains of it, so a wide
    period (a year over a few months) keeps its label.
    """

    def __init__(self, edges: mdates.DateLocator, span: float):
        self.edges = edges
        self.span = span

    def __call__(self):
        low, high = sorted(self.axis.get_view_interval())
        self.edges.set_axis(self.axis)
        edges = self.edges.tick_values(
            mdates.num2date(low - self.span), mdates.num2date(high + self.span)
        )
        edges = np.unique(np.clip(np.asarray(edges, dtype=float), low, high))
        widths = np.diff(edges)
        # a sliver of a period at the view's edge has no room for its label
        keep = widths >= widths.max() * DATE_PERIOD_MIN_SHARE if len(widths) else []
        return list(((edges[:-1] + edges[1:]) / 2)[keep])


def _project_label(period: str, moment, origin) -> str:
    """M1, M2, … or Y1, Y2, … counted from the project origin."""

    months = _months_since(origin, moment)
    if period == GANTT_DATE_PERIOD.PROJECT_MONTH:
        return f"M{months + 1}"
    return f"Y{months // 12 + 1}"


def _period_formatter(period: str, fmt, tz=None, origin=None) -> mticker.FuncFormatter:
    """A period's label at its centre: the format given, else the period's own."""

    def label(value, _pos=None):
        moment = mdates.num2date(value, tz=tz)
        if not _auto_format(fmt):
            return moment.strftime(fmt)
        if period == GANTT_DATE_PERIOD.QUARTER:
            return f"Q{(moment.month - 1) // 3 + 1}"
        if period == GANTT_DATE_PERIOD.PROJECT_MONTH:
            return _project_label(period, moment, origin)
        return moment.strftime(DATE_PERIOD_LABELS[period])

    return mticker.FuncFormatter(label)


def _apply_date_period(
    ax, axis_name: str, period: str, fmt, tz=None, origin=None, bounds=None
) -> None:
    """Divide a date axis into calendar periods (ADR 0049).

    Minor ticks mark the period edges and carry the grid lines; major ticks
    label each period at its centre. The enclosing period names its span in
    a row beneath, drawn on a secondary axis offset by one label row. Project
    months count from `origin`, the project start, under their project year.
    `bounds`, the schedule's (start, end) with a fixed limit as None, snaps
    the free ends of the view to the enclosing period edges, so every period
    shows whole and the labels sit evenly.
    """

    axis = getattr(ax, f"{axis_name}axis")
    if bounds is not None:
        _snap_to_periods(ax, axis_name, period, tz, origin, bounds)
    axis.set_minor_locator(_period_edges(period, tz, origin))
    axis.set_minor_formatter(mticker.NullFormatter())
    axis.set_major_locator(
        PeriodCentres(_period_edges(period, tz, origin), DATE_PERIOD_SPAN[period])
    )
    axis.set_major_formatter(_period_formatter(period, fmt, tz, origin))
    params = axis.get_tick_params(which="major")
    # the edge marks take the major tick look the furniture gave the axis
    edge_marks = {k: params[k] for k in ("length", "width", "color") if k in params}
    edge_marks.setdefault("length", mpl.rcParams[f"{axis_name}tick.major.size"])
    axis.set_tick_params(which="minor", **edge_marks)
    axis.set_tick_params(which="major", length=0)

    parent = DATE_PERIOD_PARENT[period]
    if parent is None:
        return
    size = params.get("labelsize", mpl.rcParams[f"{axis_name}tick.labelsize"])
    size = FontProperties(size=size).get_size_in_points()
    location = "bottom" if axis_name == "x" else "left"
    secondary = (
        ax.secondary_xaxis(location)
        if axis_name == "x"
        else ax.secondary_yaxis(location)
    )
    other = getattr(secondary, f"{axis_name}axis")
    other.set_major_locator(
        PeriodCentres(_period_edges(parent, tz, origin), DATE_PERIOD_SPAN[parent])
    )

    def parent_label(value, _pos=None):
        moment = mdates.num2date(value, tz=tz)
        if parent == PROJECT_YEAR:
            return _project_label(parent, moment, origin)
        return moment.strftime(DATE_PARENT_LABELS[parent])

    other.set_major_formatter(mticker.FuncFormatter(parent_label))
    other.set_tick_params(
        length=0,
        pad=params.get("pad", mpl.rcParams[f"{axis_name}tick.major.pad"])
        + size * DATE_PARENT_ROW_SPACING,
        labelsize=size,
        **({"labelcolor": params["labelcolor"]} if "labelcolor" in params else {}),
    )
    for spine in secondary.spines.values():
        spine.set_visible(False)


def _widen_to_ticks(ticks: np.ndarray, lo: float, hi: float) -> Tuple[float, float]:
    """A range widened outward to the ticks enclosing it.

    An end with no tick beyond it keeps its own value. Every axis that must
    start and end on a labelled value shares this shape.
    """

    if len(ticks) < 2:
        return lo, hi
    tol = float(np.min(np.diff(ticks))) * 1e-6
    below, above = ticks[ticks <= lo + tol], ticks[ticks >= hi - tol]
    return (
        float(below.max()) if len(below) else lo,
        float(above.min()) if len(above) else hi,
    )


def _snap_to_periods(ax, axis_name, period, tz, origin, bounds) -> None:
    """Extend the free view ends to the period edges enclosing the schedule."""

    axis = getattr(ax, f"{axis_name}axis")
    lo, hi = sorted(axis.get_view_interval())
    start, end = bounds
    edges = _period_edges(period, tz, origin)
    edges.set_axis(axis)
    span = DATE_PERIOD_SPAN[period]
    reach = (start if start is not None else lo, end if end is not None else hi)
    ticks = np.asarray(
        edges.tick_values(
            mdates.num2date(reach[0] - span, tz=tz),
            mdates.num2date(reach[1] + span, tz=tz),
        ),
        dtype=float,
    )
    if start is not None:
        below = ticks[ticks <= start]
        lo = below.max() if len(below) else start
    if end is not None:
        above = ticks[ticks >= end]
        hi = above.min() if len(above) else end
    (ax.set_xlim if axis_name == "x" else ax.set_ylim)(lo, hi)


# the least gap between two period tick labels, in font sizes
PERIOD_LABEL_GAP = 0.5


class PeriodTicks(mticker.Locator):
    """One tick per period, thinned so the labels never touch.

    Every period is a tick when its labels fit along the axis; otherwise
    the first and last periods stay and a period drops out when its label
    would run into the previous kept one. Measured from the axis length at
    draw time, so a narrow subplot keeps fewer ticks than a wide figure.
    """

    def __init__(self, periods):
        self.periods = np.unique(np.asarray(periods, dtype=float))

    def __call__(self):
        return self.tick_values(*self.axis.get_view_interval())

    def tick_values(self, vmin, vmax):
        periods, axis = self.periods, self.axis
        span = abs(vmax - vmin)
        if axis is None or len(periods) < 3 or span <= 0:
            return periods
        along_x = axis.axis_name == "x"
        length = axis.axes.bbox.width if along_x else axis.axes.bbox.height
        if length <= 0:
            return periods
        size = FontProperties(
            size=axis.get_tick_params(which="major").get(
                "labelsize", mpl.rcParams[f"{axis.axis_name}tick.labelsize"]
            )
        ).get_size_in_points()
        px = axis.figure.dpi / 72.0
        labels = axis.get_major_formatter().format_ticks(periods)
        extents = [
            _text_size(size, label)[0 if along_x else 1] * px for label in labels
        ]
        centres = (periods - min(vmin, vmax)) / span * length
        gap = PERIOD_LABEL_GAP * size * px

        def fits(i, j):
            return centres[j] - extents[j] / 2 >= centres[i] + extents[i] / 2 + gap

        kept = [0]
        for j in range(1, len(periods) - 1):
            if fits(kept[-1], j):
                kept.append(j)
        last = len(periods) - 1
        while len(kept) > 1 and not fits(kept[-1], last):
            kept.pop()
        kept.append(last)
        return periods[kept]
