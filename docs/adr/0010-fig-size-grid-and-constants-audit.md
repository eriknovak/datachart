---
status: accepted
---

# FIG_SIZE becomes a small A4-anchored grid; constants audit fixes

`FIG_SIZE` grew to 21 members, of which only 6 were ever used, and its
suffixes described *height* with *width* words: `A4_WIDE` (8.2×7.2) is not
wide but tall, `NARROW` meant flat. The `LETTER_*` and `TALL_*` families and
most `A4_HALF_*` variants had zero uses in the package, tests, or docs.

We rebuild `FIG_SIZE` around the sizes the package is actually for — paper
figures anchored to the printable area of an A4 page — plus presentation
frames. The grid names carry no paper-format prefix: the A4 anchor is
documentation (the docstring states the reference and each size in inches
and cm), not naming. Sizes respect print margins: the reference is A4 with
standard 2.5 cm margins (a 6.3 × 9.7 in text block), not the physical sheet,
and half-width figures account for a 0.3 in column gap.

- **Width axis**: `FULL_*` (6.3 in, the text-block width) and `HALF_*`
  (3.0 in, one of two columns separated by the gap).
- **Height axis**: `SHORT` (2.4), `MEDIUM` (4.8), `TALL` (7.2) — height
  words for heights, replacing `NARROW`/`REGULAR`/`WIDE`.
- **Printable pages**: `A4_PORTRAIT = (6.3, 9.7)`, `A4_LANDSCAPE =
  (9.7, 6.3)` — the printable area, not the 8.27 × 11.69 in sheet.
- **Squares**: `SQUARE = (4.8, 4.8)` (the only square size ever used) and
  `HALF_SQUARE = (3.0, 3.0)` (a square filling one column);
  `SQUARE_SMALL`/`SQUARE_LARGE` are removed.
- **Presentation**: both families — `SLIDE_16_9 = (13.33, 7.5)` and
  `SLIDE_4_3 = (10.0, 7.5)` (PowerPoint/Google-scale, where slides are
  actually made) and `BEAMER_16_9 = (6.3, 3.54)`, `BEAMER_4_3 =
  (5.04, 3.78)` (LaTeX frame sizes, legible at matplotlib's default fonts).
- `DEFAULT = (6.4, 4.8)` stays.

Old names are removed, not aliased — pre-1.0, no known external users, and a
`DeprecationWarning` on a plain tuple attribute would need metaclass
machinery (same policy as the ADR 0009 theme renames). Docs and notebooks
migrate in the same change.

The same audit lands the smaller fixes: `VALFMT` is renamed `VALUE_FORMAT`
(opaque abbreviation) and its `INTEGER` format becomes `"{x:.0f}"` — the old
`"{x:d}"` raised `ValueError` on float values, which heatmap cells are;
`HISTOGRAM_TYPE.STEPFILLED` becomes `STEP_FILLED` (value unchanged); exact
duplicates are dropped (`LINE_DRAW_STYLE.STEPS` = `STEPS_PRE`,
`FONT_WEIGHT.DEMI_BOLD` = `SEMIBOLD` at weight 600, the deprecated
`FIG_SIZE.A4` alias); `FONT_WEIGHT.ULTRA_HEAVY` is removed because its
value `"ultrabold"` is not a matplotlib weight and raised `ValueError`; the `COLORS` docstring is synced with the actual
members and `GnBu` re-filed as sequential. The `DEFAULT` member every class
carries stays: it documents what you get when you don't ask.

## Considered options

- **A4-prefixed grid names** (`A4_SHORT`, `A4_HALF_SHORT`, …). Rejected: the
  prefix names the reference, not the size — `FULL`/`HALF` say what the
  figure occupies, and the A4 anchor lives in the docstring with concrete
  in/cm dimensions.
- **Purpose-named sizes** (`PAPER_FULL_WIDTH`, `BANNER`, …). Rejected:
  longer names for the same information as the `FULL`/`HALF` axis.
- **Deprecation aliases for one release.** Rejected: metaclass machinery for
  a pre-1.0 package with no external users.
- **Keep `LETTER_*` for US users.** Rejected: zero uses anywhere; a Letter
  text block is close enough to A4 that the grid serves both.
- **Beamer-only slide sizes.** Rejected: presentations are mostly made in
  PowerPoint/Google Slides; beamer frames kept alongside as the
  LaTeX-native anchor.
- **Full-sheet anchoring** (the former 8.2 in width, nearly the physical A4
  width). Rejected: printed figures live inside margins; a "full-width"
  figure sized to the sheet gets scaled down or clipped in every real
  document.
