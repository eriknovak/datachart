---
status: accepted
---

# The wheel ships no data: the theme faces download too

ADR 0062 removed the basemap outlines on the principle that a drawing
library's wheel carries the code that draws and nothing else, and named the
five OFL faces under `themes/_fonts/` as the principle's next application.
It held them back for one reason: registration happens at `import datachart`,
so a download there would block every import. That blocker is cleared here by
moving registration off import entirely, and the faces follow the outlines
into the cache. The wheel now carries no data at all — 684 KB of faces and
164 KB of outlines both gone, against 0062's 164 KB alone, so this is the
larger half of the same decision.

## Commitments

- **Registration moves to `resolve_font_family`**, the single seam that turns
  a theme's font stack into concrete face names at build time. It already
  filters the stack by what matplotlib can find, so it already sees every
  name a chart will ask for. A face named in the download map is fetched and
  registered there, once per process, and `import datachart` performs no I/O.

  Theme application was the obvious alternative and is wrong: a face reaches
  the config by more routes than `set_theme`. `derive_theme`, `register_theme`,
  `update_config`, `config.override` and a theme-file round trip all put a
  stack in front of a chart without passing through it, and
  `plot_network_label_family` names a face directly rather than through a
  stack at all. Registering where the name is read covers every route by
  construction; registering where a theme is applied covers one and leaves
  the rest to be rediscovered as bugs.
- **A missing face warns and falls back; it never raises.** This is where the
  faces part company with the outlines, which raise. A map that will not
  download leaves an empty axes and nothing to show; a face that will not
  download leaves a chart that renders correctly in DejaVu Sans and merely
  looks wrong, which the caller may not notice. So the fallback warns once
  per face, naming the URL and the cache directory, and the stack drops to
  its next entry — `SKETCH_THEME` to Comic Sans MS, `QUILL_THEME` to Georgia.
  A wrong font is a worse figure, not a broken one, and the same judgement
  ADR 0062 applied to a coarse river applies here: degrade, say so, do not
  refuse.
- **The cache is shared infrastructure, so it is named as such.**
  `cache_dir`, the environment variable, the timeout and the atomic
  write-aside-and-rename move out of `basemap.py` into their own module;
  `basemap.py` and the new fonts module both read from it. Faces land beside
  the outlines under the same `DATACHART_CACHE_DIR`, in a `fonts/`
  subdirectory. The pre-warm script moves out of `charts/_basemap/` for the
  same reason and grows a font mode, so one command seeds both caches for an
  air-gapped install, a locked-down CI and this repository's own builds.
- **The source is `google/fonts` pinned to a commit SHA.** That repository
  publishes no tags, so a SHA is the only pin available; it is the same
  commitment 0062 made with a Natural Earth release tag, bought the only way
  this upstream sells it. The files are those already vendored, under
  `ofl/imfellenglish/`, `ofl/imfellenglishsc/` and `ofl/comicneue/`.
- **`themes/_fonts/` goes entirely, `OFL.txt` included.** A licence file
  ships alongside the work it licenses; with no faces in the wheel there is
  no work to license, and the SIL OFL terms travel with the download. The
  fonts module names the licence and the upstream, as
  `charts/_basemap/NATURAL_EARTH.txt` does for the outlines. `package-data`
  keeps only that one attribution file.

## Considered options

- **Register on theme application (`config.set_theme`).** Rejected: see
  above — it is one of at least five routes a face name takes into the
  config, and the other four would each fail silently in DejaVu Sans.
- **Register lazily at first draw**, in the panel rather than the style
  resolver. Rejected: the panel would need to inspect resolved styles for
  face names that `resolve_font_family` has already filtered out, which
  inverts the seam for no gain.
- **Raise on a failed font download**, matching the basemap. Rejected: the
  failure modes are not alike. A basemap is the subject of its figure and a
  face is its clothing, and a library that refuses to draw because a font is
  unreachable is worse than one that draws in the fallback and says so.
- **Keep the faces bundled and take the 684 KB.** Rejected: it is the whole
  question, and 0062 already answered it for the outlines. Half a principle
  applied to the smaller half of the data is not a position worth holding.
- **Ship the faces as a pre-seeded cache entry.** Rejected for the reason
  0062 rejected it for the outlines: the wheel still carries a dataset, under
  a different name.
