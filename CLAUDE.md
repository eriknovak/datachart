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

- **charts**: Chart creation functions (BarChart, LineChart, ScatterChart, Heatmap, Histogram, BoxPlot, ParallelCoords)
- **utils**: Utilities including FigureGridLayout, OverlayChart, save_figure, and stats functions
- **config**: Global configuration system with the singleton `config` instance
- **themes**: Predefined style themes (DEFAULT_THEME, GREYSCALE_THEME, PUBLICATION_THEME, BACKGROUND_THEME)
- **constants**: Enums and constants (THEME, FIG_SIZE, ORIENTATION, COLORS, etc.)
- **typings**: TypedDict definitions for all chart attributes and style configurations

### Internal Implementation (`datachart/utils/_internal/`)

The `_internal` submodule contains implementation details not exposed to users:

- **plot_engine.py**: Core plotting engine with chart wrapper, plot functions for each chart type, and CHART_PLOTTERS mapping
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
- Chart metadata includes a snapshot of the current theme and config for overlay operations
- The config is deep-copied when setting themes to prevent mutation

### Chart Creation Flow

1. User calls a chart function (e.g., `LineChart(attrs)`) in `datachart/charts/line_chart.py`
2. Chart function builds the chart attributes using `build_chart_attrs()` from `chart_builder.py`
3. The `chart_plot_wrapper` decorator in `plot_engine.py` handles:
   - Settings extraction and validation
   - Subplot layout calculation
   - Figure and axes creation with matplotlib
   - Chart metadata storage on the figure object
4. The specific plot function (e.g., `plot_line_chart()`) draws the chart using:
   - Style helpers from `config_helpers.py`
   - Color cycles from `colors.py`
   - Global config values
5. Post-processing applies labels, legends, and axis configurations
6. Returns the matplotlib Figure object

### Chart Metadata

Figures store metadata for composition operations (FigureGridLayout, OverlayChart):

```python
figure._chart_metadata = {
    "charts": [...],
    "type": "linechart",
    "theme": THEME.DEFAULT,
    "config_snapshot": {...},
    # ... other attributes
}
```

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

Notebook tests validate all documentation examples to ensure they execute without errors.

## Key Implementation Details

### Color Cycles

The `create_color_cycle()` function in `colors.py` creates itertools.cycle objects from palette names or color lists. Chart plotting functions use `custom_color_cycle()` to determine whether to use singular or multiple colors based on subplot configuration.

### Subplot Management

The `chart_plot_wrapper` handles both single plots and multi-subplot layouts:
- Single plots: All charts overlay on the same axes
- Multi-subplots: Each chart gets its own subplot in a grid
- The `has_multiple_subplots()` helper determines the mode

### Style Override Hierarchy

Styles are applied in this order (later overrides earlier):
1. Global config defaults
2. Current theme settings
3. Chart-specific style dictionaries passed in the `style` parameter

### Chart Hash for Color Assignment

Charts use `get_chart_hash()` to generate stable hashes for consistent color assignment across multiple charts. This ensures the same chart gets the same color even when redrawn.

### Axes Configuration

The `configure_axes_spines()`, `configure_axis_ticks_style()`, and `configure_axis_ticks_position()` functions apply global config styles to matplotlib axes objects. This centralized approach ensures consistency across all chart types.
