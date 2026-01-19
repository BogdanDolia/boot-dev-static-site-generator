"""Test the TextNode class."""

import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    """Test the TextNode class."""

    def test_eq(self):
        """Test the equality of two text nodes."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        """Test the string representation of a text node."""
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_url_is_none(self):
        """Test that the url is None if not provided."""
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_url_is_not_none(self):
        """Test that the url is None if not provided."""
        node = TextNode(
            "This is some anchor text", TextType.LINK, "https://www.boot.dev"
        )
        self.assertIsNotNone(node.url)

    def test_not_eq(self):
        """Test the equality of two text nodes."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode(
            "This is some anchor text", TextType.LINK, "https://www.boot.dev"
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
