"""Test the HTMLNode class."""

import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    """Test the HTMLNode class."""

    def test_eq(self):
        """Test the equality of two HTML nodes."""
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a text node")
        print(node)
        print(node2)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        """Test the inequality of two HTML nodes."""
        node = HTMLNode("p", "This is a text node")
        node2 = HTMLNode("p", "This is a different text node")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        """Test the string representation of an HTML node."""
        node = HTMLNode("p", "This is a text node")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag='p', value='This is a text node', children=0, props={})",
        )

    def test_props_to_html(self):
        """Test the HTML representation of an HTML node's properties."""
        node = HTMLNode("p", "This is a text node", props={"class": "test"})
        self.assertEqual(node.props_to_html(), 'class="test"')
