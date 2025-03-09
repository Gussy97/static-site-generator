import unittest
from textnode import TextNode, TextType

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
        node1 = TextNode("Test", TextType.NORMAL)
        node2 = TextNode("Test", TextType.NORMAL, "https://seqh.com.au")

if __name__ == "__main__":
    unittest.main()
