from pathlib import Path
from typing import Dict, Optional

from bs4 import BeautifulSoup
from sphinx.application import Sphinx
from sphinx.config import Config


def normalize_repository_branch(app: Sphinx, config: Config) -> None:
    branch = config.html_theme_options.get("repository_branch")
    if branch is not None:
        # The book builder injects branches as absolute paths.
        config.html_theme_options["repository_branch"] = branch.lstrip("/")


def open_repository_links_in_new_tabs(
    app: Sphinx, exception: Optional[Exception]
) -> None:
    if exception is not None or app.builder.format != "html":
        return

    for html_path in Path(app.outdir).rglob("*.html"):
        html = html_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "lxml")
        links = soup.select(".menu-dropdown-repository-buttons a.headerbtn")
        if not links:
            continue

        for link in links:
            link["target"] = "_blank"
            link["rel"] = list(
                dict.fromkeys(
                    link.get_attribute_list("rel", []) + ["noopener", "noreferrer"]
                )
            )

        updated_html = str(soup)
        if updated_html != html:
            html_path.write_text(updated_html, encoding="utf-8")


def setup(app: Sphinx) -> Dict[str, bool]:
    app.connect("config-inited", normalize_repository_branch)
    app.connect("build-finished", open_repository_links_in_new_tabs)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
