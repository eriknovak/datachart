---
status: accepted
---

# A missing value is not drawn; the builder normalises it once

No front handles a missing datum (issue #325). A record whose value is
`None` reaches numpy raw: the line, scatter and histogram fronts fail in
`stats.minimum` with a `TypeError`, the bar front in matplotlib's
arithmetic, the box front in a dimension check, and an `inf` breaks
numpy's histogram range. A column mixing `date` and `int` fails with a
`float()` `TypeError` although ADR 0037 promised one `ValueError` for a
temporal/numeric mix — its check runs across layers, not inside a column.
A single-point chart lets matplotlib warn about identical limits. Real
datasets have holes, so every caller pre-cleans or crashes.

## Commitments

- **Missing means not drawn.** `None`, `NaN` and `±inf` are one category,
  "missing", on every front. A missing value breaks a line at the hole and
  is dropped from scatter points, bars, bins, box and violin samples,
  swarm points and grid cells. Lines never reconnect across a hole. `inf`
  is missing rather than an error: it is never drawable, and a third rule
  is a rule nobody remembers.
- **A missing position drops the record.** When a position key (`x` on a
  continuous front, `label` on a group front, `start`/`end` on gantt and
  dumbbell) is missing, the whole record is not drawn. This is distinct
  from ADR 0069's shape check: a key *absent* from the record is a caller
  error and raises; a key *present but missing* is a datum and is skipped.
- **The builder normalises, once.** `build_charts_structure` (ADR 0069)
  copies numeric record values to `float` with `None` and `inf` as `NaN`
  and drops records with a missing position; layers, `get_chart_data` and
  the stats helpers read canonical, already-normalised columns. Grid fronts
  coerce their matrix to a float array the same way at build. No layer
  filters in `draw`.
- **The public stats helpers ignore missing values.** `datachart.utils.stats`
  functions (`mean`, `median`, `minimum`, `quantile`, `linear_fit`, …)
  compute over the finite values and document it, so a layer passing a
  normalised column and a user calling the helper directly get one answer.
- **An empty series draws nothing; an empty figure raises.** A layer left
  with no finite value draws nothing and keeps its legend entry — one
  subplot with no data is data. When every layer of a figure is empty,
  `render_chart` raises one `ValueError`: there is nothing to draw, which
  is a caller error.
- **A mixed column raises.** A column mixing temporal and numeric values
  raises the ADR 0037 `ValueError` from the layer's axis-kind report, so a
  mix inside one column fails the same way as a mix across layers. This
  amends ADR 0037.
- **A zero-width axis is padded, not warned about.** When a panel's data
  range on an axis is a single value, the limits step pads it by 5 % of the
  absolute value, ±0.5 when the value is 0, and ±1 day on a temporal axis.
  Matplotlib's "identical low and high lims" warning never fires.
- **One parametrised test.** Every record front runs with `None`, `NaN` and
  `inf` in a value key and in a position key; every grid front with a
  missing cell; one case per front asserts the drawn artists exclude the
  missing datum. The golden diff stays clean for finite data.

## Considered options

Raising on any missing value was rejected: it would force every caller to
pre-clean, and the guides' datasets (World Bank, Eurostat) have holes by
nature. Dropping and reconnecting lines across a hole was rejected: it
draws a trend that is not in the data. Filtering in each layer's `draw`
was rejected: twenty-six fronts would repeat one rule, and 0069 built the
builder to be the one record-reading seam. Treating `inf` as an error was
rejected for the rule count. Raising on any empty series was rejected:
in subplots and in `Grid` composition one empty panel is expected.
