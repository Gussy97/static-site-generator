import unittest
from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("Test2", TextType.CODE)
        node2 = TextNode("Test1", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_same_info_dif_url(self):
        node1 = TextNode("Test", TextType.TEXT)
        node2 = TextNode("Test", TextType.TEXT, "https://seqh.com.au")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()
