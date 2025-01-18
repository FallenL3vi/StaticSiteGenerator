import re
from htmlnode import HTMLNode
from parentnode import ParentNode
from markdown_extractors import(block_type_paragraph,
block_type_code,
block_type_heading,
block_type_unordered_list,
block_type_ordered_list,
block_type_quote, block_to_block_type, markdown_to_blocks)
from textnode import text_node_to_html, text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html(block)
        children.append(html_node)
    
    return ParentNode("div", children, None)

def block_to_html(block):
    blocks_type = block_to_block_type(block)
    if blocks_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if blocks_type == block_type_code:
        return code_to_html_node(block)
    if blocks_type == block_type_ordered_list:
        return ordered_list_to_html_node(block)
    if blocks_type == block_type_heading:
        return heading_to_html_node(block)
    if blocks_type == block_type_quote:
        return quote_to_html_node(block)
    if blocks_type == block_type_unordered_list:
        return unordered_list_to_html_node(block)
    raise ValueError("Invalid block")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block):
    if not block.startswith("```") and not block.endswith("```"):
        raise ValueError("Wrong block code: not code")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)