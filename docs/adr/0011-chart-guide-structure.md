---
status: accepted
---

# Chart how-to guides share one structure with real-world data

The chart how-to guides grew organically and diverged: customization options
were scattered under data-shape sections ("Single Line Chart"), examples ran
on random or synthetic datasets, and per-chart features documented elsewhere
(emphasis in the highlighting guide) had no entry point in the chart's own
guide. Finding "how do I customize X" required reading the whole notebook.

The bar chart revamp (PR #43) established the structure every chart guide
follows; this ADR records it so the remaining revamps (line, scatter,
histogram, heatmap, box plot, parallel coordinates) don't rediscover it:

1. **Title + intro** — what the chart is, link to the API reference, the
   double-figure-generation admonition.
2. **Input attributes** — link to the reference table.
3. **Basics** — the minimal call, introducing the guide's running dataset.
4. **Customizing the \<Chart\>** — one subsection per customization axis:
   title/labels/ticks, figure size and grid, mark style (line/bar/marker),
   chart-specific options, **emphasis**, reference lines.
5. **Multiple \<Charts\>** — multi-series, subtitles, subplots, shared axes,
   multi-series-only features (confidence intervals, bar modes).
6. **Additional features** — scales, value labels, custom data keys, and
   other cross-cutting extras.
7. **Saving the chart as an image**.
8. **Real-world examples** — named scenarios with realistic hardcoded data,
   each exercising a feature combination from the sections above.

Two content rules ride along:

- **Real data over random data.** One coherent, intuitive dataset (monthly
  sales, city temperatures) runs through Basics and Customizing so readers
  map options onto a chart they understand; `np.random` demos survive only
  where the point is the distribution itself. Data is hardcoded or computed
  inline — guides never download.
- **Per-chart emphasis sections stay thin duplicates.** The highlighting
  guide remains the cross-chart deep-dive (themes, composition); each chart
  guide shows the `emphasis` parameter once, in its own vocabulary.

## Considered options

- **Centralize customization in the styling guides only.** Rejected: users
  land on the chart's guide first; per-chart sections are the entry point,
  styling guides the deep-dive.
- **Keep synthetic math datasets** (cos curves, random walks). Rejected:
  readers translate options faster on data with real-world meaning.
- **A shared "guide template" notebook instead of an ADR.** Rejected: the
  structure varies legitimately per chart type; a prose record guides
  without constraining.
