"""Tests keeping docs/adr/README.md and the ADR frontmatter in step (ADR 0064)."""

import re
import unittest
from pathlib import Path

ADR_DIR = Path(__file__).resolve().parents[1] / "docs" / "adr"
STATUSES = ("accepted", "proposed", "deprecated")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
NUMBER_LIST = re.compile(r"\[([0-9, ]*)\]")


def adr_files():
    return sorted(p for p in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md"))


def frontmatter(path):
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if match is None:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


class TestADRIndex(unittest.TestCase):
    def setUp(self):
        self.files = adr_files()
        self.numbers = {p.name[:4] for p in self.files}
        self.readme = (ADR_DIR / "README.md").read_text(encoding="utf-8")

    def test_every_adr_is_indexed_once(self):
        entries = re.findall(r"^- \[([0-9]{4})\]\(([^)]+)\)", self.readme, re.M)
        listed = [number for number, _ in entries]
        self.assertEqual(sorted(listed), sorted(self.numbers))
        for number, target in entries:
            with self.subTest(adr=number):
                self.assertTrue((ADR_DIR / target).is_file())

    def test_index_lists_no_missing_adr(self):
        linked = set(re.findall(r"\(([0-9]{4})-[^)]*\.md\)", self.readme))
        self.assertEqual(linked - self.numbers, set())

    def test_status_is_known(self):
        for path in self.files:
            with self.subTest(adr=path.name):
                status = frontmatter(path).get("status", "")
                head = status.split(" by ")[0].strip()
                self.assertIn(head, STATUSES)

    def test_amended_by_targets_exist(self):
        for path in self.files:
            raw = frontmatter(path).get("amended-by")
            if raw is None:
                continue
            match = NUMBER_LIST.fullmatch(raw)
            self.assertIsNotNone(match, f"{path.name}: amended-by must be a list")
            targets = [n.strip() for n in match.group(1).split(",") if n.strip()]
            self.assertTrue(targets, f"{path.name}: amended-by must not be empty")
            for target in targets:
                with self.subTest(adr=path.name, target=target):
                    self.assertIn(target, self.numbers)
                    self.assertGreater(target, path.name[:4])

    def test_superseded_names_its_successor(self):
        for path in self.files:
            status = frontmatter(path).get("status", "")
            if not status.startswith("superseded"):
                continue
            with self.subTest(adr=path.name):
                successor = re.search(r"ADR ([0-9]{4})", status)
                self.assertIsNotNone(successor, f"{path.name}: name the successor")
                self.assertIn(successor.group(1), self.numbers)


if __name__ == "__main__":
    unittest.main()
