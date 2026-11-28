# Coding standards

These rules complement [`CONTRIBUTING.md`](CONTRIBUTING.md): that file says how to contribute, this one says how the code and tests are written.

- A test that changes the theme restores it in `tearDown`.
- One reason to fail per test: a test checks one behaviour.
- No unused parameters.
- No magic numbers: a literal that carries meaning gets a name, defined once.
- A comment describes the code as it stands and never narrates an edit.
- One name per concept across the code, the docs, and the ADRs.
- When a shape repeats, deduplicate it once into a shared helper.
- One job per function.
