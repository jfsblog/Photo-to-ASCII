import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QLineEdit, QTextEdit
from PySide6.QtGui import QPixmap, QImage, QClipboard
from PySide6.QtCore import QFile, Qt, QCoreApplication
from PySide6.QtUiTools import QUiLoader
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        
        # 載入 UI
        self.ui = load_ui("V1.ui")
        self.setCentralWidget(self.ui)

        # 獲取按鈕和標籤
        self.pushButton_load = self.ui.findChild(QPushButton, "pushButton_load")
        self.pushButton_image_processor = self.ui.findChild(QPushButton, "pushButton_image_processor")
        self.pushButton_ascii = self.ui.findChild(QPushButton, "pushButton_ascii")
        self.pushButton_copy = self.ui.findChild(QPushButton, "pushButton_copy")  # 新增 pushButton_copy
        self.label_path = self.ui.findChild(QLabel, "label_path")
        self.label_original = self.ui.findChild(QLabel, "label_original")
        self.label_gray = self.ui.findChild(QLabel, "label_gray")
        self.label_dilated_edges = self.ui.findChild(QLabel, "label_dilated_edges")
        self.label_mix = self.ui.findChild(QLabel, "label_mix")
        self.lineEdit_edge_thickness = self.ui.findChild(QLineEdit, "lineEdit_edge_thickness")
        self.lineEdit_edge_sensitivity_x = self.ui.findChild(QLineEdit, "lineEdit_edge_sensitivity_x")
        self.lineEdit_edge_sensitivity_y = self.ui.findChild(QLineEdit, "lineEdit_edge_sensitivity_y")
        self.lineEdit_max_width = self.ui.findChild(QLineEdit, "lineEdit_max_width")
        self.lineEdit_threshold = self.ui.findChild(QLineEdit, "lineEdit_threshold")
        self.textEdit = self.ui.findChild(QTextEdit, "textEdit")

        # 設置 QLabel 的 scaledContents 屬性
        self.label_original.setScaledContents(True)
        self.label_gray.setScaledContents(True)
        self.label_dilated_edges.setScaledContents(True)
        self.label_mix.setScaledContents(True)

        # 連接按鈕點擊事件
        self.pushButton_load.clicked.connect(self.load_image)
        self.pushButton_image_processor.clicked.connect(self.process_image)
        self.pushButton_ascii.clicked.connect(self.generate_ascii_art)
        self.pushButton_copy.clicked.connect(self.copy_to_clipboard)  # 新增複製功能

        self.img = None

    # 複製 textEdit 的內容到剪貼板
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textEdit.toPlainText())  # 從 textEdit 取得內容並複製到剪貼板

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇圖片", "", "圖片檔案 (*.png *.jpg *.bmp *.jpeg)")
        if file_path:
            self.label_path.setText(file_path)
            self.img = cv2.imread(file_path)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

            if self.img is not None:
                pixmap_original = QPixmap.fromImage(self.convert_cv_to_qimage(self.img))
                self.label_original.setPixmap(pixmap_original)
                self.label_original.setPixmap(pixmap_original.scaled(self.label_original.size(), Qt.AspectRatioMode.KeepAspectRatio))
            else:
                print(f"Error: Failed to load image from {file_path}.")
                self.label_original.clear()
                self.label_path.setText("Failed to load image.")

    def process_image(self):
        if self.img is None:
            print("Error: No image loaded.")
            return

        # 獲取用戶輸入
        edge_thickness = int(self.lineEdit_edge_thickness.text())
        edge_sensitivity_x = int(self.lineEdit_edge_sensitivity_x.text())
        edge_sensitivity_y = int(self.lineEdit_edge_sensitivity_y.text())
        edge_sensitivity = (edge_sensitivity_x, edge_sensitivity_y)

        # 將原始圖片轉為灰階並顯示
        img_gray = self.convert_to_gray(self.img)
        pixmap_gray = QPixmap.fromImage(self.convert_cv_to_qimage(img_gray, is_gray=True))
        self.label_gray.setPixmap(pixmap_gray)
        self.label_gray.setPixmap(pixmap_gray.scaled(self.label_gray.size(), Qt.AspectRatioMode.KeepAspectRatio))

        # 偵測邊緣並顯示
        edges = self.detect_edges(img_gray, edge_thickness, edge_sensitivity)
        pixmap_edges = QPixmap.fromImage(self.convert_cv_to_qimage(edges, is_gray=True))
        self.label_dilated_edges.setPixmap(pixmap_edges)
        self.label_dilated_edges.setPixmap(pixmap_edges.scaled(self.label_dilated_edges.size(), Qt.AspectRatioMode.KeepAspectRatio))

        # 邊緣疊加在灰階圖像上並顯示
        img_gray_edge = self.overlay_edges_on_gray(img_gray, edges)
        pixmap_gray_edge = QPixmap.fromImage(self.convert_cv_to_qimage(img_gray_edge, is_gray=True))
        self.label_mix.setPixmap(pixmap_gray_edge)
        self.label_mix.setPixmap(pixmap_gray_edge.scaled(self.label_mix.size(), Qt.AspectRatioMode.KeepAspectRatio))

        # 保存 img_gray_edge 用於生成 ASCII 藝術
        self.img_gray_edge = img_gray_edge

    def generate_ascii_art(self):
        if self.img_gray_edge is None:
            print("Error: No processed image available.")
            return

        # 獲取用戶輸入
        max_width = int(self.lineEdit_max_width.text())
        threshold = int(self.lineEdit_threshold.text())

        # 使用預設值 block_size
        block_size = 2

        # 將邊緣圖像轉換為 ASCII 藝術
        ascii_art = self.image_to_ascii(self.img_gray_edge, block_size, max_width, threshold)
        
        # 在 TextEdit 中顯示 ASCII 藝術
        self.textEdit.setPlainText(ascii_art)

    def convert_to_gray(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img_gray

    def detect_edges(self, img_gray, edge_thickness=3, edge_sensitivity=(100, 200)):
        edges = cv2.Canny(img_gray, edge_sensitivity[0], edge_sensitivity[1])
        kernel = np.ones((edge_thickness, edge_thickness), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)
        return dilated_edges

    def overlay_edges_on_gray(self, img_gray, edges):
        img_gray_edge = img_gray.copy()
        img_gray_edge[edges > 0] = 0
        return img_gray_edge

    def convert_cv_to_qimage(self, img, is_gray=False):
        if is_gray:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return q_image

    def image_to_ascii(self, img_gray_edge, block_size=2, max_width=60, threshold=50):
        img = Image.fromarray(img_gray_edge).convert('L')
        width, height = img.size
        img = img.resize((int(width * 1.5), height))
        new_width, new_height = img.size
        if new_width > max_width * block_size:
            scale_factor = (max_width * block_size) / new_width
            new_width = int(new_width * scale_factor)
            new_height = int(new_height * scale_factor)
            img = img.resize((new_width, new_height))
        
        ascii_art = []
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
                pixels = [
                    img.getpixel((x, y)),     # [1] 左上
                    img.getpixel((x+1, y)) if x+1 < new_width else 255,   # [2] 右上
                    img.getpixel((x, y+1)) if y+1 < new_height else 255,  # [3] 左下
                    img.getpixel((x+1, y+1)) if x+1 < new_width and y+1 < new_height else 255  # [4] 右下
                ]
                max_pixel = max(pixels)
                min_pixel = min(pixels)
                pixel_diff = max_pixel - min_pixel

                if pixel_diff <= threshold:
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
                    pattern = tuple(1 if p < 128 else 0 for p in pixels)
                    symbol = symbol_map.get(pattern, '░')  # 根據模式選擇符號，默認為白色
                
                row.append(symbol)
            ascii_art.append(''.join(row))
        
        return '\n'.join(ascii_art)

def load_ui(file_name):
    loader = QUiLoader()
    ui_file = QFile(file_name)
    ui_file.open(QFile.ReadOnly)
    ui = loader.load(ui_file)
    ui_file.close()
    return ui

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()