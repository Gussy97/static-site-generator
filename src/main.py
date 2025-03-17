import os
import shutil
from copystatic import copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"

def main():
   print("Deleting Public Folder")
   delete_public()
   print("Copying files from static to public")
   copy_files_recursive(dir_path_static, dir_path_public)


def delete_public():
   if os.path.exists(dir_path_public):
      shutil.rmtree(dir_path_public)


main()