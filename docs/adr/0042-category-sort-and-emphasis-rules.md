---
status: accepted
---

# Bar-type fronts sort their categories, and a rule fills in per-record emphasis

Bars draw in input order, so every comparison chart is sorted by hand before
it is passed in — and consistently across series, or a grouped chart falls
apart. Emphasis (ADR 0009) is a per-chart role, so "mute everything below the
median" has no expression at all for bars: the whole series is one role.

Two settings on the bar-type fronts — `BarChart`, `PyramidChart`, and
`RadialChart` (bar visual) — close both gaps: `sort` orders the categories,
`emphasis_rule` assigns per-record emphasis from the values (issue #123).

## Commitments

- **`sort` is a `SORT` value: `NONE`, `ASCENDING`, `DESCENDING`.** `NONE` is
  the default and means input order, so nothing existing moves. Sorting is by
  value, never by label — a label sort is a `sorted()` call on the caller's
  own data and needs no setting.
- **One order for every series in the chart.** A grouped or stacked chart has
  one category axis, so sorting reorders the axis, not each series
  separately. Series keep their identity; only the positions move.
- **The sort key is the total across series, and `sort_by` overrides it to
  one series by label.** The total is what a stacked chart already reads as a
  bar, and a defensible default for a grouped one. Requiring `sort_by`
  whenever a chart has more than one series would raise on the common case to
  serve the rare one.
- **A category the `sort_by` series does not carry sorts last, in input
  order.** Absence is not zero: a series without a category and a series with
  a zero there mean different things, and putting the absent ones at the end
  keeps the sort of the categories that do have a key intact.
- **Ties keep input order** — the sort is stable, everywhere.
- **A bar record carries its own `emphasis`, as public API.** This is the
  primitive the feature needs, and it is missing: today only treemap and
  network records carry a per-record role, while box and swarm layers take a
  list of roles aligned to their group labels. `BarDataPointAttrs` gains an
  optional `emphasis` key taking the same roles, so one bar can be tagged
  without any rule at all.
- **`emphasis_rule` fills in the records that set no role of their own.** It
  is sugar over the per-record key, not a second mechanism: the rule computes
  a role for every record, and an explicit per-record `emphasis` wins. That
  ordering makes "highlight the top three, and also this one" expressible.
- **A record matching the rule gets `HIGHLIGHT`, every other record
  `BACKGROUND`.** Emphasis is comparative — highlighting without muting the
  rest changes very little — so the rule commits to both ends.
- **The rule is a one-key dict**: `{"above": v}`, `{"below": v}`,
  `{"between": (lo, hi)}`, `{"top": n}`, `{"bottom": n}`. `above` and `below`
  are strict, `between` is inclusive of both bounds. `top`/`bottom` take a
  positive integer, clamp to the record count, and break ties by input order.
- **Two keys in one dict raises**, as does an unknown key, a non-positive or
  non-integer `n`, and a `between` whose bounds are reversed. Each is one
  `ValueError` from `validate.py`, in the style of the other validators
  there. Combining rules would need a composition semantics (and or or?) that
  nothing has asked for; a caller who wants one writes the per-record key.
- **The rule reads the record's own value**, not its stacked position, so it
  means the same thing under every `bar_mode`. Against a total the caller
  wants the rule to see, a single series is what they should pass.
- **Both settings are chart-front settings resolved when layers are built**,
  like every other front setting (ADR 0003). Neither is a config or theme
  attribute: they are statements about one chart's data, not a house style.
- **Sorting happens before the rule runs**, and neither is affected by the
  other. `top: 3` picks the same three records whatever the sort says, and a
  sort by total is unchanged by which records ended up muted.

## Scope

Only the three bar-type fronts get either setting in this change. The 17
fronts that accept `emphasis` carry three different shapes of it — per
series, per group label, per record — and a value-threshold rule means
something different for each. Extending `emphasis_rule` to the rest is
tracked separately (issue #151); the per-record key on bar records is the
pattern the rest would follow.

## Considered options

- *A `sort` that also takes a label order.* Rejected: an explicit category
  order is a reordering of the caller's own list, and `sort` would then mean
  two unrelated things. If explicit ordering is wanted later it is its own
  setting.
- *Sorting each series independently.* Rejected: a grouped chart's series
  share one category axis, so this would draw bars under the wrong labels.
- *Defaulting `sort_by` to the first series.* Rejected: it makes the chart's
  order depend on the order the caller happened to list its series in, which
  reads as arbitrary and changes under a harmless edit.
- *Keeping per-bar emphasis internal to the rule.* Rejected: the rule's
  "explicit emphasis wins" clause is meaningless if a user cannot write an
  explicit one, and the per-record key is the smaller thing to document.
- *An `emphasis` list on the front, aligned to records.* Rejected: on
  `BarChart` a list already means one role per chart in the charts list.
  Overloading it would make a two-series, two-record chart ambiguous.
- *A callable predicate instead of a dict.* Rejected: not serializable, not
  expressible in a theme file, and it invites arbitrary work at build time.
  The five named shapes cover the asked-for cases.
- *Non-matching records staying unset rather than muted.* Rejected: the
  contrast is the point, and a caller who wants a highlight-only chart tags
  the records directly.
