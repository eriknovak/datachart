# CalendarHeatmap

One colored cell per day, weeks as columns and weekdays as rows. The [Calendar Heatmap guide](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/calendarheatmap/index.md) shows every feature on real data; this page is the contract: the function, the shape of its data, the keys `style` takes, and the constant each parameter accepts.

## Function

### datachart.charts.CalendarHeatmap

```
CalendarHeatmap(
    data: (
        CalendarHeatmapDataAttrs
        | list[CalendarHeatmapDataAttrs]
    ),
    *,
    title: str | None = None,
    subtitle: str | list[str | None] | None = None,
    emphasis: None = None,
    year: int | None = None,
    week_start: CALENDAR_WEEKDAY | str | None = None,
    show_month_labels: bool | None = None,
    show_weekday_labels: bool | None = None,
    figsize: FIG_SIZE | tuple[float, float] | None = None,
    aspect_ratio: ASPECT_RATIO | str | None = None,
    max_cols: int | None = None,
    show_colorbars: bool | None = None,
    show_values: bool | None = None,
    value_format: VALUE_FORMAT | str | None = None,
    style: (
        CalendarHeatmapStyleAttrs
        | list[CalendarHeatmapStyleAttrs | None]
        | None
    ) = None,
    norm: str | list[str | None] | None = None,
    vmin: float | list[float | None] | None = None,
    vmax: float | list[float | None] | None = None,
    vcenter: float | list[float | None] | None = None,
    colorbar: (
        ColorbarSettingAttrs
        | list[ColorbarSettingAttrs | None]
        | None
    ) = None,
    texts: (
        TextSettingAttrs
        | list[TextSettingAttrs]
        | list[
            TextSettingAttrs | list[TextSettingAttrs] | None
        ]
        | None
    ) = None
) -> plt.Figure
```

Creates the calendar heatmap.

A calendar heatmap draws one cell per day, the weeks as columns and the weekdays as rows, colored by the day's value, with the months separated and labelled. Use it when a daily series has a weekly or seasonal rhythm worth seeing at a glance: commits, sales, steps, rainfall. Data spanning several years draws one calendar per year; for a matrix that is not a calendar, use Heatmap.

Examples:

```
>>> from datetime import date, timedelta
>>> from datachart.charts import CalendarHeatmap
>>> days = [date(2024, 1, 1) + timedelta(days=i) for i in range(366)]
>>> figure = CalendarHeatmap(
...     data={"date": days, "value": [i % 7 for i in range(366)]},
...     title="Daily values, 2024",
...     show_colorbars=True,
... )
```

| PARAMETER             | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`                | The dated values: a {"date": [...], "value": [...]} dict, or a list of such dicts drawing one calendar per dataset. Dates are temporal objects (date, datetime, numpy.datetime64, or pandas Timestamp), each appearing once; date strings are never parsed. A calendar spans the months that hold data, whole months at a time; a day absent from the list, or valued None, is drawn blank. **TYPE:** \`CalendarHeatmapDataAttrs |
| `title`               | The title of the chart. **TYPE:** \`str                                                                                                                                                                                                                                                                                                                                                                                          |
| `subtitle`            | The subtitle(s) for individual datasets. A dataset that spans several years names each calendar by its year, after the subtitle when one is given. **TYPE:** \`str                                                                                                                                                                                                                                                               |
| `emphasis`            | Not supported: a calendar is a single raster layer with no series to mute or highlight. Passing a value raises ValueError. **TYPE:** `None` **DEFAULT:** `None`                                                                                                                                                                                                                                                                  |
| `year`                | The one year to draw, colored over its own values. Without it every year the dates span is drawn, one calendar per year in year order, sharing one value range so the colors compare across years. **TYPE:** \`int                                                                                                                                                                                                               |
| `week_start`          | The weekday of the top row: CALENDAR_WEEKDAY.MONDAY or CALENDAR_WEEKDAY.SUNDAY. Defaults to the theme's plot_calendar_heatmap_week_start. **TYPE:** \`CALENDAR_WEEKDAY                                                                                                                                                                                                                                                           |
| `show_month_labels`   | Whether to label the months along the bottom axis, each over the middle of its weeks. Defaults to True. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                         |
| `show_weekday_labels` | Whether to label every other weekday along the left axis. Defaults to True. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                     |
| `figsize`             | The size of the figure. Defaults to the default width at a short height per row of calendars, the shape a calendar fills. **TYPE:** \`FIG_SIZE                                                                                                                                                                                                                                                                                   |
| `aspect_ratio`        | The aspect ratio of the cells: ASPECT_RATIO.EQUAL (the default) keeps them square, ASPECT_RATIO.AUTO stretches them to the figure. See ASPECT_RATIO. **TYPE:** \`ASPECT_RATIO                                                                                                                                                                                                                                                    |
| `max_cols`            | Maximum number of calendars per row when several are drawn. Defaults to 1, one calendar per row. **TYPE:** \`int                                                                                                                                                                                                                                                                                                                 |
| `show_colorbars`      | Whether to show the colorbar(s). **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                                |
| `show_values`         | Whether to write each day's value into its cell. **TYPE:** \`bool                                                                                                                                                                                                                                                                                                                                                                |
| `value_format`        | The format of the cell values: a VALUE_FORMAT constant (default VALUE_FORMAT.DEFAULT) or any "{x:.1f}", "{:.1f}", or "%g" style string. **TYPE:** \`VALUE_FORMAT                                                                                                                                                                                                                                                                 |
| `style`               | Style configuration(s) for the calendar(s). **TYPE:** \`CalendarHeatmapStyleAttrs                                                                                                                                                                                                                                                                                                                                                |
| `norm`                | Value normalization method(s). "centered" and "twoslope" hold vcenter in the middle of the theme's diverging colormap; see NORMALIZE. **TYPE:** \`str                                                                                                                                                                                                                                                                            |
| `vmin`                | Minimum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                            |
| `vmax`                | Maximum value(s) for normalization. **TYPE:** \`float                                                                                                                                                                                                                                                                                                                                                                            |
| `vcenter`             | The value(s) a centred normalization holds in the middle of the colormap (0 by default); ignored by every other norm. **TYPE:** \`float                                                                                                                                                                                                                                                                                          |
| `colorbar`            | The colorbar setting(s): label, location, tick format, and tick positions. See ColorbarSettingAttrs. **TYPE:** \`ColorbarSettingAttrs                                                                                                                                                                                                                                                                                            |
| `texts`               | Text annotation(s) to draw, on every calendar of their dataset. The cells sit at integer positions: the week column along x, the weekday row along y, counted from zero at the top-left cell of the drawn range. **TYPE:** \`TextSettingAttrs                                                                                                                                                                                    |

| RETURNS      | DESCRIPTION                                    |
| ------------ | ---------------------------------------------- |
| `plt.Figure` | The figure containing the calendar heatmap(s). |

| RAISES       | DESCRIPTION                                                                                                                                                                                       |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ValueError` | If emphasis is given, the data is not a dated-values dict, a date is not a temporal object, a date appears twice, year names a year without data, or week_start is not a CALENDAR_WEEKDAY member. |

## Data

Each record in `data` is a [`CalendarHeatmapDataAttrs`](#datachart.typings.CalendarHeatmapDataAttrs).

### datachart.typings.CalendarHeatmapDataAttrs

Bases: `TypedDict`

The data attributes for the calendar heatmap.

| ATTRIBUTE | DESCRIPTION                                                                                                                                                              |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `date`    | One temporal object per day: a date, datetime, numpy.datetime64, or pandas Timestamp. Date strings are never parsed, and every date appears once. **TYPE:** \`list\[date |
| `value`   | The value of each day, one per date; None leaves the day blank. **TYPE:** \`list\[int                                                                                    |

## Style

`style` takes the keys of [`CalendarHeatmapStyleAttrs`](#datachart.typings.CalendarHeatmapStyleAttrs). The chart also reads the shared groups it draws: text annotations ([`TextStyleAttrs`](https://eriknovak.github.io/datachart/dev/references/typings/#datachart.typings.TextStyleAttrs)). Every key falls back to the theme, so the same keys set the default look through [`config`](https://eriknovak.github.io/datachart/dev/references/config/index.md).

### datachart.typings.CalendarHeatmapStyleAttrs

Bases: `TypedDict`

The typing for the calendar heatmap style.

| ATTRIBUTE                                | DESCRIPTION                                                                                                                                   |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `plot_calendar_heatmap_cmap`             | The colormap of the day cells (palette name, single color, list of hex colors, or colormap); None takes the heatmap colormap. **TYPE:** \`str |
| `plot_calendar_heatmap_cmap_diverging`   | The colormap the day cells take under a centred norm; None takes the heatmap diverging colormap. **TYPE:** \`str                              |
| `plot_calendar_heatmap_alpha`            | The alpha value of the day cells. **TYPE:** \`float                                                                                           |
| `plot_calendar_heatmap_font_size`        | The font size of the cell values. **TYPE:** \`int                                                                                             |
| `plot_calendar_heatmap_font_color`       | The font color of the cell values. **TYPE:** \`str                                                                                            |
| `plot_calendar_heatmap_font_style`       | The font style of the cell values. **TYPE:** \`FONT_STYLE                                                                                     |
| `plot_calendar_heatmap_font_weight`      | The font weight of the cell values. **TYPE:** \`FONT_WEIGHT                                                                                   |
| `plot_calendar_heatmap_edge_width`       | The width of the borders drawn between the day cells (0 draws none). **TYPE:** \`int                                                          |
| `plot_calendar_heatmap_edge_color`       | The color of the borders drawn between the day cells. **TYPE:** \`str                                                                         |
| `plot_calendar_heatmap_month_line_width` | The width of the separators drawn between months (0 draws none). **TYPE:** \`int                                                              |
| `plot_calendar_heatmap_month_line_color` | The color of the separators drawn between months; None takes the heatmap frame color. **TYPE:** \`str                                         |
| `plot_calendar_heatmap_week_start`       | The weekday in the top row of every week, the default of week_start. **TYPE:** \`CALENDAR_WEEKDAY                                             |

## Constants

The parameters that accept a constant, with the class in [datachart.constants](https://eriknovak.github.io/datachart/dev/references/constants/index.md) that lists its values.

| Parameter                                                       | Constant                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `week_start`                                                    | [`CALENDAR_WEEKDAY`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.CALENDAR_WEEKDAY)                                                                                                                                                                                                                                         |
| `figsize`                                                       | [`FIG_SIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.FIG_SIZE)                                                                                                                                                                                                                                                         |
| `aspect_ratio`                                                  | [`ASPECT_RATIO`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ASPECT_RATIO)                                                                                                                                                                                                                                                 |
| `value_format`                                                  | [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT)                                                                                                                                                                                                                                                 |
| `norm`                                                          | [`NORMALIZE`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.NORMALIZE)                                                                                                                                                                                                                                                       |
| `colorbar={"location": ..., "format": ..., "orientation": ...}` | [`COLORBAR_LOCATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.COLORBAR_LOCATION), [`VALUE_FORMAT`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.VALUE_FORMAT), [`ORIENTATION`](https://eriknovak.github.io/datachart/dev/references/constants/#datachart.constants.ORIENTATION) |
