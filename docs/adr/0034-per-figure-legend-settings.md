---
status: accepted
---

# The legend is a per-figure setting, and outside locations expand to two matplotlib arguments

Legend appearance is theme-only. The seven `plot_legend_*` attributes are
collected once into the panel's legend style, and no front takes a legend
argument, so a single figure that wants its legend somewhere else has to reach
for a global `config.update_config` call and put it back afterwards. The legend
title is not settable at all — it is the literal string `"Legend"` at the point
the panel draws it. There is no column count, so a six-series legend stacks six
rows deep into the marks it is meant to explain.

We make the legend a per-figure setting, and in doing so spend a property
`LEGEND_LOCATION` has held since it was introduced: that every member is a
matplotlib location string passed straight through.

## Commitments

- **Every front that has `show_legend` takes `legend`**, and so does the
  `Panel` composition front. The payload is `LegendSettingAttrs` —
  `title`, `location`, `ncols`, `alignment` — and `None` in any field falls
  back to the theme, the same resolution ADR 0003 fixed for every other
  setting. Nothing about the legend becomes settable that a theme cannot also
  set: `plot_legend_title` and `plot_legend_ncols` join the existing five.
- **The default title stays `"Legend"`**, now as a theme value rather than a
  literal. An empty string means no title. A `None` default would have been
  the cleaner design and was rejected on cost: it repaints every existing
  figure and every golden baseline for a cosmetic preference.
- **`LEGEND_LOCATION` gains four outside members**, one per edge, and they are
  not pass-throughs. Each expands into a matplotlib location plus an anchor at
  the point legend style is resolved. The anchor is never public: no front, no
  theme key, and no constant exposes `bbox_to_anchor`. The side placements
  anchor to the top edge rather than centering, which is both the common case
  and what bare panels already do.
- **The expansion happens once, where legend style is resolved**, so a theme
  key and a per-chart setting produce identical results and neither the fronts
  nor the panel learn about anchors.
- **A user-supplied location wins over the bare-panel pin.** Charts whose marks
  fill the axes — treemap, sankey, network — currently force the legend beside
  the plot. That stays the default and stops being unconditional; a caller who
  names a location gets it.
- **Subplot layouts keep suppressing the legend**, silently. `show_legend`
  already behaves this way, and a warning would fire on figures the user never
  asked to change.
- **New setting-level TypedDicts take the `*SettingAttrs` suffix.** The
  codebase already reserves `*StyleAttrs` for the `plot_*` theme keys and
  `*SingleChartAttrs` for data payloads; the per-figure settings passed to
  fronts have no suffix of their own, so `LegendSettingAttrs` establishes one.
  The four existing peers — the vertical and horizontal reference line
  attributes, the text annotation attributes, and the heatmap colorbar
  attributes — keep their names here. Renaming public types needs a
  deprecation window and touches the reference docs, which is its own change,
  not a rider on this one.

## Considered options

**Exposing `bbox_to_anchor` on the public surface** was rejected. It puts
matplotlib's coordinate system into a settings vocabulary that is otherwise
named constants, and it is not usable alone: an anchor only means something
paired with the right location, so the caller would have to know both halves of
a convention we would then have to document.

**A figure-level legend via matplotlib's own `outside` locations** was
rejected. Those work only on figure legends, while a datachart legend belongs
to a panel's axes — which is what lets a grid cell carry its own. Moving to a
figure legend to gain outside placement would cost composition.

**Leaving outside placement out entirely**, so the four members never exist,
was rejected: placing the legend outside the marks is the single most common
reason to want per-figure control, and the internal bare-panel pin already
proves the anchor arithmetic works.
