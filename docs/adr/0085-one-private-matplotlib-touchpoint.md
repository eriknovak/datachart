---
status: accepted
---

# One private matplotlib touchpoint, guarded and locked, never a version cap

datachart reads four private matplotlib names while `pyproject.toml` says
`matplotlib>=3.8` with no upper bound (issue #319): `ax._shared_axes` at
three sites, `legend._get_anchored_bbox` at one, `gs._subplot_spec` at three,
and `NestedGridLayoutEngine` swapping the module-level
`_constrained_layout.make_layout_margins` for the duration of a layout pass
(ADR 0007's margin lift). Any of them can vanish in a matplotlib minor
release and break every install; the module swap also races when two threads
lay out figures at once.

## Commitments

- **Three of the four go.** The shared-axes grouper is read through the
  public `Axes.get_shared_x_axes()` / `get_shared_y_axes()`. The legend
  anchor is computed by datachart from public inputs — `Legend.codes`,
  `legend.borderaxespad`, `legend.prop.get_size_in_points()` — in one small
  function that places a box inside a parent box by location code with
  padding. A nested gridspec's parent cell is recorded by datachart when it
  creates the subgridspec, in a map on the owner figure, and both the margin
  lift and the column-window helper read that map; matplotlib is never
  asked for a gridspec's parent.
- **The margin lift stays, contained.** No public hook exists inside
  constrained layout, and vendoring `do_constrained_layout` would triple the
  private surface. The swap is guarded by a module-level `threading.Lock`,
  and an import-time check confirms `make_layout_margins` exists with the
  expected signature. When it does not, `new_figure` builds a plain
  `ConstrainedLayoutEngine` and warns once that a nested grid alone in a
  host row may shrink (issue #86's cosmetic case). Layout degrades; nothing
  raises. This amends ADR 0007, whose lift now has a fallback.
- **No upper bound on matplotlib.** An upper cap fails `pip install
  datachart` for every user the day a new matplotlib minor ships, and the
  resolver cannot route around it. The guard above plus the pre-release job
  below are the protection; `matplotlib>=3.8` stays as is.
- **A pre-release CI job is the early warning.** `unittests.yaml` gains a
  `matplotlib-pre` job that installs `--pre` matplotlib over the synced
  environment and runs the unit tests with `continue-on-error: true`, on
  every push and pull request and on a weekly schedule, so a breaking
  pre-release shows on the PR that would meet it and in a quiet week alike.
- **Three tests pin the behaviours at risk.** A nested grid alone in a host
  row keeps its siblings' axes height (#86, measured on axes positions);
  with the private hook patched away, `new_figure` returns a plain-engine
  figure with one warning and no exception; two threads laying out
  concurrently both leave the original function in place. The nested-grid
  goldens cover the parent-cell map and the column window.

## Considered options

Capping at the next untested minor was rejected: it trades a cosmetic
layout case for an install failure. Vendoring the constrained-layout loop
was rejected: it depends on the private layout-grid module wholesale.
Dropping the margin lift was rejected: it reopens #86. A coverage
percentage target for `figures.py` was rejected: it would pull in display
and hover code that no matplotlib change threatens.
