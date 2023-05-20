from flask import Flask, request, render_template
# from get_file_list import get_input_path_list
from cut_out_receipt import cut_out_receipts_main
from delete_image import delete
from atosyori import Atosyori
# from gui_show_receipt_contours import MakeFirstPage
import os
from flask import Flask, request, render_template
import io
import base64
import pyocr
import pyocr.builders
from PIL import Image, ImageEnhance, ImageFilter
import glob
app = Flask(__name__)
app.secret_key = 'your_secret_key'
# アップロードされたファイルを保存するディレクトリのパス
UPLOAD_FOLDER = 'src/original_receipt'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # index.htmlをレンダリングする処理
    return render_template('index.html')


# @app.route('/ocr', methods=['POST'])
# def ocr():
#     img_path = request.form['img_path']
#     session['img_path'] = img_path
#     # 画像のOCR処理を行う
#     return render_template('result.html', result=result)
# mobilenet ファインチューニング

@app.route('/result.html')
def result():
    # ocr.htmlをレンダリングする処理
    return render_template('result.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['filename']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # 保存後のパスを取得



        # ここにファイルの処理を記述する
        cut_out_receipts_main(saved_path)
        #cutした画像のパスを取得
        cut_out_path = glob.glob('src/household_accounts/templates/cut_out_receipt/*.png')
        if cut_out_path != []:
            cut_out_path_ = cut_out_path
        else:
            cut_out_path_ = glob.glob('src/original_receipt/*.JPG')
        img = Image.open(cut_out_path_[0])
        # img    
        # グレースケール化する
        img_gray = img.convert('L')
        # 輝度の調整（コントラストと明るさを調整）
        enhancer = ImageEnhance.Brightness(img_gray)
        adjusted_image = enhancer.enhance(1.5)  # コントラストの倍率（1より大きい値でコントラストが増加）
        
        # エッジの検出
        edges = adjusted_image.filter(ImageFilter.FIND_EDGES)
        
        # 二値化
        img_binary = edges.point(lambda x: 255 if x > 128 else 0, '1')  
        # 二値化する
        threshold = 150  # しきい値
        img_binary = img_gray.point(lambda x: 0 if x < threshold else 255, '1')
        #ここでocr
        #OCR
        tools = pyocr.get_available_tools()
        txt1 = tools[0].image_to_string(
            img_binary, 
            lang='jpn',
            builder = pyocr.builders.TextBuilder(tesseract_layout=6)
            )
        #ここに後処理

        # Atosyoriクラスのインスタンスを作成する
        atosyori = Atosyori(txt1)
        atosyori_lines = atosyori.lines
        # dateメソッドを呼び出して、日付と時刻のリストを取得する
        dates, times = atosyori.date()
        nen_gatu_hi = atosyori.nen_gatu_hi()
        #店名を取得
        store = atosyori.store()
        #商品名と代金のリストを取得する
        item_cost_list = atosyori.item_cost()
        #商品名と代金を分割
        item_list, cost_list = atosyori.item_cost_split(item_cost_list)
        #単語分類
        categorize_list = atosyori.word_categorize(item_list)
        #商品名、分類、値段のまとめリストを取得
        item_categorize_cost_list = atosyori.item_categorize_cost(item_list, categorize_list, cost_list)
        #合計金額
        total_cost = atosyori.total_cost()
        print(item_cost_list)
        img_path_list = []
                # img_path_list.append(file_path)
        #　画像ファイルに対する処理
                #　画像書き込み用バッファを確保
        buf = io.BytesIO()
        image = Image.open(cut_out_path_[0])
        #　画像データをバッファに書き込む
        image.save(buf, 'png')
        #　バイナリデータを base64 でエンコードして utf-8 でデコード
        base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        #　HTML 側の src の記述に合わせるために付帯情報付与する
        base64_data = 'data:image/png;base64,{}'.format(base64_str)
        img_path_list.append(base64_data)
        delete()
        return render_template('result.html',
                               img_path_list=img_path_list, 
                               ocr_text = atosyori_lines,
                               nen_gatu_hi = nen_gatu_hi,
                               store = store,
                               item_cost_list = item_cost_list,
                               item_list = item_list,
                               categorize_list = categorize_list,
                               cost_list = cost_list,
                               item_categorize_cost_list = item_categorize_cost_list,
                               total_cost = total_cost)
    else:
        return '''
        <!doctype html>
        <html>
        <head>
            <title>アップロード</title>
        </head>
        <body>
            <h1>こちらにレシート画像をアップロードしてください。</h1>
            <form method="post" enctype="multipart/form-data">
                <p><input type="file" name="filename"></p>
                <p><input type="submit" value="アップロード"></p>
            </form>
        </body>
        </html>
        '''

if __name__ == '__main__':
    app.run(port=5050, debug=True)



