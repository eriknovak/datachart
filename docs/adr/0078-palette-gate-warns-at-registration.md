---
status: accepted
---

# The palette gate warns when a theme is registered, not when one is derived

ADR 0073 made both write paths warn on a failing palette. Of the forty-nine
`COLORS` leads, every categorical one fails the deutan and protan floor of
ΔE 8 (`Dark2` and `Set2` at 0, `Tab10` at 0.7, `OkabeIto` at 1.9), so
`derive_theme` warned on every categorical lead a reader tried, and the
themes guide printed the warning under its own examples (issue #297). A
derived theme is usually an experiment, one `config.override` block long;
a warning on every attempt is noise, and noise teaches readers to filter the
warning where it matters.

## Commitments

- **`derive_theme` never warns.** It builds the theme it was asked for, a
  categorical lead included, and stays silent about the score. The score is
  one call away in `score_palette`, and the gallery reports it for every
  shipped theme.
- **`register_theme` still warns on a `fail` verdict.** Registering names a
  theme for reuse, which is the moment of commitment ADR 0073 wanted the
  warning at, and it stays the one place the gate speaks. This amends ADR
  0073's "the write paths warn" to one write path.

## Considered options

- **Warn once per palette per session.** Rejected: the first `Dark2` still
  prints, and a seen-set is state the themes module otherwise does not keep.
- **Drop the gate warning everywhere.** Rejected: ADR 0073 chose a warning
  over an error so a brand palette can still ship; silence at registration
  would drop the one moment a defect is heard at all.
- **Gate `derive_theme` behind a keyword.** Rejected: a knob for a warning is
  a knob nobody sets, and the default would still be one of the two above.
