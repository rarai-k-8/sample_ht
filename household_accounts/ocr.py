import pyocr
import pyocr.builders        
from PIL import Image
from atosyori import Atosyori
class OCR:
    def __init__(self, cut_out_path_):
        img = Image.open(cut_out_path_[0])
        # img    
        
        
        # 前処理
        
        # リサイズするサイズを計算する
        width, height = img.size
        aspect_ratio = float(height) / float(width)
        new_width = 800
        new_height = int(aspect_ratio * new_width)

        # 解像度を調整する
        img = img.resize((new_width, new_height))

        # グレースケール化する
        img_gray = img.convert('L')

        # 二値化する
        threshold = 150  # しきい値
        img_binary = img_gray.point(lambda x: 0 if x < threshold else 255, '1')
        #ここでocr
        tools = pyocr.get_available_tools()
        txt1 = tools[0].image_to_string(
            img_binary, 
            lang='jpn+eng',
            builder = pyocr.builders.TextBuilder(tesseract_layout=6)
            )
        #ここに後処理

        # Atosyoriクラスのインスタンスを作成する
        atosyori = Atosyori(txt1)
        atosyori_lines = atosyori.lines
        # dateメソッドを呼び出して、日付と時刻のリストを取得する
        dates, times = atosyori.date()