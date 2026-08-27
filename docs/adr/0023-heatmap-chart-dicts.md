---
status: accepted
---

# Heatmap takes `{x, y, z}` chart dicts; `x` and `y` are labels, not coordinates

The heatmap (issue #79) takes the chart-dict shape ADR 0022 introduced for the
contour chart — one `{x, y, z}` dict, or a list of them — instead of a bare
2-D list, so every gridded chart reads its input the same way. The bare list
is rejected outright with a `ValueError` naming the new shape: the package is
pre-1.0 and both shapes land in the same release, so there is no second input
path to keep alive.

`x` and `y` are optional and label the columns and rows of `z` (any values,
strings included; the indices by default). They are tick labels at the
integer cell positions `imshow` draws at, never coordinates. An explicit
`xticks`/`xticklabels` (`yticks`/`yticklabels`) overrides them; the length of
`x` must match the columns of `z` and `y` the rows.

## Considered options

- *Coordinates via `pcolormesh`.* Rejected: uneven axes would draw cells of
  uneven size, which is the contour's job (`filled=True` already does it),
  and category names — the heatmap's main use — cannot be coordinates. A
  numeric-means-coordinates hybrid would give `[0, 1, 2, 5]` and
  `["0", "1", "2", "5"]` different geometry.
- *One-release deprecation of the bare list.* Rejected: dual-shape detection
  in the chart builder for a shape the same release would remove.
