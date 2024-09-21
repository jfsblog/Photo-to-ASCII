# V7 灰階影像疊加邊緣並生成ASCII藝術

## 專案概述

此專案提供一個應用程式，用於將圖片轉換成ASCII藝術文字，雖然只是一個無聊的小創意，但還是把它寫成一個簡單的小程式。你問我ASCII藝術文字有什麼用？老實說我也不知道（哈），或許PTT吧！

這個程式的藝術生成邏輯有點類似點點畫（Stipple Art）或點陣圖（Bitmap）的概念，撰風在國中時有畫過這樣的畫，透過點的密集度去形成陰影的視覺效果，而在此可以利用不同全型特殊文字的差異，達到類似的效果，最直觀的就是：█、▓、▒、░、．，以及全形空格，剛好可以對應不同程度的明暗，當然也可以採用其他的符號，下載者可以自行調整。此外，撰風在查看特殊文字時，還有發現一些特殊的符號，諸如：▀、▄、▌、▐、▖、▘、▙、▚、▛、▜、▝、▞，以及▟，這些在邊緣繪製上可以達到不錯的效果。

在此專案中，首先要將圖片轉為灰階，根據生成ASCII藝術文字的寬度去分割灰階圖片，然後將每一格分割成四格小格，分別偵測其明亮度，若四格平均亮度差異不大，則根據整體亮度選擇填入「█、▓、▒、░、．，或全形空格」，若四小格中有明顯的明亮差異，則可以根據明亮程度選擇填入「▀、▄、▌、▐、▖、▘、▙、▚、▛、▜、▝、▞，以及▟」。

而後版本測試中，發現有些圖片如果只是直接進行轉換，則轉換效果有限，因此加入邊緣測試的功能，利用Canny進行邊緣偵測，並將這些邊緣進行塗色與膨脹，疊在加灰階圖上，如此生成的ASCII藝術文字在邊緣辨識度上會更好。不過經過多次測試，若是載入的圖片是較為複雜的實拍照片，短寬度ASCII藝術文字生成的效果有限，建議還是採用圖案較為簡潔、對比度高且不過過於複雜的平面藝術作品（例如：ICON、LOGO），在生成效果會不錯。

此外，由於不是每種字型都能將這些特殊文字以等寬的文字進行顯示，因此使用者的介面若採用不符合的字型，則無法有效顯示出良好的ASCII藝術文字，目前測試[Google Noto Sans](https://www.google.com/get/noto/)系列會是可以很好呈現這個效果的字型。

### 主要功能
1. **邊緣偵測與疊加**：兩種邊緣疊加方法，一種適用於示意圖（疊加的邊緣線條為黑色），另一種適用於實拍照片（疊加的線條會根據該點附近的灰階給予黑或白）。
2. **灰階轉換**：將影像轉換為灰階進行處理。
3. **邊緣自定義**：可調整的邊緣粗細和靈敏度設置。
4. **ASCII藝術生成**：從處理過的影像生成ASCII藝術，並可自定義寬度與灰階級別。
5. **互動式GUI**：基於PySide6的圖形介面，方便選擇影像、調整設置並生成ASCII藝術。

## Python模組

在運行此專案之前，請確保已安裝以下庫：

 ```bash
pip install numpy opencv-python pillow PySide6
 ```

## 檔案結構

- **V7_overlay_edges_on_gray.py**：包含兩個函數，用於將邊緣疊加到示意圖和實拍照片的灰階影像上。
- **V8_UI.py**：主應用程式腳本，負責載入UI、處理影像並生成ASCII藝術。
- **V3.ui**：使用Qt Designer設計的.ui文件，定義了GUI的佈局和組件。

## 使用步驟

### 步驟1：運行應用程式

運行應用程式，執行以下命令：

 ```bash
python V8_UI.py
 ```

### 步驟2：載入圖片

1. 點擊**載入圖片**按鈕，選擇一張影像（支援 .png、.jpg、.bmp、.jpeg 格式）。
2. 影像路徑將顯示在界面中，並將影像載入到GUI中。

### 步驟3：影像處理與參數調整

1. **邊緣粗細**：增大數值會使 ASCII 藝術中的邊緣變得更粗，能夠更清晰地突出圖像輪廓；相反，數值較小時，邊緣會變得更細緻，適合呈現柔和的效果。

2. **邊緣靈敏度**：這兩個參數用來調整邊緣檢測的敏感程度。靈敏度越低，檢測到的邊緣會越少，可能會漏掉一些細節；靈敏度越高，則可能檢測到更多邊緣，包括一些不必要的噪音。通過調整這些參數，你可以在細節和清晰度之間找到最佳平衡。

3. **文字圖寬**：這個參數決定生成的 ASCII 藝術的寬度。更大的寬度會使藝術作品更詳細，但也可能需要更長的輸出行；較小的寬度則會簡化作品，但可能損失一些細節。

4. **處理方法**：
   - **適用示意圖**：針對簡單或插圖風格的影像。
   - **適用實拍照**：針對真實照片進行處理。

5. **灰階閾值**：數值越大，影像的對比度越高，生成的 ASCII 藝術中的灰階數量會變少，圖像看起來更明亮且細節較少；數值較小時，對比度降低，可以保留更多細節，讓圖像顯得更加豐富。

### 步驟4：生成ASCII藝術

1. 調整**Graylevel**滑桿來設置ASCII轉換的灰階級別。
2. 輸入ASCII藝術的**"最大寬度"**。
3. 點擊**生成ASCII藝術**按鈕，基於處理過的影像生成ASCII藝術。
4. 生成的ASCII藝術將顯示在文字區域中。

### 步驟5：複製ASCII藝術

點擊**"複製"**按鈕將ASCII藝術複製到剪貼簿。

## 自定義

### 修改邊緣疊加行為

在V7_overlay_edges_on_gray.py文件中：
- overlay_edges_on_gray_ideogram 函數處理示意圖影像的邊緣疊加，將邊緣像素設置為黑色。
- overlay_edges_on_gray_photo 函數處理實拍照片，根據當地亮度來決定邊緣應是黑色還是白色。

### ASCII藝術自定義

將影像轉換為ASCII藝術的過程依賴於影像的亮度信息以及方向檢測，以決定哪個ASCII字符最能代表視覺細節。

#### 1. **亮度與ASCII映射**
   - 程式使用預定義的symbol_map，將亮度級別映射到特定的ASCII字符。較暗的區域使用密集字符表示（如█、▌），中等亮度的區域使用較輕的字符表示（如░），而較亮的區域則使用空白字符（　）來增強對比與結構。

#### 2. **方向檢測**
   - 程式通過加入**方向檢測**來增強ASCII表示：
     - 它分析特定方向上的亮度變化（右上、右下、左上、左下），以準確捕捉陰影和過渡。
     - 根據這些方向上的分析，程式選擇最能代表這些亮度過渡的ASCII字符（例如▛、▜）。

#### 3. **像素分組與邊緣情況**
   - 為了保持影像的細節，像素會按組處理（例如，2x2塊），並分析它們的平均亮度。
   - 在極端亮度或暗度的區域，程式簡化字符選擇，直接使用最暗或最亮的ASCII符號，而不進行進一步的檢查。

通過結合亮度映射與方向檢測，這種方法生成的ASCII藝術不僅反映了影像的亮度級別，還捕捉了邊緣與漸變等更精細的視覺細節。

要修改ASCII字符集或映射行為，可以在main.py中的image_to_ascii方法裡調整symbol_map來定制輸出效果。

## 注意事項

- 如果影像無法載入（如路徑中包含特殊字符或中文），會顯示錯誤訊息。
- 灰階滑桿允許動態調整，以生成不同細節層次的ASCII藝術。

### 字體提醒

顯示ASCII藝術時，如果設備使用的字體無法正確處理特殊字符作為全寬字符，可能會導致藝術失真。為了確保最佳顯示效果，建議使用支持全寬字符的字體。

**推薦字體**：[Google Noto Sans](https://www.google.com/get/noto/)

此字體能有效處理各種符號和多語種字符，適合用來顯示ASCII藝術。

## 聯繫方式
- 作者：SHENGLE
- 網站：[撰風旅食:旅遊美食分享](https://jfsblog.com/)、[漫步時光:全台活動資訊整理](https://strolltimes.com/)