import unittest

from inline_markdown import *
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        """Text contains no delimiters; should return the node unchanged."""
        node = TextNode("This is all a TEXT node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        # Expected result: The same node, unchanged
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is all a TEXT node")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_with_proper_delimiters(self):
        """Text contains properly paired delimiters."""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Expected result: Split into 3 nodes
        self.assertEqual(len(new_nodes), 3)

        # First node: Text before the bolded part
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        # Second node: The bolded text
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        # Third node: Text after the bolded part
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_unmatched_delimiters(self):
        """Text contains unmatched delimiters; should raise an exception."""
        node = TextNode("This is **unmatched text", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

        # Check the exception message
        self.assertEqual(str(context.exception), "Unmatched delimiter found!")

    def test_multiple_delimiters(self):
        """Text contains multiple pairs of delimiters."""
        node = TextNode("This **is** bold and **this** too", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Expected result: Split into 5 nodes
        self.assertEqual(len(new_nodes), 5)

        # First part: Text before the first delimiter
        self.assertEqual(new_nodes[0].text, "This ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

        # Second part: First bold segment
        self.assertEqual(new_nodes[1].text, "is")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        # Third part: Text between delimiters
        self.assertEqual(new_nodes[2].text, " bold and ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        # Fourth part: Second bold segment
        self.assertEqual(new_nodes[3].text, "this")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

        # Fifth part: Text after the last delimiter
        self.assertEqual(new_nodes[4].text, " too")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_unmatched_delimiters(self):
        """Text contains unmatched delimiters; should raise an exception."""
        node = TextNode("This is **unmatched text", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

        # Ensure the exception message is accurate
        self.assertEqual(str(context.exception), "Unmatched delimiter '**' found!")

    def test_no_delimiter_in_text(self):
        """Text contains no delimiters; should return unchanged nodes."""
        node = TextNode("This is normal text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Since no delimiters exist, the result should match the original node
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is normal text without delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

class TestImageAndLinkExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to somewhere](https://google.com)"
        )
        self.assertListEqual([("to somewhere", "https://google.com")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
        "Here are multiple images: ![first](https://i.imgur.com/zKrWIiW.png) and ![second](https://i.imgur.com/PGqyvPg.png)"
        )
        self.assertListEqual([
        ("first", "https://i.imgur.com/zKrWIiW.png"),
        ("second", "https://i.imgur.com/PGqyvPg.png")
        ], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
        "Here are links [first link](https://translate.google.com) and [second link](https://xbox.com)"
        )
        self.assertListEqual([
        ("first link", "https://translate.google.com"),
        ("second link", "https://xbox.com")
        ], matches)

    def test_mixed_content(self):
        text = "Text with ![image](https://cdn2.steamgriddb.com/thumb/1a05d10b4500844c83c8513d942b59b1.jpg) and [link](https://www.steamgriddb.com/projects/grid-and-tear)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("image", "https://cdn2.steamgriddb.com/thumb/1a05d10b4500844c83c8513d942b59b1.jpg")], image_matches)
        self.assertListEqual([("link", "https://www.steamgriddb.com/projects/grid-and-tear")], link_matches)

    def test_no_matches(self):
        self.assertListEqual([], extract_markdown_images("No images here"))
        self.assertListEqual([], extract_markdown_links("No links here"))

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    