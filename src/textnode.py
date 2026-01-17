"""A module for text nodes.
"""
from enum import Enum

class TextType(Enum):
    """The type of text node.
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """A node in the text tree.
    """
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def  __eq__(self, other):
        """Check if two text nodes are equal.
        """
        return self.text == other.text and \
            self.text_type == other.text_type and \
                self.url == other.url

    def __repr__(self):
        """Return a string representation of the text node.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
