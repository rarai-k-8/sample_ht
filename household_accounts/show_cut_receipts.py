import os
from PIL import Image
def display_png_images():
    directory = '/Users/harutohata/Desktop/AIレシート解析アプリ/src/cut_out_receipt'
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.png'):
                file_path = os.path.join(root, filename)
                img = Image.open(file_path)
                img.show()
    if len(file_path) == 0:
        print("レシートが検出できませんでした。")
    else:
        print("正しく検出されたレシートを選択してください。")
