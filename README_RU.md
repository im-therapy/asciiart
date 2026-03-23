# Color ASCII Art Generator [RU](README_RU.md)
Конвертирует изображения (PNG, JPG, SVG) в цветной ASCII-арт и сохраняет в PNG или текстовый файл.


## 📂 Структура проекта
``
asciiart/
├─ color_ascii.py # основной скрипт
├─ fonts/
│ └─ DejaVuSansMono-Bold.ttf # встроенный шрифт для PNG
└─ asciiarts/              # сюда сохраняются PNG и текстовые файлы ASCII
``

## , Установка
1. Клонируйте репозиторий:
`` 
git clone <repository url>
cd asciiart
``
2. Создайте виртуальное окружение (рекомендуется):
``
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate      # Windows
``
3. Установите зависимости:
``
pip install pillow requirements.txt
``

## 🖼 Использование
Запуск скрипта с изображением:
``
python color_ascii.py путь_к_изображению
``
* Если SAVE_PNG = True в настройках, PNG будет создан в папке asciiarts/.
* Если SAVE_PNG = False, ASCII-арт выведется в терминал и сохранится как asciiart.txt.

## ⚙ Настройки
Настройки скрипта находятся в начале `color_ascii.py`:
- `ASCII_CHARS' — символы по яркости (от тёмного к светлому)
- `FIXED_HEIGHT' — высота ASCII-арта в строках
- `SYMBOL_RATIO' — соотношение ширины к высоте символа
- `TRANSPARENT_GREYS' — делать тёмные пиксели прозрачными
- `GREY_THRESHOLD' — порог для прозрачных пикселей
- `SATURATION` — насыщенность цвета
- `BRIGHTNESS' — яркость
- `GAMMA' — гамма-коррекция
- `CONTRAST` — коэффициент контрастности
- `USE_TRUECOLOR' — True = 24-битный цвет, False = 256 цветов ANSI
- `SAVE_PNG' — True = сохранять PNG, False = вывод в терминал
- `FONT_PATH' — путь к шрифту для PNG (fonts/DejaVuSansMono-Bold.ttf)
- `FONT_SIZE` — размер шрифта для PNG
- `OUTPUT_DIR` — папка для сохранения файлов

## 💡 Возможности
- Поддержка изображений PNG, JPG, JPEG и SVG.
- Цветной ASCII-арт с настройкой контраста, яркости и насыщенности.
- PNG-версия ASCII-арта с встроенным шрифтом.
- Автоматическая генерация уникальных файлов (`asciiart.png', `asciiart1.png', ...).
