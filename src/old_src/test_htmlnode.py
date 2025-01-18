import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Test HTMLNode",None,{"href" : "www.google.com"})
        node2 = HTMLNode("p", "Test HTMLNode",None,{"href" : "www.google.com"})
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        child = HTMLNode("a", "Cool Image", None, {"href":"www.w.com"})
        child2 = HTMLNode("a", "Cool Image", None, {"href":"www.w.com"})
        node = HTMLNode("a", "Cool Image", [child, child2], {"href":"www.p.com"})
        node2 = HTMLNode("a", "Cool Image", [child, child2], {"href":"www.p.com"})
        self.assertEqual(node, node2)
    
    def test_eq_props_to_html(self):
        child = HTMLNode("a", "Cool Image", None, {"href":"www.w.com"})
        child2 = HTMLNode("a", "Cool Image", None, {"href":"www.w.com"})
        node = HTMLNode("a", "Cool Image", [child, child2], {"href":"www.p.com"})
        node2 = HTMLNode("a", "Cool Image", [child, child2], {"href":"www.p.com"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())

if __name__ == "__main__":
    unittest.main()