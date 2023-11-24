# ===============================================
# Color definitions and cycles
# Taken from: https://colorbrewer2.org/
# ===============================================

# ===============================================
# Scale definitions
# ===============================================

# -------------------------------------
# Sequential
# -------------------------------------

# ---------------------------
# Single-hue
# ---------------------------

# Blue
color_scale_blue = ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"]
color_scale_green = ["#edf8e9", "#bae4b3", "#74c476", "#31a354", "#006d2c"]
color_scale_orange = ["#feedde", "#fdbe85", "#fd8d3c", "#e6550d", "#a63603"]
color_scale_purple = ["#f2f0f7", "#cbc9e2", "#9e9ac8", "#756bb1", "#54278f"]
color_scale_grey = ["#f7f7f7", "#cccccc", "#969696", "#636363", "#252525"]


# ---------------------------
# Multi-hue
# ---------------------------

color_scale_ylgnbu = ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"]
color_scale_ylgn = ["#ffffcc", "#c2e699", "#78c679", "#31a354", "#006837"]
color_scale_bugn = ["#edf8fb", "#b2e2e2", "#66c2a4", "#2ca25f", "#006d2c"]
color_scale_gnbu = ["#f0f9e8", "#bae4bc", "#7bccc4", "#43a2ca", "#0868ac"]
color_scale_pubu = ["#f1eef6", "#bdc9e1", "#74a9cf", "#2b8cbe", "#045a8d"]

# -------------------------------------
# Diverging
# -------------------------------------

color_scale_rdbn = ["#ca0020", "#f4a582", "#f7f7f7", "#92c5de", "#0571b0"]
color_scale_rdylbu = ["#d7191c", "#fdae61", "#ffffbf", "#abd9e9", "#2c7bb6"]
color_scale_brng = ["#a6611a", "#dfc27d", "#f5f5f5", "#80cdc1", "#018571"]
color_scale_prgn = ["#7b3294", "#c2a5cf", "#f7f7f7", "#a6dba0", "#008837"]
color_scale_puor = ["#e66101", "#fdb863", "#f7f7f7", "#b2abd2", "#5e3c99"]
color_scale_rdgy = ["#ca0020", "#f4a582", "#ffffff", "#bababa", "#404040"]
color_scale_rdylgn = ["#d7191c", "#fdae61", "#ffffbf", "#a6d96a", "#1a9641"]
color_scale_spectral = ["#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba"]


# -------------------------------------
# Quantitative
# -------------------------------------

# mixed light
color_scale_mixed_light = [
    "#a6cee3",
    "#1f78b4",
    "#b2df8a",
    "#33a02c",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#cab2d6",
    "#6a3d9a",
]

# mixed dark
color_scale_mixed_dark = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#ffff33",
    "#a65628",
    "#f781bf",
    "#999999",
]


# ===============================================
# Color Scale Mapping
# ===============================================

COLOR_SCALE_MAPPING = {
    "blue": color_scale_blue,
    "green": color_scale_green,
    "orange": color_scale_orange,
    "purple": color_scale_purple,
    "grey": color_scale_grey,
    "ylgnbu": color_scale_ylgnbu,
    "ylgn": color_scale_ylgn,
    "bugn": color_scale_bugn,
    "gnbu": color_scale_gnbu,
    "pubu": color_scale_pubu,
    "rdbn": color_scale_rdbn,
    "rdylbu": color_scale_rdylbu,
    "brng": color_scale_brng,
    "prgn": color_scale_prgn,
    "puor": color_scale_puor,
    "rdgy": color_scale_rdgy,
    "rdylgn": color_scale_rdylgn,
    "spectral": color_scale_spectral,
    "mixed_light": color_scale_mixed_light,
    "mixed_dark": color_scale_mixed_dark,
}

# ===============================================
# Color Definitions
# ===============================================

COLOR_MAPPING = {}
