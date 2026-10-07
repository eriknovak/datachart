---
status: accepted
---

# An installed package registers its themes and names the startup theme through entry points

A team that wants its own look on every chart has two bad options: copy the
theme dictionary into each project, or fork `datachart` with a different
default theme and carry every upstream fix by hand. `register_theme` and
`derive_theme` already build the theme; what is missing is a way for a
package that holds it to be found, and a way for that package to make its
theme the one a session starts in, without each project calling
`set_theme` first.

## Commitments

- **The `datachart.themes` entry-point group registers themes.** `Config`
  reads the group when the singleton is created, in sorted name order: each
  entry point's name is the theme name and its object a theme dictionary or
  a zero-argument callable returning one, so a `derive_theme` variant is
  built lazily. Each goes through `register_theme`, so the usual filling,
  key validation, palette gate and reserved-name rule apply.
- **The `datachart.default_theme` entry-point group names the startup
  theme.** The entry point name is the theme name, predefined or installed;
  its object is never loaded. Several packages naming one are resolved to
  the first name in sorted order, with a warning.
- **An installed theme never breaks the import.** A theme that fails to
  load or register, and a default name that is not registered, are skipped
  with a warning; the session starts in the predefined default theme.
- **`reset` is unchanged.** It returns to the predefined default theme, as
  ADR 0040 and the `BUILTIN_THEMES` comment require, and `save_theme` keeps
  diffing against it. The installed default is a starting point, not a new
  baseline.

## Considered options

- **A `DATACHART_THEME` environment variable.** Rejected as the only
  mechanism: it is per machine, not per install, so a project would still
  have to set it everywhere it runs. It can be added later beside the group.
- **Registering on import of the companion package.** Works today and
  stays supported, but each project must import the package before its
  first chart, and a forgotten import silently draws in the default theme.
- **`reset` returning to the installed default.** Rejected: `reset` and
  `set_theme("default")` must agree, `_complete_theme` fills from the
  predefined default, and a theme file is diffed against it; three places
  would otherwise have to agree on a per-install baseline.
