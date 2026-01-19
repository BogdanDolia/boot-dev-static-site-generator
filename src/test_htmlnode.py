"""Test the HTMLNode class."""

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    """Test the HTMLNode class."""

    # HTMLNode tests
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

    # LeafNode tests
    def test_leaf_to_html_p(self):
        """Test the HTML representation of a leaf node with a p tag."""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        """Test the HTML representation of a leaf node with a span tag."""
        node = LeafNode("span", "Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")

    def test_leaf_to_html_none(self):
        """Test the HTML representation of a leaf node with a none tag."""
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_none_tag(self):
        """Test the HTML representation of a leaf node with a none tag."""
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # ParentNode tests
    def test_to_html_with_children(self):
        """Test the HTML representation of a parent node with a child node."""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test the HTML representation of a parent node with a grandchild node."""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_props(self):
        """Test the HTML representation of a parent node with properties."""
        parent_node = ParentNode("div", [], props={"class": "test"})
        self.assertEqual(parent_node.to_html(), '<div class="test"></div>')

    def test_to_html_with_no_children(self):
        """Test the HTML representation of a parent node with no children."""
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    # text_node_to_html_node tests
    def test_text(self):
        """Test the conversion of a text node to an HTML node."""
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_none_type(self):
        """Test the conversion of a text node with None type to an HTML node."""
        node = TextNode("Plain text", None)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Plain text")

    def test_text_node_bold(self):
        """Test the conversion of a bold text node to an HTML node."""
        node = TextNode("Bold text", TextType.BOLD)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, {})

    def test_text_node_italic(self):
        """Test the conversion of an italic text node to an HTML node."""
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, {})

    def test_text_node_code(self):
        """Test the conversion of a code text node to an HTML node."""
        node = TextNode("print('hello')", TextType.CODE)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, {})

    def test_text_node_link(self):
        """Test the conversion of a link text node to an HTML node."""
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_image(self):
        """Test the conversion of an image text node to an HTML node."""
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png"})

    def test_text_node_empty_string(self):
        """Test the conversion of a text node with empty string."""
        node = TextNode("", TextType.TEXT)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

    def test_text_node_special_characters(self):
        """Test the conversion of a text node with special characters."""
        node = TextNode("Hello & <world>", TextType.BOLD)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello & <world>")

    def test_text_node_link_complex_url(self):
        """Test the conversion of a link text node with complex URL."""
        node = TextNode(
            "Search", TextType.LINK, "https://example.com/search?q=test&page=1"
        )
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Search")
        self.assertEqual(
            html_node.props["href"], "https://example.com/search?q=test&page=1"
        )
