"""Generates everything the reference derives from the chart fronts' signatures:
the per-chart reference pages (`docs/references/charts/<chart>.md`: function,
data record, style keys, parameter-to-constant table) and their index, the
"Constants by Chart" table and the shared / chart-specific split of the
constants reference, the "Typings by Chart" table of the typings reference,
and the parameter-to-constant table under every chart guide's quick reference
(ADR 0052, ADR 0053). Rerun after a front gains or loses a parameter, a data
record, or a style typing.

Run from the repo root: python docs/assets/scripts/generate_constants_by_chart.py
"""

import glob
import inspect
import json
import pathlib
import re
import sys
import typing

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import datachart.charts as ch
import datachart.constants as K
import datachart.typings as T

CLASSES = {n for n in dir(K) if n.isupper() and inspect.isclass(getattr(K, n))}
TYPINGS = {n for n in dir(T) if n.endswith("Attrs") and not n.startswith("_")}
# chart families and their fronts, in the order of the charts reference
FAMILIES = [
    (
        "Trends and Comparisons",
        [
            "LineChart",
            "StackedAreaChart",
            "BumpChart",
            "BarChart",
            "PyramidChart",
            "RadialChart",
            "CalendarHeatmap",
            "GanttChart",
            "DumbbellChart",
        ],
    ),
    (
        "Distributions",
        [
            "Histogram",
            "BoxPlot",
            "ViolinPlot",
            "SwarmPlot",
            "RaincloudPlot",
            "RidgelinePlot",
        ],
    ),
    (
        "Relationships",
        [
            "ScatterChart",
            "Heatmap",
            "ContourChart",
            "HexbinChart",
            "ParallelCoords",
            "NetworkChart",
            "ScatterMatrix",
        ],
    ),
    ("Flows", ["SankeyChart"]),
    ("Part of a Whole", ["Treemap"]),
]
ORDER = [n for _, fronts in FAMILIES for n in fronts]
# what each chart shows, for the index tables
SHOWS = {
    "LineChart": "A value along an ordered axis, one line per series.",
    "StackedAreaChart": "Parts of a total along an ordered axis, filled on top of each other.",
    "BumpChart": "Rank over time, one line per series.",
    "BarChart": "A value per category as bars; series grouped, stacked, or overlaid.",
    "PyramidChart": "Two series as horizontal bars mirrored around a shared category axis.",
    "RadialChart": "Series on polar axes, as a radar line, an area, bars, or a histogram.",
    "CalendarHeatmap": "One colored cell per day, weeks as columns and weekdays as rows.",
    "GanttChart": "A schedule: one bar per task from its start to its end over a date axis.",
    "DumbbellChart": "Two values per category, a dot at each and a connector between them.",
    "Histogram": "The distribution of one numeric variable, binned.",
    "BoxPlot": "Median, quartiles, whiskers, and outliers per group.",
    "ViolinPlot": "The density profile of each group's distribution.",
    "SwarmPlot": "Every observation as a point, spread within its group.",
    "RaincloudPlot": "A half violin, the raw points, and a box per group.",
    "RidgelinePlot": "One density ridge per group, stacked and partly overlapping.",
    "ScatterChart": "One point per observation, placed by two numeric variables.",
    "Heatmap": "A two-dimensional matrix as colored cells.",
    "ContourChart": "A surface sampled on a grid, as iso-lines or filled bands.",
    "HexbinChart": "Point density on the plane, as colored hexagons.",
    "ParallelCoords": "Each record as a polyline across one axis per dimension.",
    "NetworkChart": "Nodes joined by edges, placed by a layout.",
    "ScatterMatrix": "A scatter chart for every pair of dimensions, distributions on the diagonal.",
    "SankeyChart": "Weighted flows between categories, as ribbons between node columns.",
    "Treemap": "Part-of-whole data as nested rectangles sized by value.",
}
# typings documented on the typings page: settings any chart takes, style
# groups several charts read, and the theme-level style
SHARED = {
    "VLineSettingAttrs",
    "HLineSettingAttrs",
    "DLineSettingAttrs",
    "VSpanSettingAttrs",
    "HSpanSettingAttrs",
    "TextSettingAttrs",
    "LegendSettingAttrs",
    "EmphasisRuleAttrs",
    "ColorbarSettingAttrs",
    "ValueLabelStyleAttrs",
    "AreaStyleAttrs",
    "RegressionStyleAttrs",
    "VLineStyleAttrs",
    "HLineStyleAttrs",
    "DLineStyleAttrs",
    "VSpanStyleAttrs",
    "HSpanStyleAttrs",
    "TextStyleAttrs",
    "StyleAttrs",
    "ColorStyleAttrs",
    "FontStyleAttrs",
    "AxesStyleAttrs",
    "LegendStyleAttrs",
    "GridStyleAttrs",
    "ThemeDefaultAttrs",
    "SketchStyleAttrs",
    "InkStyleAttrs",
}
# shared style groups a chart's `style` reads, keyed by the parameter that
# switches the feature on; heatmaps print cell values through their own font
STYLE_GROUPS = [
    (
        ("show_values",),
        "value labels",
        ["ValueLabelStyleAttrs"],
        {"Heatmap", "CalendarHeatmap"},
    ),
    (("show_area",), "the area fill", ["AreaStyleAttrs"], set()),
    (("show_regression",), "the regression line", ["RegressionStyleAttrs"], set()),
    (
        ("vlines", "hlines", "dlines"),
        "reference lines",
        ["VLineStyleAttrs", "HLineStyleAttrs", "DLineStyleAttrs"],
        set(),
    ),
    (
        ("vspans", "hspans"),
        "reference bands",
        ["VSpanStyleAttrs", "HSpanStyleAttrs"],
        set(),
    ),
    (("texts",), "text annotations", ["TextStyleAttrs"], set()),
]
# constants a parameter takes inside its payload, keyed by the parameter
PAYLOADS = {
    "norm": ("norm", ["NORMALIZE"]),
    "legend": (
        'legend={"location": ..., "alignment": ...}',
        ["LEGEND_LOCATION", "LEGEND_ALIGN"],
    ),
    "colorbar": (
        'colorbar={"location": ..., "format": ..., "orientation": ...}',
        ["COLORBAR_LOCATION", "VALUE_FORMAT", "ORIENTATION"],
    ),
}
STYLE_EXTRA = {
    "Histogram": [('style={"plot_hist_type": ...}', ["HISTOGRAM_TYPE"])],
    "GanttChart": [
        ('style={"plot_gantt_dependency_entry": ...}', ["GANTT_ARROW_ENTRY"])
    ],
}
GUIDES = {
    p.split("/")[-1].removesuffix(".ipynb"): p
    for p in glob.glob("docs/how-to-guides/charts/*.ipynb")
}
REFS = pathlib.Path("docs/references")


def slug(name):
    return name.lower()


def guide_title(name):
    title = re.sub(r"(?<!^)([A-Z])", r" \1", name)
    return title.replace("Parallel Coords", "Parallel Coordinates")


def params(name):
    source = inspect.getsource(getattr(ch, name))
    sig = source.split("):", 1)[0]
    # a parameter the docstring marks "Not supported" raises when passed
    unsupported = set(re.findall(r"^        (\w+): Not supported", source, re.M))
    rows, seen = [], set()
    for line in sig.splitlines():
        m = re.match(r"\s*(\w+):\s*([^=]*)", line)
        if not m or m.group(1) in seen or m.group(1) in unsupported:
            continue
        if m.group(1) in PAYLOADS:
            label, cs = PAYLOADS[m.group(1)]
            rows.append((f"`{label}`", cs))
            seen.add(m.group(1))
            continue
        cs = [
            c
            for c in dict.fromkeys(
                re.findall(r"(?<![.\w])([A-Z][A-Z_]{3,})\b", m.group(2))
            )
            if c in CLASSES
        ]
        if cs:
            rows.append((f"`{m.group(1)}`", cs))
            seen.add(m.group(1))
    return rows + [(f"`{k}`", v) for k, v in STYLE_EXTRA.get(name, [])]


def typings_in(annotation, acc):
    """The public typings an annotation names, outermost first."""
    if inspect.isclass(annotation) and annotation.__name__ in TYPINGS:
        if annotation.__name__ not in acc:
            acc.append(annotation.__name__)
    for arg in typing.get_args(annotation):
        typings_in(arg, acc)
    return acc


def nested(name, acc):
    """The per-chart data typings a typing's fields name, recursively."""
    for annotation in getattr(T, name).__annotations__.values():
        for inner in typings_in(annotation, []):
            if inner in acc or inner in SHARED or inner.endswith("StyleAttrs"):
                continue
            acc.append(inner)
            nested(inner, acc)
    return acc


def chart_base(name):
    return re.sub(r"(Chart|Plot)$", "", name)


def typing_prefix(name):
    return re.sub(
        r"(SingleChartAttrs|DataPointAttrs|DataAttrs|RecordAttrs|TaskAttrs"
        r"|LinkAttrs|NodeAttrs|EdgeAttrs|StyleAttrs)$",
        "",
        name,
    )


def owner(name):
    """The chart whose page documents a per-chart typing: the one it is named after."""
    if name in SHARED:
        return None
    fronts = [n for n in ORDER if chart_base(n).startswith(typing_prefix(name))]
    return min(fronts, key=len) if fronts else None


SIGS = {n: inspect.signature(getattr(ch, n)) for n in ORDER}
DATA = {
    n: [
        t
        for t in typings_in(SIGS[n].parameters["data"].annotation, [])
        if t not in SHARED
    ]
    for n in ORDER
}
STYLE = {n: typings_in(SIGS[n].parameters["style"].annotation, []) for n in ORDER}
TABLE = {n: params(n) for n in ORDER}
uses = {}
for n, rows in TABLE.items():
    for _, cs in rows:
        for c in cs:
            uses.setdefault(c, set()).add(n)
CONSTANTS_MD = REFS / "constants.md"
PAGE_ORDER = re.findall(r"::: datachart\.constants\.(\w+)", CONSTANTS_MD.read_text())
CHART_BLOCKS = re.findall(
    r"::: datachart\.constants\.(\w+)",
    CONSTANTS_MD.read_text().split("## Chart Constants", 1)[1],
)
SPECIFIC = {c for c, fronts in uses.items() if len(fronts) == 1 and c in CHART_BLOCKS}


def link(c, rel):
    return f"[`{c}`]({rel}#datachart.constants.{c})"


def tlink(t, page):
    """A link to a typing from `page` ('' for the typings page, a chart slug, or 'index')."""
    anchor = f"#datachart.typings.{t}"
    home = "" if t in SHARED else slug(owner(t))
    if home == page:
        return f"[`{t}`]({anchor})"
    if home == "":
        return f"[`{t}`]({'../' if page else ''}typings.md{anchor})"
    return f"[`{t}`]({'charts/' if page == '' else ''}{home}.md{anchor})"


def join(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def block(obj, level=3):
    return f"::: {obj}\n    options:\n        heading_level: {level}"


RENDERED = []


def render(n, names):
    """The mkdocstrings blocks of the typings chart `n` documents."""
    out = []
    for t in dict.fromkeys(names):
        if owner(t) == n:
            RENDERED.append(t)
            out += ["", block(f"datachart.typings.{t}")]
    return out


# per-chart reference pages ---------------------------------------------
def data_section(n):
    top, page = DATA[n], slug(n)
    if not top:
        return ""
    lines = ["## Data", ""]
    if top[0].endswith("SingleChartAttrs"):
        inner = nested(top[0], [])
        with_inner = (
            f", with {join([tlink(t, page) for t in inner])} inside" if inner else ""
        )
        lines.append(
            f"`data` is one {tlink(top[0], page)}, or a list of them for subplots{with_inner}."
        )
        lines += render(n, [top[0]] + inner)
        return "\n".join(lines) + "\n"
    keys = [
        p
        for p in SIGS[n].parameters
        if any(p in getattr(T, t).__annotations__ for t in top)
    ]
    rename = (
        f"; the {join([f'`{k}`' for k in keys])} parameter{'s' if len(keys) > 1 else ''} rename"
        f"{'' if len(keys) > 1 else 's'} its keys"
        if keys
        else ""
    )
    lines.append(f"Each record in `data` is a {tlink(top[0], page)}{rename}.")
    lines += render(n, top + [t for x in top for t in nested(x, [])])
    return "\n".join(lines) + "\n"


def style_section(n):
    page = slug(n)
    styles = STYLE[n]
    lines = ["## Style", ""]
    # a chart's own style typing, even when the front types `style` more widely
    named = [t for t in sorted(TYPINGS) if t.endswith("StyleAttrs") and owner(t) == n]
    own = [t for t in styles if owner(t) == n] + [t for t in named if t not in styles]
    text = f"`style` takes the keys of {join([tlink(t, page) for t in styles])}."
    for t in named:
        if t not in styles:
            text += f" Its own keys are those of {tlink(t, page)}."
    for t in own:
        bases = [
            b.__name__
            for b in getattr(getattr(T, t), "__orig_bases__", ())
            if getattr(b, "__name__", "") in TYPINGS
        ]
        if bases:
            text += f" {t} is the union of {join([tlink(b, page) for b in bases])}, one per part of the chart."
    groups = [
        f"{label} ({join([tlink(t, page) for t in ts])})"
        for ps, label, ts, skip in STYLE_GROUPS
        if n not in skip and any(p in SIGS[n].parameters for p in ps)
    ]
    if groups:
        text += f" The chart also reads the shared groups it draws: {join(groups)}."
    text += (
        " Every key falls back to the theme, so the same keys set the default look"
        " through [`config`](../config.md)."
    )
    lines.append(text)
    lines += render(n, own)
    return "\n".join(lines) + "\n"


def constants_section(n):
    rows = TABLE[n]
    if not rows:
        return ""
    ordered = [r for r in rows if any(c in SPECIFIC for c in r[1])] + [
        r for r in rows if not any(c in SPECIFIC for c in r[1])
    ]
    lines = [
        "## Constants",
        "",
        "The parameters that accept a constant, with the class in [datachart.constants](../constants.md) that lists its values.",
        "",
        "| Parameter | Constant |",
        "| :-- | :-- |",
    ] + [
        f"| {p} | {', '.join(link(c, '../constants.md') for c in cs)} |"
        for p, cs in ordered
    ]
    return "\n".join(lines) + "\n"


def chart_page(n):
    guide = f"../../how-to-guides/charts/{slug(n)}.ipynb"
    return (
        f"---\ntitle: {n}\n---\n\n# {n}\n\n"
        f"{SHOWS[n]} The [{guide_title(n)} guide]({guide}) shows every feature on real data; "
        "this page is the contract: the function, the shape of its data, the keys `style` takes, "
        "and the constant each parameter accepts.\n\n"
        "## Function\n\n"
        + block(f"datachart.charts.{n}")
        + "\n\n"
        + "\n".join(
            s for s in (data_section(n), style_section(n), constants_section(n)) if s
        )
    )


(REFS / "charts").mkdir(exist_ok=True)
for n in ORDER:
    (REFS / "charts" / f"{slug(n)}.md").write_text(chart_page(n))
# every public typing is documented exactly once: shared ones on the typings
# page, the rest on the page of the chart they are named after; the per-chart
# `*SingleChartAttrs` a front builds internally are not user input (ADR 0053)
INTERNAL = {
    t
    for t in TYPINGS
    if t.endswith("SingleChartAttrs") and not any(t in DATA[n] for n in ORDER)
}
unrendered = TYPINGS - SHARED - INTERNAL - set(RENDERED)
assert not unrendered, f"typings on no page: {sorted(unrendered)}"
twice = {t for t in RENDERED if RENDERED.count(t) > 1}
assert not set(RENDERED) & SHARED, sorted(set(RENDERED) & SHARED)
assert not twice, f"typings on two pages: {sorted(twice)}"


def chart_rows(page, guide):
    for title, fronts in FAMILIES:
        yield f"\n### {title}\n"
        head = "| Chart | Shows | Data | Style |" + (" Guide |" if guide else "")
        yield head
        yield "| :-- | :-- | :-- | :-- |" + (" :-- |" if guide else "")
        for n in fronts:
            data = ", ".join(tlink(t, page) for t in DATA[n]) or "—"
            style = ", ".join(tlink(t, page) for t in STYLE[n])
            row = f"| [{n}]({'' if page == 'index' else 'charts/'}{slug(n)}.md) | {SHOWS[n]} | {data} | {style} |"
            if guide:
                row += (
                    f" [{guide_title(n)}](../../how-to-guides/charts/{slug(n)}.ipynb) |"
                )
            yield row


(REFS / "charts" / "index.md").write_text(
    "---\ntitle: Charts Module\n---\n\n# Charts Module\n\n"
    "::: datachart.charts\n    options:\n        members: False\n        heading_level: 2\n\n"
    "## Charts by Family\n\n"
    "One page per chart: the function and its parameters, the shape of its data, the keys "
    "`style` takes, and the constant each parameter accepts. Pick the chart by the question "
    "it answers; the [chart guides](../../how-to-guides/charts/index.md) show each one on real data.\n"
    + "\n".join(chart_rows("index", guide=True))
    + "\n"
)

# typings page: the by-chart table ---------------------------------------
TYPINGS_MD = REFS / "typings.md"
s = TYPINGS_MD.read_text()
head, _, rest = s.partition("## Typings by Chart")
tail = rest.split("\n## ", 1)[1]
TYPINGS_MD.write_text(
    head + "## Typings by Chart\n\n"
    "The records a chart's `data` takes and the keys its `style` accepts are documented on the "
    "chart's own reference page, next to the function that reads them.\n"
    + "\n".join(chart_rows("", guide=False))
    + "\n\n## "
    + tail
)

# constants page ---------------------------------------------------------
lines = [
    "## Constants by Chart",
    "",
    "Which constants the parameters of each chart accept, by chart family. A constant used by one chart carries that chart's prefix; one shared across charts carries none. Style attributes take the constants named in their [typings](typings.md).",
]
for title, fronts in FAMILIES:
    lines += [
        "",
        f"### {title}",
        "",
        "| Chart | Chart-specific | Shared |",
        "| :-- | :-- | :-- |",
    ]
    for n in fronts:
        # every row lists its constants in the order they appear on the page
        cs = sorted({c for _, cc in TABLE[n] for c in cc}, key=PAGE_ORDER.index)
        spec = ", ".join(link(c, "") for c in cs if c in SPECIFIC) or "—"
        shared = ", ".join(link(c, "") for c in cs if c not in SPECIFIC) or "—"
        lines.append(
            f"| [{n}](charts/{slug(n)}.md#datachart.charts.{n}) | {spec} | {shared} |"
        )
ref_table = "\n".join(lines) + "\n"

s = CONSTANTS_MD.read_text()
head, _, rest = s.partition("## Figure Constants")
head = head.split("## Constants by Chart")[0]
chart_sec = rest.split("## Chart Constants", 1)[1]
blocks = re.findall(
    r"::: datachart\.constants\.(\w+)\n    options:\n        heading_level: 3$",
    chart_sec,
    re.M,
)
assert len(blocks) == len(CHART_BLOCKS), set(CHART_BLOCKS) - set(blocks)
shared = [c for c in blocks if c not in SPECIFIC]
by_chart = [
    c for n in ORDER for _, cc in TABLE[n] for c in cc if c in SPECIFIC and c in blocks
]
by_chart = list(dict.fromkeys(by_chart))
missing = set(blocks) - set(shared) - set(by_chart)
assert not missing, missing
CONSTANTS_MD.write_text(
    head
    + ref_table
    + "\n## Figure Constants"
    + rest.split("## Chart Constants", 1)[0]
    + "## Chart Constants\n\nConstants several charts share.\n\n"
    + "\n\n".join(block(f"datachart.constants.{c}") for c in shared)
    + "\n"
    + "\n## Chart-Specific Constants\n\nConstants one chart owns, in the order of the [charts reference](charts/index.md).\n\n"
    + "\n\n".join(block(f"datachart.constants.{c}") for c in by_chart)
    + "\n"
)

# chart guides ---------------------------------------------------------
INTRO = "The parameters that accept a constant, with the class in [datachart.constants](../../../references/constants/) that lists its values:"
for n, rows in TABLE.items():
    guide = GUIDES[slug(n)]
    nb = json.loads(pathlib.Path(guide).read_text())
    cell = next(
        c for c in nb["cells"] if "".join(c["source"]).startswith("## Customizing")
    )
    source = "".join(cell["source"])
    src = source.split("\n\n" + INTRO)[0]
    if "\n\n" + INTRO in source:
        tail = source.split("\n\n" + INTRO, 1)[1]
        tail = tail.split("\n\n", 2)[2] if tail.count("\n\n") >= 2 else ""
        src = src + ("\n\n" + tail if tail.strip() else "")
    lines = src.split("\n")
    last = max(i for i, l in enumerate(lines) if l.startswith("|"))
    ordered = [r for r in rows if any(c in SPECIFIC for c in r[1])] + [
        r for r in rows if not any(c in SPECIFIC for c in r[1])
    ]
    tbl = ["| Parameter | Constant |", "| :-- | :-- |"] + [
        f"| {p} | {', '.join(link(c, '../../../references/constants/') for c in cs)} |"
        for p, cs in ordered
    ]
    lines[last + 1 : last + 1] = ["", INTRO, ""] + tbl
    cell["source"] = [l + "\n" for l in lines[:-1]] + lines[-1:]
    pathlib.Path(guide).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
