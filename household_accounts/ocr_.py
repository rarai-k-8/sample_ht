from PIL import Image
img = Image.open('src/original_receipt/IMG_0506.JPG')
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
img_binary.show()