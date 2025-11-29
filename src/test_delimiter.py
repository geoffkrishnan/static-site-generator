import unittest

from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimiter_pair(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiter_pairs(self):
        node = TextNode("**bold** and **more bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_start(self):
        node = TextNode("**bold** normal", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" normal", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        node = TextNode("normal **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("normal ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_mixed_node_list(self):
        nodes = [
            TextNode("normal **bold**", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
            TextNode("more **bold**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("normal ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("already italic", TextType.ITALIC),
            TextNode("more ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_unpaired_delimiters_raises(self):
        node = TextNode("**unpaired", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_invalid_delimiter_raises(self):
        node = TextNode("text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "!!", TextType.BOLD)

    def test_italic_with_underscore(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_with_backtick(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
