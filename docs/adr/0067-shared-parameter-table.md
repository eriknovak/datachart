---
status: accepted
---

# A shared parameter has one name, type and default; a table enforces it

The same concept is spelled per front, so what a caller learns on one chart
does not transfer (issue #274): `show_values` on eighteen fronts and
`show_heatmap_values` on the heatmap; `value_format` on seventeen and
`valfmt` on the three surfaces; `show_values` a bool on sixteen and an enum
on the gantt and dumbbell, so `True` is invalid there; `vcenter` on two of
the four colormapped fronts; `orientation` defaulting to `VERTICAL` here and
`HORIZONTAL` there; `figsize`, `texts` and `value_format` each narrower on
one front than the rest; the basemap's first positional `features` where
every other front says `data`; `RadialChart.type` shadowing the builtin.
ADR 0066 removed the forwarding dicts and left this for its own record.

## Commitments

- **One name, one type, one signature default per shared parameter.** The
  shared parameters — the sixteen per-chart keys of ADR 0066 plus
  `show_values`, `value_format`, `orientation`, `show_outliers`, `figsize`,
  `norm`, `vcenter`, `mode` and their peers — are rows of one table beside
  `CHART_KINDS`: name, annotation, default. A conformance test reads every
  front's signature against it and fails on drift in any of the three. The
  docs generator reads the same table, so the reference and the test cannot
  disagree.
- **A per-front default lives behind the signature.** Where fronts need
  different defaults for one parameter, the signature says `None` on all of
  them and the `ChartKind.defaults` row of ADR 0066 supplies the front's own
  value: the dumbbell and ridgeline stay horizontal, the raincloud keeps its
  outliers, the swarm keeps its swarm. No rendered figure changes.
- **`show_values` says whether; `value_kind` says which.** The bool is the
  shared type. The gantt and dumbbell, whose value label has more than one
  candidate number, take that choice through a separate `value_kind`
  parameter with a documented default, so `show_values=True` works on every
  front that has it.
- **Per-front selectors keep their nouns.** `layout`, `mode`, `diagonal` and
  `rank_by` each select something only their front has and are not one
  concept; renaming them to one word would blur five meanings. Only
  `RadialChart.type` changes, to `mark`, because it shadows a builtin.
- **Renames warn for one release through ADR 0043's mechanism, widened to
  front parameters.** `show_heatmap_values`, `valfmt`, `normalize`,
  `features` and `type` stay in their fronts' signatures as deprecated
  keywords for one release; the engine maps each to its new name with a
  `DeprecationWarning`, and the release checklist removes them as it
  removes the typing aliases. `valfmt` keeps its per-subplot list shape
  under the new name — only the name changes, the routing does not.

## Considered options

Renaming every selector to `variant` was rejected: the survey showed five
different concepts, and a shared noun would suggest a shared meaning.
Unifying `orientation` by flipping the two horizontal fronts to vertical
was rejected: it changes every existing dumbbell and ridgeline figure to
buy a signature default. Making `show_values` a `Union[bool, str]` on every
front was rejected: the annotation would promise strings that twenty fronts
reject. Shipping the renames without the table was rejected: nothing would
then guard against the next drift.
