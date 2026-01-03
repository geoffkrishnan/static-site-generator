from copy_static import copy_static
from generate_page import generate_pages_recur
from pathlib import Path
import sys


def main():
    # get the base path from cli arg if given else default to /
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_static()
    root = Path(__file__).parent.parent

    content_dir = root / "content"
    public_dir = root / "docs"
    template_path = root / "template.html"
    generate_pages_recur(content_dir, template_path, public_dir, base_path)


if __name__ == "__main__":
    main()
