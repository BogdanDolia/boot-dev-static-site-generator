"""A module for HTML tag nodes."""

from textnode import TextNode, TextType


class HTMLNode:
    """A node in the HTML tree."""

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        """Return the HTML representation of the node."""
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        """Return the HTML representation of the node's properties."""
        if self.props is None:
            return ""

        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        """Return a string representation of the node."""
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={len(self.children)}, props={self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
                self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props
        )


class LeafNode(HTMLNode):
    """A leaf node in the HTML tree."""

    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        """Return the HTML representation of the node."""
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        else:
            props_html = self.props_to_html()
            if props_html:
                return f"<{self.tag} {props_html}>{self.value}</{self.tag}>"
            return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        """Return a string representation of the node."""
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props})"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
                self.tag == other.tag
                and self.value == other.value
                and self.props == other.props
        )

    @staticmethod
    def text_node_to_html_node(text_node: TextNode) -> "LeafNode":
        """Convert a text node to an HTML node."""
        if text_node.text_type is None or text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)

        type_mapping = {
            TextType.BOLD: ("b", text_node.text, None),
            TextType.ITALIC: ("i", text_node.text, None),
            TextType.CODE: ("code", text_node.text, None),
            TextType.LINK: ("a", text_node.text, {"href": text_node.url}),
            TextType.IMAGE: ("img", "", {"src": text_node.url, "alt": text_node.text}),
        }

        if text_node.text_type not in type_mapping:
            raise ValueError(f"Unsupported text type: {text_node.text_type}")

        tag, value, props = type_mapping[text_node.text_type]
        return LeafNode(tag, value, props)


class ParentNode(HTMLNode):
    """A parent node in the HTML tree."""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        """Return the HTML representation of the node."""
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")
        props_html = self.props_to_html()
        children_html = self.children_to_html()
        if props_html:
            return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"

    def children_to_html(self):
        """Return the HTML representation of the node's children."""
        return "".join([child.to_html() for child in self.children])
