## Summary
Kernel density estimation lands as two `stats` functions instead of a `KDEChart` front: `kde2d(x, y)` returns the `{x, y, z}` dict `ContourChart` already draws, and `kde1d(values)` returns the `{x, y}` points `LineChart` draws over a density `Histogram` in a `Panel`. Every rendering concern (lines, fills, colorbar, area fill) is already covered by existing fronts, so a new chart would only wrap them.

## Changes
- `stats.kde1d` / `stats.kde2d` (`matplotlib.mlab.GaussianKDE`, no new dependency) with `bandwidth` (a `BANDWIDTH` rule or scalar factor, as violins take), `gridsize`, and `cut` — the grid extends `cut` bandwidths past the data so the estimate tails off instead of being clipped.
- New `utils/_internal/validate.py` gathers the value validators: `validate_bandwidth` (shared by `kde1d`/`kde2d`, `ViolinPlot`, `RaincloudPlot`) and `validate_emphasis` (moved out of `layers.py`).
- Contour guide: the penguin `species_density` surfaces now come from `kde2d` instead of scipy; new "Density of scattered points" section and quick-reference row.
- Histogram guide: new "Density curve" section (density `Histogram` + `LineChart(kde1d(...), show_area=True)` in a `Panel`, pinned to the left axis) and quick-reference row.
- Stats guide and `docs/references/utils/stats.md` cover both functions.
- ADR 0022 and `CONTEXT.md` record that the 2-D density chart is `ContourChart(kde2d(...))` and that a `KDEChart` front was considered and rejected.
- Unit tests for both functions; `contour_kde2d` and `hist_kde1d` golden cases.

## Test plan
- `python -m unittest discover test` → 241 OK (29 in `test_stats`)
- `pytest docs/how-to-guides/charts/contourchart.ipynb docs/how-to-guides/charts/histogram.ipynb docs/how-to-guides/utility/stats.ipynb` → 3 passed; notebooks re-executed in place, new renders inspected
- `python test/golden/golden.py candidate` → 93/93 rendered; the two new cases are the only changes (listed as expected)

Closes #65

