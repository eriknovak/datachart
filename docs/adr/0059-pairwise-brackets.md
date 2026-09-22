---
status: accepted
---

# A pairwise bracket is a fourth reference-mark family, placed on the category axis and stacked automatically

A figure that compares groups needs to say which pairs differ: a line spanning
two categories with end ticks and the test result written above it. The
Statistics use-case page builds each one from an `hlines` segment and a
`texts` label placed by hand (#258): no ticks, hand-picked y values, and
category indices the author computes.

Reference marks resolve their style at build in `_resolve_ref_lines` and draw
from the panel after scales and limits are set, pooled per axes through
`REF_KEYS` (ADR 0055). The bracket takes the same seam, so it survives `Panel`
and `Grid` and never takes a cycle color, a bar slot, a legend entry or a
hover handler.

## Commitments

- **A fourth family, not an extension of `hlines`.** `brackets` sits beside
  `vlines`, `hlines` and `dlines` with its own `BracketSettingAttrs`,
  `BracketStyleAttrs` and `plot_bracket_{color,width,tick,alpha}` theme keys.
  Its endpoints are categories rather than numbers and its shape has ticks
  and a text; end-cap keys on `hlines` would make the wrong fields typable on
  every horizontal line, the argument ADR 0055 makes for the diagonal.
- **Endpoints are category labels or numbers.** `from` and `to` are required;
  `brackets={}` raises naming them. A label resolves through the panel's
  category index on the group-oriented charts (box, violin, swarm, raincloud,
  ridgeline) and through the label positions on the bar family; a number is
  the category-axis position as given. A label that resolves nowhere raises
  `ValueError` naming the label and the chart's labels, so a typo fails at
  build rather than drawing in the wrong place.
- **`y` is the value-axis position whichever way the chart runs.** One key,
  documented as the value-axis position: on a horizontal chart it is the x
  coordinate the bracket line sits at. An orientation-dependent `x` alias was
  rejected so the typings carry one field.
- **Automatic placement in fractions of the data range.** Without `y`, each
  bracket sits above the data extent within its span plus a gap, and any
  bracket that overlaps an already placed one is pushed up by one bracket
  height, so the stack never overlaps. Gap and height are fractions of the
  value-axis data range (gap 3%, step 8%), so tests are deterministic and the
  stack scales with the figure. Points via a transform were rejected for
  placement — only the tick length is in points, so it holds across figure
  sizes. Placement extends the value-axis limit to fit the topmost text; an
  explicit `ymax` (`xmax` when horizontal) from the user still wins.
- **Orientation follows the panel.** On a vertical chart the bracket spans the
  category axis horizontally, ticks point down toward the data, text is
  centred above. On a horizontal chart it spans vertically, ticks point left,
  text sits to the right.
- **One line artist and one text artist per bracket.** The path is tick, span,
  tick; the text draws in the text font keys and the bracket's colour. No text
  draws the line alone.
- **Style defaults follow the horizontal line** for colour, width and alpha;
  tick length is a few points. The keys live in the base theme so every
  predefined theme and `derive_theme` carry them.
- **Every front that takes `hlines` takes `brackets`** (ADR 0055's rule).
- **Draw order** is the reference-line rung of ADR 0054.

## Considered options

**End-cap and text keys on `hlines`** were rejected: the same objection as
ADR 0055 raises to generalising the horizontal line, plus the endpoints would
have to accept labels on some fronts and numbers on others under one field.

**A post-hoc front like `Annotate`** was rejected. Brackets belong to the
chart's declaration like every other reference mark, and a post-hoc front
could not extend the value axis before the panel sets limits.

**Star notation and p-value formatting** are out of scope. The bracket takes
a text; the test result comes from the user.
