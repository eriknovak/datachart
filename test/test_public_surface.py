import ast
import inspect
import re
import unittest
from pathlib import Path

import datachart.config.configuration as _config_module
import datachart.constants as _constants
import datachart.typings as _typings
import datachart.utils.compose as _compose
import datachart.utils.figure as _figure
import datachart.utils.stats as _stats

DOCS_ROOT = Path(__file__).resolve().parent.parent / "docs" / "references"

# a mkdocstrings directive line, e.g. "::: datachart.constants.FIG_SIZE"
DIRECTIVE = re.compile(r"^:::\s*(datachart\.[A-Za-z0-9_.]+)\s*$", re.MULTILINE)

# doc path prefix -> implementation module(s) whose __all__ it documents, and
# any documented name under that prefix that isn't an attribute of those
# modules (implemented elsewhere, or a submodule reference rather than a
# `:::` member directive). `config.configuration`, `compose`, and `figure`
# are documented under the package path they're re-exported through, not
# their own module path; `compose` and `figure` share `datachart.utils`, so
# their combined `__all__` is checked against that one documented set.
GROUPS = [
    ("datachart.constants", [_constants], set()),
    ("datachart.typings", [_typings], set()),
    ("datachart.config", [_config_module], set()),
    ("datachart.utils.stats", [_stats], set()),
    # DatachartFigure lives in _internal.figures; `stats` is a submodule link,
    # not a `:::` member directive
    ("datachart.utils", [_compose, _figure], {"DatachartFigure", "stats"}),
]


def documented_names():
    """The top-level names each doc-prefix's `docs/references` pages document.

    A name is attributed to the longest matching prefix in `GROUPS`, so a
    method directive like `datachart.config.Config.set_theme` is skipped
    (it has a further `.` after the prefix) rather than misread as a
    top-level name `Config`.
    """
    prefixes = [prefix for prefix, _, _ in GROUPS]
    surfaces = {prefix: set() for prefix in prefixes}
    for md_file in DOCS_ROOT.rglob("*.md"):
        for match in DIRECTIVE.finditer(md_file.read_text()):
            dotted = match.group(1)
            for prefix in prefixes:
                if dotted == prefix or not dotted.startswith(prefix + "."):
                    continue
                rest = dotted[len(prefix) + 1 :]
                if "." not in rest:
                    surfaces[prefix].add(rest)
    return surfaces


def deprecated_wrapper_names(module):
    """Top-level functions that only warn-and-redirect under their own name.

    A function like `stats.correlation` stays callable (and `import *`-able)
    through its deprecation window even though the docs no longer advertise
    it, so it belongs in `__all__` without being "documented".
    """
    tree = ast.parse(inspect.getsource(module))
    names = set()
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        for call in ast.walk(node):
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "warn_renamed"
                and call.args
                and isinstance(call.args[0], ast.Constant)
                and call.args[0].value == node.name
            ):
                names.add(node.name)
                break
    return names


class TestPublicSurface(unittest.TestCase):
    def test_all_matches_documented_surface(self):
        surfaces = documented_names()
        for prefix, modules, exceptions in GROUPS:
            documented = surfaces[prefix] - exceptions
            deprecated = set()
            for module in modules:
                deprecated |= deprecated_wrapper_names(module)
            expected = documented | deprecated
            actual = set()
            for module in modules:
                actual |= set(module.__all__)
            with self.subTest(prefix=prefix):
                for module in modules:
                    self.assertTrue(
                        hasattr(module, "__all__"), f"{module.__name__} missing __all__"
                    )
                self.assertEqual(actual, expected)

    def test_all_has_no_duplicates(self):
        for _, modules, _exceptions in GROUPS:
            for module in modules:
                with self.subTest(module=module.__name__):
                    self.assertEqual(len(module.__all__), len(set(module.__all__)))

    def test_grouped_modules_dont_overlap(self):
        for prefix, modules, _exceptions in GROUPS:
            if len(modules) < 2:
                continue
            seen = set()
            for module in modules:
                with self.subTest(prefix=prefix, module=module.__name__):
                    self.assertEqual(seen & set(module.__all__), set())
                seen |= set(module.__all__)
