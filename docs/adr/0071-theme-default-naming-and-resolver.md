---
status: accepted
---

# A theme default is named for its parameter and read through one resolver

A theme-level default for a front parameter lived under two prefixes:
`chart_default_show_grid`, `chart_default_show_values` and
`chart_default_node_label_position`, but `plot_calendar_heatmap_week_start`
and `plot_ridgeline_overlap` under the `plot_<chart>_` prefix that otherwise
names a mark's look (issue #279). `chart_default_node_label_position` named
neither the parameter nor the chart, though two fronts take a
`label_position`. Each default was read at its own site, and the calendar and
ridgeline defaults were read through the per-chart style dict, so
`style={"plot_ridgeline_overlap": ...}` was a second way to say what
`overlap=` says.

## Commitments

- **One naming rule, mirroring ADR 0052.** A theme default for a parameter
  several fronts take is `chart_default_<parameter>`; one a single front owns
  is `chart_default_<chart>_<parameter>`, with the chart named as in its style
  keys. A mark's look stays `plot_<chart>_<key>`. The set is `show_grid`,
  `show_values`, `chart_default_calendar_heatmap_week_start`,
  `chart_default_ridgeline_overlap` and `chart_default_network_label_position`;
  it does not grow here (ADR 0004).
- **The descriptor says which parameters have one.** `ChartKind.theme_defaults`
  maps a front's own parameter to its key; `SharedParameter.theme_default`
  names a shared parameter's. A test checks every key against the rule and
  that no other `chart_default_` key exists in the base theme.
- **One resolver.** `theme_default(chart_type, settings, name)` returns the
  setting when not `None`, else the theme's value for the descriptor's key,
  else `None`. Each caller keeps its own post-processing — the value-axis grid
  swap and the explicit-grid flag of ADR 0015, `bool()` for value labels, a
  constant's `DEFAULT` — because `overlap` has no constant and a `None`
  `show_grid` means something. Nothing else reads a `chart_default_` key.
- **Theme defaults come from the config only.** A per-chart style dict no
  longer sets `week_start` or `overlap`.
- **Renamed keys warn for one release.** The old names are `STYLE_ALIASES`
  entries; `canonical_style` warns with `DeprecationWarning` on every write
  path, while `config[...]` and `config.get(...)` reads stay silent. The
  release checklist removes an alias that already shipped.

## Considered options

- **A slug derived from the row name** (`chart_default_ridgelineplot_overlap`).
  Rejected: the row names are not the chart names users see in style keys.
- **Filling theme defaults into the settings in `render()`.** Rejected: a
  polar panel must tell an explicit `show_grid` from a theme one (ADR 0015),
  and `Panel` resolves the grid without a front.
- **The resolver owning the constant `DEFAULT`.** Rejected: not every
  parameter has a constant, and `show_grid`'s `None` is meaningful.
