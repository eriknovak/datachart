---
status: accepted
---

# Nested grids render in the parent gridspec, with a reserved heading row

ADR 0006 rendered a nested grid as a matplotlib subfigure so its title could be
a local suptitle. A subfigure runs its own constrained-layout pass, so the
nested axes drift from sibling cells' axes — tops and bottoms visibly misalign.
We replace the subfigure with a nested gridspec in the parent figure — the
mechanism multi-subplot chart figures already use in Grid cells, which is why
those already align — so one layout pass aligns every cell.

## Commitments

- **Envelope alignment.** A nested grid's axes envelope meets its siblings':
  first-row tops and last-row bottoms line up with sibling cells' axes.
  Internal row splits remain the nested grid's own business; rows of unrelated
  nested grids are not aligned to each other.
- **The title costs one heading row.** A titled nested grid reserves a thin
  extra gridspec row and renders the title there in the `subtitle` text style
  (demoted from `title` — inside a composition it is a section heading, not
  the figure's). Bottom/left/right still align exactly; the top edge sits
  lower by the thin reserved heading row only when a title exists. An untitled
  nested grid aligns exactly on all four sides — the heading row is never
  reserved for it. This keeps ADR 0006's furniture preservation.
- **One rendering mechanism for nested cells.** Nested grids and multi-subplot
  figures both rebuild via subgridspec in the owner figure; the subfigure path
  is deleted. The transport (recursive cell tree) is unchanged.
- **Golden churn is the fix.** Nested-grid golden images change and are
  re-baselined deliberately; all non-nested cases stay pixel-identical.
