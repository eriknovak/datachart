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
explicit — matplotlib's stock `Figure.show()` raises on unmanaged figures,
so the subclass overrides it: in notebooks it displays the figure inline; in
scripts it adopts the figure into a pyplot manager and opens the GUI window.
Unmanaged figures also never trigger IPython's matplotlib integration (that
only activates when a pyplot API runs in the kernel), so the subclass carries
`_repr_png_` — inline display works with no pyplot call anywhere.

## Commitments

- **No datachart seam creates a pyplot-managed figure.** All three creation
  sites construct the subclass directly; rendering N charts registers
  nothing in pyplot's figure manager (pinned by a regression test).
- **Nothing shows implicitly.** Notebook display is by last expression,
  `display(fig)`, or `fig.show()`; script display is `fig.show()` only.
- **`plt.close(fig)` stays a harmless no-op** on datachart figures, so
  existing user cleanup code keeps working.
- **The subclass is invisible surface.** It passes every
  `isinstance(fig, plt.Figure)` check and adds only `show()` and the
  `_repr_png_` display hook; composition fronts keep consuming the metadata
  transport unchanged.
- **Golden parity must hold** — the move changes lifecycle, not pixels.

## Considered options

Closing figures in bulk callers (gallery, harness) was rejected: it patches
datachart's own scripts while every downstream bulk user keeps the leak.
Suppressing the warning via `figure.max_open_warning` was rejected: it hides
the retention without fixing it. A module-level `datachart.utils.show(fig)`
function instead of the subclass was rejected: matplotlib users instinctively
call `fig.show()`, which would keep failing with a misleading error.
