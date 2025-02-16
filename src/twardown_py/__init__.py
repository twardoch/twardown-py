"""
twardown_py - Python plugin for the Python Markdown ecosystem that provides an opinionated Markdown flavor
"""

__version__ = "0.1.0"

from typing import Any, Dict, Optional
from markdown import Markdown
from markdown.extensions import Extension


class TwardownExtension(Extension):
    """
    A Markdown extension that implements the Twardown flavor.
    """

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        self.config = {
            "option_name": ["default_value", "Description of the option"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        """
        Register all the extensions that make up the Twardown flavor.

        Args:
            md: The Markdown instance to extend
        """
        # TODO: Add actual extension registration here
        pass


def makeExtension(**kwargs: Dict[str, Any]) -> TwardownExtension:
    """
    Return an instance of the TwardownExtension
    """
    return TwardownExtension(**kwargs)
