# V7 Overlay Edges on Gray with ASCII Art Generation

## Overview

This project provides an application for processing images by overlaying detected edges on grayscale versions and generating ASCII art from the processed images. It supports two methods of overlaying edges, suited for schematic images or photographs, and offers customizable parameters for edge detection and ASCII art generation.

UPDATE: V7.py

### Key Features:
1. **Edge Detection and Overlay:** 
   - Two methods for overlaying edges: one optimized for ideograms and one for real-life photos.
2. **Grayscale Conversion:** Convert images to grayscale before processing.
3. **Edge Customization:** Adjustable edge thickness and sensitivity settings.
4. **ASCII Art Generation:** Generate ASCII art from the processed image with customizable width and gray level thresholds.
5. **Interactive GUI:** PySide6-based GUI for selecting images, adjusting settings, and generating ASCII art.

## Prerequisites

Make sure you have the following libraries installed before running the project:

bash
pip install numpy opencv-python pillow PySide6


## File Structure

- **V7_overlay_edges_on_gray.py**: Contains two functions to overlay edges on a grayscale image for ideograms and photos.
- **main.py**: The main application script which loads the UI, handles image processing, and generates ASCII art.
- **V3.ui**: The Qt Designer .ui file that defines the GUI layout and components.

## Usage

### Step 1: Running the Application

To run the application, execute the following command:

bash
python main.py


### Step 2: Loading an Image

1. Click the **"載入圖片"** button to select an image (.png, .jpg, .bmp, .jpeg).
2. The selected image's path will be displayed, and the image will be loaded into the GUI.

### Step 3: Processing the Image

1. Adjust the edge thickness and sensitivity values in the text boxes.
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

In the main.py file:
- You can adjust the symbol_map in the image_to_ascii method to modify how pixel values are mapped to ASCII characters.

## Notes

- If an image fails to load due to issues with the path (e.g., containing special characters or Chinese), an error message will be shown.
- The slider for gray levels allows dynamic adjustment for generating ASCII art with different levels of detail.

### Font Reminder

When displaying ASCII art, if the font used by the device does not correctly treat special characters as full-width, it may lead to distortion of the art. To ensure the best display quality, it is recommended to use a font that supports full-width characters.

Recommended Font: [Google Noto Sans](https://www.google.com/get/noto/)

This font effectively handles various symbols and multilingual characters, making it suitable for displaying ASCII art.