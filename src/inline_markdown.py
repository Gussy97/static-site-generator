from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
import re

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt":text_node.text})
        case _:
            raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid markdown syntax")
        splits = node.text.split(delimiter)
        for i in range(len(splits)):
            if splits[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splits[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(splits[i], text_type))
    return new_nodes
       

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for alt_text, url in images:
            sections = text.split(f"![{alt_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid lmarkdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for alt_text, url in links:
            sections = text.split(f"[{alt_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid lmarkdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

# def text_to_textnodes(text):
#     node = TextNode(text, TextType.TEXT)
#     get_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
#     get_italic = split_nodes_delimiter(get_bold, "_", TextType.ITALIC)
#     get_code = split_nodes_delimiter(get_italic, "`", TextType.CODE)
#     get_images = split_nodes_image(get_code)
#     return split_nodes_link(get_images)

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
                split_nodes_image(
                    split_nodes_delimiter(
                        split_nodes_delimiter(
                            split_nodes_delimiter(
                                [node], "**", TextType.BOLD),
                                "`", TextType.CODE),
                                    "_", TextType.ITALIC)))

            