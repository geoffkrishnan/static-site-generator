import unittest

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_only(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_only(self):
        text = "This is *italic* text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_only(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_only(self):
        text = "This is an ![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_link_only(self):
        text = "This is a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold(self):
        text = "**First** and **second** bold"
        result = text_to_textnodes(text)
        expected = [
            TextNode("First", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold_and_italic(self):
        text = "This is **bold** and *italic*"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_all_inline_types(self):
        text = "**bold** *italic* `code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_image_and_link(self):
        text = "![img](img.png) and [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_comprehensive_example(self):
        text = (
            "This is **text** with an *italic* word and a "
            "`code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_formatting_at_start(self):
        text = "**Bold** at start"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_formatting_at_end(self):
        text = "End with **bold**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_consecutive_formatting(self):
        text = "**bold***italic*`code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_bold_with_asterisk_inside(self):
        text = "**bold*text**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold*text", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_only_formatting(self):
        text = "**bold**"
        result = text_to_textnodes(text)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_image_with_bold_alt_text(self):
        text = "![**bold** alt](url.com)"
        result = text_to_textnodes(text)
        # Alt text should stay as-is, not split
        expected = [
            TextNode("**bold** alt", TextType.IMAGE, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_link_with_italic_text(self):
        text = "[*italic* link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("*italic* link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images_and_links(self):
        text = "![img1](url1.png) text [link1](site1.com) more ![img2](url2.png) [link2](site2.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("img1", TextType.IMAGE, "url1.png"),
            TextNode(" text ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "site1.com"),
            TextNode(" more ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "site2.com"),
        ]
        self.assertEqual(result, expected)

    def test_complex_nesting_scenario(self):
        text = "Check out **my `code` repo** at [GitHub](https://github.com) with ![logo](logo.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("my `code` repo", TextType.BOLD),
            TextNode(" at ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
            TextNode(" with ", TextType.TEXT),
            TextNode("logo", TextType.IMAGE, "logo.png"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
