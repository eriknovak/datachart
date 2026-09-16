---
title: Development
---

# Development

This section is for developers only. It describes the requirements, the setup process, how to run tests, and how the documentation is deployed.

## Requirements

Before starting the project make sure these requirements are available:

- [python][python]. The python programming language (v3.10 or higher).

- [uv][uv]. The package manager that creates the environment and installs the dependencies.

- [git][git]. For versioning your code.


## Setup

### Install

`uv` creates the virtual environment in `.venv` and installs the package with its development dependencies in one step:

```bash
uv sync --group dev
```

Run the commands below through `uv run` (for example `uv run pytest`), or activate the environment first:

```bash
# activate the environment (UNIX)
. ./.venv/bin/activate

# activate the environment (WINDOWS)
./.venv/Scripts/activate

# deactivate the environment (UNIX & WINDOWS)
deactivate
```

**Githooks.** Githooks enable automatic commit and push hooks. The project is configured to format the code on each commit and to format the code and run the tests on each push. See the configuration in `.githooks.ini`. To enable git hooks, run:

```bash
githooks
```


## Tests

To run the unit tests, run:

```bash
python -m unittest discover test
```

To execute the documentation notebooks as tests, run:

```bash
pytest
```

The notebook paths and the `--nbmake` flag are configured in `pyproject.toml`, so no arguments are needed.

## Documentation

To start live-reloading the documentation, run:

```bash
mkdocs serve [-a localhost:9999]
```

The notebooks execute at build time and their runs are cached by content in `.cache/mkdocs-jupyter`; after changing the package, delete that directory so the outputs re-render.

When suggesting changes, please refer to the [Material for MkDocs] documentation.

### Deployment

The documentation is versioned with `mike` and deployed by GitHub Actions: every push to `main` publishes the `dev` version, and every GitHub release publishes its version and moves the `latest` alias, the site default. Never deploy the site by hand.


[python]: https://www.python.org/
[uv]: https://docs.astral.sh/uv/
[git]: https://git-scm.com/
[Material for MkDocs]: https://squidfunk.github.io/mkdocs-material/getting-started/
