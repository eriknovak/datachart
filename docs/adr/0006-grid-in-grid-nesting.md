---
status: accepted
---

# Grid figures nest inside Grid via a recursive cell-tree transport

ADR 0002 shipped Grid with `{"type": "grid"}` as its whole transport — no
panel, so grid figures were rejected everywhere and Grid-in-Grid stayed open.
We close it: a Grid figure placed in a Grid cell occupies that one cell and
rebuilds its internal layout inside it with a subgridspec — the same mechanism
multi-subplot chart figures already use. `Grid([fig_grid, fig4])` and the
nested-rows form both accept grid figures; `Panel` still rejects them.

## Commitments

- **Subgrid-in-cell semantics.** A nested grid never flattens into the parent's
  layout; it is one cell whose interior is the nested grid's own cell tree.
  Nesting composes to any depth — the transport is recursive and so is the
  render.
- **The transport becomes a cell tree.** Grid figures carry
  `{"type": "grid", "cells": [...], ...}` plus the grid-level settings
  composition consumes (title, sharex/sharey, layout shape). Each cell node
  holds its layout spec and one of: a panel, subplot panels + shape, or a
  nested grid node. This supersedes ADR 0002's "grid figures cannot be
  composed further" — but only for Grid; Grid-in-Panel remains an error.
- **Nested furniture is preserved, not merged.** A nested grid keeps its own
  title (rendered as a heading spanning its subgrid) and its own
  sharex/sharey among its own cells. The parent's sharex/sharey applies only
  to its top-level cells; sharing never crosses a nesting boundary.
- **Uniform cells, no auto-weighting.** A nested grid gets exactly one cell,
  the same size as any sibling — its content renders denser. Layout intent
  stays with the user (nested rows, `layout_spec`, `figsize`).
- **The auto-figsize heuristic is unchanged**: cell size comes from the first
  figure's actual size, so a large grid figure propagates its size as the
  per-cell base. Explicit `figsize` is the escape hatch.
- **Deprecated fronts inherit nesting silently** (`FigureGridLayout`,
  `figure_grid_layout`) through the shared implementation.
- **Verified by equivalence and pixels**: unit tests pin the recursive
  transport, the still-rejected Grid-in-Panel case, and the already-working
  `Grid([Panel(...), fig])`; golden cases pin nested-grid rendering.
