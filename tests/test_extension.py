"""
Tests for the Twardown extension
"""

import pytest
from markdown import Markdown
from twardown_py import TwardownExtension, makeExtension


def test_extension_creation():
    """Test that the extension can be created"""
    ext = TwardownExtension()
    assert isinstance(ext, TwardownExtension)


def test_make_extension():
    """Test the makeExtension function"""
    ext = makeExtension()
    assert isinstance(ext, TwardownExtension)


def test_markdown_registration():
    """Test that the extension can be registered with Markdown"""
    md = Markdown(extensions=[TwardownExtension()])
    assert any(isinstance(ext, TwardownExtension) for ext in md.registeredExtensions)
