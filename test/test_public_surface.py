import ast
import inspect
import re
import unittest
from pathlib import Path

import datachart.config.configuration as _config_module
import datachart.constants as _constants
import datachart.typings as _typings
import datachart.utils.stats as _stats

DOCS_ROOT = Path(__file__).resolve().parent.parent / "docs" / "references"

# a mkdocstrings directive line, e.g. "::: datachart.constants.FIG_SIZE"
DIRECTIVE = re.compile(r"^:::\s*(datachart\.[A-Za-z0-9_.]+)\s*$", re.MULTILINE)

# doc path prefix -> the module whose __all__ it documents; `config.configuration`
# is documented under the `datachart.config` package path it's re-exported through
MODULES = {
    "datachart.constants": _constants,
    "datachart.typings": _typings,
    "datachart.config": _config_module,
    "datachart.utils.stats": _stats,
}


def documented_names():
    """The top-level names each module's `docs/references` pages document.

    A name is attributed to the longest matching prefix in `MODULES`, so a
    method directive like `datachart.config.Config.set_theme` is skipped
    (it has a further `.` after the prefix) rather than misread as a
    top-level name `Config`.
    """
    surfaces = {prefix: set() for prefix in MODULES}
    for md_file in DOCS_ROOT.rglob("*.md"):
        for match in DIRECTIVE.finditer(md_file.read_text()):
            dotted = match.group(1)
            for prefix in MODULES:
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
        for prefix, module in MODULES.items():
            expected = surfaces[prefix] | deprecated_wrapper_names(module)
            with self.subTest(module=module.__name__):
                self.assertTrue(hasattr(module, "__all__"), "missing __all__")
                self.assertEqual(set(module.__all__), expected)

    def test_all_has_no_duplicates(self):
        for module in MODULES.values():
            with self.subTest(module=module.__name__):
                self.assertEqual(len(module.__all__), len(set(module.__all__)))
