---
status: accepted
---

# Figures are unmanaged; showing is explicit via `Figure.show()`

Every figure datachart creates goes through pyplot (`plt.subplots` /
`plt.figure`) at three seams: `render_chart`, the Panel overlay
implementation, and the Grid layout implementation. Pyplot registers each
figure in its global manager and retains it until explicitly closed, so any
caller rendering many charts — the theme gallery, the golden harness, user
batch scripts — leaks memory and trips the "More than 20 figures have been
opened" RuntimeWarning unless it remembers to `plt.close`.

We move all three seams off pyplot: figures are constructed directly as a
`matplotlib.figure.Figure` subclass with `layout="constrained"`. Unmanaged
figures are owned by the caller and garbage-collected normally; no cleanup
call is needed and the warning cannot occur.

The trade-off is display: pyplot no longer auto-shows figures at notebook
cell end, and `plt.show()` in scripts does not see them. Displaying becomes
explicit, and `show()` is the only way a figure appears — matplotlib's stock
`Figure.show()` raises on unmanaged figures, so the subclass overrides it: in
notebooks it displays the figure inline as a raw PNG payload (needing no
pyplot call, repr hook, or IPython matplotlib integration — and therefore
unable to display twice); in scripts it adopts the figure into a pyplot
manager and opens the GUI window. The subclass deliberately carries no
`_repr_png_`: a bare figure at cell end, or `display(figure)`, renders only
a text repr, so which figures appear is always the author's explicit choice.

## Commitments

- **No datachart seam creates a pyplot-managed figure.** All three creation
  sites construct the subclass directly; rendering N charts registers
  nothing in pyplot's figure manager (pinned by a regression test).
- **Nothing shows without `show()`.** In notebooks and scripts alike,
  `fig.show()` is the single display affordance; bare expressions and
  `display(fig)` render text, never the chart. Composition docs show only
  the composed figure — source figures feeding a Panel/Grid are not shown.
- **`plt.close(fig)` stays a harmless no-op** on datachart figures, so
  existing user cleanup code keeps working.
- **The subclass is invisible surface.** It passes every
  `isinstance(fig, plt.Figure)` check and adds only `show()`; composition
  fronts keep consuming the metadata transport unchanged.
- **Golden parity must hold** — the move changes lifecycle, not pixels.

## Considered options

Closing figures in bulk callers (gallery, harness) was rejected: it patches
datachart's own scripts while every downstream bulk user keeps the leak.
Suppressing the warning via `figure.max_open_warning` was rejected: it hides
the retention without fixing it. A module-level `datachart.utils.show(fig)`
function instead of the subclass was rejected: matplotlib users instinctively
call `fig.show()`, which would keep failing with a misleading error.
