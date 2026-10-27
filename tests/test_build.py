import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import build  # noqa: E402

DOCS_DIR = REPO_ROOT / "docs"
EXPECTED_CHAPTERS = [
    "00-start-here",
    "01-image-tools-vs-chat",
    "02-prompt-patterns-styles",
    "03-prompt-patterns-edits",
    "04-upscale-and-cleanup",
    "05-honest-limits",
    "06-copyright-and-watermarks",
    "07-never-fake-real-people",
    "08-family-photo-respect",
    "09-printing-habits",
    "10-tool-safety-checklist",
    "11-glossary",
]


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "site"
        cls.result = build.build_site(DOCS_DIR, cls.out, write=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def page(self, slug):
        return (self.out / f"{slug}.html").read_text(encoding="utf-8")

    def test_all_chapter_pages_written(self):
        for slug in EXPECTED_CHAPTERS:
            self.assertTrue((self.out / f"{slug}.html").exists(), f"missing {slug}.html")
        self.assertTrue((self.out / "index.html").exists())
        self.assertTrue((self.out / "styles.css").exists())

    def test_index_links_to_every_chapter(self):
        index = self.page("index")
        for slug in EXPECTED_CHAPTERS:
            self.assertIn(f'href="{slug}.html"', index)

    def test_prompt_cards_render(self):
        page = self.page("02-prompt-patterns-styles")
        self.assertIn('class="prompt-card"', page)
        self.assertIn("Before", page)
        self.assertIn("After", page)

    def test_callouts_render(self):
        self.assertIn("callout-caution", self.page("01-image-tools-vs-chat"))
        self.assertIn("callout-caution", self.page("05-honest-limits"))
        self.assertIn("callout-tip", self.page("06-copyright-and-watermarks"))

    def test_checklist_renders_real_checkboxes(self):
        page = self.page("10-tool-safety-checklist")
        self.assertIn('type="checkbox"', page)
        self.assertIn('class="checklist"', page)
        input_tags = re.findall(r'<input[^>]*>', page)
        self.assertTrue(input_tags)
        for tag in input_tags:
            self.assertIn("disabled", tag)
            self.assertNotIn("checked", tag)

    def test_tables_render(self):
        page = self.page("01-image-tools-vs-chat")
        self.assertIn("<table>", page)
        self.assertIn("<thead>", page)
        self.assertIn("<tbody>", page)

    def test_html_is_escaped(self):
        rendered = build.render_blocks("# T\n\nhello <script>alert(1)</script> world")
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_internal_links_resolve(self):
        self.assertEqual(self.result["problems"], [], f"link problems: {self.result['problems']}")
        href_re = re.compile(r'href="([^"]+)"')
        for path in self.out.glob("*.html"):
            for href in href_re.findall(path.read_text(encoding="utf-8")):
                if href.startswith(("http://", "https://", "#")):
                    continue
                target = href.split("#")[0]
                self.assertTrue((self.out / target).exists(), f"{path.name} -> {href}")

    def test_containers_are_balanced(self):
        for doc in build.load_documents(DOCS_DIR):
            fences = doc["markdown"].count(":::")
            if fences:
                self.assertEqual(fences % 2, 0, f"unbalanced ::: in {doc['file']}")

    def test_rough_page_counts_sane(self):
        page = self.page("00-start-here")
        self.assertIn("Chapter 1 of 12", page)

    def test_glossary_terms_present(self):
        page = self.page("11-glossary")
        for term in ["Diffusion model", "Seed", "Inpainting", "Outpainting", "DPI", "Watermark"]:
            self.assertIn(term, page)

    def test_footer_credit_present(self):
        self.assertIn("Asdale Dynamics, LLC", self.page("index"))
        self.assertIn("Asdale Dynamics, LLC", self.page("00-start-here"))

    def test_license_copyright_line_exact(self):
        license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", license_text)


class CliTests(unittest.TestCase):
    def test_cli_build_exit_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            proc = subprocess.run(
                [sys.executable, str(REPO_ROOT / "build.py"), "--out", str(out)],
                capture_output=True, text=True, cwd=REPO_ROOT,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertTrue((out / "index.html").exists())

    def test_cli_check_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            proc = subprocess.run(
                [sys.executable, str(REPO_ROOT / "build.py"), "--out", str(out), "--check"],
                capture_output=True, text=True, cwd=REPO_ROOT,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertFalse(out.exists(), "--check must not write output")


if __name__ == "__main__":
    unittest.main()
