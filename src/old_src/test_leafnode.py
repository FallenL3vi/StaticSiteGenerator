import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_eq(self):
        node = LeafNode("Test tag", None, "p")
        node2 = LeafNode("Test tag", None, "p")
        
        self.assertEqual(node, node2)
    
    def test_raw_data(self):
        node = LeafNode("Test tag", None, None)
        node2 = LeafNode("Test tag", None, None)
        self.assertEqual(node.to_html(), node2.to_html())
    
    def test_to_html(self):
        node = LeafNode("Test tag", None, "p")
        node2 = LeafNode("Test tag", None, "p")
        self.assertEqual(node.to_html(), node2.to_html())
    
    def test_to_html_props(self):
        node = LeafNode("Test tag", {"href":"www.a.io","href":"www.b.io"}, "a")
        node2 = LeafNode("Test tag", {"href":"www.a.io","href":"www.b.io"}, "a")
        self.assertEqual(node.to_html(), node2.to_html())   


if __name__ == "__main__":
    unittest.main()