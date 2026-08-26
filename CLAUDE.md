# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`datachart` is a Python data visualization package built on matplotlib that provides a simple API for creating highly customizable charts. The package emphasizes ease of use while maintaining flexibility through a global configuration system and theme support.

## Development Commands

### Testing
```bash
# Run all unit tests
python -m unittest discover test

# Run tests for a specific file
python -m unittest test.test_colors

# Test documentation notebooks
pytest --nbmake ./docs/how-to-guides/**/*ipynb
```

### Code Quality
```bash
# Format code with black
python -m black datachart

# The pre-commit hook automatically runs black
# The pre-push hook runs black, unit tests, and notebook tests
```

### Documentation
```bash
# Install package with dev dependencies
pip install -e .[dev]

# Build and serve documentation locally
mkdocs serve

# Deploy documentation to GitHub Pages
mkdocs gh-deploy --force
```

`llms.txt`, `llms-full.txt`, and per-page `.md` endpoints are generated at build
by the `llmstxt` plugin in mkdocs.yml — never hand-write them. A new guide or
reference page must be added to the plugin's `sections` config with a
description, or `docs/hooks/llmstxt_guard.py` fails the build.

ADRs are internal records: never reference them in docstrings or anything else
mkdocs renders (`docs/adr/` and `docs/agents/` are excluded from the site via
`exclude_docs`). Citing ADRs in code comments is fine — comments never render.

### Building and Publishing
```bash
# Install package in development mode
pip install -e .

# Install with all dependencies (dev + test)
pip install -e .[all]

# Build distribution packages
python -m build --sdist --wheel --outdir dist/
```

## Architecture

### Module Structure

The package is organized into six main modules:

- **charts**: Chart creation functions (BarChart, LineChart, ScatterChart, Heatmap, Histogram, BoxPlot, ViolinPlot, PyramidChart, RadialChart, ParallelCoords)
- **utils**: Utilities including the Panel/Grid composition fronts (ADR 0002; OverlayChart, FigureGridLayout, and figure_grid_layout are their deprecated predecessors), save_figure, and stats functions
- **config**: Global configuration system with the singleton `config` instance
- **themes**: Predefined style themes (DEFAULT_THEME, GREYSCALE_THEME, INK_THEME, HATCH_THEME, MINIMAL_THEME, MATERIAL_THEME), named for their visual trait
- **constants**: Enums and constants (THEME, FIG_SIZE, ORIENTATION, COLORS, etc.)
- **typings**: TypedDict definitions for all chart attributes and style configurations

### Internal Implementation (`datachart/utils/_internal/`)

The `_internal` submodule contains implementation details not exposed to users:

- **layers.py**: The single drawing seam (ADR 0001): `Layer` classes per chart type with `draw(ax, ctx)`, `Panel` owning every cross-layer concern (colors, bar slotting, shared bins, scales, limits, legend, twin axes), `LayerGroup`, and the frozen `DrawContext`
- **plot_engine.py**: Figure assembly: `render_chart()` builds layers, assembles panels, renders them, and stores the metadata transport
- **chart_builder.py**: Chart attribute building and validation logic
- **config_helpers.py**: Helper functions for retrieving and applying style configurations
- **colors.py**: Color cycle creation and colormap utilities

### Global Configuration System

The package uses a singleton configuration pattern:

```python
from datachart.config import config

# The `config` instance is a global singleton that stores all style attributes
# Users can modify it via config.set_theme(), config.update_config(), or config.reset_config()
```

**Key points:**
- The `config` object is instantiated once in `datachart/config/configuration.py` as `config: Config = Config()`
- Chart functions access styles via `config[attr_name]` or `config.get(attr_name, default)`
- Style is resolved against the config when layers are built, never at draw time — composition needs no config snapshots
- The config is deep-copied when setting themes to prevent mutation

### Chart Creation Flow

1. User calls a chart front (e.g., `LineChart(...)`) in `datachart/charts/line_chart.py`
2. The front builds the charts structure via `build_charts_structure()` from `chart_builder.py` and an explicit settings dict, then calls `render_chart(chart_type, charts, settings)` (ADR 0003)
3. `render_chart()` in `plot_engine.py`:
   - Calculates the subplot layout; `None` settings resolve to defaults at point of use
   - Builds the layers via `build_layers()` — style is resolved here, once
   - Assembles one `Panel` per coordinate space (one for single plots, one per subplot otherwise) and calls `panel.render(ax)`
   - Applies figure-level labels and stores the metadata transport on the figure
4. `Panel.render(ax)` assigns colors, computes bar slots and shared histogram bins, draws each layer with a frozen `DrawContext`, then applies scales, grid, ticks, limits, reference lines, and legend
5. Returns the matplotlib Figure object

### Chart Metadata

Figures store metadata for composition operations (Panel, Grid):

```python
figure._chart_metadata = {
    "type": "linechart",    # or "overlay"
    "panel": Panel(...),    # Layer objects + panel settings; redraws into any axes
}
```

The transport carries only what composition consumes — never the fronts' inputs.

`Panel` concatenates the source figures' layer groups into one panel with
twin-axis assignment; `Grid` renders each figure's stored panel into a grid
cell (nested rows define the layout; `layout_spec` dicts are the escape hatch).
Both consume the panel — there is no second drawing path. Grid figures carry a
recursive cell tree (`{"type": "grid", "cells": [...], ...}`, ADR 0006) so they
nest inside `Grid` — each occupies one cell and rebuilds its layout there —
but stay rejected in `Panel`.

### Theme System

Themes are dictionaries conforming to the `StyleAttrs` TypedDict. Each theme defines all style attributes:

- Color palettes (singular/multiple chart colors)
- Font properties (family, size, weight, color)
- Axes styling (spine visibility, tick positioning)
- Plot-specific styles (line width, marker size, bar width, etc.)

When a theme is applied via `config.set_theme(THEME.X)`, the config is replaced with a deep copy of the theme dictionary.

### Testing

Tests are organized by functionality:
- `test_colors.py`: Color cycle and colormap functions
- `test_config.py`: Configuration management
- `test_config_helpers.py`: Style helper functions
- `test_overlay.py`: Figure overlay functionality
- `test_stats.py`: Statistical utility functions
- `test/golden/golden.py`: Golden-image harness — `python test/golden/golden.py baseline|candidate` renders ~40 chart/overlay/grid cases and pixel-diffs candidate against baseline

Notebook tests validate all documentation examples to ensure they execute without errors.

## Key Implementation Details

### Color Cycles

The `create_color_cycle()` function in `colors.py` creates cycle-backed color lookups from palette names or color lists. A `Panel` builds one cycle per palette, pooled across its `LayerGroup`s (singular palette for subplots, multiple palette otherwise), so composed single-series figures draw in distinct colors; each layer receives its color through the `DrawContext`.

### Subplot Management

`render_chart` handles both single plots and multi-subplot layouts:
- Single plots: all layers go into one `Panel` on the same axes
- Multi-subplots: each layer gets its own single-layer `Panel` in a grid

### Style Override Hierarchy

Styles are applied in this order (later overrides earlier):
1. Global config defaults
2. Current theme settings
3. Chart-specific style dictionaries passed in the `style` parameter

### Chart Hash for Color Assignment

Layers use `get_chart_hash()` (in `layers.py`) to key color assignment, so the same chart data gets the same color even when redrawn.

### Axes Configuration

Spine and tick styles are snapshotted from the config at build time by `Panel.snapshot_furniture()` and applied to every axes in `Panel.render()`; `configure_axis_ticks_position()` applies user-provided tick positions. This centralized approach ensures consistency across all chart types.

## Agent skills

### Issue tracker

Issues live as GitHub issues in `eriknovak/datachart`, managed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles, label strings unchanged. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
