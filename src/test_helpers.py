from textnode import TextNode, TextType
from helpers import split_nodes_delimiter, extract_markdown_images
import unittest


class TestHelpers(unittest.TestCase):
    """Test the helpers module."""

    def test_split_nodes_delimiter(self):
        """Test the split_nodes_delimiter function."""
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("`code block`", TextType.CODE)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_bold(self):
        """Test splitting with bold delimiter."""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        """Test splitting with italic delimiter."""
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_no_delimiter(self):
        """Test with text that has no delimiter."""
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("Plain text with no delimiters", TextType.TEXT)],
        )

    def test_split_nodes_delimiter_multiple_sections(self):
        """Test with multiple delimited sections."""
        node = TextNode("Start `code1` middle `code2` end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" middle ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_empty_list(self):
        """Test with empty input list."""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_split_nodes_delimiter_unmatched_raises(self):
        """Test that unmatched delimiter raises ValueError."""
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_at_start(self):
        """Test delimiter at start of text."""
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" at start", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_at_end(self):
        """Test delimiter at end of text."""
        node = TextNode("text ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text ends with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_split_nodes_delimiter_multiple_text_nodes(self):
        """Test with multiple TEXT nodes in input list."""
        node1 = TextNode("First `code1` text", TextType.TEXT)
        node2 = TextNode("Second `code2` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" text", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_extract_markdown_images(self):
        """Test the extract_markdown_images function."""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_images_no_images(self):
        """Test with text containing no images."""
        text = "This is text with no images."
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_images_with_links(self):
        """Test that it doesn't extract normal links as images."""
        text = "This is a [link](https://www.google.com) and an ![image](https://i.imgur.com/z39yRDC.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [("image", "https://i.imgur.com/z39yRDC.png")],
        )


if __name__ == "__main__":
    unittest.main()
