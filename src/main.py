import os
import shutil
from copystatic import copy_files_recursive
from block_markdown import markdown_to_blocks, get_heading_type, markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./public"
dir_to_markdown = "./content/index.md"
dir_to_template = "./template.html"

def main():
   print("Deleting Public Folder")
   delete_public()
   print("Copying files from static to public")
   copy_files_recursive(dir_path_static, dir_path_public)

   generate_pages_recursive("./content", "./template.html", "./public")


def delete_public():
   if os.path.exists(dir_path_public):
      shutil.rmtree(dir_path_public)


def extract_title(markdown):
   for block in markdown_to_blocks(markdown):
      if get_heading_type(block) == 1:
         return block.strip("#").strip()
   raise Exception("no h1 present")

def generate_page(from_path, template_path, dest_path):
   print(f"Generating page from {from_path} to {dest_path} using {template_path}")
   markdown = get_contents(from_path)
   template = get_contents(template_path)
   html = markdown_to_html_node(markdown).to_html()
   title = extract_title(markdown)
   template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
   print_to_file(template, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
      if not os.path.exists(dest_dir_path):
         os.mkdir(dest_dir_path)
    
      for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
        print(f"* {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

def get_contents(file_path):
   with open(file_path) as f:
      return f.read()
   
def print_to_file(content, dest_path):
   with open(dest_path, "x") as f:
      f.write(content)
      f.close()

main()