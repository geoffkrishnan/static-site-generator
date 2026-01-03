from copy_static import copy_static
from generate_page import generate_page
from pathlib import Path


def main():
    copy_static()
    root = Path(__file__).parent.parent
    from_path = root / "content" / "index.md"
    dest_path = root / "public" / "index.html"
    template_path = root / "template.html"
    generate_page(from_path, dest_path, template_path)


if __name__ == "__main__":
    main()
