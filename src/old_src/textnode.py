from enum import Enum
from leafnode import LeafNode
from markdown_extractors import (extract_markdown_images, extract_markdown_links)

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINKS = "Links"
    IMAGES = "Images"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (self.text_type == value.text_type and self.text == value.text and
                self.url == value.url)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(text_node.text, None, None)
        case TextType.BOLD:
            return LeafNode(text_node.text, None, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, None, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, None, "code")
        case TextType.LINKS:
            return LeafNode(text_node.text, {"href":text_node.url}, "a")
        case TextType.IMAGES:
            return LeafNode("", {"src":text_node.url, "alt":text_node.text}, "img")
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        text_copy = node.text
        if node.text and node.text != "":
            extracted = extract_markdown_images(node.text)
            if len(extracted) == 0:
                new_nodes.append(node)
                continue
            print("\n")
            print(node)
            if extracted:
                for extract in extracted:
                    splited_text = text_copy.split(f"![{extract[0]}]({extract[1]})",1)
                    if len(splited_text) !=2:
                        raise ValueError("Invalid markdown, image section not closed")
                    if splited_text[0] != "" and not splited_text[0].isspace():
                        new_nodes.append(TextNode(splited_text[0], TextType.NORMAL))
                    new_nodes.append(TextNode(extract[0], TextType.IMAGES, extract[1]))
                    text_copy = splited_text[1]
            
            if text_copy != "" and not text_copy.isspace():
                new_nodes.append(TextNode(text_copy, TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        text_copy = node.text
        if node.text and node.text != "":
            sections = []
            extracted = extract_markdown_links(node.text)
            if len(extracted) == 0:
                new_nodes.append(node)
                continue
            if extracted:
                for extract in extracted:
                    splited_text = text_copy.split(f"[{extract[0]}]({extract[1]})",1)
                    if len(splited_text) !=2:
                        raise ValueError("Invalid markdown, image section not closed")
                    if splited_text[0] != "" and not splited_text[0].isspace():
                        new_nodes.append(TextNode(splited_text[0], TextType.NORMAL))
                    new_nodes.append(TextNode(extract[0], TextType.LINKS, extract[1]))
                    text_copy = splited_text[1]
            
            if text_copy != "" and not text_copy.isspace():
                new_nodes.append(TextNode(text_copy, TextType.NORMAL))
    return new_nodes


def text_to_textnodes(text):
    
    if text.isspace():
        raise ValueError(f"Text To Textnodes: Empty text input {text}")
    
    new_nodes = []
    node = [TextNode(text, TextType.NORMAL)]
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    new_nodes = split_nodes_image(new_nodes)

    new_nodes = split_nodes_link(new_nodes)

    return new_nodes
