import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><span>child2</span><span>child3</span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(), '<div class="container"><span>child</span></div>'
        )

    def test_to_html_with_multiple_props(self):
        child_node = LeafNode("p", "text")
        parent_node = ParentNode(
            "div", [child_node], {"class": "container", "id": "main"}
        )
        html = parent_node.to_html()
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertIn("<div", html)
        self.assertIn("<p>text</p></div>", html)

    def test_to_html_none_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_none_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_multiple_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("i", "grandchild2")
        grandchild_node3 = LeafNode("i", "grandchild3")
        child_node = ParentNode(
            "span", [grandchild_node, grandchild_node2, grandchild_node3]
        )
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><i>grandchild2</i><i>grandchild3</i></span></div>",
        )

    def test_to_html_deep_nesting(self):
        great_grandchild = LeafNode("i", "bottom")
        grandchild = ParentNode("span", [great_grandchild])
        child = ParentNode("p", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(), "<div><p><span><i>bottom</i></span></p></div>"
        )

    def test_to_html_mixed_children(self):
        leaf1 = LeafNode("p", "paragraph")
        grandchild = LeafNode("b", "bold text")
        parent_child = ParentNode("span", [grandchild])
        leaf2 = LeafNode("i", "italic")
        parent = ParentNode("div", [leaf1, parent_child, leaf2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>paragraph</p><span><b>bold text</b></span><i>italic</i></div>",
        )

    def test_repr_basic(self):
        child = LeafNode("p", "text")
        node = ParentNode("div", [child])
        # Note: repr will show the child's repr too
        expected = f"ParentNode(tag = div, children=[{repr(child)}], props=None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_props(self):
        child = LeafNode("p", "text")
        node = ParentNode("div", [child], {"class": "container"})
        expected = f"ParentNode(tag = div, children=[{repr(child)}], props={{'class': 'container'}})"
        self.assertEqual(repr(node), expected)

    def test_repr_multiple_children(self):
        child1 = LeafNode("p", "first")
        child2 = LeafNode("p", "second")
        node = ParentNode("div", [child1, child2])
        expected = f"ParentNode(tag = div, children=[{repr(child1)}, {repr(child2)}], props=None)"
        self.assertEqual(repr(node), expected)

    def test_repr_nested_parent(self):
        leaf = LeafNode("p", "text")
        inner_parent = ParentNode("div", [leaf])
        outer_parent = ParentNode("section", [inner_parent])
        expected = (
            f"ParentNode(tag = section, children=[{repr(inner_parent)}], props=None)"
        )
        self.assertEqual(repr(outer_parent), expected)
