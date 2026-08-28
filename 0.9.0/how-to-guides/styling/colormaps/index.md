# Colormaps

This section shows the different colormaps that are available in `datachart` module. The colormaps are used to customize the colors of the charts.

`datachart` uses [pypalettes](https://y-sunflower.github.io/pypalettes/) under the hood, giving you access to **2500+ color palettes**. A curated selection of popular palettes is available via the [datachart.constants.COLORS](https://eriknovak.github.io/datachart/0.9.0/references/constants/#datachart.constants.COLORS) constant, but you can use any valid pypalettes palette name directly.

The predefined palettes include:

- **Sequential**: `Blues`, `Greens`, `Oranges`, `Purples`, `Reds`, `Sunset2`, `YlGnBu`, `YlOrRd`, `PuBuGn`
- **Diverging**: `RdBu`, `BrBG`, `PuOr`, `Spectral`, `RdYlBu`, `RdYlGn`
- **Categorical**: `Pastel`, `Set2`, `Accent`, `Dark2`, `Paired`, `Set1`
- **Grayscale**: `Greys` (print-friendly)
- **Color-blind friendly**: `Viridis`, `Cividis`, `Inferno`, `Plasma`

```
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
```

```
from datachart.constants import COLORS
from datachart.utils._internal.colors import get_colormap
```

```
def plot_color_gradients(cmap_list: List[Tuple[str, str]], n_sections: int = 256):
    """Plots the gradients of multiple colormaps.

    Args:
        cmap_list (List[Tuple[str, str]]): The list of colormaps to plot.
        n_sections (int, optional): The number of sections to plot. Defaults to 256.

    """

    gradient = np.linspace(0, 1, n_sections)
    gradient = np.vstack((gradient, gradient))

    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows + 1, figsize=(8.2, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh, left=0.2, right=0.99)
    axs[0].set_title(f"datachart colormaps", fontsize=14)

    for ax, (name, value) in zip(axs, cmap_list):
        ax.imshow(gradient, aspect="auto", cmap=get_colormap(value))
        ax.text(
            -0.01,
            0.5,
            name,
            va="center",
            ha="right",
            fontsize=10,
            transform=ax.transAxes,
        )

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()
```

```
cmap_list = [
    ("COLORS.Blues", COLORS.Blues),
    ("COLORS.Greens", COLORS.Greens),
    ("COLORS.Oranges", COLORS.Oranges),
    ("COLORS.Purples", COLORS.Purples),
    ("COLORS.Reds", COLORS.Reds),
    ("COLORS.Sunset2", COLORS.Sunset2),
    ("COLORS.YlGnBu", COLORS.YlGnBu),
    ("COLORS.YlOrRd", COLORS.YlOrRd),
    ("COLORS.PuBuGn", COLORS.PuBuGn),
    ("COLORS.RdBu", COLORS.RdBu),
    ("COLORS.BrBG", COLORS.BrBG),
    ("COLORS.PuOr", COLORS.PuOr),
    ("COLORS.Spectral", COLORS.Spectral),
    ("COLORS.RdYlBu", COLORS.RdYlBu),
    ("COLORS.RdYlGn", COLORS.RdYlGn),
    ("COLORS.Pastel", COLORS.Pastel),
    ("COLORS.Set2", COLORS.Set2),
    ("COLORS.Accent", COLORS.Accent),
    ("COLORS.Dark2", COLORS.Dark2),
    ("COLORS.Paired", COLORS.Paired),
    ("COLORS.Set1", COLORS.Set1),
    ("COLORS.Greys", COLORS.Greys),
    ("COLORS.Viridis", COLORS.Viridis),
    ("COLORS.Cividis", COLORS.Cividis),
    ("COLORS.Inferno", COLORS.Inferno),
    ("COLORS.Plasma", COLORS.Plasma)
]
```

**Continuous scales**

```
plot_color_gradients(cmap_list=cmap_list)
```

**Discrete scales**

```
# change the number of sections `n_sections`
plot_color_gradients(cmap_list=cmap_list, n_sections=10)
```

**Custom datachart palettes**

Besides the pypalettes names, `datachart` registers a few palettes of its own, resolved before pypalettes: `COLORS.PaperYlGnBu` (the diversified YlGnBu categorical palette used by the publication theme) and `COLORS.PaperAccent` (a two-color blue/red accent pair). Unlike pypalettes names, these cycle through their exact colors instead of interpolating.

```
plot_color_gradients(
    cmap_list=[
        ("COLORS.PaperYlGnBu", COLORS.PaperYlGnBu),
        ("COLORS.PaperAccent", COLORS.PaperAccent),
    ],
    n_sections=6,
)
```
