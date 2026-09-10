# Template: template-book

This template provides a boilerplate repository for books in Duckietown.


## What to change

These are the fields you **must** update to create your book.


### Placeholders in `src/_config.yml`

This file configures the build of the book.
Replace the placeholder string `BOOK_NAME_HERE` (there should be two separate instances of it) with
the name of the repository hosting your book (e.g., `book-devmanual-docs`).


### Structure in `src/_toc.yml`

Use the instructions [here](https://jupyterbook.org/en/stable/structure/toc.html#structure-of-a-book)
to learn how to structure your book using the Table of Contents file `_toc.yml`.
A simple example is already provided by this template. Adapt it to your needs.


### Logo in `src/logo.png`

There is a default logo in `src/logo.png`. This is the book's logo, change it with something that 
reflects the scope of your book. Transparent PNGs are recommended.


## Build

You can build this book by running the command,

```shell
dts docs build
```

## Self-assessment prototype (v0.1)

The book-local `dt-question` extension is registered through
`sphinx.local_extensions` in `src/_config.yml`. It requires no shared builder
changes or new production dependencies. Try the **Self-assessment prototype**
page under **Prototype** for three complete examples.

````markdown
```{dt-question}
:id: steady-hover
:correct: b
:feedback-correct: In steady hover, thrust balances weight.
:feedback-incorrect: Consider the vertical force balance.

What balances the drone's weight in steady hover?

- (a) Zero thrust.
- (b) Upward thrust.
```
````

Use one question paragraph followed by at least two single-paragraph bullets.
Each choice starts with a unique lowercase label `(a)` through `(z)`; `correct`
must name exactly one label. Choices accept text, emphasis, and inline code;
links, images, and nested blocks are rejected. Feedback options are plain text
and optional. There are no nested feedback directives in v0.1.

An optional `id` accepts lowercase letters, digits, and hyphens, starting with a
letter. It creates a page-local `#dt-question-ID` anchor. Keep explicit IDs unique
within the page; omit `id` for an automatically generated anchor that may change
when questions are reordered. Avoid explicit IDs starting with `auto-`.

Without JavaScript (including a failed asset load), questions remain readable
with disabled radio buttons and an expandable answer/explanation. JavaScript
enables the radios and Check answer button and supplies live feedback. Non-HTML
builders receive ordinary paragraphs, choices, and the answer explanation.

This is practice, not secure assessment: answers ship in the HTML, and users can
inspect them. The extension performs no network requests, storage, analytics,
authentication, grading, or score reporting. Existing shared-builder tracking is
outside this component. Reloading starts a fresh attempt.

Build with `dts docs build` as described above. Tests can run in the existing builder image:

```shell
docker run --rm --network none --entrypoint /bin/bash \
  -v "$PWD:/book:ro" -w /book duckietown/dt-jupyter-book:ente-arm64v8 \
  -c 'source /environment.sh && python3 -m unittest discover -s tests -v'
```

Use the matching architecture tag on non-ARM hosts. Tests cover the actual YAML
local-extension registration, generated HTML/assets, the three examples, invalid
authoring, and LaTeX fallback. The optional browser check needs Playwright in the
development environment (it is not a book dependency):

```shell
node tests/dt-question.browser.cjs http://127.0.0.1:8765/self-assessment-prototype.html
```

Serve the generated HTML locally before running the browser check. It exercises
keyboard input, empty selection, retry feedback, independent radio groups,
reload behavior, mobile width, and JavaScript-disabled reading. It blocks external
theme requests during testing. Screen-reader behavior and PDF printing still
need manual review before promoting the component to the shared builder.
