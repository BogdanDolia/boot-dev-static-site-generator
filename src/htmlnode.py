"""A module for HTML tag nodes."""


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
