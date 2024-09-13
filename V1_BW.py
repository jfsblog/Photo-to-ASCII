#V1_BW.py
#圖片轉為黑白的ASCII藝術

from PIL import Image

# 符號對應表，根據[1][2][3][4]的黑白組合選取符號
symbol_map = {
    (1, 1, 1, 1): '█', (1, 1, 0, 0): '▀', (0, 0, 1, 1): '▄', 
    (1, 0, 1, 0): '▌', (0, 1, 0, 1): '▐', (0, 0, 0, 1): '▖', 
    (1, 0, 0, 0): '▘', (1, 0, 1, 1): '▙', (1, 0, 1, 0): '▚',
    (1, 1, 1, 0): '▛', (1, 1, 0, 1): '▜', (0, 0, 1, 0): '▝', 
    (0, 1, 1, 0): '▞', (0, 1, 1, 1): '▟', (0, 0, 0, 0): '░'
}

# 讀取並處理圖片
def image_to_ascii(image_path, block_size=2, max_width=60):
    img = Image.open(image_path).convert('L')  # 轉換為灰階

    # 先將圖片寬度拉伸兩倍，防止ASCII圖案寬高比例失調
    width, height = img.size
    img = img.resize((width * 2, height))

    # 縮小圖片以適應最大寬度
    new_width, new_height = img.size
    if new_width > max_width * block_size:
        scale_factor = (max_width * block_size) / new_width
        new_width = int(new_width * scale_factor)
        new_height = int(new_height * scale_factor)
        img = img.resize((new_width, new_height))

    # 二值化
    img = img.point(lambda p: p > 128 and 255)

    ascii_art = []

    for y in range(0, new_height, block_size):
        row = []
        for x in range(0, new_width, block_size):
            # 提取每個4像素方塊內的像素
            pixels = [
                img.getpixel((x, y)),     # [1] 左上
                img.getpixel((x+1, y)) if x+1 < new_width else 255,   # [2] 右上
                img.getpixel((x, y+1)) if y+1 < new_height else 255,  # [3] 左下
                img.getpixel((x+1, y+1)) if x+1 < new_width and y+1 < new_height else 255  # [4] 右下
            ]

            # 將每個像素轉換為0或1，黑為1，白為0
            binary_pixels = tuple(1 if p == 0 else 0 for p in pixels)
            
            # 從對應表中查找符號
            symbol = symbol_map.get(binary_pixels, '░')
            row.append(symbol)
        ascii_art.append(''.join(row))

    # 將結果合併為多行字符串
    return '\n'.join(ascii_art)

# 使用範例，指定最大寬度為60格
ascii_image = image_to_ascii('t1.jpg', max_width=40)
print(ascii_image)