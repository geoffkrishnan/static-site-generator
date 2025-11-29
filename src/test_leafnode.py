import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "Hello, world!")
        self.assertEqual(node.to_html(), "<code>Hello, world!</code>")

    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("a", "Link", {"href": "https://google.com", "target": "_blank"})
        html = node.to_html()
        self.assertIn('href="https://google.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertIn("<a", html)
        self.assertIn(">Link</a>", html)

    def test_leaf_to_html_props_none(self):
        node = LeafNode("p", "Text", None)
        self.assertEqual(node.to_html(), "<p>Text</p>")

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("p", "Text", {})
        self.assertEqual(node.to_html(), "<p>Text</p>")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_special_chars(self):
        node = LeafNode("p", "Hello & goodbye")
        self.assertEqual(node.to_html(), "<p>Hello & goodbye</p>")
