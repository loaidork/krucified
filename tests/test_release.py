"""Offline release smoke tests; requires only Python standard library."""
import ast
import pathlib
import unittest
from unittest.mock import patch
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def test_all_python_sources_parse(self):
        for filename in ROOT.rglob("*.py"):
            if ".venv" not in filename.parts:
                with self.subTest(file=str(filename.relative_to(ROOT))):
                    ast.parse(filename.read_text(encoding="utf-8"), filename=str(filename))

    def test_ipinfo_has_no_embedded_token(self):
        source = (ROOT / "tools/ip-lookup/main.py").read_text()
        self.assertIn('os.environ.get("IPINFO_TOKEN")', source)
        self.assertNotIn('IPINFO_TOKEN = "', source)

    def test_wayback_uses_https(self):
        source = (ROOT / "tools/wayback/main.py").read_text()
        self.assertIn('https://web.archive.org/cdx/search/cdx', source)
        self.assertNotIn('http://web.archive.org/cdx/search/cdx', source)

    def test_repo_contains_no_virtualenv(self):
        self.assertFalse((ROOT / ".venv").exists())


if __name__ == "__main__":
    unittest.main()
