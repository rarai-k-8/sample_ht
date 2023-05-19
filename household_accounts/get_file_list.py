# get_file_path_list.py
import os
import re
import sys

# def get_input_path_list(relative_path, extension):
#     drive.mount('/content/drive')
#     input_path = os.path.join('/content/drive/MyDrive/', relative_path)
#     input_filename_list = [f for f in os.listdir(input_path) if f.endswith(extension)]
def get_input_path_list(relative_path, extension):
    # drive.mount('/content/drive')
    input_path = os.path.join('/content/drive/MyDrive/', relative_path)
    input_filename_list = [f for f in os.listdir(input_path) if f.endswith(extension)]
    filename = r"\.({}|{})$".format(extension, extension.upper())
    input_filename_extension_list = [
        f for f in input_filename_list if re.search(filename, f)
    ]
    if len(input_filename_extension_list) == 0:
        sys.exit("{}ファイルがないため処理を終了します".format(extension))
    input_path_list = list(
        map(
            lambda x: os.path.join('/content/drive/MyDrive/', relative_path, x),
            input_filename_extension_list,
        )
    )
    return input_path_list



