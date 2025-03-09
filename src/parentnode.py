from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag must have a value")
        if self.children is None:
            raise ValueError("element must have children")
        
        if isinstance(self, LeafNode):
            return self.to_html()
        
        return "".join(map(lambda node: f"<{node.tag}{node.props_to_html()}>{node.to_html()}</{node.tag}>", self.children))
        