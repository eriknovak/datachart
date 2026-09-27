import ast
import inspect
import unittest

from datachart.utils._internal.chart_kinds import CHART_KINDS, LAYER_POLICIES
from datachart.utils._internal.layers import Layer, panel


def _named_classes(node) -> list:
    """The names an isinstance call's class argument lists."""

    items = node.elts if isinstance(node, ast.Tuple) else [node]
    return [item.id for item in items if isinstance(item, ast.Name)]


class TestPanelChecks(unittest.TestCase):
    def test_panel_names_no_concrete_layer_class(self):
        tree = ast.parse(inspect.getsource(panel))
        for call in ast.walk(tree):
            if not (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "isinstance"
            ):
                continue
            for name in _named_classes(call.args[1]):
                value = getattr(panel, name, None)
                with self.subTest(name=name, line=call.lineno):
                    concrete = (
                        inspect.isclass(value)
                        and issubclass(value, Layer)
                        and value is not Layer
                    )
                    self.assertFalse(concrete)

    def test_every_policy_defaults_off_on_the_layer(self):
        for name in LAYER_POLICIES:
            with self.subTest(policy=name):
                self.assertIs(getattr(Layer, name), False)

    def test_built_layers_carry_their_row_policies(self):
        chart = {"data": [{"task": "a", "start": 0, "end": 2}]}
        kind = CHART_KINDS["ganttchart"]
        for layer in kind.build_layers([chart], {}):
            for name in LAYER_POLICIES:
                with self.subTest(policy=name):
                    self.assertEqual(getattr(layer, name), getattr(kind, name))


if __name__ == "__main__":
    unittest.main()
