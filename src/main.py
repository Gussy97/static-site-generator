from inline_markdown import *
from block_markdown import *


def main():
   markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item

```
This is code
```

>This is a quote
>That continues **to** this line
>and this _line_

1. this is the first _item_ in an ordered list
2. and this is the `second`
3. and this is the **third**

"""
   for block in markdown_to_blocks(markdown):
      if block_to_blocktype(block) in (BlockType.ORDERED_LIST,):
         for node in get_nodes_from_blocks([block]):
            print(node.to_html())
main()