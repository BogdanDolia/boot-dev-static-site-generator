"""The main module.
"""
from textnode import TextNode, TextType

def main():
    """The main function.
    """
    link_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(link_node)

if __name__ == "__main__":
    main()