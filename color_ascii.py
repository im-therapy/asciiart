#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import sys, colorsys, cairosvg
from io import BytesIO
import os

# ===================== НАСТРОЙКИ =====================
ASCII_CHARS = "@#$%&*+=-:. "   # символы по яркости (от тёмных к светлым)
FIXED_HEIGHT = 60               # высота ASCII-арта в строках
SYMBOL_RATIO = 2.0              # отношение ширины к высоте символа
TRANSPARENT_GREYS = False       # True = тёмные пиксели <= GREY_THRESHOLD становятся пробелами
GREY_THRESHOLD = 50             # порог для прозрачных пикселей
SATURATION = 3.0                # насыщенность (>1 = ярче)
BRIGHTNESS = 1.0                # яркость (0=чёрный, 1=оригинал)
GAMMA = 1.0                     # гамма-коррекция яркости
CONTRAST = 1.0                  # контрастность (>1 = более контрастно)
USE_TRUECOLOR = True            # True = 24-бит цвет, False = 256 цветов ANSI
SAVE_PNG = True                 # True = сохранять PNG вместо вывода в терминал
FONT_PATH = "fonts/DejaVuSansMono-Bold.ttf"  # путь к шрифту для PNG
FONT_SIZE = 24                  # размер шрифта в пикселях для PNG
OUTPUT_DIR = "asciiarts"        # папка для сохранения артов
# ======================================================

# ------------------- Работа с изображением -------------------
def open_image(path: str) -> Image.Image:
    """Открывает изображение с обработкой ошибок, конвертирует SVG в PNG."""
    if not os.path.exists(path):
        print(f"Ошибка: файл '{path}' не найден.")
        sys.exit(1)
    try:
        if path.lower().endswith(".svg"):
            png_bytes = cairosvg.svg2png(url=path)
            return Image.open(BytesIO(png_bytes))
        return Image.open(path)
    except OSError as e:
        print(f"Ошибка при открытии изображения '{path}': {e}")
        sys.exit(1)

def resize_image(image: Image.Image) -> Image.Image:
    """Изменяет размер изображения с учётом высоты и пропорций символа."""
    try:
        ratio = image.width / image.height * SYMBOL_RATIO
        new_width = int(FIXED_HEIGHT * ratio)
        return image.resize((new_width, FIXED_HEIGHT))
    except Exception as e:
        print(f"Ошибка при изменении размера изображения: {e}")
        sys.exit(1)

# ------------------- Цвет и символ -------------------
def apply_hsv_contrast(r:int, g:int, b:int) -> tuple[int,int,int]:
    """Применяет насыщенность, яркость, гамму и контраст к RGB."""
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    s *= SATURATION
    v *= BRIGHTNESS
    v = v ** GAMMA
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
    r2 = max(0, min((r2-0.5)*CONTRAST+0.5,1))
    g2 = max(0, min((g2-0.5)*CONTRAST+0.5,1))
    b2 = max(0, min((b2-0.5)*CONTRAST+0.5,1))
    return int(r2*255), int(g2*255), int(b2*255)

def gray_to_char(gray:int) -> str:
    """Преобразует яркость в символ ASCII."""
    if TRANSPARENT_GREYS and gray <= GREY_THRESHOLD:
        return " "
    index = int(gray/255*(len(ASCII_CHARS)-1))
    return ASCII_CHARS[index]

def generate_ascii(img: Image.Image):
    """Создаёт структуру ASCII-арта: [[(char, (r,g,b)), ...], ...]."""
    ascii_lines = []
    try:
        for y in range(img.height):
            line = []
            for x in range(img.width):
                r, g, b = img.getpixel((x, y))
                r, g, b = apply_hsv_contrast(r, g, b)
                gray = int(0.299*r + 0.587*g + 0.114*b)
                char = gray_to_char(gray)
                line.append((char, (r, g, b)))
            ascii_lines.append(line)
    except Exception as e:
        print(f"Ошибка при генерации ASCII: {e}")
        sys.exit(1)
    return ascii_lines

# ------------------- Работа с файлами -------------------
def get_next_filename(base="asciiart.png"):
    """Возвращает путь к следующему свободному файлу в OUTPUT_DIR."""
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
        except OSError as e:
            print(f"Ошибка при создании папки '{OUTPUT_DIR}': {e}")
            sys.exit(1)
    base_name, ext = os.path.splitext(base)
    counter = 0
    while True:
        fname = f"{base_name}{counter if counter>0 else ''}{ext}"
        path = os.path.join(OUTPUT_DIR, fname)
        if not os.path.exists(path):
            return path
        counter += 1

def save_ascii_png(ascii_lines):
    """Сохраняет ASCII-арт в PNG с обработкой ошибок."""
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except OSError as e:
        print(f"Ошибка: не удалось загрузить шрифт '{FONT_PATH}': {e}")
        sys.exit(1)

    char_h = FONT_SIZE
    char_w = int(FONT_SIZE / SYMBOL_RATIO)
    width = char_w * len(ascii_lines[0])
    height = char_h * len(ascii_lines)

    try:
        img = Image.new("RGB", (width, height), color=(0,0,0))
        draw = ImageDraw.Draw(img)
        for y, line in enumerate(ascii_lines):
            for x, (char, (r,g,b)) in enumerate(line):
                w, h = draw.textbbox((0,0), char, font=font)[2:4]
                offset_x = (char_w - w)//2
                offset_y = (char_h - h)//2
                draw.text((x*char_w + offset_x, y*char_h + offset_y), char, fill=(r,g,b), font=font)
        out_path = get_next_filename("asciiart.png")
        img.save(out_path)
        print(f"ASCII-арт сохранён в {out_path}")
    except Exception as e:
        print(f"Ошибка при сохранении PNG: {e}")
        sys.exit(1)

def print_ascii_terminal(ascii_lines):
    """Печатает ASCII-арт в терминал и сохраняет файл тоже."""
    lines_str = []
    try:
        for line in ascii_lines:
            out_line = ""
            for char, (r,g,b) in line:
                out_line += f"\033[38;2;{r};{g};{b}m{char}" if char != " " else " "
            out_line += "\033[0m"
            print(out_line)
            lines_str.append(out_line)
        out_path = get_next_filename("asciiart.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines_str))
        print(f"ASCII-арт для терминала сохранён в {out_path}")
    except Exception as e:
        print(f"Ошибка при выводе ASCII в терминал или сохранении файла: {e}")
        sys.exit(1)

# ------------------- Основная функция -------------------
def main(path: str):
    img = open_image(path).convert("RGB")
    img = resize_image(img)
    ascii_lines = generate_ascii(img)
    if SAVE_PNG:
        save_ascii_png(ascii_lines)
    else:
        print_ascii_terminal(ascii_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python color_ascii.py путь_к_изображению")
        sys.exit(1)
    main(sys.argv[1])