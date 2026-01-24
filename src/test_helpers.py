from textnode import TextNode, TextType
from helpers import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node,
)
import unittest


class TestHelpers(unittest.TestCase):
    """Test the helpers' module."""

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
                node2,
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

    def test_extract_markdown_links(self):
        """Test the extract_markdown_links function."""
        text = "This is text with a [link](https://www.google.com) and [another](https://www.example.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("link", "https://www.google.com"),
                ("another", "https://www.example.com"),
            ],
        )

    def test_extract_markdown_links_no_links(self):
        """Test with text containing no links."""
        text = "This is text with no links."
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links_with_images(self):
        """Test that it doesn't extract images as links."""
        text = "This is a [link](https://www.google.com) and an ![image](https://i.imgur.com/z39yRDC.png)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [("link", "https://www.google.com")],
        )

    def test_split_nodes_delimiter_preserves_other_types(self):
        """Test that non-TEXT nodes are preserved."""
        node1 = TextNode("Already bold", TextType.BOLD)
        node2 = TextNode("text with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                node1,
                TextNode("text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_split_images_boot_dev(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image(self):
        """Test the split_nodes_image function."""
        node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_edge_cases(self):
        """Test split_nodes_image with edge cases."""
        node = TextNode(
            "![image](https://example.com/image.png) is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" is at the start", TextType.TEXT),
            ],
        )

        node2 = TextNode(
            "image is at the end ![end](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes2 = split_nodes_image([node2])
        self.assertEqual(
            new_nodes2,
            [
                TextNode("image is at the end ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
        )

    def test_split_nodes_link(self):
        """Test the split_nodes_link function."""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to google](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to google", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_preserves_other_nodes(self):
        """Test that split_nodes_image preserves other node types."""
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = TextNode("Image ![img](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                node1,
                TextNode("Image ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
            ],
        )

    def test_split_nodes_link_preserves_other_nodes(self):
        """Test that split_nodes_link preserves other node types."""
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = TextNode("Link [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                node1,
                TextNode("Link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_order_code_protection(self):
        """Ensure code blocks protect their content from other delimiters."""
        text = "Text with `**not bold**` and `*not italic*`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("**not bold**", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("*not italic*", TextType.CODE),
            ],
            nodes,
        )

    def test_text_to_textnodes_order_bold_before_italic(self):
        """Ensure bold is processed before italic to avoid conflict with **."""
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_order_link_protection(self):
        """Ensure links/images don't get split by earlier text delimiters incorrectly, 
        or rather how the current order handles them.
        In current order (Bold then Link), **[link](url)** becomes BOLD node.
        If Link was first, it would be LINK node.
        """
        text = "This is **[link](url)**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("[link](url)", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_order_italic_vs_link(self):
        """Test italic vs link order."""
        text = "This is *[link](url)*"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("[link](url)", TextType.ITALIC),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading_levels(self):
        cases = [
            ("# Heading", BlockType.HEADING),
            ("## Heading", BlockType.HEADING),
            ("###### Heading", BlockType.HEADING),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(block_to_block_type(text), expected)

    def test_block_to_block_type_heading_requires_space(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_max_level(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block(self):
        text = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_block_to_block_type_code_block_requires_newline(self):
        text = "```code here\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_block_to_block_type_quote_block(self):
        text = "> line one\n> line two"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_block_to_block_type_quote_requires_space(self):
        text = ">line one\n> line two"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        text = "- item one\n- item two"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_requires_dash(self):
        text = "* item one\n- item two"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        text = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_requires_sequence(self):
        text = "1. item one\n3. item two"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_fallback(self):
        text = "Just a normal paragraph\nwith two lines"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here
    
    This is another paragraph with _italic_ text and `code` here
    
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title(self):
        from helpers import extract_title
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

        markdown = "#  Hello   "
        self.assertEqual(extract_title(markdown), "Hello")

        markdown = "## Hello\n# World"
        self.assertEqual(extract_title(markdown), "World")

        with self.assertRaises(ValueError):
            extract_title("Hello")


if __name__ == "__main__":
    unittest.main()
