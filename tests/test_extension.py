# this_file: twardown-py/tests/test_extension.py
"""Tests for the Twardown Markdown extension."""

from markdown import Markdown

from twardown_py import TwardownExtension, makeExtension


def test_extension_creation():
    """Test that the extension can be created."""
    extension = makeExtension()
    assert extension is not None
    assert isinstance(extension, TwardownExtension)


def test_markdown_registration():
    """Test that the extension can be registered with Markdown."""
    md = Markdown()
    extension = makeExtension()
    extension.extendMarkdown(md)
    # Check that the extension has been properly configured
    assert hasattr(md, 'preprocessors')
    assert hasattr(md, 'parser')
    assert hasattr(md.parser, 'blockprocessors')


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
    md = Markdown(extensions=[makeExtension(
        filename="test.md", enable_toc=False, enable_meta=True)])
    text = "# Test\n\nSome content"
    md.convert(text)
    # Magic records should be in metadata, not in HTML
    assert hasattr(md, 'Meta')
    assert 'this_file' in md.Meta
    assert md.Meta['this_file'] == ['test.md']


def test_magic_record_preprocessor_with_existing_frontmatter():
    """Test that magic records are not added when frontmatter exists."""
    md = Markdown(extensions=[makeExtension(filename="test.md", enable_toc=False)])
    text = "---\ntitle: Test\n---\n\n# Test\n\nSome content"
    md.convert(text)
    # Should not add another magic record
    frontmatter_delimiter_count = 2
    assert text.count("---") == frontmatter_delimiter_count


def test_magic_record_preprocessor_with_existing_this_file():
    """Test that magic records are not added when this_file already exists."""
    md = Markdown(extensions=[makeExtension(filename="test.md", enable_toc=False)])
    text = "---\nthis_file: existing.md\n---\n\n# Test\n\nSome content"
    html = md.convert(text)
    # Should not add another magic record
    assert "this_file: test.md" not in html


def test_magic_record_preprocessor_disabled():
    """Test that magic records are not added when disabled."""
    md = Markdown(extensions=[makeExtension(
        filename="test.md", enable_magic_records=False, enable_toc=False)])
    text = "# Test\n\nSome content"
    html = md.convert(text)
    assert "this_file: test.md" not in html


def test_task_list_processor():
    """Test that task lists are processed correctly."""
    md = Markdown(extensions=[makeExtension(enable_toc=False)])
    text = "- [ ] Unchecked task\n- [x] Checked task"
    html = md.convert(text)
    assert 'class="task-list"' in html
    assert 'type="checkbox"' in html
    assert 'checked="checked"' in html


def test_task_list_processor_unchecked():
    """Test that unchecked tasks are processed correctly."""
    md = Markdown(extensions=[makeExtension(enable_toc=False)])
    text = "- [ ] Unchecked task"
    html = md.convert(text)
    assert 'class="task-list"' in html
    assert 'type="checkbox"' in html
    assert 'checked="checked"' not in html


def test_task_list_processor_with_text():
    """Test that task list text is preserved."""
    md = Markdown(extensions=[makeExtension(enable_toc=False)])
    text = "- [ ] Buy groceries\n- [x] Walk the dog"
    html = md.convert(text)
    assert "Buy groceries" in html
    assert "Walk the dog" in html


def test_task_list_processor_disabled():
    """Test that task lists are not processed when disabled."""
    md = Markdown(extensions=[makeExtension(enable_task_lists=False, enable_toc=False)])
    text = "- [ ] Unchecked task\n- [x] Checked task"
    html = md.convert(text)
    assert 'class="task-list"' not in html
    assert 'type="checkbox"' not in html


def test_tables_enabled():
    """Test that tables work when enabled."""
    md = Markdown(extensions=[makeExtension(
        enable_tables=True, enable_toc=False, enable_magic_records=False)])
    text = "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |"
    html = md.convert(text)
    assert "<table>" in html
    assert "<th>" in html
    assert "<td>" in html


def test_tables_disabled():
    """Test that tables don't work when disabled."""
    md = Markdown(extensions=[makeExtension(
        enable_tables=False, enable_toc=False, enable_magic_records=False)])
    text = "| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |"
    html = md.convert(text)
    assert "<table>" not in html


def test_fenced_code_enabled():
    """Test that fenced code blocks work when enabled."""
    md = Markdown(extensions=[makeExtension(
        enable_fenced_code=True, enable_toc=False, enable_magic_records=False)])
    text = "```python\nprint('hello')\n```"
    html = md.convert(text)
    assert "<pre>" in html
    assert "<code>" in html


def test_fenced_code_disabled():
    """Test that fenced code blocks don't work when disabled."""
    md = Markdown(extensions=[makeExtension(
        enable_fenced_code=False, enable_toc=False, enable_magic_records=False)])
    text = "```python\nprint('hello')\n```"
    html = md.convert(text)
    # Should not be processed as fenced code block (no <pre> tag)
    assert "<pre>" not in html
    # Should be processed as inline code instead
    assert "<code>" in html


def test_meta_enabled():
    """Test that metadata works when enabled."""
    md = Markdown(extensions=[makeExtension(
        enable_meta=True, enable_toc=False, enable_magic_records=False)])
    text = "---\ntitle: Test Document\nauthor: Test Author\n---\n\n# Content"
    md.convert(text)
    assert hasattr(md, 'Meta')
    assert 'title' in md.Meta
    assert md.Meta['title'] == ['Test Document']


def test_meta_disabled():
    """Test that metadata doesn't work when disabled."""
    md = Markdown(extensions=[makeExtension(
        enable_meta=False, enable_toc=False, enable_magic_records=False)])
    text = "---\ntitle: Test Document\nauthor: Test Author\n---\n\n# Content"
    html = md.convert(text)
    # Metadata should not be processed
    assert "title: Test Document" in html


def test_empty_input():
    """Test that empty input is handled correctly."""
    md = Markdown(extensions=[makeExtension(enable_toc=False, enable_magic_records=False)])
    text = ""
    html = md.convert(text)
    assert html == ""


def test_all_features_enabled():
    """Test that all features work together."""
    md = Markdown(extensions=[makeExtension(
        filename="test.md",
        enable_tables=True,
        enable_fenced_code=True,
        enable_meta=True,
        enable_task_lists=True,
        enable_magic_records=True,
        enable_toc=False
    )])
    text = """# Test Document

- [ ] Task 1
- [x] Task 2

```python
print('hello')
```

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
    html = md.convert(text)
    assert 'class="task-list"' in html
    assert 'type="checkbox"' in html
    assert "<pre>" in html
    assert "<table>" in html
    # Magic records should be in metadata
    assert hasattr(md, 'Meta')
    assert 'this_file' in md.Meta
    assert md.Meta['this_file'] == ['test.md']


def test_version_import():
    """Test that version can be imported."""
    from twardown_py import __version__  # noqa: PLC0415
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0
