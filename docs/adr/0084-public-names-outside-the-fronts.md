---
status: accepted
---

# Public names outside the fronts follow the front rule, and a stats helper returns columns

ADR 0083 settled the naming rule for front parameters. A few public names
outside the fronts break the same rule (issue #327): `save_figure(format=)`
shadows a builtin and its `path` is `str` where `save_theme` and
`load_theme` already take a `PathLike`; `correlation` and `spearman` are
siblings named unlike; `Config.update_config` and `reset_config` repeat the
class name beside their scoped twins `override` and `using_theme`;
`set_theme` is annotated `THEME` while its docstring accepts a registered
name; `Grid` cannot set an axis scale although `Panel` can. And `kde1d`
returns a list of `{x, y}` records where `kde2d` returns a dict of columns.

## Commitments

- **The rule extends to every public name.** Utilities, composition fronts
  and `Config` follow ADR 0083's rule: snake_case whole words, no builtin
  shadowing, siblings named alike. A name that would shadow a builtin keeps
  its qualifier: `sum_values` stays, for the reason `format` goes.
- **Renames.** `save_figure(format=)` → `fmt=`; `correlation` → `pearson`;
  `Config.update_config` → `update`, `reset_config` → `reset`. `set_theme`
  keeps its verb: it does not repeat the class name, and `using_theme` is
  its scoped twin.
- **Widened annotations.** `save_figure(path=)` takes `Union[str,
  os.PathLike]`; `set_theme` and `using_theme` take `Union[THEME, str]`,
  which is what the registry accepts.
- **`Grid` gains `scalex` and `scaley`**, applied to every cell the way
  `sharex`/`sharey` apply to every cell; ADR 0041's resolution and log
  check cover them unchanged. `Grid.ylabel` stays: it labels the figure,
  and a grid has no right axis to distinguish from a left one.
- **`kde1d` returns a dict of columns**, `{"x": [...], "y": [...]}`, the
  shape `kde2d` already returns and the shape every record front reads as
  records since the builder's column branch. The three layers that call it
  read the columns; the guides keep passing its result to `LineChart`
  unchanged.
- **Deprecated for one release through a visible wrapper.** Each old name —
  `correlation`, `update_config`, `reset_config`, the `format=` keyword —
  is a thin `def` that warns with a `DeprecationWarning` naming both
  spellings and forwards. The release checklist removes them beside the
  `_DEPRECATED_ALIASES` entries. `kde1d`'s old shape is not kept: a return
  shape cannot be aliased, and the fronts accept both.

## Considered options

Renaming `Grid.ylabel` to `ylabel_left` was rejected: it would promise a
twin axis a grid does not have. `kind` for the save format was rejected:
`kind` is the chart-kind word in this codebase. `correlation(method=)` was
rejected: the module is one function per statistic. Keeping `kde1d`'s
record list and documenting the difference was rejected: two helpers of one
family returning two shapes is the drift the issue names, and the fronts
now read either. A module `__getattr__` for the stats alias was rejected:
one mechanism for four names.
