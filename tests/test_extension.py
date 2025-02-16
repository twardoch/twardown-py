# this_file: twardown-py/tests/test_extension.py
"""Tests for the Twardown Markdown extension."""

from markdown import Markdown

from twardown_py import makeExtension


def test_extension_creation():
    """Test that the extension can be created."""
    extension = makeExtension()
    assert extension is not None


def test_markdown_registration():
    """Test that the extension can be registered with Markdown."""
    md = Markdown()
    extension = makeExtension()
    extension.extendMarkdown(md)
    assert extension in md.registeredExtensions


def test_extension_with_config():
    """Test that the extension can be created with configuration."""
    config = {
        "filename": "test.md",
        "enable_tables": True,
        "enable_fenced_code": True,
        "enable_code_highlighting": True,
        "enable_toc": False,  # Disable TOC to avoid initialization issues
        "enable_meta": True,
        "enable_task_lists": True,
        "enable_magic_records": True,
    }
    extension = makeExtension(**config)
    assert extension.getConfig("filename") == "test.md"
    assert extension.getConfig("enable_tables") is True


def test_magic_record_preprocessor():
    """Test that magic records are added correctly."""
    md = Markdown(extensions=[makeExtension(filename="test.md", enable_toc=False)])
    text = "# Test\n\nSome content"
    html = md.convert(text)
    assert "this_file: test.md" in html


def test_task_list_processor():
    """Test that task lists are processed correctly."""
    md = Markdown(extensions=[makeExtension(enable_toc=False)])
    text = "- [ ] Unchecked task\n- [x] Checked task"
    html = md.convert(text)
    assert 'class="task-list"' in html
    assert 'type="checkbox"' in html
    assert 'checked="checked"' in html
