---
status: accepted
---

# Themes travel as JSON diff files, and temporary style changes are context-managed scopes

A theme built with `register_theme` or assembled with `update_config` cannot
leave the process. There is no way to hand a house style to a colleague, commit
it beside a paper, or reload it in the next session. Separately, a temporary
style change costs a manual set/reset pair that leaks whenever the block
raises, and there is no way to list what themes are registered at all.

We add file persistence, enumeration, and two context managers, and settle the
serialization format here because it decides whether the package gains a
dependency.

## Commitments

- **Theme files are JSON, and JSON only.** Every style value is a string,
  number, boolean, list, or null, so the whole style dictionary serializes with
  the standard library and no new dependency. `Config.__repr__` already emits
  JSON, so the format is one the package speaks.
- **A file holds the diff against `BASE_THEME`, not the whole style.** A theme
  is defined by the handful of attributes that give it its identity; writing
  all 258 keys would bury them. Saving an unmodified default theme therefore
  writes an empty attribute set.
- **A file names itself and states its format version**, alongside the
  attributes. A bare diff of arbitrary style keys cannot say what it is or
  which reader it expects, and both fields cost one line each to write.
- **`load_theme` returns the name it registered.** The name may come from the
  caller, the file, or the file's stem in that order, so the caller cannot
  always predict it, and returning it lets loading and applying compose.
- **Loading validates through the same path as `register_theme`**: missing keys
  fill from the default theme, unknown keys raise `ValueError`. A file is an
  untrusted hand-edited surface and gets no weaker check than a dictionary
  passed in code.
- **Saving and loading canonicalise alias keys**, so a file written with an
  alias key loads back to the canonical key (ADR 0033).
- **A scope restores wholesale on exit, including when the block raises.**
  `override` restores the previous style dictionary; `using_theme` restores both
  it and the active theme name. Any `set_theme` or `update_config` performed
  inside the block is discarded at exit. The block means one thing: the state
  that entered it is the state that leaves it.
- **The scope managers are plain save-and-restore on a global singleton.** They
  are not thread-safe or async-safe, and say so. Concurrency on a global
  configuration is a separate problem and not one a context manager solves.
- **`reset_config` also resets the active theme name.** It restores the style
  dictionary today but leaves the name pointing at the previous theme, so the
  two can disagree. A scope that promises to restore state cannot sit next to a
  method with a weaker definition of the same word.
- **The theme scope is named `using_theme`, not `theme`.** `Config.theme` is an
  existing string attribute holding the active theme name.

## Considered options

**TOML** was rejected. The standard library reads TOML but cannot write it, so
saving would need a third-party writer and the dependency-free argument
collapses. TOML also has no null, while at least one built-in theme's diff sets
an attribute to null, so a diff file would be lossy for exactly the shape we
write.

**YAML** was rejected. It needs `pyyaml`, which would arrive either as a hard
dependency for a peripheral feature or as an optional extra whose absence turns
a documented method into an import error at call time.

**Writing the full style dictionary** rather than a diff was rejected. It makes
every file 258 keys of mostly-default values, which no one can read or review,
and it freezes today's defaults into every saved file so a later change to the
base theme never reaches themes built before it.

**Taking `theme` for the context manager** by renaming the attribute to
`active_theme` was rejected. Existing code comparing `config.theme` against a
string would then compare a bound method against a string and silently evaluate
false, which is worse than the awkward name.

**Warning about, or merging forward, changes made inside a scope** was rejected.
Merging would make the manager restore something other than what it saved, and
warning adds noise to a rule that is simpler stated than detected.
