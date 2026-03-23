# Color ASCII Art Generator [RU](README_RU.md)
Converts images (PNG, JPG, SVG) to ASCII color art and saves it to PNG or text file.


## Installation
1. Clone the repository:
`` 
git clone <repository url>
cd asciiart
``
2. Create a virtual environment (recommended):
``
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate      # Windows
``
3. Install dependencies:
``
pip install pillow requirements.txt
``

## 🖼 Usage
Running the script with the image:
``
python color_ascii.py path to the image
``
* If SAVE_PNG = True in the settings, a PNG will be created in the asciiarts/ folder.
* If SAVE_PNG = False, ASCII art will be output to the terminal and saved as asciiart.txt .

## ⚙ Settings
The script settings are at the beginning `color_ascii.py `:
- `ASCII_CHARS' — characters by brightness (from dark to light)
- `FIXED_HEIGHT' — height of ASCII art in lines
- `SYMBOL_RATIO' — the ratio of the width to the height of the symbol
- `TRANSPARENT_GREYS' — make dark pixels transparent
- `GREY_THRESHOLD' — threshold for transparent pixels
- `SATURATION` — color saturation
- `BRIGHTNESS' — brightness
- `GAMMA' — gamma correction
- `CONTRAST` — contrast ratio
- `USE_TRUECOLOR' — True = 24-bit color, False = 256 colors ANSI
- `SAVE_PNG' — True = save PNG, False = output to terminal
- `FONT_PATH' is the path to the PNG font (fonts/DejaVuSansMono-Bold.ttf)
- `FONT_SIZE` is the font size for PNG
- `OUTPUT_DIR` — folder for saving files

## 💡 Features
- Supports PNG, JPG, JPEG and SVG images.
- Color ASCII art with adjustable contrast, brightness and saturation.
- PNG version of ASCII art with embedded font.
- Automatic generation of unique files (`asciiart.png', `asciiart1.png', ...).
