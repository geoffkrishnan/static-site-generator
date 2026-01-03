from markdown_to_html import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, dest_path, template_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md = from_path.read_text()
    template = template_path.read_text()

    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    dest_path.write_text(page)
