import cv2
import numpy as np
from PySide6.QtWidgets import QMessageBox, QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QLineEdit, QTextEdit, QSlider, QDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QFile, Qt, QCoreApplication
from PySide6.QtUiTools import QUiLoader
from PIL import Image

from V7_overlay_edges_on_gray import overlay_edges_on_gray_ideogram
from V7_overlay_edges_on_gray import overlay_edges_on_gray_photo

class InstructionsWindow(QDialog):
    def __init__(self):
        super(InstructionsWindow, self).__init__()

        # 加載 Instructions.ui
        loader = QUiLoader()
        file = QFile("Instructions.ui")
        file.open(QFile.ReadOnly)
        self.window = loader.load(file, self)
        self.setWindowTitle("參數說明")
        file.close()

        # 連接 pushButton_close 到關閉方法
        self.window.pushButton_close.clicked.connect(self.close)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        
        # 載入 UI
        self.ui = load_ui("V4.ui")
        self.setCentralWidget(self.ui)
        self.setWindowTitle("圖片轉ASCII文字產生器")

        # 獲取按鈕和標籤
        self.pushButton_load = self.ui.findChild(QPushButton, "pushButton_load")
        self.pushButton_image_processor = self.ui.findChild(QPushButton, "pushButton_image_processor")
        self.pushButton_ascii = self.ui.findChild(QPushButton, "pushButton_ascii")
        self.pushButton_copy = self.ui.findChild(QPushButton, "pushButton_copy")
        self.pushButton_instructions = self.ui.findChild(QPushButton, "pushButton_instructions")  # 新增說明按鈕
        self.label_path = self.ui.findChild(QLabel, "label_path")
        self.label_original = self.ui.findChild(QLabel, "label_original")
        self.label_gray = self.ui.findChild(QLabel, "label_gray")
        self.label_dilated_edges = self.ui.findChild(QLabel, "label_dilated_edges")
        self.label_mix = self.ui.findChild(QLabel, "label_mix")
        self.lineEdit_edge_thickness = self.ui.findChild(QLineEdit, "lineEdit_edge_thickness")
        self.lineEdit_edge_sensitivity_x = self.ui.findChild(QLineEdit, "lineEdit_edge_sensitivity_x")
        self.lineEdit_edge_sensitivity_y = self.ui.findChild(QLineEdit, "lineEdit_edge_sensitivity_y")
        self.horizontalSlider_contrast = self.ui.findChild(QSlider, "horizontalSlider_contrast")
        self.label_contrast = self.ui.findChild(QLabel, "label_contrast")
        self.lineEdit_max_width = self.ui.findChild(QLineEdit, "lineEdit_max_width")
        self.textEdit = self.ui.findChild(QTextEdit, "textEdit")
        self.horizontalSlider_graylevel = self.ui.findChild(QSlider, "horizontalSlider_graylevel")
        self.label_graylevel = self.ui.findChild(QLabel, "label_graylevel")

        # 設置 QLabel 的 scaledContents 屬性
        self.label_original.setScaledContents(True)
        self.label_gray.setScaledContents(True)
        self.label_dilated_edges.setScaledContents(True)

        # 連接按鈕點擊事件
        self.pushButton_load.clicked.connect(self.load_image)
        self.pushButton_image_processor.clicked.connect(self.process_image)
        self.pushButton_ascii.clicked.connect(self.generate_ascii_art)
        self.pushButton_copy.clicked.connect(self.copy_to_clipboard)
        self.pushButton_instructions.clicked.connect(self.show_instructions)  # 連接說明按鈕到對應的槽函數

        # 連接 slider 的值變化事件到槽函數
        self.horizontalSlider_contrast.valueChanged.connect(self.update_contrastlevel)
        self.horizontalSlider_graylevel.valueChanged.connect(self.update_graylevel)

        # 初始化 img
        self.img = None        
        # 初始化 img_gray_edge 為 None
        self.img_gray_edge = None

    # 更新 horizontalSlider_contrast 和 label_contrast
    def update_contrastlevel(self):
        constrast_value = self.horizontalSlider_contrast.value() / 10  # 獲取滑動條的當前值
        self.label_contrast.setText(str(constrast_value))  # 更新 label_contrast 的顯示

    # 更新 horizontalSlider_graylevel 和 label_graylevel
    def update_graylevel(self):
        graylevel_value = self.horizontalSlider_graylevel.value()  # 獲取滑動條的當前值
        self.label_graylevel.setText(str(graylevel_value))  # 更新 label_graylevel 的顯示

    # 複製 textEdit 的內容到剪貼板
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textEdit.toPlainText())  # 從 textEdit 取得內容並複製到剪貼板

    def load_image(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "選擇圖片", "", "圖片檔案 (*.png *.jpg *.bmp *.jpeg)")
            self.label_path.setText(file_path)
            self.img = cv2.imread(file_path)
            
            # 檢查影像是否成功載入
            if self.img is None:
                raise ValueError("影像載入失敗！請檢查路徑不能有特殊字元或中文")

            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

            # 轉換影像並顯示
            pixmap_original = QPixmap.fromImage(self.convert_cv_to_qimage(self.img))
            self.label_original.setPixmap(pixmap_original)
            self.label_original.setPixmap(pixmap_original.scaled(self.label_original.size(), Qt.AspectRatioMode.KeepAspectRatio))
            
        except ValueError as e:
            self.show_error_message(str(e))
            self.label_original.clear()
            self.label_path.setText("影像載入失敗")

    def process_image(self):
        if self.img is None:
            self.show_error_message("請先載入圖片")
            return

        try:
            # 檢測 edge_thickness
            edge_thickness = self.lineEdit_edge_thickness.text()
            if not edge_thickness.isdigit() or int(edge_thickness) <= 0:
                raise ValueError("邊緣線粗細必須為正整數")
            
            # 檢測 edge_sensitivity_x 和 edge_sensitivity_y
            edge_sensitivity_x = self.lineEdit_edge_sensitivity_x.text()
            edge_sensitivity_y = self.lineEdit_edge_sensitivity_y.text()
            if not edge_sensitivity_x.isdigit() or not edge_sensitivity_y.isdigit():
                raise ValueError("邊緣敏感度必須為正整數")
            if int(edge_sensitivity_x) <= 0 or int(edge_sensitivity_y) <= 0:
                raise ValueError("邊緣敏感度必須為正整數")
            if int(edge_sensitivity_y) < int(edge_sensitivity_x):
                raise ValueError("邊緣敏感度上限必須大於或等於下限")
            
            # 檢測 max_width
            max_width = self.lineEdit_max_width.text()
            if not max_width.isdigit() or int(max_width) <= 0:
                raise ValueError("文字圖寬度必須為正整數")
            
            # 將值轉為整數
            edge_thickness = int(edge_thickness)
            edge_sensitivity = (int(edge_sensitivity_x), int(edge_sensitivity_y))
            max_width = int(max_width)

        except ValueError as e:
            # 顯示自訂錯誤訊息
            self.show_error_message(str(e))
            return

        # 將原始圖片轉為灰階並顯示
        img_gray = self.convert_to_gray(self.img)
        pixmap_gray = QPixmap.fromImage(self.convert_cv_to_qimage(img_gray, is_gray=True))
        self.label_gray.setPixmap(pixmap_gray)
        self.label_gray.setPixmap(pixmap_gray.scaled(self.label_gray.size(), Qt.AspectRatioMode.KeepAspectRatio))

        #調整圖片對比度
        contrast_parameter = self.horizontalSlider_contrast.value()
        alpha = contrast_parameter
        img_contrast = cv2.convertScaleAbs(self.img, alpha=alpha, beta=0)

        # 偵測邊緣並顯示
        edges = self.detect_edges(img_contrast, edge_thickness, edge_sensitivity)
        pixmap_edges = QPixmap.fromImage(self.convert_cv_to_qimage(edges, is_gray=True))
        self.label_dilated_edges.setPixmap(pixmap_edges)
        self.label_dilated_edges.setPixmap(pixmap_edges.scaled(self.label_dilated_edges.size(), Qt.AspectRatioMode.KeepAspectRatio))

        # 根據 comboBox_method 的選擇決定使用哪個方法
        selected_method = self.ui.comboBox_method.currentText()
        if selected_method == "適用示意圖":
            img_gray_edge = overlay_edges_on_gray_ideogram(img_gray, edges)
        elif selected_method == "適用實拍照":
            img_gray_edge = overlay_edges_on_gray_photo(img_gray, edges)
        else:
            self.show_error_message("無效的處理方法選擇")
            return

        # 邊緣疊加在灰階圖像上並顯示
        pixmap_gray_edge = QPixmap.fromImage(self.convert_cv_to_qimage(img_gray_edge, is_gray=True))
        self.label_mix.setPixmap(pixmap_gray_edge)
        self.label_mix.setPixmap(pixmap_gray_edge.scaled(self.label_mix.size(), Qt.AspectRatioMode.KeepAspectRatio))

        # 保存 img_gray_edge 用於生成 ASCII 藝術
        self.img_gray_edge = img_gray_edge

    def generate_ascii_art(self):
        if self.img_gray_edge is None:
            self.show_error_message(f"請載入照片後進行影像處理，再進行ASCII生成")
            return

        # 獲取用戶輸入
        max_width = int(self.lineEdit_max_width.text())
        threshold = int(self.horizontalSlider_graylevel.value())

        # 使用預設值 block_size
        block_size = 2

        # 將邊緣圖像轉換為 ASCII 藝術
        ascii_art = self.image_to_ascii(self.img_gray_edge, block_size, max_width, threshold)
        
        # 在 TextEdit 中顯示 ASCII 藝術
        self.textEdit.setPlainText(ascii_art)

    def convert_to_gray(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img_gray

    def detect_edges(self, img, edge_thickness, edge_sensitivity):
        edges = cv2.Canny(img, edge_sensitivity[0], edge_sensitivity[1])
        kernel = np.ones((edge_thickness, edge_thickness), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)
        return dilated_edges

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
            "dark_gray": '▓',  # 深灰色
            "light_gray": '▒',  # 淺灰色
            "light_light_gray": '░', # 淺淺灰色
            "light_light_light_gray": '．', # 淺淺灰色
            (0, 0, 0, 0): '　',  # 白色
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
                    elif avg_pixel_value < 110:
                        symbol = symbol_map["dark_gray"]  # 深灰
                    elif avg_pixel_value < 145:
                        symbol = symbol_map["light_gray"]  # 淺灰
                    elif avg_pixel_value < 180:
                        symbol = symbol_map["light_light_gray"]  # 淺灰
                    elif avg_pixel_value < 215:
                        symbol = symbol_map["light_light_light_gray"]  # 淺灰  
                    else:
                        symbol = symbol_map[(0, 0, 0, 0)]  # 白色
                else:
                    pattern = tuple(1 if p < 128 else 0 for p in pixels)
                    symbol = symbol_map.get(pattern, '░')  # 根據模式選擇符號，默認為白色
                
                row.append(symbol)
            ascii_art.append(''.join(row))
        
        return '\n'.join(ascii_art)

    def show_instructions(self):
        # 創建並顯示 InstructionsWindow 作為非模態窗口
        self.instructions_window = InstructionsWindow()
        self.instructions_window.show()  # 使用 show() 方法，讓窗口非模態化

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("錯誤")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

def load_ui(ui_file_path):
    loader = QUiLoader()
    ui_file = QFile(ui_file_path)
    ui_file.open(QFile.ReadOnly)
    ui = loader.load(ui_file)
    ui_file.close()
    return ui

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()