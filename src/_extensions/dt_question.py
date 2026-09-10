"""Book-local single-answer self-assessment; no runtime dependencies beyond Sphinx."""

import re
from html import escape

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.errors import SphinxError
from sphinx.util.docutils import SphinxDirective


class Question(nodes.General, nodes.Element):
    pass


class Legend(nodes.Inline, nodes.TextElement):
    pass


class Choice(nodes.Inline, nodes.TextElement):
    pass


class QuestionError(SphinxError):
    category = "dt-question error"


class DTQuestion(SphinxDirective):
    has_content = True
    option_spec = {
        "correct": directives.unchanged_required,
        "id": directives.unchanged_required,
        "feedback-correct": directives.unchanged_required,
        "feedback-incorrect": directives.unchanged_required,
    }

    def fail(self, message):
        raise QuestionError(f"{self.env.docname}:{self.lineno}: {message}")

    def run(self):
        parsed = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, parsed)
        if (len(parsed) != 2 or not isinstance(parsed[0], nodes.paragraph)
                or not isinstance(parsed[1], nodes.bullet_list)):
            self.fail("Expected one question paragraph followed by a bullet list.")

        choices = []
        for item in parsed[1]:
            if len(item) != 1 or not isinstance(item[0], nodes.paragraph):
                self.fail("Each choice must be a single paragraph starting with (a), (b), etc.")
            paragraph = item[0]
            first = paragraph[0] if len(paragraph) else None
            match = re.match(r"^\(([a-z])\)\s+", str(first)) if isinstance(first, nodes.Text) else None
            if not match:
                self.fail("Each choice must start with a lowercase letter in parentheses, e.g. (a).")
            key = match[1]
            if key in [entry[0] for entry in choices]:
                self.fail(f"Duplicate choice label ({key}).")
            paragraph[0] = nodes.Text(str(first)[match.end():])
            if not paragraph.astext().strip():
                self.fail(f"Choice ({key}) must not be empty.")
            # A label cannot contain links, images, or nested interactive content.
            allowed = (nodes.Text, nodes.emphasis, nodes.strong, nodes.literal,
                       nodes.superscript, nodes.subscript)
            if any(not isinstance(child, allowed) for child in paragraph.traverse(include_self=False)):
                self.fail("Choices support text, emphasis, and inline code only.")
            choices.append((key, paragraph))
        if len(choices) < 2:
            self.fail("Provide at least two choices.")
        correct = self.options.get("correct", "")
        if correct not in [key for key, _ in choices]:
            self.fail(":correct: must name exactly one existing choice label.")

        stable_id = self.options.get("id")
        if stable_id is not None and not re.fullmatch(r"[a-z][a-z0-9-]*", stable_id):
            self.fail(":id: must start with a lowercase letter and contain only a-z, 0-9, and hyphens.")
        if stable_id:
            qid = f"dt-question-{stable_id}"
            if qid in self.state.document.ids:
                self.fail(f"Duplicate question ID: {stable_id}.")
        else:
            qid = f"dt-question-auto-{self.env.new_serialno('dt-question')}"
            while qid in self.state.document.ids:
                qid = f"dt-question-auto-{self.env.new_serialno('dt-question')}"

        question = Question(ids=[qid], correct=correct,
                            feedback_correct=self.options.get("feedback-correct", "That is the correct choice."),
                            feedback_incorrect=self.options.get("feedback-incorrect", "Try again."))
        self.set_source_info(question)
        self.state.document.note_explicit_target(question)
        legend = Legend()
        legend.extend(parsed[0].children)
        question += legend
        options = nodes.bullet_list(classes=["dt-question-options"])
        for key, paragraph in choices:
            choice = Choice(key=key, group=qid)
            choice.extend(paragraph.children)
            options += nodes.list_item("", nodes.paragraph("", "", choice))
        question += options
        return [question]


def visit_question(self, node):
    self.body.append(self.starttag(node, "fieldset", CLASS="dt-question"))


def depart_question(self, node):
    # Answers necessarily ship to the browser. No obfuscation or security claim.
    correct = escape(node["correct"], quote=True)
    good = escape(node["feedback_correct"], quote=True)
    bad = escape(node["feedback_incorrect"], quote=True)
    self.body.append(
        '<button type="button" class="dt-question-check" hidden>Check answer</button>'
        '<p class="dt-question-status" role="status" aria-live="polite" aria-atomic="true"></p>'
        f'<details class="dt-question-solution" data-answer="{correct}" '
        f'data-feedback-correct="{good}" data-feedback-incorrect="{bad}">'
        '<summary>Answer and explanation</summary>'
        f'<p>Correct answer: ({correct}). {good}</p></details></fieldset>'
    )


def visit_legend(self, node):
    self.body.append("<legend>")


def depart_legend(self, node):
    self.body.append("</legend>")


def visit_choice(self, node):
    group, key = escape(node["group"], quote=True), escape(node["key"], quote=True)
    self.body.append(f'<label><input type="radio" name="{group}" value="{key}" disabled> ({key}) ')


def depart_choice(self, node):
    self.body.append("</label>")


def readable_fallback(app, doctree, docname):
    if app.builder.format == "html":
        return
    for question in list(doctree.traverse(Question)):
        fallback = nodes.container(ids=question["ids"])
        prompt = nodes.paragraph()
        prompt.extend(child.deepcopy() for child in question[0].children)
        fallback += prompt
        options = nodes.bullet_list()
        for choice in question.traverse(Choice):
            paragraph = nodes.paragraph("", f'({choice["key"]}) ')
            paragraph.extend(child.deepcopy() for child in choice.children)
            options += nodes.list_item("", paragraph)
        fallback += options
        fallback += nodes.paragraph("", f'Correct answer: ({question["correct"]}). {question["feedback_correct"]}')
        question.replace_self(fallback)


def setup(app):
    app.add_node(Question, html=(visit_question, depart_question))
    app.add_node(Legend, html=(visit_legend, depart_legend))
    app.add_node(Choice, html=(visit_choice, depart_choice))
    app.add_directive("dt-question", DTQuestion)
    app.add_js_file("dt-question.js")
    app.add_css_file("dt-question.css")
    app.connect("doctree-resolved", readable_fallback)
    return {"version": "0.1.0", "parallel_read_safe": True, "parallel_write_safe": True}
