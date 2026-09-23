"""Tests keeping docs/adr/README.md and the ADR frontmatter in step (ADR 0064)."""

import re
import unittest
from pathlib import Path

ADR_DIR = Path(__file__).resolve().parents[1] / "docs" / "adr"
STATUSES = ("accepted", "superseded")
PROSE_HEADINGS = ("Architecture decision records", "How to read an entry")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
NUMBER_LIST = re.compile(r"\[([0-9, ]*)\]")
ENTRY = re.compile(r"^- \[([0-9]{4})\]\(([^)]+)\)(.*)$")
LINK = re.compile(r"\[([0-9]{4})\]\(([0-9]{4})-[^)]*\.md\)")


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


def amended_by(path):
    raw = frontmatter(path).get("amended-by")
    if raw is None:
        return []
    match = NUMBER_LIST.fullmatch(raw)
    if match is None:
        return None
    return [number.strip() for number in match.group(1).split(",") if number.strip()]


def index_entries(readme):
    """One (number, link target, heading, amendments) per indexed ADR."""
    entries = []
    heading = ""
    for line in readme.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            continue
        match = ENTRY.match(line)
        if match is not None:
            number, target, rest = match.groups()
            entries.append(
                (number, target, heading, [n for n, _ in LINK.findall(rest)])
            )
    return entries


class TestADRIndex(unittest.TestCase):
    def setUp(self):
        self.files = {p.name[:4]: p for p in adr_files()}
        self.readme = (ADR_DIR / "README.md").read_text(encoding="utf-8")
        self.entries = index_entries(self.readme)

    def test_every_adr_is_indexed_once(self):
        listed = [number for number, _, _, _ in self.entries]
        self.assertEqual(sorted(listed), sorted(self.files))

    def test_every_entry_links_its_own_file(self):
        for number, target, _, _ in self.entries:
            with self.subTest(adr=number):
                self.assertEqual(target, self.files[number].name)

    def test_every_entry_sits_under_a_subsystem(self):
        for number, _, heading, _ in self.entries:
            with self.subTest(adr=number):
                self.assertTrue(heading, "entry outside any section")
                self.assertNotIn(heading, PROSE_HEADINGS)

    def test_index_links_resolve(self):
        linked = {number for number, _ in LINK.findall(self.readme)}
        self.assertEqual(linked - set(self.files), set())

    def test_index_amendments_match_frontmatter(self):
        for number, _, _, amendments in self.entries:
            with self.subTest(adr=number):
                self.assertEqual(amendments, amended_by(self.files[number]) or [])

    def test_status_is_known(self):
        for number, path in self.files.items():
            with self.subTest(adr=number):
                status = frontmatter(path).get("status", "")
                self.assertIn(status.split(" by ")[0].strip(), STATUSES)

    def test_amended_by_targets_exist(self):
        for number, path in self.files.items():
            targets = amended_by(path)
            if targets == []:
                continue
            self.assertIsNotNone(targets, f"{path.name}: amended-by must be a list")
            self.assertTrue(targets, f"{path.name}: amended-by must not be empty")
            for target in targets:
                with self.subTest(adr=number, target=target):
                    self.assertIn(target, self.files)
                    self.assertGreater(int(target), int(number))

    def test_superseded_names_its_successor(self):
        for number, path in self.files.items():
            status = frontmatter(path).get("status", "")
            if not status.startswith("superseded"):
                continue
            with self.subTest(adr=number):
                successor = re.search(r"ADR ([0-9]{4})", status)
                self.assertIsNotNone(successor, f"{path.name}: name the successor")
                self.assertIn(successor.group(1), self.files)


if __name__ == "__main__":
    unittest.main()
