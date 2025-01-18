import unittest
from markdown_extractors import *

class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_links(self):
        matches = extract_markdown_links("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)")

        self.assertListEqual([("link", "https://boot.dev"), ("another link","https://blog.boot.dev")], matches)
    
    def test_extract_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)

    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

        self.assertListEqual([
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],markdown_to_blocks(markdown))
    
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

        self.assertListEqual([
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],markdown_to_blocks(markdown))

    def block_to_block_paragraph(self):
        block = "This is **bolded** paragraph"
        self.assertEqual(block_type_paragraph, block_to_block_type(block))
    
    def block_to_block_heading(self):
        block = "### This is heading"
        self.assertEqual(block_type_heading, block_to_block_type(block))
    
    def block_to_block_code(self):
        block = """```Mega code\n
        mega code\n
        mulitline code```"""
        self.assertEqual(block_type_code, block_to_block_type(block))
    
    def block_to_block_unordered_list(self):
        block = """* First point\n
        * 2nd point"""
        self.assertEqual(block_type_unordered_list, block_to_block_type(block))
    
    def block_to_block_unordered_list_2(self):
        block = """- First point\n
        - 2nd point"""
        self.assertEqual(block_type_unordered_list, block_to_block_type(block))
    
    def block_to_block_ordered_list(self):
        block = """1. First point\n
        2. 2nd point"""
        self.assertEqual(block_type_ordered_list, block_to_block_type(block))
    
        
    def block_to_block_quote(self):
        block = """>First quote\n
        >2nd quote"""
        self.assertEqual(block_type_quote, block_to_block_type(block))