# Earth Science: Seismology and Geodesy

An earthquake report asks the same questions in the same order: where the shaking concentrates, what the ground under it looks like, how the sizes are distributed, how fast the aftershocks die away, when they arrived, which way the rupture ran, and which instruments were watching. This page walks one year of one region through those questions and names the figure that answers each, so the chart to reach for arrives with the question rather than the other way round. Every figure links to the chart guide that covers it in full.

The region is the Aegean and Anatolia, between 34 and 42 degrees north and 19 and 45 degrees east, and the year is 2023, when the Kahramanmaraş sequence struck southern Türkiye. Every number is real. The 831 earthquakes of magnitude 4 and above come from the [USGS earthquake catalogue](https://earthquake.usgs.gov/fdsnws/event/1/) (public domain), the relief grid from [NOAA's ETOPO](https://www.ncei.noaa.gov/products/etopo-global-relief-model) global model (public domain), and the 28 broadband seismic stations from the [FDSN station service](https://service.iris.edu/fdsnws/station/1/) (EarthScope, CC BY 4.0). The axes carry longitude and latitude in degrees. datachart draws no coastlines, so the map under the epicentres is the relief grid itself, placed on the same axes as a picture.

```
import math
from datetime import date, timedelta

import numpy as np

from datachart.charts import (
    CalendarHeatmap,
    ContourChart,
    HexbinChart,
    ImageChart,
    LineChart,
    NetworkChart,
    RadialChart,
)
from datachart.constants import (
    ASPECT_RATIO,
    FIG_SIZE,
    NETWORK_LABEL_POSITION,
    NETWORK_LAYOUT,
    NORMALIZE,
    RADIAL_TYPE,
    SCALE,
    SHOW_GRID,
)
from datachart.utils import Grid, Panel
```

The hidden cell below holds the three tables. `EVENTS` is one tuple per earthquake: the hours since the start of 2023, the latitude, the longitude, the depth in kilometres, and the magnitude. `RELIEF` is the ETOPO grid as `lat` and `lon` axes and a `z` row per latitude, in metres above sea level. `STATIONS` is one tuple per station: its code, latitude, longitude, network, and the place it stands. The sections that follow only reshape those into the records the charts take.

## Where the earthquakes are

### Where does the seismicity concentrate?

The first figure of an earthquake report is the map of the epicentres, and eight hundred points on one axes overplot wherever the activity is densest, which is exactly where the reader looks. A [hexbin chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/hexbinchart/index.md) bins them instead: the plane is tiled with hexagons and each one is coloured by the number of events inside it, so density reads as colour and nothing hides behind a marker. The counts span three orders of magnitude between a quiet hexagon and the aftershock zone, so `norm=NORMALIZE.LOG` gives the colour scale a logarithmic reach and keeps the sparse cells visible. `mincnt=1` leaves the empty cells blank rather than colouring them as zero, and through them shows the ground: an [image chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/imagechart/index.md) draws the relief grid as a faded grey picture stretched over its extent, and [Panel](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/panel/index.md) puts it under the hexagons, so the density reads against the land and the sea it falls on. The grid's first row is its southern edge while a picture's first row is its top, so the rows are flipped.

```
LATITUDE, LONGITUDE, DEPTH, MAGNITUDE = 1, 2, 3, 4
latitude = np.array([event[LATITUDE] for event in EVENTS])
longitude = np.array([event[LONGITUDE] for event in EVENTS])
magnitude = np.array([event[MAGNITUDE] for event in EVENTS])

# the largest event of the year, and the one that followed it nine hours later
main = int(magnitude.argmax())
second = int(np.where(magnitude < magnitude[main], magnitude, 0).argmax())

# the relief as a faded grey picture; a picture's first row is its top, so
# the grid's rows go north first, and each sample is a quarter-degree cell
HALF_STEP = 0.125
relief_image = ImageChart(
    {
        "image": np.array(RELIEF["z"])[::-1],
        "extent": (
            RELIEF["lon"][0] - HALF_STEP,
            RELIEF["lon"][-1] + HALF_STEP,
            RELIEF["lat"][0] - HALF_STEP,
            RELIEF["lat"][-1] + HALF_STEP,
        ),
    },
    style={"plot_image_alpha": 0.45, "plot_image_interpolation": "bilinear"},
)

density = HexbinChart(
    {"x": longitude.tolist(), "y": latitude.tolist()},
    gridsize=42,
    # counts run from 1 to several hundred, so the colour scale is logarithmic
    norm=NORMALIZE.LOG,
    mincnt=1,
    # a hairline edge keeps the single-event cells visible on white
    style={"plot_hexbin_edge_width": 0.3, "plot_hexbin_edge_color": "#d0d0d0"},
    show_colorbars=True,
    colorbar={"label": "Earthquakes of magnitude 4 and above"},
    texts={
        "text": "Kahramanmaraş\nsequence",
        "x": 0.63,
        "y": 0.88,
        "coords": "axes",
        "target": (longitude[main], latitude[main]),
    },
)

# the image sits below the hexagons whatever the order of the figures
epicentre_figure = Panel(
    [relief_image, density],
    title="A year of earthquakes: the faults draw themselves",
    xlabel="Longitude (°E)",
    ylabel_left="Latitude (°N)",
    figsize=(9.0, 4.2),
)
epicentre_figure.show()
```

The bright cells trace lines rather than filling the box, and the lines are the faults. One dense band runs northeast to southwest at about 37 degrees east, where 560 of the year's 831 events fall within 200 km of a single epicentre: that is the Kahramanmaraş sequence, and the rest of this page is largely about it. A second, fainter band curves down the west of the region, from Albania through western Greece and along the arc south of Crete, where the African plate dives beneath the Aegean. The two together hold 90% of the year's earthquakes, and the ground between them is nearly blank.

### What does the ground under them look like?

Epicentres are points on a surface, and the surface is what a reader needs in order to place them. A [contour chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/contourchart/index.md) draws a gridded field as filled bands between its level lines, so the ETOPO relief becomes the shape of the region: the Aegean basin, the Anatolian plateau, and the mountain front between them. The grid goes in as `z` with its `lat` and `lon` axes, `filled` shades the bands, and `levels` sets how many are drawn. Elevation is signed, so the colormap is a diverging one and `vmin` and `vmax` are set symmetrically about zero: sea level lands on its pale midpoint, and the coastline appears without a coastline dataset. The two mainshocks are `texts` notes anchored to their own coordinates.

```
relief_figure = ContourChart(
    {"x": RELIEF["lon"], "y": RELIEF["lat"], "z": RELIEF["z"]},
    title="The Aegean basin, the Anatolian plateau, and the front between them",
    xlabel="Longitude (°E)",
    ylabel="Latitude (°N)",
    filled=True,
    levels=14,
    # a diverging colormap with the range symmetric about zero, so sea
    # level falls on its pale midpoint and the coastline draws itself
    style={"plot_contour_cmap": "BrBG_r"},
    vmin=-4500,
    vmax=4500,
    show_colorbars=True,
    colorbar={"label": "Elevation (m)"},
    texts=[
        {
            "text": f"M{magnitude[index]:.1f}",
            "x": longitude[index] + offset,
            "y": latitude[index] + 1.4,
            "target": (longitude[index], latitude[index]),
        }
        for index, offset in [(main, -2.2), (second, 2.2)]
    ],
    figsize=(9.0, 4.2),
)
relief_figure.show()
```

Sea level sits at the midpoint of the colour scale, so the coastline is the band where the shading changes sign and the Aegean reads as a shallow sea between two land masses. The two mainshocks sit on the mountain front that runs northeast from the corner of the Mediterranean, where the colour changes fastest. The relief is steep there for the same reason the earthquakes are there: the Arabian plate is pushing north into Anatolia, so the crust is both breaking and rising. The deepest cells, in the lower left, are the Hellenic trench at more than 4,000 m below sea level, which is the surface expression of the arc the hexbin figure picked out.

## The sequence

### How are the magnitudes distributed?

Earthquake sizes follow the Gutenberg-Richter law: the number of events of magnitude M or greater falls by a constant factor for every unit of magnitude, so a plot of the cumulative count against magnitude is a straight line on a logarithmic count axis. The slope of that line is the b-value, which is close to 1 for most of the world and is the number a seismicity report quotes. A [line chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md) with `scaley=SCALE.LOG` draws it, and a second series carries the fitted line so the eye can judge the fit rather than trust it.

The line bends away from the data at the left because a catalogue misses small events far from stations. The magnitude where that begins is the completeness magnitude, taken here as 4.5 and marked with `vlines`; the b-value is estimated from the events above it with the Aki maximum-likelihood formula, which needs only their mean magnitude.

```
MC = 4.5  # the magnitude above which the catalogue is complete

steps = np.round(np.arange(4.0, magnitude.max() + 0.1, 0.1), 1)
cumulative = [int((magnitude >= step - 1e-9).sum()) for step in steps]

# Aki's maximum-likelihood b-value, from the mean magnitude above MC
complete = magnitude[magnitude >= MC]
b_value = 1 / (math.log(10) * (complete.mean() - (MC - 0.05)))
a_value = math.log10(len(complete)) + b_value * MC

gutenberg_figure = LineChart(
    [
        [{"x": float(step), "y": count} for step, count in zip(steps, cumulative)],
        [
            {"x": float(step), "y": 10 ** (a_value - b_value * step)}
            for step in steps
        ],
    ],
    title=f"Ten times fewer earthquakes for every unit of magnitude (b = {b_value:.2f})",
    xlabel="Magnitude",
    ylabel="Earthquakes of this magnitude or greater",
    subtitle=["Catalogue", f"Fit above M{MC}"],
    # the counts fall by three orders of magnitude across the axis
    scaley=SCALE.LOG,
    # the fit runs on below one event a year; the axis stops where the data does
    ymin=0.8,
    vlines={"x": MC, "label": f"Completeness (M{MC})"},
    show_legend=True,
    show_grid=SHOW_GRID.BOTH,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
gutenberg_figure.show()
```

Below the completeness line the observed curve falls away from the fit, which is the catalogue missing small events rather than the Earth producing fewer of them. Above it the two follow each other from magnitude 4.5 to about 5.5, and then part again in the other direction: the catalogue counts six events of magnitude 6 and above where the fit predicts 3.4, and two above magnitude 7 where the fit predicts 0.2. The fitted b-value of 1.26 sits a little above the global average of 1, which means the region produces proportionally more small earthquakes than large ones. The excess at the top of the scale is the other half of the same reading: a rate of 0.2 magnitude 7 events a year is one every five years, and 2023 had two, so this was not an average year.

### How fast did the aftershocks die away?

Aftershock rates decay as one over the time since the mainshock, which is Omori's law, and the decay spans three orders of magnitude in both time and rate. Both axes therefore need a logarithmic scale, set with `scalex` and `scaley` on the same [line chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/linechart/index.md), where the power law is again a straight line. The rate is counted in bins that widen with time, because a fixed daily bin would hold hundreds of events on the first day and none at all after a month.

```
HOURS = 0
hours = np.array([event[HOURS] for event in EVENTS])

# everything after the mainshock within 200 km of it
km_per_degree_east = 111.2 * math.cos(math.radians(latitude[main]))
distance = np.hypot(
    (latitude - latitude[main]) * 111.2,
    (longitude - longitude[main]) * km_per_degree_east,
)
after = (hours > hours[main]) & (distance <= 200)
elapsed = (hours[after] - hours[main]) / 24

# bins that widen with time, so each one holds enough events to count
edges = np.array([0.02, 0.05, 0.1, 0.3, 1, 3, 10, 30, 100, 330])
counts, _ = np.histogram(elapsed, bins=edges)
centres = np.sqrt(edges[:-1] * edges[1:])
rate = counts / np.diff(edges)

observed = counts > 0
slope, intercept = np.polyfit(
    np.log10(centres[observed]), np.log10(rate[observed]), 1
)

omori_figure = LineChart(
    [
        [
            {"x": float(day), "y": float(value)}
            for day, value in zip(centres[observed], rate[observed])
        ],
        [
            {"x": float(day), "y": 10 ** (intercept + slope * math.log10(day))}
            for day in centres
        ],
    ],
    title=f"The aftershock rate falls as one over the elapsed time (p = {-slope:.2f})",
    xlabel="Days since the mainshock",
    ylabel="Aftershocks per day",
    subtitle=["Observed rate", "Omori fit"],
    scalex=SCALE.LOG,
    scaley=SCALE.LOG,
    show_legend=True,
    show_grid=SHOW_GRID.BOTH,
    figsize=FIG_SIZE.FULL_MEDIUM,
)
omori_figure.show()
```

The first day carried 214 aftershocks of magnitude 4 and above, and by the end of the year the rate is under one a week. The points lie on the fitted line from a few hours out to the tenth month, so one power law describes the whole decay. The fitted exponent of 0.93 is within the usual range of 0.9 to 1.4, and it has a practical reading: the rate roughly halves every time the elapsed time doubles, so the hazard a week after the mainshock is about a seventh of the hazard on the first day. The first two points sit below the line rather than on it, which is a known limitation of catalogues rather than a feature of the Earth: in the hours after a great earthquake the ground never stops shaking, and smaller events are lost in the noise before they can be measured.

### When did they arrive?

A power law gives the shape of the decay, and the calendar gives its size against the rest of the year. Daily counts over a year are 365 numbers with a strong local structure, which a [calendar heatmap](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/calendarheatmap/index.md) lays out as a calendar, one cell per day coloured by its count. The mainshock day holds more than two hundred events and every ordinary day holds none or one, so `vmax` caps the colour scale well below the peak: the February cells saturate and the rest of the year keeps its contrast.

```
DAYS = [date(2023, 1, 1) + timedelta(days=offset) for offset in range(365)]
per_day = np.bincount((hours // 24).astype(int), minlength=365)[:365]

calendar_figure = CalendarHeatmap(
    {"date": DAYS, "value": per_day.tolist()},
    title="Earthquakes per day in 2023: one week holds half the year",
    figsize=(9.0, 2.6),
    aspect_ratio=ASPECT_RATIO.AUTO,
    # the mainshock day is an order of magnitude above any other
    vmax=12,
    show_colorbars=True,
    colorbar={"label": "Earthquakes of magnitude 4 and above"},
)
calendar_figure.show()
```

The year is almost empty apart from February, which is dark for its whole length and black in its first week. The single darkest cell is 6 February, with 224 events, and the week beginning there holds 47% of the year's earthquakes. The figure also shows what the Omori fit implies: the cells fade through March and April rather than stopping, because an aftershock sequence has no end, only a rate that falls below the rate of everything else.

### Which way did the rupture run?

A fault is a line, so its aftershocks spread along a direction rather than filling a circle, and the direction is the strike of the fault that broke. The azimuth from the mainshock to each aftershock is an angle, and angles belong on a circular axis: a [radial chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/radialchart/index.md) with `type=RADIAL_TYPE.HISTOGRAM` counts them into sectors and draws the rose diagram that structural geology has used for a century. The chart bins the raw angles itself, so each record carries one azimuth as `x`, and the default orientation already puts north at the top and runs clockwise, which is the compass convention.

```
# the compass bearing from the mainshock to each aftershock
azimuth = np.degrees(
    np.arctan2(
        (longitude[after] - longitude[main]) * km_per_degree_east,
        (latitude[after] - latitude[main]) * 111.2,
    )
) % 360

rose_figure = RadialChart(
    [{"x": float(bearing)} for bearing in azimuth],
    type=RADIAL_TYPE.HISTOGRAM,
    title="The aftershocks spread northeast and southwest, along the fault",
    # 16 sectors of 22.5 degrees, the usual resolution of a rose diagram
    num_bins=16,
    show_grid=SHOW_GRID.BOTH,
    figsize=FIG_SIZE.SQUARE,
)
rose_figure.show()
```

The rose has three lobes and an empty quarter. The pair pointing northeast and southwest are opposite bearings along one line, and that line is the strike of the East Anatolian Fault: an aftershock zone is the length of the rupture, so its shape is the fault drawn by its own earthquakes. Only four aftershocks fall in the whole quarter between east and south, which is the measure of how tightly the rest is aligned. The third lobe, between northwest and north, is the second rupture: the magnitude 7.5 event nine hours later broke a different fault 88 km almost due north of the first, and its aftershocks spread on either side of that bearing. A map of the same points would leave the reader to estimate the trends by eye.

## The instruments

### Which stations were watching?

Every number on this page comes from instruments, and the geometry of those instruments decides how well an earthquake can be located: an event inside a dense array is pinned down, one outside it is not. A [network chart](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/networkchart/index.md) with `layout=NETWORK_LAYOUT.FIXED` draws each station at the position given in its own `x` and `y`, so the figure is the station map rather than a diagram of one. The layout works inside a unit square, so both axes take one scale factor and the region keeps its proportions. The region is three times as wide as it is tall, which packs the western stations into a corner, so a second panel repeats the exercise for the stations west of 30 degrees east alone and names every one of them. The edges are the baselines between stations closer than 250 km to each other, excluding the zero-length one where two operators share a single site, and node size counts the baselines each station has. Five operators are represented: the Albanian Seismological Network, GEOFON, the Aristotle University of Thessaloniki network, the Global Seismograph Network, and MedNet.

```
CODE, STATION_LAT, STATION_LON = 0, 1, 2
BASELINE_KM = 250
ZOOM_EAST = 30  # the meridian the enlarged panel stops at


def separation(one, other):
    """The distance between two stations in kilometres."""
    mean_latitude = math.radians((one[STATION_LAT] + other[STATION_LAT]) / 2)
    return math.hypot(
        (one[STATION_LAT] - other[STATION_LAT]) * 111.2,
        (one[STATION_LON] - other[STATION_LON]) * 111.2 * math.cos(mean_latitude),
    )


def station_map(group, subtitle, name_every):
    """A map of `group`, scaled into the unit square the fixed layout uses."""
    edges = [
        {"source": one[CODE], "target": other[CODE], "weight": separation(one, other)}
        for index, one in enumerate(group)
        for other in group[index + 1 :]
        # a zero-length baseline is two operators sharing one site, not a pair
        if 0 < separation(one, other) <= BASELINE_KM
    ]
    baselines = {station[CODE]: 0 for station in group}
    for edge in edges:
        baselines[edge["source"]] += 1
        baselines[edge["target"]] += 1

    # both axes take one scale factor, so the region keeps its proportions
    middle = math.radians(sum(s[STATION_LAT] for s in group) / len(group))
    east = {s[CODE]: s[STATION_LON] * 111.2 * math.cos(middle) for s in group}
    north = {s[CODE]: s[STATION_LAT] * 111.2 for s in group}
    span = max(
        max(east.values()) - min(east.values()),
        max(north.values()) - min(north.values()),
    )

    def unit(places, value):
        reach = max(places.values()) - min(places.values())
        return (value - min(places.values())) / span + (1 - reach / span) / 2

    return NetworkChart(
        {
            "nodes": [
                {
                    "id": station[CODE],
                    # the wide panel names only the stations with no baseline
                    "label": station[CODE].split(".")[1]
                    if name_every or not baselines[station[CODE]]
                    else "",
                    "x": unit(east, east[station[CODE]]),
                    "y": unit(north, north[station[CODE]]),
                    "size": 1 + baselines[station[CODE]],
                }
                for station in group
            ],
            "edges": edges,
        },
        layout=NETWORK_LAYOUT.FIXED,
        label_position=NETWORK_LABEL_POSITION.ABOVE,
        subtitle=subtitle,
        style={"plot_network_node_size_min": 16, "plot_network_node_size_max": 95},
    )


aegean = [station for station in STATIONS if station[STATION_LON] <= ZOOM_EAST]

Grid(
    [
        [
            station_map(STATIONS, "The whole region", name_every=False),
            station_map(aegean, f"West of {ZOOM_EAST}°E, enlarged", name_every=True),
        ]
    ],
    title=f"Broadband stations and the baselines shorter than {BASELINE_KM} km",
    figsize=(11.0, 5.6),
).show()
```

The array breaks into three linked groups and five stations standing alone, and the split runs from west to east. The enlarged panel holds two of the groups and 79 of the 80 baselines: thirteen stations across Albania and northern Greece, where the busiest carries eleven, and eight more ringing Crete and the southern Aegean. East of there the map empties out. A pair sits in eastern Türkiye, and the rest are singletons: Cyprus, Ankara, Garni in Armenia, and Isparta, where two operators run instruments at one site, so the figure draws them on top of each other and one label covers both. The 28 stations here are the globally shared broadband instruments alone, and the national networks that do the routine work in Türkiye and Greece are denser, so a location computed from them is better than this array by itself would give. Read against the first figure the geometry still matters, because the most active part of the region is where this array is thinnest.

## The report figure

A paper has room for one figure, not seven. The four that carry the argument (where the earthquakes are, how their sizes are distributed, how the aftershocks decayed, and which way the rupture ran) go into one panel with [Grid](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/grid/index.md), which takes the figures already drawn above and redraws them into its cells. Nested lists are the layout, one inner list per row.

```
Grid(
    [
        [epicentre_figure, gutenberg_figure],
        [omori_figure, rose_figure],
    ],
    title="The Kahramanmaraş year: the map, the sizes, the decay, and the direction",
    figsize=(14.0, 9.0),
).show()
```

One number on this page is worth a caveat: 445 of the 831 events, more than half, carry a depth of exactly 10 km, which is the value the catalogue assigns when the depth is not resolved, so a figure of depth against anything would be drawing the convention rather than the Earth. This page therefore has no depth figure. Every other figure is one call to a chart function over a list of dicts, and every number in them comes from a few lines of numpy written out in the cell above it. To adapt any of them, open the guide it links to and read the parameter that does the job; the [annotations guide](https://eriknovak.github.io/datachart/dev/how-to-guides/utility/annotations/index.md) covers the reference lines and notes the figures share. The charts index lists them all: [Charts](https://eriknovak.github.io/datachart/dev/how-to-guides/charts/index.md).
