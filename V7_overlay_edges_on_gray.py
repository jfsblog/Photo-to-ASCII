import numpy as np

def overlay_edges_on_gray_ideogram(img_gray, edges):
    img_gray_edge = img_gray.copy()
    img_gray_edge[edges > 0] = 0
    return img_gray_edge

def overlay_edges_on_gray_photo(img_gray, edges):
    img_gray_edge = img_gray.copy()
    
    # 獲取邊緣的坐標
    edge_coords = np.argwhere(edges > 0)
    
    for coord in edge_coords:
        y, x = coord
        
        # 定義一個小區域（例如3x3）
        y_start = max(y - 1, 0)
        y_end = min(y + 2, img_gray.shape[0])
        x_start = max(x - 1, 0)
        x_end = min(x + 2, img_gray.shape[1])
        
        # 獲取局部區域的亮度
        local_region = img_gray[y_start:y_end, x_start:x_end]
        local_mean_brightness = local_region.mean()

        # 根據局部亮度決定邊緣顏色
        if local_mean_brightness < 100:  # 較暗
            img_gray_edge[y, x] = 255  # 用白色
        elif local_mean_brightness >= 100 and local_mean_brightness < 200:  # 暗與亮的邊界
            # img_gray_edge[y, x] = 0  # 用黑色
            continue  # 跳過這個像素，不疊加邊緣
        else:  # 較亮
            img_gray_edge[y, x] = 0  # 用黑色
            
    return img_gray_edge