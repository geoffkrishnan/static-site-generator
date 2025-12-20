import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        result = [(m.group("alt"), m.group("url")) for m in matches]
        self.assertEqual(result, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        result = [(m.group("alt"), m.group("url")) for m in matches]
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images")
        result = [(m.group("alt"), m.group("url")) for m in matches]
        self.assertEqual(result, [])

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        result = [(m.group("alt"), m.group("url")) for m in matches]
        self.assertEqual(result, [("", "https://example.com/image.png")])

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("This is a [link](https://www.example.com)")
        result = [(m.group("alt"), m.group("url")) for m in matches]
        self.assertEqual(result, [("link", "https://www.example.com")])

    def test_extract_markdown_links_multiple(self):
        text = "Check out [Google](https://google.com) and [GitHub](https://github.com)"
        matches = extract_markdown_links(text)
        result = [(m.group("alt"), m.group("url")) for m in matches]
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links")
        result = [(m.group("alt"), m.group("url")) for m in matches]
        self.assertEqual(result, [])

    def test_extract_markdown_links_ignores_images(self):
        # Links should NOT match image
        text = "This has ![an image](https://img.com) but not a link"
        matches = extract_markdown_links(text)
        result = [(m.group("alt"), m.group("url")) for m in matches]
        self.assertEqual(result, [])

    def test_extract_markdown_images_ignores_links(self):
        # Images should NOT match link
        text = "This has [a link](https://example.com) but not an image"
        matches = extract_markdown_images(text)
        result = [(m.group("alt"), m.group("url")) for m in matches]
        self.assertEqual(result, [])

    def test_extract_both_mixed(self):
        text = "![image](https://img.com) and [link](https://example.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)

        images_result = [(m.group("alt"), m.group("url")) for m in images]
        links_result = [(m.group("alt"), m.group("url")) for m in links]

        self.assertEqual(images_result, [("image", "https://img.com")])
        self.assertEqual(links_result, [("link", "https://example.com")])
