"""Real-file fixture tests for article50-marking-checker.

Runs check_file() against the binary fixtures committed under
tests/fixtures/ (minimal valid PNGs/JPEGs/text, with and without
Article 50 machine-readable markings). Stdlib unittest only.
"""

import json
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import article50_check as a50  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "fixtures")


class TestRealFixtures(unittest.TestCase):
    def path(self, name):
        return os.path.join(FIXTURES, name)

    def check(self, name):
        return a50.check_file(self.path(name))

    def kinds(self, result):
        return [f["kind"] for f in result["findings"]]

    # -- PNG ----------------------------------------------------------
    def test_png_with_c2pa_jumbf_passes(self):
        r = self.check("c2pa.png")
        self.assertEqual(r["status"], "PASS")
        self.assertIn("c2pa-jumbf-box", self.kinds(r))

    def test_plain_png_fails(self):
        r = self.check("plain.png")
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(r["findings"], [])

    # -- JPEG ---------------------------------------------------------
    def test_jpeg_with_jumbf_passes(self):
        r = self.check("c2pa.jpg")
        self.assertEqual(r["status"], "PASS")
        self.assertIn("c2pa-jumbf-segment", self.kinds(r))

    def test_plain_jpeg_fails(self):
        r = self.check("plain.jpg")
        self.assertEqual(r["status"], "FAIL")
        self.assertEqual(r["findings"], [])

    # -- Text ---------------------------------------------------------
    def test_text_with_disclosure_header_passes(self):
        r = self.check("marked.txt")
        self.assertEqual(r["status"], "PASS")
        self.assertIn("disclosure-marker", self.kinds(r))

    def test_plain_text_fails(self):
        r = self.check("plain.txt")
        self.assertEqual(r["status"], "FAIL")

    # -- Duty mapping --------------------------------------------------
    def test_duties_map_to_article50(self):
        joined = " ".join(self.check("c2pa.png")["duties"])
        self.assertIn("50(2)", joined)
        self.assertIn("50(4)", joined)
        joined2 = " ".join(self.check("plain.jpg")["duties"])
        self.assertIn("50(2)", joined2)

    # -- CLI end-to-end over the fixture directory ---------------------
    def test_cli_over_fixtures_dir(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, "article50_check.py"),
             "--json", FIXTURES],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 1)  # plain.* fixtures FAIL
        doc = json.loads(proc.stdout)
        by_name = {os.path.basename(r["file"]): r["status"]
                   for r in doc["results"]}
        self.assertEqual(by_name["c2pa.png"], "PASS")
        self.assertEqual(by_name["c2pa.jpg"], "PASS")
        self.assertEqual(by_name["marked.txt"], "PASS")
        self.assertEqual(by_name["plain.png"], "FAIL")
        self.assertEqual(by_name["plain.jpg"], "FAIL")
        self.assertEqual(by_name["plain.txt"], "FAIL")


if __name__ == "__main__":
    unittest.main()
