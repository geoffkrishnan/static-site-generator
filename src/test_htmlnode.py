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

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a", props={"href": "https://www.google.com", "target": "_blank"}
        )
        html = node.props_to_html()
        # Order might vary, so check both possibilities
        self.assertIn('href="https://www.google.com"', html)
        self.assertIn('target="_blank"', html)

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_special_chars(self):
        node = HTMLNode(tag="a", props={"data-value": "test & verify"})
        self.assertEqual(node.props_to_html(), ' data-value="test & verify"')

    # Tests for __repr__()
    def test_repr_all_none(self):
        node = HTMLNode()
        self.assertEqual(
            repr(node), "HTMLNode(tag = None, value = None, children=None, props=None)"
        )

    def test_repr_with_tag(self):
        node = HTMLNode(tag="p")
        self.assertEqual(
            repr(node), "HTMLNode(tag = p, value = None, children=None, props=None)"
        )

    def test_repr_with_value(self):
        node = HTMLNode(value="Hello")
        self.assertEqual(
            repr(node), "HTMLNode(tag = None, value = Hello, children=None, props=None)"
        )

    def test_repr_with_children(self):
        child = HTMLNode("span")
        node = HTMLNode(children=[child])
        repr_str = repr(node)
        self.assertIn("tag = None", repr_str)
        self.assertIn("value = None", repr_str)
        self.assertIn("children=", repr_str)

    def test_repr_with_props(self):
        node = HTMLNode(props={"href": "url"})
        repr_str = repr(node)
        self.assertIn("props={'href': 'url'}", repr_str)

    # Edge case tests
    def test_empty_children_list(self):
        node = HTMLNode(children=[])
        self.assertEqual(len(node.children), 0)
        self.assertIsNotNone(node.children)

    def test_empty_value_string(self):
        node = HTMLNode(value="")
        self.assertEqual(node.value, "")
        self.assertIsNotNone(node.value)

    def test_empty_tag_string(self):
        node = HTMLNode(tag="")
        self.assertEqual(node.tag, "")
        self.assertIsNotNone(node.tag)

    def test_long_value(self):
        long_text = "a" * 1000
        node = HTMLNode(value=long_text)
        self.assertEqual(node.value, long_text)

    def test_nested_children(self):
        grandchild = HTMLNode("span")
        child = HTMLNode("p", children=[grandchild])
        parent = HTMLNode("div", children=[child])
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(len(parent.children[0].children), 1)

    # Test to_html raises NotImplementedError
    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # Test __eq__ method
    def test_eq_identical(self):
        node1 = HTMLNode(tag="p", value="test", props={"class": "text"})
        node2 = HTMLNode(tag="p", value="test", props={"class": "text"})
        self.assertEqual(node1, node2)

    def test_eq_different_tag(self):
        node1 = HTMLNode(tag="p", value="test")
        node2 = HTMLNode(tag="div", value="test")
        self.assertNotEqual(node1, node2)

    def test_eq_different_value(self):
        node1 = HTMLNode(tag="p", value="test1")
        node2 = HTMLNode(tag="p", value="test2")
        self.assertNotEqual(node1, node2)

    def test_eq_different_props(self):
        node1 = HTMLNode(tag="p", props={"class": "a"})
        node2 = HTMLNode(tag="p", props={"class": "b"})
        self.assertNotEqual(node1, node2)

    def test_eq_with_children(self):
        child1 = HTMLNode("span")
        child2 = HTMLNode("span")
        node1 = HTMLNode(children=[child1])
        node2 = HTMLNode(children=[child2])
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
