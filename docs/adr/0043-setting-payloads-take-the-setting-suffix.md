---
status: accepted
amended-by: [0067, 0072]
---

# Every setting payload takes the `*SettingAttrs` suffix, old names warn for one release

ADR 0034 reserved `*SettingAttrs` for the per-figure settings a caller passes
to a front and deferred renaming the existing peers; ADR 0035 renamed the
colorbar type but kept its old name as a silent alias. The rest still read
as something else: `VLinePlotAttrs` like a chart type, `TextAttrs` one word
from the theme-side `TextStyleAttrs`. The reference bands added by ADR 0036
copied the `*PlotAttrs` pattern before shipping (issue #138).

## Commitments

- **Six types carry the suffix:** `VLineSettingAttrs`, `HLineSettingAttrs`,
  `VSpanSettingAttrs`, `HSpanSettingAttrs`, `TextSettingAttrs`, joining
  `LegendSettingAttrs` and `ColorbarSettingAttrs`. Fields are unchanged.
- **Released names warn; unreleased names just go.** `VLinePlotAttrs`,
  `HLinePlotAttrs`, `TextAttrs`, and `HeatmapColorbarAttrs` shipped in 0.9.1,
  so a module `__getattr__` in `datachart/typings.py` resolves them from one
  `_DEPRECATED_ALIASES` table with a `DeprecationWarning` — the ADR 0003
  mechanism. `VSpanPlotAttrs` and `HSpanPlotAttrs` never shipped and get no
  alias.
- **`HeatmapColorbarAttrs` joins the table.** A silent alias has no end; one
  rule for every old name is simpler than two.
- **Aliases are removed one release after they land.** The release checklist
  in `CLAUDE.md` carries the reminder, since that is where a release is
  prepared.

## Considered options

**Renaming only the four types the issue named** was rejected: the band types
would need their own deprecation cycle the moment they shipped.

**Keeping the old names as permanent aliases** was rejected: two names for
one type split the docs and search results for no gain once callers have had
a release to move.
