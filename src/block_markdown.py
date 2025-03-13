from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from inline_markdown import text_to_textnodes, text_node_to_html_node



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(lambda block: block != "", list(map(lambda block: block.strip(), blocks))))

def block_to_blocktype(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if lines[0].startswith(">"):
        for i in range(1, len(lines)):
            if not lines[i].startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if lines[0].startswith("- "):
        for i in range(1, len(lines)):
            if not lines[i].startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if lines[0].startswith("1. "):
        for i in range(1, len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return ParentNode("div", get_nodes_from_blocks(blocks))

def get_nodes_from_blocks(blocks):
    nodes = []
    for block in blocks:
        match block_to_blocktype(block):
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                nodes.append(ParentNode(f"h{get_heading_type(block)}", text_to_children(block)))
            case BlockType.QUOTE:
                nodes.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.UNORDERED_LIST:
                nodes.append(ParentNode("ul", block_to_list_items(block)))
            case BlockType.ORDERED_LIST:
                nodes.append(ParentNode("ol", block_to_list_items(block)))
            case BlockType.CODE:
                nodes.append(ParentNode("pre", [LeafNode("code", strip_block_type_tag(block))]))
    return nodes

                

def text_to_children(text):
    formatted_text = strip_block_type_tag(text)
    text_nodes = text_to_textnodes(formatted_text)
    child_nodes = []
    for node in text_nodes:
        child_nodes.append(text_node_to_html_node(node))
    return child_nodes

def block_to_list_items(block):
    if not block_to_blocktype(block) in (BlockType.ORDERED_LIST, BlockType.UNORDERED_LIST):
        raise Exception("not a list block type")
    lines = strip_block_type_tag(block).split("\n")
    return list(map(lambda line: ParentNode("li", text_to_children(line)), lines))

def get_heading_type(heading_block):
    for i in range(1,7):
        if heading_block.startswith(f"{"#"*i} "):
            return i
    raise ValueError("not a proper heading tag")

def strip_block_type_tag(block):
    match block_to_blocktype(block):
        case BlockType.HEADING:
            heading_type = get_heading_type(block)
            return block[heading_type + 1:]
        case BlockType.PARAGRAPH:
            return " ".join(list(map(lambda line: line.strip(), block.split("\n"))))
        case BlockType.CODE:
            return block[4:-3]
        case BlockType.QUOTE:
            return " ".join(list(map(lambda line: line[1:].strip(), block.split("\n"))))
        case BlockType.UNORDERED_LIST:
            return "\n".join(list(map(lambda line: line[2:], block.split("\n"))))
        case BlockType.ORDERED_LIST:
            return "\n".join(list(map(lambda line: line[3:], block.split("\n"))))