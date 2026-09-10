"""Integration tests on the actual Jupyter Book local-extension configuration.

Run with Python in the dt-jupyter-book image: python3 -m unittest discover -s tests -v
"""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
QUESTION = """```{dt-question}
:correct: b
:id: example
:feedback-correct: Thrust & weight balance.
:feedback-incorrect: Try <again>.

What balances **weight**?

- (a) Nothing.
- (b) Upward *thrust*.
```
"""


class QuestionTests(unittest.TestCase):
    def build(self, content, builder="html", strict=True):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        src = root / "src"
        src.mkdir()
        for directory in ("_extensions", "_static"):
            shutil.copytree(ROOT / "src" / directory, src / directory)
        config = yaml.safe_load((ROOT / "src/_config.yml").read_text())
        # The shared builder registers this existing directive for all book pages.
        config["sphinx"]["extra_extensions"].append("dt_sphinx_seo")
        (src / "_config.yml").write_text(yaml.safe_dump({
            "title": "Question test", "sphinx": config["sphinx"],
            "execute": {"execute_notebooks": "off"},
        }))
        (src / "_toc.yml").write_text("format: jb-book\nroot: index\n")
        (src / "index.md").write_text("# Practice\n\n" + content)
        command = ["jb", "build", str(src), "--builder", builder]
        if strict:
            command += ["--warningiserror", "--nitpick"]
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return result, src / "_build" / builder

    def test_semantic_html_and_assets(self):
        result, output = self.build(QUESTION)
        self.assertEqual(result.returncode, 0, result.stdout)
        soup = BeautifulSoup((output / "index.html").read_text(), "html.parser")
        question = soup.select_one("fieldset.dt-question")
        self.assertEqual(question["id"], "dt-question-example")
        self.assertIsNotNone(question.select_one("legend strong"))
        radios = question.select('label input[type="radio"]')
        self.assertEqual(len(radios), 2)
        self.assertTrue(all(radio.has_attr("disabled") for radio in radios))
        self.assertEqual(len({radio["name"] for radio in radios}), 1)
        self.assertEqual(question.select_one("button")["type"], "button")
        self.assertTrue(question.select_one("button").has_attr("hidden"))
        self.assertEqual(question.select_one('[role="status"]')["aria-live"], "polite")
        self.assertFalse(question.select_one("details").has_attr("hidden"))
        self.assertIn("Correct answer: (b). Thrust & weight balance.", question.get_text())
        self.assertEqual(question.select_one("details")["data-feedback-incorrect"], "Try <again>.")
        for asset in ("dt-question.js", "dt-question.css"):
            self.assertTrue((output / "_static" / asset).is_file())

    def test_three_demo_questions(self):
        content = (ROOT / "src/self-assessment-prototype.md").read_text()
        result, output = self.build(content)
        self.assertEqual(result.returncode, 0, result.stdout)
        soup = BeautifulSoup((output / "index.html").read_text(), "html.parser")
        questions = soup.select("fieldset.dt-question")
        self.assertEqual(len(questions), 3)
        self.assertEqual(len({q["id"] for q in questions}), 3)

    def test_latex_fallback(self):
        result, output = self.build(QUESTION, "latex")
        self.assertEqual(result.returncode, 0, result.stdout)
        text = "\n".join(path.read_text() for path in output.glob("*.tex"))
        self.assertIn("Correct answer: (b).", text)
        self.assertIn("Nothing.", text)
        self.assertNotIn("<fieldset", text)

    def test_malformed_questions_fail_with_location(self):
        cases = [
            (QUESTION.replace(":correct: b\n", ""), ":correct:"),
            (QUESTION.replace(":correct: b", ":correct: a,b"), ":correct:"),
            (QUESTION.replace("- (b)", "- (a)"), "Duplicate choice"),
            (QUESTION.replace("- (a) Nothing.\n", ""), "at least two"),
            (QUESTION.replace("- (a) Nothing.", "- Nothing."), "must start"),
            (QUESTION.replace("- (a) Nothing.", "- (a) [Link](https://example.org)"), "Choices support"),
            (QUESTION.replace(":id: example", ":id: Bad ID"), ":id:"),
            (QUESTION + "\n" + QUESTION, "Duplicate question ID"),
            (QUESTION.replace("What balances **weight**?", "First paragraph.\n\nSecond paragraph."), "one question paragraph"),
        ]
        for content, message in cases:
            with self.subTest(message=message):
                result, _ = self.build(content)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stdout)
                self.assertIn("index:", result.stdout)


if __name__ == "__main__":
    unittest.main()
