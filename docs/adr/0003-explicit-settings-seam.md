---
status: accepted
---

# Chart fronts pass explicit settings; the attrs dict is retired

Every chart front packs its ~30 keyword arguments into one attrs dict
(`build_attrs_dict`) that `render_chart` immediately unpacks again through
three bookkeeping tables (`settings_attr_mapping`, `settings_chart_mapping`,
`SUPPORTED_SETTINGS`) plus `get_settings`/`assert_chart_settings`. Since the
transport slimming, the attrs dict has exactly one consumer — `render_chart` —
and the `SUPPORTED_SETTINGS` warnings are unreachable from the public API
because each front's fixed signature already forbids unsupported flags. The
hop is a pure middle-man: parameters are named in the signature, forwarded
into a dict, then re-extracted against a defaults table.

We retire it: fronts call `render_chart(chart_type, charts, settings)` with
the charts structure and an explicit settings dict. No behavior change —
golden parity must hold.

## Commitments

- **`render_chart` stays the single assembly point** for subplot layout,
  panel construction, and the metadata transport. Fronts do not build layers.
- **The front signatures are the allowlist.** `build_attrs_dict`,
  `get_settings`, `assert_chart_settings`, and all three mapping tables are
  deleted. A chart supports a setting iff its front names the parameter.
- **Defaults apply at the point of use**: `figsize=FIG_SIZE.DEFAULT` and
  `max_cols=4` inside `render_chart`, `aspect_ratio=AUTO` where the panel
  settings are built (`build_chart_panel_settings`). Public
  signatures keep `None` = "resolve downstream"; no promotion into signature
  defaults.
- **Signatures stay explicit and per-front.** The ~20 common parameters
  repeated across the 7 fronts are declarative API surface, kept; only the
  body forwarding is deduplicated (each parameter forwarded once). No
  `**kwargs` machinery.
- **`ChartAttrs` and the 7 `*ChartAttrs` TypedDicts are deprecated**, not
  removed: a module `__getattr__` in `datachart/typings.py` emits
  `DeprecationWarning` for one release (the `OverlayChart` precedent). The
  `*SingleChartAttrs` chart-dict types stay untouched. Docs repoint: notebook
  "for more details" links and `references/typings.md` entries move to the
  chart-function reference (`references/charts.md`).

## Considered options

Having fronts build layers directly (retiring `render_chart` down to a figure
helper) was rejected: it would spread subplot/transport logic across 7 files.
Keeping the attrs dict but inlining `get_settings` was rejected as preserving
the middle-man. Shared `**common_kwargs` for the repeated parameters was
rejected: it destroys IDE discoverability and per-chart typing.
