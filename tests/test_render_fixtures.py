# this_file: tests/test_render_fixtures.py
"""Render fixtures pinning the twardown flavor's expected output substrings.

Each fixture is a (source, must_contain) pair. These act as a lightweight
conformance suite: given a Markdown source, rendering with the full twardown
flavor must produce HTML containing every listed substring.
"""

import markdown
import pytest

from twardown_py import makeExtension

RENDER_FIXTURES = [
    pytest.param(
        "- [x] Done\n- [ ] Todo",
        ['class="task-list"', 'class="task-list-item"', 'checked="checked"'],
        id="task-list",
    ),
    pytest.param(
        "| A | B |\n|---|---|\n| 1 | 2 |",
        ["<table>", "<th>A</th>", "<td>1</td>"],
        id="table",
    ),
    pytest.param(
        "```python\nprint('hi')\n```",
        ["<pre>", "<code>"],
        id="fenced-code",
    ),
    pytest.param(
        "# Heading\n\nParagraph.",
        ["<h1", "Heading", "<p>Paragraph.</p>"],
        id="heading-and-paragraph",
    ),
]


@pytest.mark.parametrize(("source", "must_contain"), RENDER_FIXTURES)
def test_render_fixture(source: str, must_contain: list[str]) -> None:
    """The rendered HTML must contain each expected substring."""
    html = markdown.markdown(source, extensions=[makeExtension(enable_toc=False)])
    for needle in must_contain:
        assert needle in html, f"expected {needle!r} in rendered output:\n{html}"


def test_this_file_record_lands_in_meta() -> None:
    """The this_file magic record is injected into metadata, not the HTML body."""
    md = markdown.Markdown(extensions=[makeExtension(filename="doc.md", enable_toc=False)])
    md.convert("Body text with no frontmatter.")
    assert md.Meta["this_file"] == ["doc.md"]


def test_existing_this_file_is_not_overwritten() -> None:
    """A document that already declares this_file keeps its own value."""
    md = markdown.Markdown(extensions=[makeExtension(filename="injected.md", enable_toc=False)])
    md.convert("---\nthis_file: original.md\n---\n\nBody.")
    assert md.Meta["this_file"] == ["original.md"]
