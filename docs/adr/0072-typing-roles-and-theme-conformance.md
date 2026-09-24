---
status: accepted
---

# Every public typing carries one of four role suffixes, and the theme keys are the style types

`datachart.typings` spelled "one input record" six ways: `*DataPointAttrs`,
`*RecordAttrs`, and the bare `SankeyLinkAttrs`, `NetworkNodeAttrs`,
`NetworkEdgeAttrs`, `GanttTaskAttrs`. Twenty-two `*SingleChartAttrs` existed,
and only the three the Sankey, Treemap and Network fronts take as `data=`
were reachable from any signature. The theme and the types disagreed both
ways: `BarStyleAttrs` declared three `plot_bar_value_*` keys that are only
`STYLE_ALIASES`, while the eleven `overlay_*` keys of the base theme were in
no TypedDict. `plot_xticks_label_rotate` and `plot_yticks_label_rotate` were
declared in four style types, set in the base theme, and read by nothing
(issue #277).

## Commitments

- **Four roles, four suffixes.** A public TypedDict in `datachart.typings`
  ends in one of `RecordAttrs` (one input record of a record front),
  `DataAttrs` (one non-record dataset of a `dict_data` front: a grid, an
  image, a feature set), `StyleAttrs` (a theme key group), or `SettingAttrs`
  (a setting payload, ADR 0043). The record suffix follows the chart kind's
  record shape (ADR 0069); a type never decides what the row declares.
- **The three reachable `*SingleChartAttrs` stay.** They are the one-chart
  dict the Sankey, Treemap and Network fronts take, a shape no other front
  has. The nineteen no front takes are removed.
- **Old names warn for one release.** Every renamed record type and every
  removed single-chart type is a `_DEPRECATED_ALIASES` entry, the ADR 0043
  mechanism; a removed type keeps a private `_<old>` so the alias resolves.
  `ImageDataAttrs` and `BasemapDataAttrs` never shipped and need none.
- **The base theme is the style types, by test.** Every base-theme key is
  declared by exactly one `*StyleAttrs` class's own annotations, and every
  such key is in the base theme. The `overlay_*` keys form
  `OverlayStyleAttrs`; the `plot_bar_value_*` aliases leave `BarStyleAttrs`
  (their canonical `plot_value_*` keys live in `ValueLabelStyleAttrs`); a
  key declared by several groups is declared once.
- **Tick-label rotation is axes furniture that works.** The rotation keys
  are `axes_xticks_label_rotate` and `axes_yticks_label_rotate` in
  `AxesStyleAttrs`, the old `plot_*` names are `STYLE_ALIASES` entries, and
  `Panel` applies a set value through the same furniture pass that applies
  tick length and label size. The default stays `None`, so no figure changes.
- **`font_subtitle_style` and `font_subtitle_weight` accept `str`** like
  every sibling font key.

## Considered options

- **Giving the three reachable `*SingleChartAttrs` a role suffix.** Rejected:
  none of the four roles is "one chart's whole `data` dict", and reshaping
  those fronts to take records is a separate decision.
- **Retiring the rotation keys instead of wiring them.** Rejected: a theme
  key should do what its name says, and the theme layer has no "removed key"
  alias form; wiring them is one `tick_params` call at a seam that exists.
- **Renaming the rotation keys without a reader.** Rejected: a cleaner name
  for a silent knob.
