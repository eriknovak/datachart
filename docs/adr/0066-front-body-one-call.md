---
status: accepted
amended-by: [0067]
---

# A chart front's body is one engine call; the row declares the key split

Every chart front writes each keyword three times: in its signature, in its
docstring, and in one of two forwarding dicts — `build_charts_structure(...)`
for keys indexed per chart and `settings = {...}` for keys read per figure —
before calling `render_chart`. That is 50–60 lines per large front, and the
per-chart / per-figure split is re-decided in each one. Three fronts hand-roll
a `show_legend` default with three rules, six fronts word the same "one chart's
data is a dict with key X" check six ways, and a parameter's routing is
whatever the front that named it chose (issue #273). The `ChartKind` row (ADR
0065) already holds what a front rejects and whether its data is a dict; the
key split and the legend default are the last two facts about a front that
live in front bodies instead.

## Commitments

- **The front is its signature, its docstring, its own one-off checks, and
  one call.** The body copies `locals()` as its first statement —
  `params = dict(locals())`; at entry that is exactly the arguments, and the
  copy keeps later locals out under a tracer, where Python before 3.13
  writes them back into the frame's dict — may validate or warn on what it
  names, and returns `render(kind, params)`. A front whose one chart is not
  its `data` argument sets `params["data"]` (the pyramid's negated left side,
  the basemap's features); a front whose charts are not one per dataset
  passes `render` an `expand` step (the calendar's one chart per year). No
  forwarding dict remains in any front.
- **The row declares the split; the engine performs it.** Sixteen per-chart
  keys are shared by every front and live as one constant in the engine
  (`subtitle`, `style`, the tick lists and rotations, the reference-mark
  lists, `texts`). A row's `chart_keys` adds the front's own per-chart
  parameters (`x`, `y`, `yerr`; `valfmt`); a row's `figure_keys` pulls a
  shared key back to the figure when the panel needs it whole (the pyramid's
  mirrored `xticks`). Every other signature parameter is per-figure by
  complement, so a new figure-level parameter needs no row edit.
- **The repeated shapes become row facts.** `legend_default` is a callable
  of the charts and settings that supplies `show_legend` when the caller left
  it `None` (the gantt rule reads the records' groups); `data_keys` names the
  keys one chart's dict must carry, and the builder raises one message
  pattern naming the front and the keys; `defaults` holds the settings a
  front fixes when the caller left them unset (the gantt's one column, the
  pyramid's horizontal orientation). One-off
  validation and warnings stay in the front: a hook with one caller is
  indirection, and ADR 0003's allowlist reads as "the front may check what it
  names".
- **ADR 0003 holds, amended on one line.** Signatures stay explicit and
  per-front with no `**kwargs`; `render_chart` stays the single assembly
  point, now called only by `render`. 0003's "each parameter forwarded once"
  still holds, but the once is in the engine, not the front body.
- **The forwarding is tested once.** A unit test asserts every row's
  `chart_keys` and `figure_keys` name parameters its front's signature has,
  and that `render` splits one front per data shape (point list, group list,
  dict data) into the charts and settings the old body built. Golden parity
  gates the change.

## Considered options

A decorator wrapping each front and forwarding its bound arguments was
rejected: it hides the call, and the fronts that validate before rendering
would need a second seam. An explicit `render("linechart", data,
subtitle=subtitle, …)` was rejected as the forwarding dict under another name.
Declaring both key sets fully on every row was rejected: the per-figure set
is the large, stable one and would drift again. Moving one-off validation
onto the row as hooks was rejected for the reason above. Normalising the
existing routing choices (`valfmt` per chart against `value_format` per
figure) was left out: they differ in semantics — a per-subplot list against
one string — and renaming is a public API change for another record.
