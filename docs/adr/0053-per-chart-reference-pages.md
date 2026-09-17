---
status: accepted
---

# The API reference is organized per chart, with clickable signatures

The reference mirrored the package layout: one page per module. A user
drawing a line chart visited three of them — `charts` for the function,
`typings` for the record and style keys, `constants` for the values a
parameter accepts — and each was a flat list: 25 fronts on one 1.8 MB page,
a signature full of `Optional[Union[...]]` that linked to nothing, and a
typings page that listed the `*SingleChartAttrs` the fronts build internally
beside the dictionaries users actually write.

Each chart now has its own reference page (`docs/references/charts/<chart>.md`):
the function, the record its `data` takes, the keys its `style` accepts (its
own typing plus the shared groups it draws: value labels, area fill,
regression line, reference lines and bands, text annotations), and the
parameter-to-constant table. The typings page keeps what every chart shares —
the settings passed beside the data, the shared style groups, and the theme
style — and points to the chart pages for the rest. A typing is documented
on exactly one page: a shared one on the typings page, a per-chart one on the
page of the chart it is named after (`LineDataPointAttrs` on the line chart's,
also for the bump and stacked area charts that reuse it). The 19
`*SingleChartAttrs` that no front accepts as input are documented nowhere;
the three that are the `data` payload (network, Sankey, treemap) stay.

Signatures render modern annotations (`X | None`) and cross-reference their
types (`modernize_annotations`, `signature_crossrefs`), and the docstrings
of the public fronts link every constant and typing they name in backticks,
so a parameter leads to its contract in one click. Module docstrings carry a
short intro instead of member lists the pages already show.

The per-chart pages, their index, the charts-by-family tables on the typings
page and the constants page, and the guide tables come from one script,
`docs/assets/scripts/generate_constants_by_chart.py` (ADR 0052), which also
asserts the document-once rule. Every `datachart.<module>.<Name>` anchor is
unchanged, so links from the guides survived a path rewrite; the charts
index keeps its URL.

## Considered options

- **One page per module with tables on top.** Rejected: the charts page stays
  huge, and a chart's contract stays split over three pages.
- **Per-chart typings grouped on the typings page.** Rejected: halves the
  problem; the record and style keys sit one page away from the function
  that reads them.
- **Render a shared record on every page that uses it.** Rejected:
  duplicate anchors make cross-references ambiguous; the reusing chart
  links to the owner instead.
