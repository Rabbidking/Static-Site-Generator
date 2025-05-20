import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

    def test_parent_node_no_tag(self):
        """Test that ParentNode raises ValueError when tag is None"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_empty_children_list(self):
        """Test that ParentNode raises ValueError when children list is empty"""
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_none_children(self):
        """Test that ParentNode raises ValueError when children is None"""
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_multiple_children(self):
        """Test that ParentNode correctly handles multiple children"""
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("b", "child2")
        child3 = LeafNode(None, "plain text")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><b>child2</b>plain text</div>"
        )

    def test_deeply_nested_nodes(self):
        """Test deeply nested hierarchy of parent nodes"""
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        mid_parent1 = ParentNode("p", [leaf1, leaf2])
        leaf3 = LeafNode("u", "underline")
        mid_parent2 = ParentNode("div", [leaf3])
        top_parent = ParentNode("section", [mid_parent1, mid_parent2])
        self.assertEqual(
            top_parent.to_html(),
            "<section><p><b>bold</b><i>italic</i></p><div><u>underline</u></div></section>"
        )

if __name__ == "__main__":
    unittest.main()