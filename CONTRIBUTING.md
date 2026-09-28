# Contributing

Bug reports, feature requests, and pull requests are welcome — open an
[issue](https://github.com/eriknovak/datachart/issues) to report a problem or
propose a chart, theme, or option you are missing.

## Setup, tests, and docs

Environment setup, running the unit tests and the documentation-notebook
tests, and serving the docs locally are all covered in
[`docs/development.md`](docs/development.md) — follow that page rather than
duplicating its steps here.

## Golden-image tests

Chart rendering is also checked with a pixel-diff harness against a baseline:

```bash
python test/golden/golden.py baseline    # render ~40 cases into baseline/
python test/golden/golden.py candidate   # render into candidate/, diff vs baseline/
```

Run `baseline` before your change and `candidate` after; a diff means the
change altered rendered output, which is expected for a styling change but
worth double-checking otherwise.

## Architecture decision records (ADRs)

A design decision that was hard to reverse, surprising without context, or
the result of a real trade-off gets an ADR in [`docs/adr/`](docs/adr/README.md)
— read that file for how entries are numbered, amended, and superseded before
adding one. ADRs are internal records: nothing mkdocs renders may reference
them, though code comments may cite them freely.

## Commit style

Commits follow [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `refactor:`, `docs:`, etc., with a short imperative summary.
The pre-commit hook runs `black`; the pre-push hook runs `black`, the unit
tests, and the notebook tests.

## Versioning and deprecation

See [`docs/versioning.md`](docs/versioning.md) for what's covered by semantic
versioning and how a name gets deprecated and removed.
