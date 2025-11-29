import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.children)
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)

    def test_tag(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.children)
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)

    def test_val(self):
        node = HTMLNode(value="blah")
        self.assertIsNone(node.tag)
        self.assertIsNone(node.children)
        self.assertEqual(node.value, "blah")
        self.assertIsNone(node.props)

    def test_child(self):
        child = HTMLNode("h3")
        node = HTMLNode(children=[child])
        self.assertIsNone(node.tag)
        self.assertEqual(len(node.children), 1)
        self.assertIsNone(node.props)
        self.assertIsNone(node.value)

    def test_tag_and_value(self):
        node = HTMLNode(tag="p", value="Hello")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_tag_and_children(self):
        child = HTMLNode("p")
        node = HTMLNode(tag="div", children=[child])
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children), 1)
        self.assertIsNone(node.props)

    def test_tag_and_props(self):
        node = HTMLNode(tag="a", props={"href": "google.com"})
        self.assertEqual(node.tag, "a")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "google.com"})

    def test_multiple_children(self):
        children = [HTMLNode("p"), HTMLNode("span"), HTMLNode("a")]
        node = HTMLNode(tag="div", children=children)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)

    def test_multiple_props(self):
        props = {"href": "url", "class": "btn", "id": "submit"}
        node = HTMLNode(tag="a", props=props)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.props, props)

    def test_all(self):
        node = HTMLNode(tag="a", value="Click", props={"href": "google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "google.com"})


if __name__ == "__main__":
    unittest.main()
