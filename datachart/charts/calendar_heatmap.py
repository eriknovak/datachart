import math
from typing import Union, List, Optional, Tuple

import matplotlib.pyplot as plt

from ..utils._internal.plot_engine import render
from ..utils._internal.validate import (
    validate_calendar_dates,
    validate_calendar_year,
    validate_unique_dates,
)
from ..typings import (
    CalendarHeatmapDataAttrs,
    CalendarHeatmapStyleAttrs,
    ColorbarSettingAttrs,
    TextSettingAttrs,
)
from ..constants import ASPECT_RATIO, FIG_SIZE, VALUE_FORMAT, CALENDAR_WEEKDAY

# a calendar is wide and short: the default figure keeps the default width
# and stacks this much height per row of calendars
CALENDAR_ROW_HEIGHT = 1.9

# ================================================
# Main Chart Definition
# ================================================


def CalendarHeatmap(
    data: Union[CalendarHeatmapDataAttrs, List[CalendarHeatmapDataAttrs]],
    *,
    title: Optional[str] = None,
    subtitle: Optional[Union[str, List[Optional[str]]]] = None,
    emphasis: None = None,
    year: Optional[int] = None,
    week_start: Optional[Union[CALENDAR_WEEKDAY, str]] = None,
    show_month_labels: Optional[bool] = None,
    show_weekday_labels: Optional[bool] = None,
    figsize: Optional[Union[FIG_SIZE, Tuple[float, float]]] = None,
    aspect_ratio: Optional[Union[ASPECT_RATIO, str]] = None,
    max_cols: Optional[int] = None,
    show_colorbars: Optional[bool] = None,
    show_values: Optional[bool] = None,
    value_format: Optional[Union[VALUE_FORMAT, str]] = None,
    style: Optional[
        Union[CalendarHeatmapStyleAttrs, List[Optional[CalendarHeatmapStyleAttrs]]]
    ] = None,
    norm: Optional[Union[str, List[Optional[str]]]] = None,
    vmin: Optional[Union[float, List[Optional[float]]]] = None,
    vmax: Optional[Union[float, List[Optional[float]]]] = None,
    vcenter: Optional[Union[float, List[Optional[float]]]] = None,
    colorbar: Optional[
        Union[ColorbarSettingAttrs, List[Optional[ColorbarSettingAttrs]]]
    ] = None,
    texts: Optional[
        Union[
            TextSettingAttrs,
            List[TextSettingAttrs],
            List[Union[TextSettingAttrs, List[TextSettingAttrs], None]],
        ]
    ] = None,
) -> plt.Figure:
    """Creates the calendar heatmap.

    A calendar heatmap draws one cell per day, the weeks as columns and the
    weekdays as rows, colored by the day's value, with the months separated
    and labelled. Use it when a daily series has a weekly or seasonal
    rhythm worth seeing at a glance: commits, sales, steps, rainfall. Data
    spanning several years draws one calendar per year; for a matrix that
    is not a calendar, use [`Heatmap`][datachart.charts.Heatmap].

    Examples:
        >>> from datetime import date, timedelta
        >>> from datachart.charts import CalendarHeatmap
        >>> days = [date(2024, 1, 1) + timedelta(days=i) for i in range(366)]
        >>> figure = CalendarHeatmap(
        ...     data={"date": days, "value": [i % 7 for i in range(366)]},
        ...     title="Daily values, 2024",
        ...     show_colorbars=True,
        ... )

    Args:
        data: The dated values: a `{"date": [...], "value": [...]}` dict, or
            a list of such dicts drawing one calendar per dataset. Dates are
            temporal objects (`date`, `datetime`, `numpy.datetime64`, or
            pandas `Timestamp`), each appearing once; date strings are never
            parsed. A calendar spans the months that hold data, whole months
            at a time; a day absent from the list, or valued `None`, is
            drawn blank.
        title: The title of the chart.
        subtitle: The subtitle(s) for individual datasets. A dataset that
            spans several years names each calendar by its year, after the
            subtitle when one is given.
        emphasis: Not supported: a calendar is a single raster layer with no
            series to mute or highlight. Passing a value raises `ValueError`.
        year: The one year to draw, colored over its own values. Without it
            every year the dates span is drawn, one calendar per year in
            year order, sharing one value range so the colors compare
            across years.
        week_start: The weekday of the top row:
            [`CALENDAR_WEEKDAY.MONDAY`][datachart.constants.CALENDAR_WEEKDAY] or
            [`CALENDAR_WEEKDAY.SUNDAY`][datachart.constants.CALENDAR_WEEKDAY]. Defaults
            to the theme's `plot_calendar_heatmap_week_start`.
        show_month_labels: Whether to label the months along the bottom
            axis, each over the middle of its weeks. Defaults to `True`.
        show_weekday_labels: Whether to label every other weekday along the
            left axis. Defaults to `True`.
        figsize: The size of the figure. Defaults to the default width at a
            short height per row of calendars, the shape a calendar fills.
        aspect_ratio: The aspect ratio of the cells:
            [`ASPECT_RATIO.EQUAL`][datachart.constants.ASPECT_RATIO] (the default) keeps
            them square, [`ASPECT_RATIO.AUTO`][datachart.constants.ASPECT_RATIO]
            stretches them to the figure. See
            [`ASPECT_RATIO`][datachart.constants.ASPECT_RATIO].
        max_cols: Maximum number of calendars per row when several are
            drawn. Defaults to `1`, one calendar per row.
        show_colorbars: Whether to show the colorbar(s).
        show_values: Whether to write each day's value into its cell.
        value_format: The format of the cell values: a
            [`VALUE_FORMAT`][datachart.constants.VALUE_FORMAT] constant (default
            [`VALUE_FORMAT.DEFAULT`][datachart.constants.VALUE_FORMAT]) or any
            `"{x:.1f}"`, `"{:.1f}"`, or `"%g"` style string.
        style: Style configuration(s) for the calendar(s).
        norm: Value normalization method(s). `"centered"` and `"twoslope"`
            hold `vcenter` in the middle of the theme's diverging colormap;
            see [`NORMALIZE`][datachart.constants.NORMALIZE].
        vmin: Minimum value(s) for normalization.
        vmax: Maximum value(s) for normalization.
        vcenter: The value(s) a centred normalization holds in the middle of
            the colormap (0 by default); ignored by every other norm.
        colorbar: The colorbar setting(s): label, location, tick format, and tick
            positions. See
            [`ColorbarSettingAttrs`][datachart.typings.ColorbarSettingAttrs].
        texts: Text annotation(s) to draw, on every calendar of their
            dataset. The cells sit at integer positions: the week column
            along x, the weekday row along y, counted from zero at the
            top-left cell of the drawn range.

    Returns:
        The figure containing the calendar heatmap(s).

    Raises:
        ValueError: If `emphasis` is given, the data is not a dated-values
            dict, a date is not a temporal object, a date appears twice,
            `year` names a year without data, or `week_start` is not a
            [`CALENDAR_WEEKDAY`][datachart.constants.CALENDAR_WEEKDAY] member.

    """
    params = dict(locals())
    return render("calendarheatmap", params, expand=_year_panels)


def _year_panels(
    charts: Union[dict, List[dict]], settings: dict
) -> Tuple[List[dict], dict]:
    """One chart per calendar year, on a figure tall enough for their rows."""

    charts = charts if isinstance(charts, list) else [charts]
    year = settings.get("year")
    charts = [panel for chart in charts for panel in _year_charts(chart, year)]
    if settings.get("figsize") is None:
        rows = math.ceil(len(charts) / settings["max_cols"])
        figsize = (FIG_SIZE.DEFAULT[0], CALENDAR_ROW_HEIGHT * rows)
        settings = {**settings, "figsize": figsize}
    return charts, settings


def _year_charts(chart: dict, year: Optional[int]) -> List[dict]:
    """One chart per year of a dataset, in year order; `year` keeps one.

    The years of one dataset share its value range unless `vmin`/`vmax`
    pin one, so the same value takes the same color on every calendar.
    """

    data = chart["data"]
    dates = validate_calendar_dates(data["date"])
    values = list(data["value"])
    if len(values) != len(dates):
        raise ValueError(
            "CalendarHeatmap `data` needs one value per date: "
            f"{len(dates)} dates, {len(values)} values."
        )
    if not dates:
        raise ValueError("CalendarHeatmap `data` needs at least one date.")
    validate_unique_dates(dates)
    years = {day.year for day in dates}
    validate_calendar_year(year, years)
    if year is not None:
        years = {year}

    by_year = {y: ([], []) for y in sorted(years)}
    for day, value in zip(dates, values):
        if day.year in by_year:
            by_year[day.year][0].append(day)
            by_year[day.year][1].append(value)

    shared = _shared_range(values, chart.get("norm"))
    charts = []
    for y, (year_dates, year_values) in by_year.items():
        panel = dict(chart)
        panel["data"] = {"date": year_dates, "value": year_values}
        panel["year"] = y
        if len(by_year) > 1:
            subtitle = chart.get("subtitle")
            panel["subtitle"] = str(y) if subtitle is None else f"{subtitle} {y}"
            for key, bound in zip(("vmin", "vmax"), shared or ()):
                if panel.get(key) is None:
                    panel[key] = bound
        charts.append(panel)
    return charts


def _shared_range(values: list, norm) -> Optional[Tuple[float, float]]:
    """The (min, max) of the values a normalization can show; None without any.

    A log norm shows the positive values, a logit norm those inside (0, 1);
    the range skips what the norm would mask, as its own autoscale does.
    """

    numbers = [v for v in values if v is not None and not math.isnan(v)]
    if norm == "log":
        numbers = [v for v in numbers if v > 0]
    elif norm == "logit":
        numbers = [v for v in numbers if 0 < v < 1]
    if not numbers:
        return None
    return min(numbers), max(numbers)
