---
status: accepted
---

# A palette is scored by one function, and every predefined theme passes its gate

The theme gallery scored each predefined theme's series palette for
colour-blind readers, but the scoring lived in a hidden notebook cell: the
package could not run it, no test read it, and `register_theme` and
`derive_theme` accepted any palette. Measured over every pair of colours,
five shipped themes failed the gallery's own gate (greyscale, hatch, ink,
sketch, material), two of them in the print group whose whole point is
telling series apart (issues #289, #290).

## Commitments

- **One scoring function.** `datachart.themes.score_palette(colors, face)`
  returns a frozen `PaletteScore`: the worst pair of the palette under
  deuteranopia, protanopia and tritanopia and under normal vision, the
  smallest lightness step between two colours (the greyscale gap), the
  number of colours under 3:1 contrast on the face, the worst pair itself,
  and a verdict. The simulation is Machado, Oliveira and Fernandes (2009)
  at full severity in linear RGB, the distance Euclidean in OKLab ×100; the
  model is part of the gate, since the thresholds are calibrated to it. The
  gallery notebook imports this function; it keeps no copy.
- **One gate.** `pass` when the worst deutan and protan pair is ΔE 8 or
  more and the worst normal-vision pair 15 or more; `weak` when deutan and
  protan sit between 6 and 8 with normal still 15 or more, which a theme
  may ship only with a pattern cycle carrying identity; `fail` otherwise.
  Tritan and the greyscale gap are reported, not gated: tritanopia is rare
  and the gap is what a print theme's cycles exist for.
- **Every predefined theme passes.** A test scores every theme's
  `color_general_multiple` against its axes face and asserts `pass`, with
  no allowlist. A theme whose hues cannot be stepped that far holds fewer
  colours: greyscale holds five greys, since six of one hue cannot keep
  every pair 15 apart, and carries the hatch, dash and marker cycles so a
  print still tells a sixth series apart. A one-ink theme (quill) is
  exempt by having one colour.
- **The write paths warn.** `register_theme` and `derive_theme` warn with
  `UserWarning` on a `fail` verdict, naming the worst pair and its ΔE.
  `weak` is a design choice and stays silent; `fail` is a defect the user
  should hear about once, at the moment the palette is chosen. A
  sequential lead is not gated: its six samples are one hue stepped in
  lightness, which by construction sits near ΔE 9 for every reader alike
  and cannot reach the normal-vision floor; the ramp is what the caller
  asked for. Colours the caller chose, a categorical lead or a registered
  palette, are.
- **`PaletteScore` is a dataclass, not a typing.** ADR 0072's four suffixes
  classify the TypedDicts of `datachart.typings`, the shapes a caller
  passes in. A score is a result, lives in `datachart.themes`, and takes
  no suffix.

## Considered options

- **Keep the scoring in the notebook and add a test that executes it.**
  Rejected: the package would still accept a failing palette from
  `register_theme`, and a test that imports a notebook cell is a second
  copy in all but name.
- **Raise instead of warn.** Rejected: a user's brand palette may fail and
  still be the right palette for their audience; the package says so and
  draws it.
- **Allowlist material and sketch as "brand" and "marker-pen" looks.**
  Rejected: a look is a look, and a reader with deuteranopia does not care
  whose brand it is. Their hues stay; their lightness moves.
- **Gate the tritan score too.** Rejected: it would force every palette to
  spread in lightness as far as greyscale does, at a cost to every reader
  for the rarest deficiency.
