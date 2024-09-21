# V7 Overlay Edges on Gray with ASCII Art Generation

## Overview

This project provides an application for processing images by overlaying detected edges on grayscale versions and generating ASCII art from the processed images. It supports two methods for overlaying edges, suited for schematic images or photographs, and offers customizable parameters for edge detection and ASCII art generation.

### Key Features:
1. **Edge Detection and Overlay:** Two methods for overlaying edges: one optimized for ideograms and one for real-life photos.
2. **Grayscale Conversion:** Convert images to grayscale before processing.
3. **Edge Customization:** Adjustable edge thickness and sensitivity settings.
4. **ASCII Art Generation:** Generate ASCII art from the processed image with customizable width and gray level thresholds.
5. **Interactive GUI:** PySide6-based GUI for selecting images, adjusting settings, and generating ASCII art.

## Prerequisites

Make sure you have the following libraries installed before running the project:

 ```bash
pip install numpy opencv-python pillow PySide6
 ```

## File Structure

- **V7_overlay_edges_on_gray.py**: Contains two functions to overlay edges on a grayscale image for ideograms and photos.
- **V8_UI.py**: The main application script which loads the UI, handles image processing, and generates ASCII art.
- **V3.ui**: The Qt Designer .ui file that defines the GUI layout and components.

## Usage

### Step 1: Running the Application

To run the application, execute the following command:

 ```bash
python V8_UI.py
 ```

### Step 2: Loading an Image

1. Click the **"載入圖片"** button to select an image (.png, .jpg, .bmp, .jpeg).
2. The selected image's path will be displayed, and the image will be loaded into the GUI.

### Step 3: Processing the Image

1. Adjust the edge thickness and sensitivity values in the text boxes:
   - **Edge Thickness**: Determines how thick the detected edges will be.
   - **Edge Sensitivity**: Adjust the lower and upper bounds for edge detection.
2. Click the **"進行影像處理"** button to process the image:
   - The image will be converted to grayscale.
   - Edges will be detected and overlaid based on the method selected in the **"comboBox_method"** (either for ideograms or photos).

### Step 4: Generating ASCII Art

1. Adjust the **"Graylevel"** slider to set the threshold for ASCII conversion.
2. Enter the **"Max Width"** for the ASCII art.
3. Click the **"生成ASCII藝術"** button to generate ASCII art based on the processed image.
4. The generated ASCII art will be displayed in the text area.

### Step 5: Copying the ASCII Art

Click the **"複製"** button to copy the ASCII art to the clipboard.

## Customization

### Modifying Edge Overlay Behavior

In the V7_overlay_edges_on_gray.py file:
- The overlay_edges_on_gray_ideogram function handles the overlay for schematic images, setting edge pixels to black.
- The overlay_edges_on_gray_photo function handles photographs, using local brightness to determine whether edges should be black or white.

### ASCII Art Customization

The process of converting images to ASCII art relies on the brightness information of the image and directional analysis to determine which ASCII characters best represent the visual details.

#### 1. **Brightness and ASCII Mapping**
   - The program uses a predefined symbol_map, which maps brightness levels to specific ASCII characters. Darker regions are represented by dense characters (e.g., █, ▌), mid-level brightness areas are shown using lighter shading characters (e.g., ░), and lighter areas use blank spaces (　), enhancing the contrast and structure of the final ASCII art.
  
#### 2. **Directional Detection**
   - The program enhances the ASCII representation by incorporating **directional detection**:
     - It analyzes the brightness changes in specific directions (upper-right, lower-right, upper-left, lower-left) to accurately capture shading and transitions.
     - Based on this directional analysis, the program selects ASCII characters (such as ▛, ▜) that best represent these transitions in brightness between neighboring pixels.

#### 3. **Pixel Grouping and Edge Cases**
   - To maintain the image’s details, pixels are processed in groups (e.g., 2x2 blocks), and their average brightness is analyzed.
   - In regions of extreme brightness or darkness, the program simplifies character selection, directly using the darkest or lightest ASCII symbols without further checks.

By combining brightness-based mapping with directional detection, this approach produces ASCII art that not only reflects the brightness levels of the image but also captures finer visual details like edges and gradients.

To modify the ASCII character set or mapping behavior, you can adjust the symbol_map in the image_to_ascii method inside main.py to tailor the output to your preferences.

## Notes

- If an image fails to load due to issues with the path (e.g., containing special characters or Chinese), an error message will be shown.
- The slider for gray levels allows dynamic adjustment for generating ASCII art with different levels of detail.

### Font Reminder

When displaying ASCII art, if the font used by the device does not correctly treat special characters as full-width, it may lead to distortion of the art. To ensure the best display quality, it is recommended to use a font that supports full-width characters.

**Recommended Font**: [Google Noto Sans](https://www.google.com/get/noto/)

This font effectively handles various symbols and multilingual characters, making it suitable for displaying ASCII art.


## Contact
- Author: SHENGLE
- Website: [撰風旅食:旅遊美食分享](https://jfsblog.com/)、[漫步時光:全台活動資訊整理](https://strolltimes.com/)