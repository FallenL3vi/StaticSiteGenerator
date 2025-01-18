import unittest
from textnode import (TextType, TextNode, text_node_to_html, split_nodes_delimiter, split_nodes_image, split_nodes_link,
                      text_to_textnodes)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.CODE, "www.polska.pl")
        node2 = TextNode("This is a text node", TextType.CODE, "www.googl.com")
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.IMAGES)
        node2 = TextNode("This is a text node", TextType.CODE, "www.googl.com")
        self.assertNotEqual(node, node2)
    
    def test_eq_none(self):
        node = TextNode("This is a text node", TextType.LINKS)
        node2 = TextNode("This is a text node", TextType.LINKS)
        self.assertEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    def test_link(self):
        node = TextNode("This is a link", TextType.LINKS, "www.link.com")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href":"www.link.com"})
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGES, "www.image.com")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src":"www.image.com", "alt": "This is an image"})
        self.assertEqual(html_node.value, "")
    
class TestTextNodeSplit(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is a text node **bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [TextNode("This is a text node ", TextType.NORMAL),
             TextNode("bold", TextType.BOLD)],
             new_nodes
        )
    
    def test_delim_bold_double(self):
        node = TextNode("This is a text node **bold** and what **mega bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [TextNode("This is a text node ", TextType.NORMAL),
             TextNode("bold", TextType.BOLD),
             TextNode(" and what ", TextType.NORMAL),
             TextNode("mega bold", TextType.BOLD)],
             new_nodes
        )

    def test_delim_italic(self):
        node = TextNode("This is a text node *italic* pasta", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            [TextNode("This is a text node ", TextType.NORMAL),
             TextNode("italic", TextType.ITALIC),
             TextNode(" pasta", TextType.NORMAL)],
             new_nodes
        )
    
    def test_delim_bold_italic(self):
        node = TextNode("This is a text node **bold** pasta and mega *italic*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            [TextNode("This is a text node ", TextType.NORMAL),
             TextNode("bold", TextType.BOLD),
             TextNode(" pasta and mega ", TextType.NORMAL),
             TextNode("italic", TextType.ITALIC)],
             new_nodes
        )
    
    def test_delim_italic_code(self):
        node = TextNode("This is a text node *italic* pasta and mega `code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
            [TextNode("This is a text node ", TextType.NORMAL),
             TextNode("italic", TextType.ITALIC),
             TextNode(" pasta and mega ", TextType.NORMAL),
             TextNode("code", TextType.CODE)],
             new_nodes
        )

class TestTextImagesSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with a link ![super image](https://www.superimage.io/super.jpg) and ![to mega image](https://www.megaimagee.com/megaimage.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("super image", TextType.IMAGES, "https://www.superimage.io/super.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to mega image", TextType.IMAGES, "https://www.megaimagee.com/megaimage.png"),])
    
    def test_split_image(self):
        node = TextNode("![new image](///:new_image.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])

        self.assertListEqual(new_nodes,
                             [TextNode("new image",TextType.IMAGES,"///:new_image.png")])
        
class TestTextLinksSplit(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"),])

    def test_split_link(self):
        node = TextNode("[mega link](https://www.megalink.pl)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])

        self.assertListEqual(new_nodes,
                             [TextNode("mega link",TextType.LINKS,"https://www.megalink.pl")])
        
class TestTextToTextNodes(unittest.TestCase):
    def test_no_link_no_images(self):
        text = "This is **text** with an *italic* word and a `code block` and more `code blocks` and **big bold text**"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(new_nodes, [TextNode("This is ", TextType.NORMAL),
                                         TextNode("text", TextType.BOLD),
                                         TextNode(" with an ", TextType.NORMAL),
                                         TextNode("italic", TextType.ITALIC),
                                         TextNode(" word and a ", TextType.NORMAL),
                                         TextNode("code block", TextType.CODE),
                                         TextNode(" and more ", TextType.NORMAL),
                                         TextNode("code blocks", TextType.CODE),
                                         TextNode(" and ", TextType.NORMAL),
                                         TextNode("big bold text", TextType.BOLD)])
    
    def test_no_links(self):
        text = "This is **text** with an *italic* word and a `code block` and more ![mega dog](::mega_dog_image.png::) `code blocks` and **big bold text**"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(new_nodes, [TextNode("This is ", TextType.NORMAL),
                                         TextNode("text", TextType.BOLD),
                                         TextNode(" with an ", TextType.NORMAL),
                                         TextNode("italic", TextType.ITALIC),
                                         TextNode(" word and a ", TextType.NORMAL),
                                         TextNode("code block", TextType.CODE),
                                         TextNode(" and more ", TextType.NORMAL),
                                         TextNode("mega dog", TextType.IMAGES, "::mega_dog_image.png::"),
                                         TextNode("code blocks", TextType.CODE),
                                         TextNode(" and ", TextType.NORMAL),
                                         TextNode("big bold text", TextType.BOLD)])

    def test_no_images(self):
        text = "This is **text** with an *italic* word and a `code block` and more [mega link](wwww.linkbingo.io) `code blocks` and **big bold text**"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(new_nodes, [TextNode("This is ", TextType.NORMAL),
                                         TextNode("text", TextType.BOLD),
                                         TextNode(" with an ", TextType.NORMAL),
                                         TextNode("italic", TextType.ITALIC),
                                         TextNode(" word and a ", TextType.NORMAL),
                                         TextNode("code block", TextType.CODE),
                                         TextNode(" and more ", TextType.NORMAL),
                                         TextNode("mega link", TextType.LINKS, "wwww.linkbingo.io"),
                                         TextNode("code blocks", TextType.CODE),
                                         TextNode(" and ", TextType.NORMAL),
                                         TextNode("big bold text", TextType.BOLD)])
    def test_links_images(self):
        text = "This is **text** with an *italic* word and a `code block` and more ![mega image](:://mega_image.png)[mega link](wwww.linkbingo.io) `code blocks` and **big bold text**"
        new_nodes = text_to_textnodes(text)

        self.assertListEqual(new_nodes, [TextNode("This is ", TextType.NORMAL),
                                         TextNode("text", TextType.BOLD),
                                         TextNode(" with an ", TextType.NORMAL),
                                         TextNode("italic", TextType.ITALIC),
                                         TextNode(" word and a ", TextType.NORMAL),
                                         TextNode("code block", TextType.CODE),
                                         TextNode(" and more ", TextType.NORMAL),
                                         TextNode("mega image", TextType.IMAGES, ":://mega_image.png"),
                                         TextNode("mega link", TextType.LINKS, "wwww.linkbingo.io"),
                                         TextNode("code blocks", TextType.CODE),
                                         TextNode(" and ", TextType.NORMAL),
                                         TextNode("big bold text", TextType.BOLD)])


if __name__ == "__main__":
    unittest.main()