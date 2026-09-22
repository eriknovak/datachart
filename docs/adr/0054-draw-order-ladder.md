---
status: accepted
---

# Draw order is a fixed ladder: surfaces at the bottom, reference lines near the top

Issues #194 and #180 showed filled layers covering what should read over
them. Stacked area bands and filled contours draw at zorder 3, while
reference lines landed on matplotlib's `LineCollection` default of 2 and the
lines of a `Panel` overlay sit at 2. A band or contour therefore hid both.
The workaround was a per-figure `plot_area_zorder` style.

The package already fixes most zorders in code: ADR 0036 made the band
zorder the one theme key, and the Panel overlay table gives bars and
histograms 1 and lines and scatter 2. This ADR names the whole ladder so the
next layer lands on a known rung.

## Commitments

- **The ladder, bottom to top:**

  | zorder | what |
  | --- | --- |
  | 0.25 | an image placed below (`IMAGE_ZORDER`, ADR 0060) |
  | 0.5 | gridlines (`set_axisbelow(True)`) |
  | 1 | overlay surfaces, bars, histograms (Panel table) |
  | 1.75 | reference bands (`plot_{v,h}span_zorder`, ADR 0036) |
  | 2 | overlay lines, scatter, and contour lines (Panel table) |
  | 3 | standalone marks (`plot_*_zorder` theme defaults) |
  | 3.25 | an image placed above (`IMAGE_ZORDER`, ADR 0060) |
  | 3.5 | reference lines (`REF_LINE_ZORDER`) |
  | 5 | annotations (`TEXT_ANNOTATION_ZORDER`) |
  | 100 | spines (`axes_spines_zorder`) |

- **A surface is a layer flag, not a chart kind.** `Layer.surface` marks a
  filled layer that reads as background: stacked area bands, hexbin tiles,
  and a contour when `filled`. The overlay lookup reads the layer's
  `zorder_key`: `"surface"` before its `kind`, so one contour class draws at 1
  when filled and at 2 as lines; an image names its position instead
  (ADR 0060).
- **Surfaces sit at the bottom of an overlay.** A surface covers its whole
  area, so anything under it disappears. ADR 0024 already promised that
  lines, scatter, or contours can sit on top of a hexbin. At 1, a surface
  shares its rung with bars and histograms, and a reference band still
  shades over it.
- **Reference lines are a computed constant, not a theme key.** A reference
  line marks a threshold on top of the data, so it sits above every mark
  default (3) and below annotations (5). ADR 0036 made the band zorder a
  theme key because moving a band in front of the data is a real need; no
  such need exists for a line, which is already on top.
- **Standalone defaults stay.** `plot_area_zorder` and `plot_contour_zorder`
  stay 3; outside an overlay nothing else competes with them except the
  reference lines, which sit above them. An explicit `z_order` per figure
  in `Panel` still beats the table.

## Considered options

**Theme keys for the overlay surface rung** (`overlay_default_zorder_surface`)
were rejected. The existing `overlay_default_zorder_*` keys are theme keys,
but no theme sets a different value, and each new key widens the theme
contract ADR 0036 kept to one zorder.

**Dropping the standalone `plot_area_zorder` and `plot_contour_zorder` to 1**
was rejected. It fixes the reference lines only by accident, and it would
move every themed figure that sets those keys.
