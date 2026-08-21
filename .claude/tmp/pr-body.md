## Summary
Revises `datachart/constants.py` per ADR 0010: `FIG_SIZE` had 21 members with only 6 ever used and suffixes that described height with width words (`A4_WIDE` was tall, `NARROW` was flat). It becomes a small A4-anchored grid, presentation sizes are added, and a constants-wide audit lands the accumulated naming and correctness fixes.

## Changes
- `FIG_SIZE` rebuilt: `A4_*` / `A4_HALF_*` widths crossed with `SHORT`/`MEDIUM`/`TALL` heights, `A4_PORTRAIT`/`A4_LANDSCAPE` pages, one `SQUARE = (4.8, 4.8)`, and new `SLIDE_16_9`, `SLIDE_4_3`, `BEAMER_16_9`, `BEAMER_4_3`; `LETTER_*`, `TALL_*`, unused squares, and the deprecated `A4` alias are removed (hard break, no aliases — pre-1.0 policy as in ADR 0009)
- `VALFMT` renamed `VALUE_FORMAT`; its `INTEGER` format fixed from `"{x:d}"` (raised `ValueError` on float values, which heatmap cells are) to `"{x:.0f}"`
- Exact duplicates dropped: `LINE_DRAW_STYLE.STEPS` (= `STEPS_PRE`), `FONT_WEIGHT.DEMI_BOLD` (= `SEMIBOLD` at weight 600)
- `HISTOGRAM_TYPE.STEPFILLED` renamed `STEP_FILLED` (value unchanged)
- `COLORS` docstring synced with the actual members (`Egypt`, `Hiroshige`, `Lake`, `Neon`, `OkabeIto`, `OkabeIto_Black`) and `GnBu` re-filed as sequential multi-hue
- Docs notebooks migrated to the new names, including the heatmap guide's format table that recommended the broken `"{x:d}"`
- ADR 0010 records the redesign; CONTEXT.md gains a "Figure size grid" glossary entry

## Test plan
- `python -m unittest discover test` → 86/86 OK
- Smoke test: `Heatmap(..., valfmt=VALUE_FORMAT.INTEGER)` on float data draws without error (previously `ValueError`); removed names asserted absent
- Repo-wide grep for every removed/renamed name → zero stale references outside ADR prose
- Notebook tests not run locally — the uv kernel imports the main-checkout editable install, so they exercise the wrong code from a worktree; covered by CI
