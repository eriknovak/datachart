---
status: accepted
---

# Text annotations ride the layer, with a post-hoc Annotate front

Charts need explanatory text tied to the data — naming a model's line,
explaining an outlier bar, calling out the highlighted series. Matplotlib's
`annotate` exists, but calling it on a returned figure bypasses the metadata
transport: the text is lost the moment the figure is composed with `Panel` or
`Grid`, and it cannot follow themes. We make texts a first-class chart
attribute on the reference-line seam.

## Commitments

- **Declared with the chart.** Every chart front gains a `texts` parameter
  (`TextAttrs` or a list; list-of-lists indexes per subplot chart, exactly as
  `vlines`/`hlines`). Texts are stored on the `Layer` with style resolved at
  build time, and drawn by the panel after scales and limits are applied —
  the reference-line slot — so they survive `Panel` and `Grid` composition.
- **`TextAttrs` is flat and small.** `text` (required), `x`/`y` (text
  position), `coords` (`"data"` default, `"axes"` for figure-stable notes),
  `target` (optional `(x, y)` arrow target, always data coordinates), and
  `style` (per-text override). Alignment (`ha`/`va`) is presentation and
  lives in style, not placement. One target per text; several arrows means
  several texts.
- **A post-hoc front for finished figures.** `Annotate(figure, texts=...)`
  returns a new figure by appending a carrier text layer — kind `"text"`, no
  data, excluded from legend, color cycle, and orientation/projection
  inference — to the figure's panel. It works on any single-coordinate-space
  figure, including `Panel` output, and rejects grid figures: annotate the
  sources before composing. It never mutates an existing layer, preserving
  the chart-hash → color invariant.
- **One text-styling vocabulary.** A `plot_text_*` family (font, box face and
  edge, arrow color/width/style) joins every theme, with box and arrow each
  hideable. The half-implemented `plot_text_color` and
  `plot_annotation_fontsize` reads (scatter correlation box) are absorbed
  into the family; no parallel key names survive.
- **Defaults were chosen visually.** From rendered side-by-side variants:
  the connector is a curved plain line (no arrowhead, `arc3` curvature 0.2),
  the box is rounded with a white fill and a thin light edge. Every rejected
  variant stays reachable through the style keys.
- **The connector is themed, like every mark.** Each theme sets
  `plot_text_arrow_color` (and box colors) to values visible against its own
  grounds and palette — the arrow never disappears when the theme changes.
- **`ARROW_STYLE` names complete connector looks.** A constant beside
  `LINE_STYLE`: `CURVE` (curved plain line with a small text-side gap; the
  base default), `CURVE_ARROW` (the same curve with an arrowhead),
  `TOUCHING` (straight plain line starting flush at the box border — the
  connector is clipped at the box patch, it never crosses it), `ARROW`
  (straight line with an arrowhead). A preset expands to arrow style,
  curvature, and gap; individual `plot_text_arrow_*` keys override single
  properties. The docs guide shows the variants image.
- **The connector places itself.** Where it starts and which way it bows are
  decided at draw time, when the panel holds every layer's data and the final
  limits: the connector leaves the box from the border point facing the
  target; a curved look left on its default tries several bows to either side
  and keeps the flattest arc whose body clears the data (the final approach
  is exempt — the target sits on the data); a connector shorter than its own
  gaps straightens with minimal gaps, then disappears entirely. An explicit
  `plot_text_arrow_curve` pins the bow — side and depth — exactly.
