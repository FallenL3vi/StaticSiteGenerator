import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b")], "Test Parent")
        node2 = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b")], "Test Parent")
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b"), ParentNode("p", [LeafNode("Test Child 3", None, "b"), LeafNode("Test Child 4", None, "b")], "Test Parent 3")], "Test Parent 2")
        node2 = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b"), ParentNode("p", [LeafNode("Test Child 3", None, "b"), LeafNode("Test Child 4", None, "b")], "Test Parent 3")], "Test Parent 2")
        self.assertEqual(node, node2)
    
    def test_eq3(self):
        node = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b")], "Test Parent")
        node2 = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b")], "Test Parent")
        #print(f"{node.to_html()} \n {node2.to_html()}")
        self.assertEqual(node.to_html(), node2.to_html())
    
    def test_eq4(self):
        node = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b"), ParentNode("p", [LeafNode("Test Child 3", None, "b"), LeafNode("Test Child 4", None, "b")], "Test Parent 3")], "Test Parent 2")
        node2 = ParentNode("p", [LeafNode("Test Child", None, "b"), LeafNode("Test Child 2", None, "b"), ParentNode("p", [LeafNode("Test Child 3", None, "b"), LeafNode("Test Child 4", None, "b")], "Test Parent 3")], "Test Parent 2")
        #print(f"{node.to_html()} \n {node2.to_html()}")
        self.assertEqual(node.to_html(), node2.to_html())