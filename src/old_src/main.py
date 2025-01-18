from textnode import TextType, TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_textnodes
from markdown_extractors import markdown_to_blocks



def main():
    new_text_node = TextNode("Hello World", TextType.CODE, "https://www.boot.dev")
    print(new_text_node)

    node = TextNode("`This is text with` a code block word", TextType.NORMAL)
    split_nodes_delimiter([node],"`", TextType.CODE)
    markdown = '''# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item'''
    markdown_to_blocks(markdown)

if __name__ == "__main__":
    main()