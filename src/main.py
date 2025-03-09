from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

def main():
    child = LeafNode("a", "Angus", props={"href":"https://angus.com", "target":"_blank"})
    parent = ParentNode("div", [child])

    print(parent.to_html())


main()