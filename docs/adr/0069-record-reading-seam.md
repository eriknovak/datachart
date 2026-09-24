---
status: accepted
---

# The builder is the one record-reading seam; the row declares the record shape and the dataset policy

"One dataset or many" is decided in four places — `isinstance(data[0], list)`
in the builder and again in the dumbbell and gantt fronts, `isinstance(data[0],
dict)` behind the row's `dict_data`, and the calendar heatmap multiplying its
charts per year after the builder has run. Key remaps (`x=`, `label=`, …)
exist on fourteen record fronts and not on twelve, so layers read the caller's
key names through `get_chart_data`, and `label` is a category key on eight
fronts but the per-point name on the scatter. Five group fronts taking the
identical `{label, value}` records answer "several datasets" three ways,
expressed as two booleans on the row (issue #276). ADR 0065 moved the
multiplot and single-dataset rules onto the row; this record finishes the
seam.

We make `build_charts_structure` the only adapter from a caller's `data` to
canonical chart dicts, driven by a record shape and a dataset policy the row
declares.

## Commitments

- **The row declares the record shape.** A record front's row names its
  canonical keys in order and which of them are required; a grid front
  (`dict_data`) names none. The builder's shape check reads that
  declaration: a missing required key raises one `ValueError` naming the
  front, the record index and the key, in one format across fronts.
- **The builder decides multiplicity, alone.** Dataset count comes from the
  `data` shape and the row; no front runs its own `isinstance` check and no
  front multiplies charts after the builder. The calendar heatmap's per-year
  split is a row-declared step the builder applies.
- **Every record key is a remap parameter, on every record front.** The
  union of all rows' canonical keys generates shared parameters in the ADR
  0067 table, so the conformance test enforces the remap on every front
  whose row declares the key. The builder copies each record into a dict
  under canonical keys — the caller's records are never mutated — and
  layers, `get_chart_data` and `_chart_column` read canonical keys only. A
  grid front gets no remap: nothing names a grid's key.
- **`label` is the category key everywhere.** The scatter's per-point name
  parameter becomes `annotation`; `label` stays in its signature for one
  release through the row's `renamed` mapping and warns.
- **One dataset policy per row.** `multiplot` and `single_dataset` are
  replaced by one `datasets` value — `OVERLAY`, `SUBPLOT` or `RAISE` — read
  in one place. `RAISE` has one message. No front changes policy: the box
  and violin raise, the raincloud and ridgeline subplot, the swarm overlays,
  and every grid front keeps splitting into subplots.
- **Golden parity plus builder tests.** The pixel diff is clean for every
  case that does not rename the scatter's key; a unit test feeds each row a
  single-record and a multi-dataset input and asserts the canonical dicts
  out, without rendering.

## Considered options

Remapping grid keys too (`z=` on the heatmap) was rejected: no caller has a
grid under another name, and a rule with no use case is a rule nobody tests.
Keeping the scatter's `label` and documenting the exception was rejected:
one key with two meanings is the defect the seam exists to remove. Splitting
the remap into a follow-up was rejected: without it the builder cannot
promise canonical dicts, so its tests would assert nothing.
