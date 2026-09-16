"""Generates the constants-by-chart tables from the chart fronts' signatures:
the "Constants by Chart" table and the shared / chart-specific split of the
constants reference, and the parameter-to-constant table under every chart
guide's quick reference (ADR 0052). Rerun after a front gains or loses a
constant-typed parameter.

Run from the repo root: python docs/assets/scripts/generate_constants_by_chart.py
"""

import glob
import inspect
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
import datachart.charts as ch
import datachart.constants as K

CLASSES = {n for n in dir(K) if n.isupper() and inspect.isclass(getattr(K, n))}
# chart families and their fronts, in the order of the charts reference
GROUPS = [
    (title, re.findall(r"::: datachart\.charts\.(\w+)", body))
    for title, body in re.findall(
        r"^## (.+)\n((?:(?!^## ).*\n?)*)",
        pathlib.Path("docs/references/charts.md").read_text(),
        re.M,
    )
]
ORDER = [n for _, fronts in GROUPS for n in fronts]
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


TABLE = {n: params(n) for n in ORDER}
uses = {}
for n, rows in TABLE.items():
    for _, cs in rows:
        for c in cs:
            uses.setdefault(c, set()).add(n)
PAGE_ORDER = re.findall(
    r"::: datachart\.constants\.(\w+)",
    pathlib.Path("docs/references/constants.md").read_text(),
)
CHART_BLOCKS = re.findall(
    r"::: datachart\.constants\.(\w+)",
    pathlib.Path("docs/references/constants.md")
    .read_text()
    .split("## Chart Constants", 1)[1],
)
SPECIFIC = {c for c, fronts in uses.items() if len(fronts) == 1 and c in CHART_BLOCKS}


def link(c, rel):
    return f"[`{c}`]({rel}#datachart.constants.{c})"


# reference page -------------------------------------------------------
lines = [
    "## Constants by Chart",
    "",
    "Which constants the parameters of each chart accept, by chart family. A constant used by one chart carries that chart's prefix; one shared across charts carries none. Style attributes take the constants named in their [typings](typings.md).",
]
for title, fronts in GROUPS:
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
        lines.append(f"| [{n}](charts.md#datachart.charts.{n}) | {spec} | {shared} |")
ref_table = "\n".join(lines) + "\n"

p = pathlib.Path("docs/references/constants.md")
s = p.read_text()
head, _, rest = s.partition("## Figure Constants")
head = head.split("## Constants by Chart")[0]
chart_sec = rest.split("## Chart Constants", 1)[1]
blocks = re.findall(
    r"::: datachart\.constants\.(\w+)\n    options:\n        heading_level: 3\n",
    chart_sec,
)


def block(c):
    return f"::: datachart.constants.{c}\n    options:\n        heading_level: 3\n"


shared = [c for c in blocks if c not in SPECIFIC]
by_chart = [
    c for n in ORDER for _, cc in TABLE[n] for c in cc if c in SPECIFIC and c in blocks
]
by_chart = list(dict.fromkeys(by_chart))
missing = set(blocks) - set(shared) - set(by_chart)
assert not missing, missing
new = (
    head
    + ref_table
    + "\n## Figure Constants"
    + rest.split("## Chart Constants", 1)[0]
    + "## Chart Constants\n\nConstants several charts share.\n\n"
    + "\n".join(block(c) for c in shared)
    + "\n## Chart-Specific Constants\n\nConstants one chart owns, in the order of the [charts reference](charts.md).\n\n"
    + "\n".join(block(c) for c in by_chart)
)
p.write_text(new)

# chart guides ---------------------------------------------------------
INTRO = "The parameters that accept a constant, with the class in [datachart.constants](../../../references/constants/) that lists its values:"
for n, rows in TABLE.items():
    guide = GUIDES[n.lower()]
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
