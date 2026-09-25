---
status: accepted
amended-by: [0075]
---

# A look owns its furniture, a trait composes, a palette is a lead

Fourteen predefined themes were fourteen hand-copied dictionaries, but a
diff against the base showed two axes. Quill, sketch, minimal, material,
dark and ink change the furniture: fonts, spines, faces, rendering. Harbor,
muted, contrast, hatch, mutedhatch and slatehatch change a palette and a
handful of mark keys that recur across them: flat bars, black edges, a hatch
cycle, dash and marker cycles. `derive_theme` (ADR 0073's sibling, #245)
covered the palette axis only, and a colormap lead scores weaker than any
hand-tuned palette, so the tuned palettes had no name a caller could reuse
(issue #291).

## Commitments

- **Three kinds of theme ingredient.** A *look* is a predefined theme that
  owns furniture and is the `base` of a derivation. A *trait* is a partial
  style dictionary that changes how marks are drawn and nothing about the
  furniture: `FLAT` (no bar, histogram or band edges, opaque bars, 2 pt
  lines), `EDGED` (black edges on bars and histograms, opaque bars),
  `HATCHED` (`EDGED` plus the six-entry hatch cycle and a 0.8 pt bar edge),
  `OUTLINED` (black outlines on every other mark: bands, nodes, tiles,
  points, bodies, boxes, arrows, the heatmap frame) and `PATTERNED` (the
  dash and marker cycles). A *lead* is a palette; the tuned categorical
  palettes are `COLORS` constants (`TolMuted`, `Harbor`, `Contrast`, `Rust`,
  `Slate`) that cycle exactly, like `PaperYlGnBu`.
- **Traits are a domain and compose in order.** `TRAIT` is a constant class
  (ADR 0068); `derive_theme(base, lead, traits=[...], **overrides)` applies
  the lead, then each trait in the order given, then the overrides, so a
  later trait wins a shared key and an override wins everything. A trait
  never sets a palette, a colormap or a font.
- **The six bundle themes are derivations.** `HARBOR_THEME`, `MUTED_THEME`,
  `CONTRAST_THEME`, `HATCH_THEME`, `MUTEDHATCH_THEME` and `SLATEHATCH_THEME`
  are each one `derive_theme` call: a lead, traits, and the theme's own
  value scale, ramp, dumbbell pair and residual furniture as overrides. Each
  equals the dictionary it replaced key for key, checked once against the
  previous release and by the golden harness; the only difference is that
  `CONTRAST` and `MUTEDHATCH` carry the six-entry hatch cycle, whose sixth
  entry a five-colour palette never reaches. Their names, `THEME` members
  and gallery cards stay: a name is how a user finds a look.
- **Residue stays explicit.** Where two bundles disagree on a furniture
  value (muted's 1.2 pt lines, contrast's 1.4 pt, hatch's dotted grid), the
  value is an override in that theme's file, not a trait parameter. A trait
  with knobs is a theme again.

## Considered options

- **Normalising the residue into the traits** (one line width, one grid).
  Rejected here: it changes how three themes render, which is #292's
  deliberate change, not this refactor's; the equality check is what makes
  the refactor reviewable.
- **Traits as functions** (`hatched(theme)`). Rejected: a dictionary is what
  `register_theme`, `save_theme` and the JSON theme files already speak; a
  function cannot be saved.
- **Dropping the six bundle names** and documenting the recipes. Rejected
  by the maintainer: the names are the discoverable surface and the gallery
  cards are the documentation.
- **A prefix on the palette constants** (`PaperHarbor`). Rejected: the
  palette is the theme's trait, so sharing the theme's name says so.
