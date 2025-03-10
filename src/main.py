from inline_markdown import *

def main():
   node = TextNode(
            "This is text with a link to [bootdev](https://boot.dev) and another to [seqh](https://seqh.com.au)",
            TextType.TEXT
        )
   
   split_nodes_link([node]) 



main()