"""Twardown Markdown extension for Python-Markdown."""

# this_file: twardown-py/src/twardown_py/__init__.py

try:
    from importlib.metadata import version as _version
except ImportError:
    # Python < 3.8
    from importlib_metadata import version as _version  # type: ignore

try:
    __version__ = _version("twardown_py")
except Exception:
    # Fallback version for development
    __version__ = "0.0.0+dev"

from typing import Any
from xml.etree import ElementTree

from markdown import Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.meta import MetaExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.preprocessors import Preprocessor


class MagicRecordPreprocessor(Preprocessor):
    """Preprocessor for handling magic record comments."""

    def __init__(self, md: Markdown, filename: str):
        """Initialize the preprocessor with the markdown instance and filename."""
        super().__init__(md)
        self.filename = filename

    def run(self, lines: list[str]) -> list[str]:
        """Process the document and add magic record if needed."""
        # Skip if no lines
        if not lines:
            return lines

        # Check if the first line is a magic record
        if lines[0].strip() == "---":
            for line in lines[1:]:
                if line.strip() == "---":
                    # Found the end of frontmatter, no need to add magic record
                    return lines
                if line.strip().startswith("this_file:"):
                    # Found existing magic record, no need to add
                    return lines

        # If we get here, we need to add the magic record
        return [
            "---",
            f"this_file: {self.filename}",
            "---",
            "",
            *lines,
        ]


class TaskListProcessor(BlockProcessor):
    """Block processor for handling task lists."""

    def test(self, parent: ElementTree.Element, block: str) -> bool:
        """Test if the block is a task list item."""
        return block.strip().startswith("- [ ]") or block.strip().startswith("- [x]")

    def run(self, parent: ElementTree.Element, blocks: list[str]) -> None:
        """Process task list items."""
        block = blocks.pop(0)
        ul = ElementTree.SubElement(parent, "ul", {"class": "task-list"})

        for line in block.split("\n"):
            if line.strip().startswith("- [ ]"):
                li = ElementTree.SubElement(ul, "li", {"class": "task-list-item"})
                ElementTree.SubElement(li, "input", {"type": "checkbox"})
                text = line[5:].strip()
                if text:
                    li.text = text
            elif line.strip().startswith("- [x]"):
                li = ElementTree.SubElement(ul, "li", {"class": "task-list-item"})
                ElementTree.SubElement(li, "input", {"type": "checkbox", "checked": "checked"})
                text = line[5:].strip()
                if text:
                    li.text = text


class TwardownExtension(Extension):
    """Extension for Twardown Markdown flavor."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the extension with configuration options.

        Args:
            **kwargs: Configuration options for the extension.
                     Supported options:
                     - filename: The name of the file being processed
                     - enable_tables: Enable table support (default: True)
                     - enable_fenced_code: Enable fenced code blocks (default: True)
                     - enable_code_highlighting: Enable code highlighting (default: True)
                     - enable_toc: Enable table of contents (default: True)
                     - enable_meta: Enable metadata (default: True)
                     - enable_task_lists: Enable task lists (default: True)
                     - enable_magic_records: Enable magic records (default: True)
        """
        self.config = {
            "filename": ["", "Name of the file being processed"],
            "enable_tables": [True, "Enable table support"],
            "enable_fenced_code": [True, "Enable fenced code blocks"],
            "enable_code_highlighting": [True, "Enable code highlighting"],
            "enable_toc": [True, "Enable table of contents"],
            "enable_meta": [True, "Enable metadata"],
            "enable_task_lists": [True, "Enable task lists"],
            "enable_magic_records": [True, "Enable magic records"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:  # noqa: N802
        """Register all the extensions that make up the Twardown flavor.

        This method registers the core extensions (tables, fenced code, etc.)
        and our custom processors for magic records and task lists.

        Args:
            md: The Markdown instance to extend.
        """
        # Create and register core extensions if enabled
        if self.getConfig("enable_meta"):
            meta_ext = MetaExtension()
            meta_ext.extendMarkdown(md)
        if self.getConfig("enable_tables"):
            table_ext = TableExtension()
            table_ext.extendMarkdown(md)
        if self.getConfig("enable_fenced_code"):
            fenced_ext = FencedCodeExtension()
            fenced_ext.extendMarkdown(md)
        if self.getConfig("enable_code_highlighting"):
            codehilite_ext = CodeHiliteExtension()
            codehilite_ext.extendMarkdown(md)
        if self.getConfig("enable_toc"):
            toc_ext = TocExtension()
            toc_ext.extendMarkdown(md)

        # Register custom processors
        if self.getConfig("enable_magic_records"):
            md.preprocessors.register(
                MagicRecordPreprocessor(md, self.getConfig("filename")),
                "magic_record",
                175,  # After meta, before everything else
            )
        if self.getConfig("enable_task_lists"):
            md.parser.blockprocessors.register(
                TaskListProcessor(md.parser),
                "task_list",
                175,  # After lists, before everything else
            )


def makeExtension(**kwargs: Any) -> TwardownExtension:  # noqa: N802
    """Create an instance of the Twardown extension."""
    return TwardownExtension(**kwargs)
