"""The main module.
"""
import os
import shutil
import sys
from textnode import TextNode, TextType
from helpers import markdown_to_html_node, extract_title


def copy_directory_contents(source_dir, dest_dir):
    """Recursively copy all contents from source_dir to dest_dir.

    First, deletes all contents of dest_dir to ensure a clean copy.
    Copies all files and subdirectories recursively.

    Args:
        source_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Create fresh destination directory
    print(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir)

    # Recursively copy contents
    _copy_contents_recursive(source_dir, dest_dir)


def _copy_contents_recursive(source_dir, dest_dir):
    """Helper function to recursively copy directory contents.

    Args:
        source_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            # Copy file
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy2(source_path, dest_path)
        elif os.path.isdir(source_path):
            # Create subdirectory and recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.makedirs(dest_path)
            _copy_contents_recursive(source_path, dest_path)


def generate_page(from_path, template_path, dest_path, base_url="/"):
    """Generate an HTML page from a markdown file and a template.

    Args:
        from_path: Path to the source markdown file
        template_path: Path to the HTML template file
        dest_path: Path to the destination HTML file
        base_url: The base URL for the site
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path} (base_url: {base_url})")

    # Read markdown and template files
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()

    # Extract title
    title = extract_title(markdown)

    # Replace placeholders in template
    # Using .replace() for simplicity, assuming placeholders are exactly as below
    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", content_html)

    # Handle base_url for absolute links and images
    if base_url != "/":
        final_html = final_html.replace('href="/', f'href="{base_url}')
        final_html = final_html.replace('src="/', f'src="{base_url}')

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write final HTML to destination
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_url="/"):
    """Recursively generate HTML pages from all markdown files in a directory.

    Args:
        dir_path_content: Path to the content directory
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory
        base_url: The base URL for the site
    """
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)

        if os.path.isfile(source_path):
            if item.endswith(".md"):
                # Determine destination HTML path
                dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
                generate_page(source_path, template_path, dest_path, base_url)
        elif os.path.isdir(source_path):
            # Recursively handle subdirectory
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(source_path, template_path, new_dest_dir, base_url)


def main():
    """The main function."""
    base_url = "/"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    static_dir = "./static"
    docs_dir = "./docs"
    content_dir = "./content"
    template_path = "./template.html"

    print(f"Base URL: {base_url}")

    print("Copying static assets to docs directory...")
    copy_directory_contents(static_dir, docs_dir)

    print("Generating pages...")
    generate_pages_recursive(content_dir, template_path, docs_dir, base_url)


if __name__ == "__main__":
    main()
