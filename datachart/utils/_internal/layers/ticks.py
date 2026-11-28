"""Tick locators and formatters for date periods, schedules and matrix cells."""

import math
from datetime import datetime, tzinfo
from typing import List, Optional, Tuple
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as mticker
from matplotlib.axes import Axes
from ..validate import is_number
from ....constants import DATE_FORMAT, GANTT_DATE_PERIOD
from .base import _format_value, _px_to_points, _text_size, _text_width

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


# the tick steps a fitted cell picks from, times a power of ten; 2.5 is long
TICK_STEPS = [1, 2, 5, 10]
# the clear space between neighbouring tick labels, in ems of their font
TICK_LABEL_GAP = 0.5
# the most bins a fitted axis tries, as matplotlib's automatic count caps it
MAX_TICK_BINS = 9
# the labels a fitted axis shows when that many fit apart
MIN_TICK_LABELS = 2
# the fallbacks when no count clears every label, the most preferred first
EVEN_SUBSET, ALL_OF_FEWER, ANY_SUBSET = 1, 2, 3
# a short tick label divides by a power of a thousand and names it
SHORT_SCALE = 1000
SHORT_SUFFIXES = ("k", "M", "G", "T")
# the most characters a short label's number keeps: 1.5k, never 2.01k
SHORT_CHARACTERS = 3
# a power of ten no tick reaches: a large label takes a suffix, never 1e6
NO_SCIENTIFIC_ABOVE = 100


class _ShortFormatter(mticker.ScalarFormatter):
    """Tick labels that name a thousand and up by a suffix: 2000 is 2k.

    An axis takes the suffix only when every tick of a thousand or more
    shortens to a number of at most three characters (2k, 1.5k, 125k).
    Otherwise, as for years like 2010, the axis keeps matplotlib's own format.
    """

    def __init__(self):
        super().__init__()
        self.is_short = False

    def set_locs(self, locs):
        # a short axis needs no offset, and its large values take no 1e6
        large = [x for x in locs if abs(x) >= SHORT_SCALE]
        self.is_short = bool(large) and all(
            len(_short_number(x)[0].lstrip("-")) <= SHORT_CHARACTERS for x in large
        )
        limits = mpl.rcParams["axes.formatter.limits"]
        self.set_useOffset(
            not self.is_short and mpl.rcParams["axes.formatter.useoffset"]
        )
        self.set_powerlimits(
            (limits[0], NO_SCIENTIFIC_ABOVE) if self.is_short else limits
        )
        super().set_locs(locs)

    def __call__(self, x, pos=None):
        if not self.is_short or abs(x) < SHORT_SCALE:
            return super().__call__(x, pos)
        number, suffix = _short_number(x)
        return self.fix_minus(number + suffix)


def _short_number(x: float) -> Tuple[str, str]:
    """A value of a thousand or more as a number and its suffix: ("1.5", "k")."""

    power = min(int(math.log10(abs(x)) // 3), len(SHORT_SUFFIXES))
    # twelve significant digits keep a tick's digits but drop float noise
    return f"{x / SHORT_SCALE**power:.12g}", SHORT_SUFFIXES[power - 1]


class _FittingTicks(mticker.MaxNLocator):
    """Round ticks, as many as keep a cell's labels apart from every other.

    The count starts at matplotlib's own for the axis length and drops until
    neighbouring labels sit a gap apart. If that leaves fewer than two
    labels, a larger count that shows two apart wins, or else an evenly
    spaced subset of one count's labels. A label at a cell's end may reach
    into the space beside the cell only up to its middle, so it never meets
    a label of the next cell.
    """

    def __init__(self):
        super().__init__(nbins="auto", steps=TICK_STEPS)

    def __call__(self):
        # an empty view keeps matplotlib's ticks
        axis = self.axis
        lo, hi = sorted(axis.get_view_interval())
        if not hi > lo:
            return super().__call__()

        # the label font and the cell's place along the axis, in points
        along_x = axis.axis_name == "x"
        font = axis.get_major_ticks(1)[0].label1.get_fontproperties()
        size = font.get_size_in_points()
        gap = TICK_LABEL_GAP * size
        start, end, before, after = _cell_span(axis.axes, along_x)
        formatter = axis.get_major_formatter()

        # the ticks in reach and which clear, labelled as the axis labels them
        def labels_in_reach(values):
            labels = formatter.format_ticks(values)
            if along_x:
                extents = [_text_width(label, font) for label in labels]
            else:
                extents = [_text_size(size, label)[1] for label in labels]
            half = np.array(extents) / 2
            centres = start + (values - lo) / (hi - lo) * (end - start)
            reach = (centres - half >= start - before) & (centres + half <= end + after)
            return values[reach], _apart(centres[reach], half[reach], gap)

        # whether every value stays in reach and clear, labelled on its own
        def all_clear(values):
            in_reach, apart = labels_in_reach(values)
            return len(in_reach) == len(values) and apart.all()

        # matplotlib's count first, then fewer bins, then more, until two clear
        nbins = int(np.clip(axis.get_tick_space(), 1, MAX_TICK_BINS))
        order = [*range(nbins, 0, -1), *range(nbins + 1, MAX_TICK_BINS + 1)]
        best_rank, best = np.inf, np.array([])
        for bins in order:
            values = mticker.MaxNLocator(nbins=bins, steps=TICK_STEPS).tick_values(
                lo, hi
            )
            values, apart = labels_in_reach(values[(values >= lo) & (values <= hi)])
            kept = values[apart]
            shows_two = len(kept) >= MIN_TICK_LABELS
            if apart.all() and shows_two:
                return values

            # short of that: keep the best fallback, each still clear once its
            # own labels are formatted
            if shows_two and _evenly_spaced(kept):
                rank = EVEN_SUBSET
            elif apart.all():
                rank = ALL_OF_FEWER
            else:
                rank = ANY_SUBSET
            if rank < best_rank and (apart.all() or all_clear(kept)):
                best_rank, best = rank, kept
        return best


def _apart(centres: np.ndarray, half: np.ndarray, gap: float) -> np.ndarray:
    """Which labels to keep, in order, so each clears the last kept by a gap."""

    keep = np.zeros(len(centres), dtype=bool)
    edge = -np.inf
    for k, (centre, extent) in enumerate(zip(centres, half)):
        if centre - extent >= edge + gap:
            keep[k] = True
            edge = centre + extent
    return keep


def _evenly_spaced(values: np.ndarray) -> bool:
    """Whether two or more values sit one step apart throughout."""

    steps = np.diff(values)
    return bool(np.allclose(steps, steps[0]))


def _cell_span(ax: Axes, along_x: bool) -> Tuple[float, float, float, float]:
    """The axes' (start, end, reach before, reach after) along one direction.

    All four are in points. A reach is half the space to the nearest axes on
    that side in the same row or column; a side with none reaches without
    limit.
    """

    # the axes' own extent along and across the direction, in pixels
    box = ax.bbox
    start, end = (box.x0, box.x1) if along_x else (box.y0, box.y1)
    across = (box.y0, box.y1) if along_x else (box.x0, box.x1)

    # half the space to the nearest shown axes on each side in its row or column
    before = after = np.inf
    for other in ax.figure.axes:
        if not other.get_visible():
            continue
        b = other.bbox
        o_start, o_end = (b.x0, b.x1) if along_x else (b.y0, b.y1)
        o_across = (b.y0, b.y1) if along_x else (b.x0, b.x1)
        if o_across[1] <= across[0] or o_across[0] >= across[1]:
            continue
        if o_start >= end:
            after = min(after, (o_start - end) / 2)
        elif o_end <= start:
            before = min(before, (start - o_end) / 2)
    return (
        _px_to_points(ax, start),
        _px_to_points(ax, end),
        _px_to_points(ax, before),
        _px_to_points(ax, after),
    )


def fit_ticks(ax: Axes) -> None:
    """Give both axes short tick labels, as many as stay apart at draw time."""

    for axis in (ax.xaxis, ax.yaxis):
        # a log or other scale keeps its own ticks
        if axis.get_scale() != "linear":
            continue
        axis.set_major_locator(_FittingTicks())
        axis.set_major_formatter(_ShortFormatter())
