import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.seqh.com.au) and [another](https://vbs.1-stop.biz)"
        )
        self.assertListEqual(
            [
                ("link","https://www.seqh.com.au"),
                ("another", "https://vbs.1-stop.biz")
            ], matches)
        
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link to [bootdev](https://boot.dev) and another to [seqh](https://seqh.com.au)",
            TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link to ", TextType.TEXT),
                TextNode("bootdev", TextType.LINK, "https://boot.dev"),
                TextNode(" and another to ", TextType.TEXT),
                TextNode("seqh", TextType.LINK, "https://seqh.com.au")
            ],
            split_nodes_link([node])
        )

    def test_split_nodes_lin_single(self):
        node = TextNode(
            "[bootdev](https://boot.dev)",
            TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("bootdev", TextType.LINK, "https://boot.dev"),
            ],
            split_nodes_link([node])
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a link to ![bootdev](https://boot.dev) and another to ![seqh](https://seqh.com.au)",
            TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link to ", TextType.TEXT),
                TextNode("bootdev", TextType.IMAGE, "https://boot.dev"),
                TextNode(" and another to ", TextType.TEXT),
                TextNode("seqh", TextType.IMAGE, "https://seqh.com.au")
            ],
            split_nodes_image([node])
        )

    def test_split_nodes_image_single(self):
        node = TextNode(
            "![seqh](https://seqh.com.au)",
            TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("seqh", TextType.IMAGE, "https://seqh.com.au"),
            ],
            split_nodes_image([node])
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],  
        text_to_textnodes(text)
    )

if __name__ == "__main__":
    unittest.main()
