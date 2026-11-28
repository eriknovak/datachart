---
status: accepted
---

# Readable text has a 10.5 pt floor in every predefined theme, and text that does not fit is left out

The default theme printed tick labels, legend text and value labels at 8 pt
and axis labels at 9 pt. At matplotlib's default 100 dpi, the density the
figures render at, that is about 11 to 12.5 px. Text meant to be read needs
14 px at 96 dpi, which is 10.5 pt (issue #363). Raising the sizes alone
broke two charts. A full-year calendar cell is about 7 pt square at the
default size, so a 10.5 pt value cannot fit in it at any size the floor
allows. A scatter matrix of thousands-scale data had tick labels touching
across neighbouring cells. Network names, Sankey values, contour labels and
pyramid age bands crowded the same way. The theme values and the rules for
cell values, matrix ticks and these labels are one decision: readable text
stays readable, and when it cannot fit, it is left out rather than shrunk.

## Commitments

- **Readable text is at least 10.5 pt in every predefined theme.** 14 px at
  96 dpi is 10.5 pt. The base theme sets general, subtitle, axis labels,
  legend title, parallel dimension labels and the matrix correlation text to
  11 pt, and tick labels, legend, value labels, annotation text, heatmap and
  calendar cells, parallel ticks and contour labels to 10.5 pt. Quill and
  minimal keep their own overrides at or above the floor (quill 10.5 to
  11.5 pt, minimal value labels 11 pt). The six derivations of the default
  inherit the base (ADR 0074). The title stays the largest text at 14 pt
  (15 pt in sketch, 16 pt in quill).
- **The floor lives in a test, not in the code.** A test walks the
  predefined `*_THEME` names, as the palette gate test does (ADR 0073), and
  asserts that each readable-text key is at least 10.5 pt and that the title
  is strictly larger than every other size key. A theme installed by another
  package is never checked (ADR 0088). No render path clamps a size: a user
  who sets 9 pt gets 9 pt.
- **Contour labels set their own 10.5 pt.** The derived default, the general
  size minus 2, would give 9 pt. A theme that sets the key to `None` still
  derives it (ADR 0022).
- **The treemap minimum stays 6 pt.** It is the size below which a nested
  label is dropped, not a size anything is drawn at, so it is exempt from the
  floor. It is still compared with the title in the rank test.
- **Heatmap and calendar write cell values only when the widest fits a
  cell.** The cell value rule lives in the heatmap layer's value routine, so
  the calendar inherits it. It runs before layout with no margin: the width
  is measured from the glyphs of the cell font, the height is the
  line-height estimate, and the cell is the axes size in points over the
  cells in view. Layout usually grows a cell, but long tick labels beside a
  colorbar can shrink it below the size checked.
- **The cell value rule measures what the user's limits show.** The layer
  receives the axis limits the user set, and only values inside them are
  measured, so a zoomed heatmap keeps the values that fit. A locked aspect
  uses the shorter side for both. Equal limits leave no span and skip the
  rule.
- **Values go all or none, with one warning.** When the widest value does
  not fit, no value is written and one `UserWarning` names the font size,
  the cell size in points and the widest value, and suggests a larger
  `figsize` or a shorter `value_format`. The floor never shrinks to make text
  fit. A full-year calendar at the default size now writes no values, and a
  January–February span writes every one.
- **A scatter matrix fits its tick labels to its cells.** A cell shows as
  many round ticks as stay apart, at least two where two can. The rule is a
  locator and formatter carried in the stored matrix layout as a flag, so
  `Grid` applies it when it rebuilds a nested matrix. The default cell size
  and the page-width cap stay as ADR 0051 sets them.
- **Matrix labels shorten only when every label stays short.** An axis writes
  thousands and up with a suffix (2000 as 2k, 3000000 as 3M) only when every
  such tick reads three characters or fewer before the suffix: 2k, 1.5k and
  125k qualify, 2.01k does not. Otherwise, as for years, the plain format
  stays. An axis on a log or other non-linear scale keeps its own ticks.
- **Network names and edge values go to the first clear spot, else are left
  out.** A network writes each name beside its marker and each edge value on
  its edge, then re-places them at the figure's first draw, once layout has
  fixed the sizes. A text that collides tries its candidate spots in the order
  they are built: a name the spots around its marker, a value the points along
  its edge from the midpoint outward. It takes the first spot clear of the
  other nodes, the figure's other axes and texts, and the labels already
  placed. A text with no clear spot is left out. One `UserWarning` per figure
  gives the total left out and suggests a larger `figsize`, whatever the
  number of networks in it. A name repeated at the same point, such as two
  nodes of one place, is written once.
- **Sankey values are measured by glyph width and warned about when left
  out.** A ribbon value is placed by the width of its glyphs, as the cell
  value rule measures. A value with no spot clear of the node bars, the labels
  and the other values is left out, and one `UserWarning` gives how many and
  suggests a larger `figsize`.
- **Contour labels are re-placed after layout and kept only where they fit.**
  A label is kept only where it lies inside the axes and clears every kept
  label. Each level keeps one label where one fits, trying other spots along
  its line when its first labels crowd. The lines are cut anew under the kept
  labels only, so a label that is left out leaves no gap. Nothing is warned:
  the lines still show where each level runs.
- **A pyramid labels every k-th age band.** Every band keeps its tick, and a
  label is written on every k-th band, counted from the first, where k is the
  smallest step at which neighbouring labels clear each other by one point.
  The step is measured at draw from the tick font's glyphs, the rotation and
  the axis length in points, so a figure that fits every label shows them all.
  Ticks and labels the user sets through `yticks` or `yticklabels` are left
  as set.
- **The label rules share one draw-time queue.** Network names and values
  and contour labels queue their placement on the figure's deferred fits that
  the legend fit already uses. They run at the first draw, once layout has
  run, and measure the laid-out text. Sankey values are measured as the layer
  draws, and a pyramid's step by its tick formatter when the ticks are drawn.
  None of these rules resizes a font.
- **A lone limit is judged by the axis direction before limits apply.** Marks
  anchored past a limit the user set are hidden. On an inverted axis a min
  limit names the high end, and a lone limit past the far end, which flips
  the axis, still crops on the side it named. The cell value rule and the
  hide rule read the same limits.

## Considered options

- **Estimate a value's width at 0.55 em per character.** Rejected: it put
  "0.55" at 23.1 pt against a 22.3 pt cell, though the glyphs render 20.2 pt,
  and so rejected a 16 × 16 heatmap whose values fit. Width comes from the
  font; height keeps the line estimate.
- **A fit margin constant.** Rejected: the rule runs before layout, which
  usually grows the cell, so a margin would drop values that fit.
- **Draw the values below the floor to make them fit.** Rejected: it breaks
  the one rule this ADR sets, and values at 6 pt are the unreadable text the
  issue is about.
- **Thin the values per cell, leaving the ones that fit.** Rejected: a
  grid with some cells labelled and some not reads as missing data.
- **Raise the calendar's row height until a full year fits.** Rejected: a
  full year needs cells of about 17 × 13 pt against today's 7 pt, which adds
  blank space to every calendar.
- **Measure cells over the full data span, ignoring the user's limits.**
  Rejected: a zoomed heatmap whose visible cells fit then lost all values.
- **Fewer ticks per matrix cell, in matplotlib's plain format.** Rejected:
  plain labels stayed apart only by leaving one label in some cells, which
  gives no sense of scale; short labels let two or three fit per cell.
- **A matrix tick rule applied inside the front only.** Rejected: `Grid`
  rebuilds a nested matrix from its stored layout and would drop the rule.
- **Suffix every axis, years included.** Rejected: 2010 read as 2.01k is
  worse than a crowded label, so the suffix needs every label to stay short.
- **Clamp every size to the floor at draw time.** Rejected: it would override
  a size the user chose on purpose, and the floor is a promise about the
  predefined themes.
- **Raise the title with the other sizes.** Not needed: 14 pt already clears
  the 11 pt general size, and the rank test guards it.
- **Shrink a crowded label's font.** Rejected for network, Sankey, contour
  and pyramid labels as for cell values: a label below the floor is the
  unreadable text the issue is about, and the rank test would not hold.
- **Leave the crowded labels and note them in the guides.** Rejected: the
  figures the floor made worse should not ship worse, so the fix is in the
  library, and the guides only widen the few figures that need room.
- **Place network names once at build, by the estimated size.** Rejected:
  layout moves the axes and grows the margins, so a build-time spot can
  collide at the first draw. Placement waits for the laid-out extents.
- **One warning per network, or per left-out label.** Rejected: a figure of
  several networks would warn several times for one cause, so the figure
  warns once with the total.
- **Warn when a contour label is dropped.** Rejected: the lines still show
  where each level runs, and a warning on every crowded plot would be noise
  for a drop the chart absorbs. Network names and edge values and Sankey
  values are the data's own text, so they warn.
- **Cut the contour lines under every label, kept or not.** Rejected: a label
  that is left out would leave a gap in its line with nothing in it.
- **Draw every pyramid band label, and thin the ticks instead.** Rejected: a
  tick with no label gives no scale, and fewer ticks hide bands the reader
  can count; every band keeps its tick and only the labels thin.
- **Pick the pyramid step at build from the figure size.** Rejected: layout
  and a rotation change the axis length, so the step is measured at draw.
- **Test rotated labels by their window extents in the inspection scans.**
  Rejected for the scans: the axis-aligned box of a 45-degree label overlaps
  its neighbour when the glyphs do not touch, so the scans test rotated
  rectangles. The committed tests keep the stricter window-extent rule, so
  the check is not loosened.
