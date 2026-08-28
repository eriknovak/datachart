---
status: accepted
---

# llms.txt is generated at docs build, with hand-written descriptions guarded by the nav

`docs/llms.txt` was hand-maintained and drifted: the radial chart guide
shipped without ever reaching it. The audiences are LLMs browsing the docs
site and LLM doc registries — nothing LLM-oriented ships in the package
itself. We move generation into the mkdocs build so the file cannot fall
behind the site again.

## Commitments

- **`mkdocs-llmstxt` (pinned) generates `llms.txt`, `llms-full.txt`, and
  per-page `.md` endpoints at build time.** The committed `docs/llms.txt` is
  deleted; the artifacts exist only in the deployed site. The plugin works
  from rendered HTML converted back to markdown, which is what captures
  mkdocs-jupyter notebook pages and mkdocstrings reference pages; a
  source-markdown approach fails on both. The project is in maintenance
  mode, so the version is pinned and the small codebase can be vendored as a
  hook if it ever breaks.
- **`llms-full.txt` carries guides plus API reference, no outputs.** Nav
  order, markdown and code cells only; the plugin's autoclean drops images
  and SVGs, so chart outputs never reach the file. Changelog and development
  pages stay out — noise for a code-writing reader. One `sections:` config
  drives both files, so they leave the llms.txt link index too — accepted.
- **Descriptions stay hand-written, one per page, in the plugin's
  `sections:` config.** No auto-extraction (the plugin has none). The site
  summary blockquote comes from `site_description` plus the plugin's
  `markdown_description`, seeded from the old llms.txt intro.
- **A build hook fails the build on unlisted pages.** The plugin silently
  omits pages missing from `sections:`; the hook cross-checks the nav's
  guide and reference pages against the config so a new page without a
  description breaks `mkdocs build` instead of silently vanishing — drift
  is impossible, not discouraged.
- **The root `llms.txt` is a CI copy of `latest/`.** mike deploys only
  version directories, so the docs workflow copies `latest/llms.txt` and
  `latest/llms-full.txt` to the gh-pages root alongside `404.html`; their
  links stay pinned to the released version directory, which resolves.
- **Registries are one-time submissions after deploy.** Context7 and the
  llms.txt directories (llmstxt.site, directory.llmstxt.cloud) are pointed
  at the deployed files; nothing in the repo tracks them.
