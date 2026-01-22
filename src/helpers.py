import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Split the nodes into a list of nodes delimited by the delimiter."""
    new_nodes = []
    for node in old_nodes:
        if node.text_type is None or node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError(f"Invalid markdown: unmatched delimiter '{delimiter}'")
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extract alt text and URL of Markdown images from text."""
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract Markdown links from text."""
    return re.findall(r"(?<!!)\[(.*?)]\((.*?)\)", text)
