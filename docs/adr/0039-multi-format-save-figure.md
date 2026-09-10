---
status: accepted
---

# `save_figure` takes a list of formats, treats the path as a stem, and always returns the written paths

A figure that appears in a paper is usually needed twice — a PDF for the
manuscript and a PNG for the preview — and often a third time as an SVG for
slides. `save_figure` writes exactly one file per call and returns `None`, so
the caller repeats the call and retypes the path once per format, keeping the
stem in sync by hand.

We widen `format` to accept a list, and make the return value the written
paths.

## Commitments

- **`format` accepts a single value, a list of values, or `None`.** A single
  value or `None` behaves exactly as before: one file at `path`, the format
  taken from the argument or inferred from the extension.
- **With a list, `path` is a stem** and one file per format is written as
  `<stem>.<format>`, in the order given. Formats repeated in the list are
  written once per entry; nothing is deduplicated, because a caller who names
  a format twice has made a mistake worth seeing in the returned paths rather
  than one worth silently absorbing.
- **The stem strips `path`'s final suffix only when it names a supported
  format**, matched case-insensitively against `FIG_FORMAT`. So `out/fig1.png`
  and `out/fig1` both stem to `out/fig1`, while `out/fig.v2` stems to itself
  and yields `out/fig.v2.pdf`. Version-suffixed and dotted file names are
  ordinary in a figures directory; a rule that strips any trailing suffix would
  silently rename them.
- **Every call returns `List[str]`.** A single-format call returns a
  one-element list. The function returns `None` today, so no caller can be
  reading a scalar, and one return type spares every caller an `isinstance`
  branch on an argument it already knows the shape of.
- **An empty list raises `ValueError`.** It names no output, and writing
  nothing while reporting success is worse than failing.
- **`dpi` and `transparent` apply to every write.** matplotlib already ignores
  `dpi` for vector backends, so per-format handling would encode a rule the
  backend enforces.

## Considered options

**A scalar return for the single-format case and a list for the list case**
was rejected. The return type would then depend on the argument's shape, which
neither annotates cleanly nor consumes cleanly, and it buys the caller nothing
that indexing does not.

**A separate `save_figures` front** was rejected. It would duplicate the whole
signature to vary one argument, and the two fronts would drift as `save_figure`
grows options.

**Per-format `dpi` or `transparent`** was rejected as out of proportion. It
would turn a list of formats into a list of option dicts, and a caller who
genuinely needs different options per format still has separate calls.
