import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(matches, expected)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertEqual(matches, [])

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertEqual(matches, [("", "https://example.com/image.png")])

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("This is a [link](https://www.example.com)")
        self.assertEqual(matches, [("link", "https://www.example.com")])

    def test_extract_markdown_links_multiple(self):
        text = "Check out [Google](https://google.com) and [GitHub](https://github.com)"
        matches = extract_markdown_links(text)
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertEqual(matches, [])

    def test_extract_markdown_links_ignores_images(self):
        # Links should NOT match image
        text = "This has ![an image](https://img.com) but not a link"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_images_ignores_links(self):
        # Images should NOT match link
        text = "This has [a link](https://example.com) but not an image"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_both_mixed(self):
        text = "![image](https://img.com) and [link](https://example.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(images, [("image", "https://img.com")])
        self.assertEqual(links, [("link", "https://example.com")])
