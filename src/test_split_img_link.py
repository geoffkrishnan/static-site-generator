import unittest

from inline_markdown import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("Text with ![alt](https://url.com) here", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://url.com"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode(
            "Start ![first](url1.com) middle ![second](url2.com) end", TextType.TEXT
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("first", TextType.IMAGE, "url1.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        node = TextNode("![start](url.com) then text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "url.com"),
            TextNode(" then text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        node = TextNode("Some text ![end](url.com)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Some text ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_only_image(self):
        node = TextNode("![only](url.com)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("only", TextType.IMAGE, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_consecutive_images(self):
        node = TextNode("![first](url1.com)![second](url2.com)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "url1.com"),
            TextNode("second", TextType.IMAGE, "url2.com"),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Just plain text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_alt_text(self):
        node = TextNode("Text ![](url.com) more", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "url.com"),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First ![img1](url1.com)", TextType.TEXT),
            TextNode("Second ![img2](url2.com)", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1.com"),
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.com"),
        ]
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        node = TextNode("already an image", TextType.IMAGE, "url.com")
        result = split_nodes_image([node])
        expected = [node]  # Should pass through unchanged
        self.assertEqual(result, expected)

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("Click [here](https://example.com) to continue", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" to continue", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode(
            "Visit [Google](google.com) or [GitHub](github.com)", TextType.TEXT
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "google.com"),
            TextNode(" or ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "github.com"),
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode("[Start](url.com) text after", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Start", TextType.LINK, "url.com"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode("Text before [end](url.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_only_link(self):
        node = TextNode("[only](url.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("only", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_consecutive_links(self):
        node = TextNode("[first](url1.com)[second](url2.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "url1.com"),
            TextNode("second", TextType.LINK, "url2.com"),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Just plain text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_link_text(self):
        node = TextNode("Click [](url.com) here", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("", TextType.LINK, "url.com"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_with_special_chars(self):
        node = TextNode("Read [C++ Guide](learncpp.com) now", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Read ", TextType.TEXT),
            TextNode("C++ Guide", TextType.LINK, "learncpp.com"),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First [link1](url1.com)", TextType.TEXT),
            TextNode("Second [link2](url2.com)", TextType.TEXT),
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1.com"),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2.com"),
        ]
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        node = TextNode("already a link", TextType.LINK, "url.com")
        result = split_nodes_link([node])
        expected = [node]
        self.assertEqual(result, expected)


class TestMixedImageAndLink(unittest.TestCase):
    def test_image_and_link_together(self):
        node = TextNode("Check ![img](img.com) and [link](url.com)", TextType.TEXT)
        # Split images first
        result = split_nodes_image([node])
        # Then split links
        result = split_nodes_link(result)

        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)
