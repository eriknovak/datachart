---
title: Versioning
---

# Versioning

This page states what `datachart` promises across releases, starting at
`1.0.0`, and how a name gets deprecated and removed.

## Semantic versioning

From `1.0.0`, `datachart` follows [semantic versioning](https://semver.org/):
a major release for breaking changes, a minor release for backward-compatible
features, a patch release for backward-compatible fixes.

This guarantee covers the **programmatic API** only: function and class
signatures, parameter names, constant values, and return shapes/types. It does
not cover **visual output** — theme colors, spacing, default marker or line
styling, or rendered pixel output. A minor or patch release may change how a
chart looks without being a breaking change; it may not change how you call
the package or what a call returns.

## What counts as the public API

The public API is exactly what each module's `__all__` declares — `charts`,
`utils`, `config`, `themes`, `constants`, `typings`, and their submodules —
cross-checked against what [the reference pages][references] document.
`test/test_public_surface.py` enforces this for `constants`, `typings`,
`config`, and `utils`: it fails if a name in one of their `__all__` goes
undocumented, or a documented name isn't in `__all__`.

A name that is not in its module's `__all__` is internal. It can change or
disappear in any release, including a patch, with no notice.

## Deprecation policy

Removing a public name happens in two steps, one release apart:

1. **Deprecate.** The old name becomes a thin wrapper that raises a
   `DeprecationWarning` naming both the old and new spelling, and forwards to
   the replacement. It ships alongside the replacement for one full release.
2. **Remove.** The next release deletes the wrapper. The release notes list
   the removal under a "Breaking Changes" heading in [the changelog][changelog],
   citing the release that announced the deprecation — for example:

   > Removed the deprecated `VLinePlotAttrs`, `HLinePlotAttrs`, ... names
   > announced in 0.10.0

If you're on a version that still emits the warning, follow it to the
replacement before upgrading past the release that removes it.

[references]: references/index.md
[changelog]: changelog.md
