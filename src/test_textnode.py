import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node, node2)

    def test_text_type_plain(self):
        node = TextNode("Plain text", TextType.PLAIN)
        self.assertEqual(node.text_type, TextType.PLAIN)
        self.assertEqual(node.text_type.value, "text")

    def test_text_type_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.text_type.value, "bold")

    def test_text_type_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertEqual(node.text_type.value, "italic")

    def test_text_type_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        self.assertEqual(node.text_type, TextType.CODE)
        self.assertEqual(node.text_type.value, "code")

    def test_text_type_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.text_type.value, "link")

    def test_text_type_images(self):
        node = TextNode("Alt text", TextType.IMAGES, "https://example.com/image.png")
        self.assertEqual(node.text_type, TextType.IMAGES)
        self.assertEqual(node.text_type.value, "images")

    # Test __repr__() method
    def test_repr_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        self.assertEqual(
            repr(node), "TextNode(Click here, link, https://www.google.com)"
        )

    def test_repr_without_url(self):
        node = TextNode("Bold text", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(Bold text, bold, None)")

    def test_repr_plain_text(self):
        node = TextNode("Plain text", TextType.PLAIN)
        self.assertEqual(repr(node), "TextNode(Plain text, text, None)")

    def test_repr_with_none_url(self):
        node = TextNode("Text", TextType.ITALIC, None)
        self.assertEqual(repr(node), "TextNode(Text, italic, None)")

    # Edge case tests
    def test_empty_text(self):
        node = TextNode("", TextType.PLAIN)
        self.assertEqual(node.text, "")

    def test_empty_url(self):
        node = TextNode("Link", TextType.LINK, "")
        self.assertEqual(node.url, "")

    def test_long_text(self):
        long_text = "a" * 1000
        node = TextNode(long_text, TextType.PLAIN)
        self.assertEqual(node.text, long_text)

    def test_special_chars_in_text(self):
        text = "Special chars: <>&\"'"
        node = TextNode(text, TextType.PLAIN)
        self.assertEqual(node.text, text)

    def test_newlines_in_text(self):
        text = "Line 1\nLine 2\nLine 3"
        node = TextNode(text, TextType.CODE)
        self.assertEqual(node.text, text)

    def test_unicode_text(self):
        text = "Hello 世界 🌍"
        node = TextNode(text, TextType.PLAIN)
        self.assertEqual(node.text, text)

    def test_url_with_query_params(self):
        url = "https://example.com/page?param1=value1&param2=value2"
        node = TextNode("Link", TextType.LINK, url)
        self.assertEqual(node.url, url)

    def test_url_with_fragment(self):
        url = "https://example.com/page#section"
        node = TextNode("Link", TextType.LINK, url)
        self.assertEqual(node.url, url)

    # Test inequality with different attributes
    def test_not_eq_different_text(self):
        node1 = TextNode("Text 1", TextType.BOLD)
        node2 = TextNode("Text 2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_type(self):
        node1 = TextNode("Text", TextType.BOLD)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("Link", TextType.LINK, "https://google.com")
        node2 = TextNode("Link", TextType.LINK, "https://bing.com")
        self.assertNotEqual(node1, node2)

    def test_not_eq_one_with_url_one_without(self):
        node1 = TextNode("Link", TextType.LINK, "https://google.com")
        node2 = TextNode("Link", TextType.LINK)
        self.assertNotEqual(node1, node2)

    # Test equality with all attributes matching
    def test_eq_all_attributes(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_eq_code_with_special_chars(self):
        code = "def func():\n    return True"
        node1 = TextNode(code, TextType.CODE)
        node2 = TextNode(code, TextType.CODE)
        self.assertEqual(node1, node2)

    # Test different text types are not equal
    def test_all_text_types_different(self):
        text = "Same text"
        nodes = [
            TextNode(text, TextType.PLAIN),
            TextNode(text, TextType.BOLD),
            TextNode(text, TextType.ITALIC),
            TextNode(text, TextType.CODE),
            TextNode(text, TextType.LINK),
            TextNode(text, TextType.IMAGES),
        ]
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i != j:
                    self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
