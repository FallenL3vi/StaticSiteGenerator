import unittest
from markdown_converter import *

class TestTextNode(unittest.TestCase):

    def test_paragraph(self):
            md = """
    This is **bolded** paragraph
    text in a p
    tag here

    """
            node = markdown_to_html_node(md)
            html = node.to_html()

            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
            )