from pathlib import Path
import os
import time

DISPLAY_ROW = 7

def get_directory_list(target_path):
  def sort_by_name(path_obj):
    return path_obj.name
  
  folder_list = []
  file_list = []
  directory_list = []

  for file in target_path.iterdir():
    if file.is_dir():
      folder_list.append(file)
    else:
      file_list.append(file)
      
  folder_list.sort(key=sort_by_name)
  file_list.sort(key=sort_by_name)

  directory_list.extend(folder_list)
  directory_list.extend(file_list)

  return directory_list

# start with current dir
cwd_path = Path.cwd()
dir_list = get_directory_list(cwd_path.joinpath('scripts-menu'))

# TODO -- check if directory is empty

display_row_index = 0
highlighted_file = []
highlighted_file.append(dir_list[6])

scoped_menu = dir_list[display_row_index:display_row_index + DISPLAY_ROW]

# import subprocess
# subprocess.run(['sh', './a-script.sh'])

# -----------------------------------------
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Raspberry Pi pin configuration:
RST = 24

# Custom ttf font
font_small = ImageFont.truetype('./font/slkscr.ttf', 8)
font_large = ImageFont.truetype('./font/slkscr.ttf', 16)

def setup_oled():
  disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
  disp.begin()
  disp.clear()
  disp.display()

  return disp

  # image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))

  # draw = ImageDraw.Draw(image)
  # draw.rectangle((0,0,DISPLAY_WIDTH-1,DISPLAY_HEIGHT-1), outline=False, fill=0)

  # draw highlighted menu
  # draw.rectangle((0,0,DISPLAY_WIDTH-1,9), outline=1, fill=1)

  # draw.text((2, 0), ">Hello World!", font=font_small, fill=0)
  # draw.text((2, 10), "Hello World!", font=font_small, fill=255)
  # draw.text((2, 20), "Hello World!", font=font_small, fill=255)
  # draw.text((2, 30), "Hello World!", font=font_small, fill=255)
  # draw.text((2, 40), "Hello World!", font=font_small, fill=255)
  # draw.text((2, 48), "Hello World!", font=font_small, fill=255)

  # draw.text((2, 18), "Logging...", font=font_large, fill=255)

  # disp.image(image)
  # disp.display()

  # time.sleep(5)
  # disp.clear()
  # disp.display()

oled = setup_oled()

def draw_menu(oled, menu, highlighted_file):
  LINE_HEIGHT = 9

  # setup image canvas
  image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
  draw = ImageDraw.Draw(image)

  # clear oled
  oled.clear()

  def print_highlighted_dir(x, y, dir):
    draw.rectangle((x, y, DISPLAY_WIDTH-1, y+(LINE_HEIGHT-1)), outline=1, fill=1)
    draw.text((x+2, y-1), "> " + str(dir), font=font_small, fill=0)

  def print_normal_dir(x, y, dir):
    draw.text((x+2, y-1), "> " + str(dir), font=font_small, fill=1)

  def print_highlighted_file(x, y, file):
    draw.rectangle((x, y, DISPLAY_WIDTH-1, y+(LINE_HEIGHT-1)), outline=1, fill=1)
    draw.text((x+2, y-1), "  " + str(file), font=font_small, fill=0)

  def print_normal_file(x, y, file):
    draw.text((x+2, y-1), "  " + str(file), font=font_small, fill=1)

  # print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
  index = 0
  for file in menu:
    if file.is_dir():
      if file.samefile(highlighted_file[len(highlighted_file) - 1]):
        print_highlighted_dir(0, index * LINE_HEIGHT, file.name)
      else:
        print_normal_dir(0, index * LINE_HEIGHT, file.name)
    else:
      if file.samefile(highlighted_file[len(highlighted_file) - 1]):
        print_highlighted_file(0, index * LINE_HEIGHT, file.name)
      else:
        print_normal_file(0, index * LINE_HEIGHT, file.name)
    index = index + 1
  # print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

  # display image
  oled.image(image)
  oled.display()

  # clear display
  oled.clear()
  oled.display()
      
draw_menu(oled, scoped_menu, highlighted_file)

