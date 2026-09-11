---
status: accepted
---

# Panel takes axis scales, and a layer group carries its source figure's scale

`Panel` (issue #124) sets the scale of each of its axes, and adopts a source
figure's scale when the caller sets none. The seam already honoured `scalex`
and `scaley` in its settings; only the composition front never passed them,
so `Panel([LineChart(..., scaley="log")])` rendered linear.

## Commitments

- **Three settings, addressed by role.** `scalex`, `scaley` and
  `scaley_right` take a `SCALE` value. Like `xmin`/`ymin` and the labels,
  they name the axis by role, not by letter: `scaley` is the primary value
  axis, `scalex` the category axis, `scaley_right` the secondary value axis.
  A horizontal panel maps them to the literal axes the other way round.
- **The primary and secondary value axes scale independently.** Linear bars
  on the left against a log line on the right is the motivating case. Each
  setting governs the axis it names and no more: an explicit `scaley` fixes
  the primary axis and leaves the secondary to inherit, exactly as `ymin`
  does not touch `ymin_right`. A polar panel has no twin, so `scaley_right`
  is inert there, as `ymin_right` already is.
- **A scale is a per-group pref, not panel furniture.** The composition
  front stamps each layer group with the scale of the figure it came from,
  and the group carries it to whichever axis twin assignment sends it to.
  Inheritance cannot live in the front: twin assignment runs at render time
  inside the seam, so at the moment the front builds its settings, no
  figure's axis is known yet. Baking an inherited scale into the panel's
  primary axis would put a log scale on the bars while the line that needed
  it drew linear.
- **Both axes ride the group**, as `value_scale` and `category_scale`, so
  the seam resolves and warns for every axis in one place. Only the value
  axis strictly needs to travel per group, since the category axis has no
  twin to follow, but splitting the two across different mechanisms would
  put two resolution paths in the seam for one concept.
- **A stamped scale survives nesting**, under the None-means-keep rule that
  already governs `y_axis`, `z_order`, `legend_label` and `emphasis`. A
  nested panel's explicit `scaley` reaches its own groups, so
  `Panel([Panel([f1, f2], scaley="log"), f3])` keeps the inner log. Its
  `scaley_right` reaches only the groups it pinned with `"y_axis": "right"`,
  and its `scaley` reaches the rest: the inner call's own twin assignment
  does not survive flattening, so the pin is the only record of which
  figures it meant by "right".
- **An explicit setting beats a stamped one**, per axis. Among the groups on
  one axis, the first in panel order wins — first-one-wins, as the tick
  formats and the stacked baseline already do, narrowed to that axis.
- **A figure that set no scale was built linear**, so it takes part in
  first-one-wins and in the conflict warning as `"linear"` rather than
  abstaining. A linear bar chart listed before a log line on the same axis
  keeps that axis linear and warns. Treating an unset scale as "no opinion"
  would let one log figure anywhere in the list silently drag every
  unscaled figure on its axis onto log.
- **The category axis has no twin**, so `scalex` collapses to a single
  first-one-wins across every group, and there is no `scalex_right`.
- **Conflicts warn, under `overlay_warn_scale_conflict`.** The loser is
  redrawn on a scale it was not built for, which renders without complaint
  and misleads. Setting the scale explicitly silences the warning, because
  the caller has then chosen. The warning fires per axis, so one panel can
  warn twice.
- **The two axes get different warnings, because only one has a remedy.**
  A value-axis conflict is recoverable: move the series to the secondary
  axis with `y_axis` and give it `scaley_right`, and both scales are drawn.
  The warning says so. A category-axis conflict has no remedy — a panel has
  one category axis and no twin for it — so the warning names the scale that
  won and stops there.
- **`scaley_right` set on a panel that never grows a twin also warns**, on
  the same key. Asking for a secondary-axis scale states an expectation that
  a secondary axis exists; silence there is the failure this feature exists
  to remove. The polar case is exempt and documented as inert.
- **The horizontal swap belongs to the chart-front settings builder.** The
  group fronts — box, violin, swarm, raincloud — name the value axis
  `scaley` whatever their orientation, so the builder swaps the keys for a
  horizontal one and the seam's `scalex`/`scaley` are literal for every
  front. A layer-level remap cannot survive composition: the panel front
  swaps role-addressed arguments once on the way in, and a layer swapping
  again at draw time would undo it for a horizontal panel holding a box
  plot.
- **No validation of a scale against the data.** A log panel over
  non-positive values behaves exactly as a log `LineChart` over the same
  values behaves today. That rule belongs to every front, not to panels
  (issue #147).

## Why a new config key

`overlay_warn_scale_groups` gates a different warning, about how many
order-of-magnitude clusters compete for two axes. That "scale" is data
magnitude; ours is the axis transform. Sharing one switch would mean someone
silencing magnitude-clustering noise loses the log-versus-linear warning
too, so the conflict warning gets `overlay_warn_scale_conflict` of its own.

## Why scale, when nothing else is inherited

`CONTEXT.md` holds the rule this bends: a nested panel keeps its per-figure
prefs "while the outermost call supplies all panel-level furniture", and
lists axis scale among that furniture. Scale earns the exception because of
how its loss presents. A dropped label or limit is visible — the reader sees
a blank axis or a different range and goes looking. A dropped log scale is
not: the panel renders a clean chart that misstates the data, and nothing on
it says a scale was discarded. Treating it as a per-group pref moves it to
where the other things that survive composition already live. Limits and
labels stay panel furniture.

## Considered options

- *No inheritance; the caller restates the scale on the panel.* Rejected:
  it is the status quo, and the status quo silently downgrades a correct
  figure. Composing two figures should not change what either one claims.
- *Inherit in the front, into the panel's primary axis.* Rejected: the front
  runs before twin assignment, so it cannot know which axis a figure lands
  on. It puts the scale on the wrong axis in exactly the dual-axis case the
  feature was built for, and a scale on the wrong axis is worse than none,
  because the chart looks deliberate.
- *Inherit only when the panel has a single axis.* Rejected: same objection,
  narrower. It gives up the motivating case to avoid the hard part.
- *Inherit limits too.* Rejected: a limit that goes missing is visible, so
  it does not have scale's failure mode, and inheriting a source figure's
  limits would fight the panel's own autoscaling over the union of the data.
- *Raise on a conflict.* Rejected: both figures render fine alone, and a
  panel of a log line over linear bars is a reasonable thing to ask for once
  the secondary axis carries one of them. An error would block the legible
  case to prevent the misleading one.
- *Reuse `overlay_warn_scale_groups`.* Rejected: see above — one word, two
  meanings, and silencing one warning should not silence the other.
- *Keeping the swap in the layer's `apply_scales`.* Rejected: it swaps at
  draw time, after the panel front has already swapped, so a horizontal
  panel holding a box plot swaps twice and lands the scale on the category
  axis.
- *Letting an unset scale abstain from first-one-wins.* Rejected: it sounds
  permissive and behaves aggressively, since a single log figure would then
  set the axis for every figure that never asked for one.
- *A `scalex_right`.* Rejected: the secondary axis is always a second value
  axis (`twinx` vertical, `twiny` horizontal), so there is no second
  category axis for it to name.
