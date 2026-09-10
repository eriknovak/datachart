---
status: accepted
---

# The axis kind is a panel snapshot, and date strings are never parsed

Charts could not take datetime `x` at all: the chart-hash encoder had no
datetime branch, the column-range helper coerced through `float`, and the
one input that survived (ISO strings) drew as unordered categories. There
was no tick-format setting and no date-format constant.

## Commitments

- **Datetime-like means a real temporal object.** `datetime`, `date`,
  `numpy.datetime64`, and their subclasses (pandas `Timestamp`) put an axis
  on time. Strings are never parsed: `"2024"`, `"01-02"`, and `"2024-Q1"` are
  plausible category labels users already ship, and inferring dates from
  them would silently change existing charts. A regression test pins the
  categorical behaviour of ISO strings.
- **The axis kind is a `Panel`-owned, cross-layer concern.** Each layer
  reports the kind its `x` column asks for (temporal, numeric, categorical,
  or none); the panel resolves one kind at build, in `__init__`, from every
  layer it holds — the same place scales, limits, and orientation are
  decided (ADR 0001). Resolving on the panel rather than in the chart
  builder means `Panel` and `Grid` composition inherit the kind with the
  layers, and a mix across composed figures fails the same way a mix within
  one front does.
- **Temporal and numeric `x` cannot share a panel.** `validate_axis_kinds`
  raises one `ValueError` from the validation module. Category positions
  (bars, boxes, violins, swarms, heatmap cells) sit on their own index and
  never conflict; when their labels are dates they print through the date
  format, and the panel treats that axis as dated for validation.
- **Two tiers, one format setting.** Continuous fronts (line, stacked area,
  scatter, hexbin, contour) draw on a real time axis: `AutoDateLocator` plus
  `ConciseDateFormatter` by default, a `DateFormatter` pattern when
  `xticks_format` names one. Group fronts (bar, box, violin, swarm,
  raincloud, pyramid, parallel coordinates) keep categorical positions and
  format the date into the tick label only; a heatmap's coordinates are
  labels of index positions, so it sits in this tier. Hexbin and contour
  draw floats, so a temporal column converts to matplotlib date numbers at
  build and the panel's locator and formatter make the axis read as time.
  On the group tier `AUTO` has no locator to lean on, so it prints the ISO
  date, plus the time when any label carries one.
- **`xticks_format` / `yticks_format` are panel settings** that resolve by
  the axis they land on: a `strftime` pattern on a dated axis, a
  `VALUE_FORMAT` or `{x}` / `%` string elsewhere, applied like the heatmap's
  `valfmt`. `DATE_FORMAT.AUTO` leaves a numeric axis untouched. A value
  format on a numeric axis is validated at build so a bad pattern fails at
  the front. Explicit ticks without labels print through the same format.
  Composition takes the first source figure that sets a format.
- **Explicit positions pass through matplotlib's unit machinery.** `xticks`,
  `xmin` / `xmax`, reference lines, and bands take datetimes because the
  axes convert them; the panel sets its locator and formatter before the
  limits so unit updates never reset them. Timezone-aware input keeps its
  zone: the locator and formatter read it back from the axis, or from the
  layer when it drew date numbers. A value format on a dated axis, like a
  date pattern on a numeric one, is rejected at build with one message
  rather than printing date numbers.
- **The public `minimum` / `maximum` pass non-numeric values through**
  rather than the column-range helper bypassing them. Only one internal
  caller exists; the change is to the published contract, recorded with an
  `Added in Unreleased` note.
- **Date binning stays out.** Histogram and radial histogram bin raw
  samples and need a bin width in time units, which is undesigned; they are
  a follow-up.
