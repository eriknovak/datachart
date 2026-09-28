---
status: accepted
---

# The package ships `py.typed`, the figure type is public, and composition items are settings

`datachart` types every record, style and setting, yet ships no `py.typed`
marker, so an installed copy is untyped to every checker (issue #326). The
fronts return a private `Figure` subclass that adds `show(interactive=)`
without saying so in a return annotation, so a caller cannot annotate or
`isinstance`-check the result. `Panel` and `Grid` items and `layout_spec`
are bare `Dict[str, Any]`.

## Commitments

- **`datachart/py.typed` ships in the package data.** It is empty; the
  annotations already in place are what it declares.
- **`DatachartFigure` is public at `datachart.utils`**, beside `Panel`,
  `Grid` and `save_figure`: the module of finished figures. The class keeps
  its definition in `_internal` and is re-exported. The name keeps its
  qualifier so it never shadows matplotlib's `Figure` in a file importing
  both.
- **Every front returns `DatachartFigure` by annotation.** The chart fronts,
  `Panel`, `Grid` and `Annotate` carry it as their return type; the front
  body test checks it for every front. `Panel` and `Grid` keep accepting any
  `matplotlib.figure.Figure` as input, since the transport, not the class,
  is what they read.
- **A composition item is a setting payload.** `PanelItemSettingAttrs`
  (`figure`, `y_axis`), `GridItemSettingAttrs` (`figure`, `layout_spec`) and
  `LayoutSpecSettingAttrs` (`row`, `col`, `rowspan`, `colspan`) live in
  `datachart.typings`. ADR 0043's "one per-figure element" widens to one
  cell of a composition; no fifth suffix.
- **An optional field is `NotRequired`.** A field of a record, data,
  setting or single-chart type whose annotation admits `None` is
  `NotRequired`, so the partial literals every guide writes type-check once
  the marker ships; `EmphasisRuleAttrs` is `total=False`, since a rule is
  one of its keys. Style types stay total: a theme is a complete dict. On
  Python 3.10 `NotRequired` comes from `typing_extensions`, a dependency
  only there.
- **One usage file type-checks in CI.** Pyright runs over a test file that
  calls a front, composes with `Panel` and `Grid` (with a `layout_spec`
  item) and calls `show(interactive=True)`, as one step of the unit job.
  The package itself is not held to strict checking.

## Considered options

Exporting at the package root was rejected: the root exports only
submodules. Renaming to `Figure` was rejected: a user file importing both
would carry two names spelled alike. A `*RecordAttrs` suffix for the items
was rejected: a record is data, and `layout_spec` is not a record of
anything. A fifth `*ItemAttrs` suffix was rejected: one more rule for three
types. Strict checking of the whole package was rejected: the marker
promises the annotations exist, not that matplotlib's stubs agree with them.
A required-keys base class per type, instead of `NotRequired`, was rejected:
forty private classes to avoid a dependency that exists only on one
Python version with a month of support left.
