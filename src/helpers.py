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
    return new_nodes
