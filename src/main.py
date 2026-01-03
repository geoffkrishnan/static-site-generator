from copy_static import copy_static
from generate_page import generate_pages_recur
from pathlib import Path


def main():
    copy_static()
    root = Path(__file__).parent.parent

    content_dir = root / "content"
    public_dir = root / "public"
    template_path = root / "template.html"
    generate_pages_recur(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()
