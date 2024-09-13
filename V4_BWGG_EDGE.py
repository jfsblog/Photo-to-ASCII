#V4_BWGG_EDGE.py
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 顯示圖片函數
def show(image, title='Image', is_gray=False):
    if is_gray:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

# 圖像轉為灰階
def convert_to_gray(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    show(img_gray, 'Gray Image', is_gray=True)
    return img_gray

# 邊緣檢測並調整粗細與敏感度
def detect_edges(img_gray, edge_thickness=3, edge_sensitivity=(100, 200)):
    edges = cv2.Canny(img_gray, edge_sensitivity[0], edge_sensitivity[1])
    
    # 使用膨脹操作來調整邊緣的粗細
    kernel = np.ones((edge_thickness, edge_thickness), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    
    show(dilated_edges, 'Dilated Edges', is_gray=True)
    return dilated_edges

# 疊加邊緣到灰階圖像
def overlay_edges_on_gray(img_gray, edges):
    img_gray_edge = img_gray.copy()
    img_gray_edge[edges > 0] = 0  # 將邊緣部分設為黑色
    show(img_gray_edge, 'Gray Image with Edges', is_gray=True)
    return img_gray_edge

# 圖片轉為黑白灰與深灰的ASCII藝術
def image_to_ascii(img_gray_edge, block_size=2, max_width=60, threshold=50):
    # PIL 需要的灰階轉換
    img = Image.fromarray(img_gray_edge).convert('L')
    
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
    
    ascii_art = []
    
    # 符號對應表，根據更多的灰度範圍選取符號
    symbol_map = {
        (1, 1, 1, 1): '█',  # 黑色
        (1, 1, 0, 0): '▀',  # 上半部
        (0, 0, 1, 1): '▄',  # 下半部
        (1, 0, 1, 0): '▌',  # 左半部
        (0, 1, 0, 1): '▐',  # 右半部
        (0, 0, 0, 1): '▖',  # 左下角
        (1, 0, 0, 0): '▘',  # 左上角
        (1, 0, 1, 1): '▙',  # 左邊和下方
        (1, 0, 1, 0): '▚',  # 左上和右下
        (1, 1, 1, 0): '▛',  # 上方和左邊
        (1, 1, 0, 1): '▜',  # 上方和右邊
        (0, 0, 1, 0): '▝',  # 右上角
        (0, 1, 1, 0): '▞',  # 右邊和下方
        (0, 1, 1, 1): '▟',  # 右邊和下方加左上角
        "light_gray": '▒',  # 淺灰色
        "dark_gray": '▓',  # 深灰色
        (0, 0, 0, 0): '░',  # 白色
    }
    
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
            
            # 計算灰階值差異
            max_pixel = max(pixels)
            min_pixel = min(pixels)
            pixel_diff = max_pixel - min_pixel

            if pixel_diff <= threshold:
                # 若灰階差異不大，根據平均灰階值選擇符號
                avg_pixel_value = sum(pixels) / 4
                if avg_pixel_value < 64:
                    symbol = symbol_map[(1, 1, 1, 1)]  # 黑色
                elif avg_pixel_value < 128:
                    symbol = symbol_map["dark_gray"]  # 深灰
                elif avg_pixel_value < 192:
                    symbol = symbol_map["light_gray"]  # 淺灰
                else:
                    symbol = symbol_map[(0, 0, 0, 0)]  # 白色
            else:
                # 若灰階差異大，根據像素模式選擇符號
                pattern = tuple(1 if p < 128 else 0 for p in pixels)
                symbol = symbol_map.get(pattern, '░')  # 根據模式選擇符號，默認為白色
            
            row.append(symbol)
        ascii_art.append(''.join(row))
    
    return '\n'.join(ascii_art)

# 主流程
def process_image(image_path, edge_thickness=3, edge_sensitivity=(100, 200), block_size=2, max_width=60, threshold=50):
    # 1. 讀取照片
    img = cv2.imread(image_path)
    show(img, 'Original Image')
    
    # 2. 轉為灰階
    img_gray = convert_to_gray(img)
    
    # 3. 偵測邊緣
    edges = detect_edges(img_gray, edge_thickness, edge_sensitivity)
    
    # 4. 將邊緣疊加到灰階圖上
    img_gray_edge = overlay_edges_on_gray(img_gray, edges)
    
    # 5. 將結果轉換為 ASCII 藝術
    ascii_art = image_to_ascii(img_gray_edge, block_size, max_width, threshold)
    print(ascii_art)

# 使用範例
process_image('t1.jpg', edge_thickness=5, edge_sensitivity=(30, 200), block_size=2, max_width=60, threshold=50)