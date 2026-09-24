---
status: accepted
---

# A constant class is a self-validating domain, checked once at the front

`datachart.constants` is 48 plain classes, none an `Enum`; `Union[SCALE, str]`
type-checks nothing and the engine has nothing to check against, so five
validation policies coexist (issue #275): `scalex`, `orientation`,
`aspect_ratio` and `value_format` are never checked; `bar_mode` warns and
falls back to `"group"` against a literal list; four layers raise at draw
time; three fronts hand-roll a check; and the validate module holds 22
`if value not in TUPLE: raise` bodies, six identical but for the tuple.
`NONE` is `None`, `""` or `"none"` depending on the class, 19 classes lack
the `DEFAULT` ADR 0010 promised, and the module does not say which parameter
reads which class.

## Commitments

- **One base for every constant class.** Each class derives from a base whose
  metaclass collects the upper-case attributes of the class body into
  `members()`; the body stays `LINEAR = "linear"`, members stay plain `str`
  (or `None`), and a raw string equal to a member is the member. Every class
  carries `DEFAULT`. `check(value, parameter)` returns the value or raises one
  `ValueError` shape naming the parameter, the rejected value and the members;
  `None` passes as "unset, the default applies".
- **A constant-typed parameter is checked once, at the front, before a layer
  is built.** For a shared parameter (ADR 0067) the domain is the constant
  class in its `SharedParameter` annotation; for a front's own key the
  `ChartKind` row (ADR 0065) names it in a `domains` mapping. The engine's
  split-by-row step runs every check element-wise over per-chart lists. No
  layer, front, or validate function re-checks a constant domain; the validate
  module keeps only checks that read data or the relation between parameters.
  `bar_mode` raises like the rest.
- **`NONE` means one thing: `None`, no explicit value.** A member that names a
  drawing choice — no marker, no line, a blank scatter-matrix cell — takes a
  descriptive name; the old attribute resolves through a `DeprecationWarning`
  for one release, via ADR 0043's alias mechanism widened to constant members
  and classes.
- **A class name says which parameter reads it.** `SCALE` becomes
  `AXIS_SCALE` and `NORMALIZE` becomes `COLOR_NORM`, each with the members its
  parameter accepts and nothing shared by accident; `RIDGELINE_SCALE` already
  carries its chart's prefix (ADR 0052). The module docstring lists every
  class with the parameter, config key or theme that reads it. ADR 0010's flat
  module and ADR 0052's prefix rule stand.

## Considered options

`enum.Enum` with a `str` mixin was rejected: members would stop being plain
strings, `None` members would need a sentinel, and `==` against a raw string
changes meaning for callers. An explicit `_MEMBERS` tuple per class was
rejected: it is the same list twice and drifts. Checking in each layer's
`draw` was rejected: a bad value would reach the figure before the message.
Keeping the `bar_mode` fallback was rejected: silently drawing the wrong
chart is the failure this record removes.
