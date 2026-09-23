---
status: accepted
---

# A chart front's identity is one `ChartKind` row, not eight registries

A chart front's identity — which layer draws it, whether it groups, whether
it can overlay, whether it takes a grid, which emphasis unit it counts, what
its multiplot and subplot rules are — is spread over eight independent
tables (`LAYER_TYPES`, `EMPHASIS_RULE_UNITS`, `BAR_RECORD_CHARTS`,
`GROUP_CHART_TYPES`, the gridless and `tighten_xlim` tuples,
`CHART_CONFIGS`, `BARE_FIGURES`, `OVERLAYABLE_LAYERS`) and some forty
`chart_type == "…"` comparisons across the layer module, the plot engine and
composition. Fronts repeat three more facts in their own bodies (`is_2d_data`,
the `emphasis: None` rejection, `validate_single_dataset`). Adding a front
touches six to nine files, a missing table entry fails as a `KeyError` at
render time, and `ScatterMatrix` has no config row at all, so it renders under
`kde`/`histogram`'s identity (issue #272).

We replace all of it with one frozen `ChartKind` dataclass per front, in one
table, read through one accessor.

## Commitments

- **One row per front, one table, one accessor.** `ChartKind` is a frozen
  dataclass in its own `_internal` module, importing the layer classes it
  names; `CHART_KINDS` maps each chart-type string to a row; `chart_kind(name)`
  is the only lookup, and a name with no row raises `ValueError` naming the
  front, before any drawing. Internal identities that are not fronts (`kde`,
  the `ScatterMatrix` diagonal) may have rows; every exported front must.
- **The row holds every fact the engine reads about a front**: layer class
  (or the builder for fronts assembled from several layers), whether one
  chart's data is a dict, projection, the group / overlayable / gridless /
  tighten-xlim flags, emphasis unit builder and default `by`, the multiplot
  and subplot rules, and the parameters it rejects. A fact about a front that
  the engine, builder, or composition branches on lives on the row — not in a
  tuple next to the branch; a fact nothing branches on stays off it.
  Whether a single *layer* may join an overlay is the layer class's own
  `overlayable` attribute, since overlays filter layers, not fronts.
- **The eight registries and the string dispatches go.** `build_layers`,
  `build_chart_panel_settings`, `build_charts_structure`, `render_chart`,
  `Panel` and `Grid` read the row. No `chart_type == "…"` or `chart_type in
  (…)` remains in the layer module, plot engine, or composition. The front
  bodies drop their repeated `is_2d_data`, emphasis rejection and
  single-dataset validation once the row carries them.
- **ADR 0003 holds.** `render_chart` stays the single assembly point and the
  front signatures stay the settings allowlist. The row describes what a
  front *is*; it never becomes a `**kwargs` channel for what a front
  *accepts*. `config/charts.py` (`CHART_CONFIGS`) is deleted: it was only ever
  read by the subplot-layout helper, and nothing public documents it.
- **Golden parity is the acceptance test**, plus a unit test that every name
  in `datachart.charts.__all__` resolves to a row whose layer exists.

## Considered options

Growing `CHART_CONFIGS` into the descriptor was rejected: it lives under
`config/`, which is the user-facing style namespace, and it cannot import
layer classes without a cycle. Folding the table into the layer module was
rejected: that file is the largest in the package and the table is read by
three other modules. A `TypedDict` row was rejected: the fields are
heterogeneous (a class, callables, enums, tuples) and a dict literal gives no
construction-time check that a row is complete. Splitting the fold into two
PRs (tables first, dispatches second) was considered and rejected for one
gated by golden parity — the dispatch conversion is where the value is, and
the tables cannot be deleted until it lands.
