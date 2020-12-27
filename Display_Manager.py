import Adafruit_SSD1306
import Adafruit_GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from threading import Timer

# Raspberry Pi pin configuration:
RST = 24

# OLED resolution
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# Custom ttf font
FONT_SMALL = ImageFont.truetype('./font/slkscr.ttf', 8)
FONT_LARGE = ImageFont.truetype('./font/slkscr.ttf', 16)

# Pixel per line
LINE_HEIGHT = 9

class Display_Manager:
  def __init__(self, sleep=None):
    self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
    self.disp.begin()
    self.disp.clear()
    self.disp.display()
    self.sleep_sec = sleep
    self.sleep_timer = None
    self.is_sleep = False
    self.start_sleep_timer()

  # draw menu list with highlighted item
  def draw_menu(self, menu, highlighted_file):
    # setup image canvas
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    draw = ImageDraw.Draw(image)

    # clear oled
    self.disp.clear()

    def __print_highlighted_dir(x, y, dir):
      draw.rectangle((x, y, DISPLAY_WIDTH-1, y+(LINE_HEIGHT-1)), outline=1, fill=1)
      draw.text((x+2, y-1), "> " + str(dir), font=FONT_SMALL, fill=0)

    def __print_normal_dir(x, y, dir):
      draw.text((x+2, y-1), "> " + str(dir), font=FONT_SMALL, fill=1)

    def __print_highlighted_file(x, y, file):
      draw.rectangle((x, y, DISPLAY_WIDTH-1, y+(LINE_HEIGHT-1)), outline=1, fill=1)
      draw.text((x+2, y-1), "  " + str(file), font=FONT_SMALL, fill=0)

    def __print_normal_file(x, y, file):
      draw.text((x+2, y-1), "  " + str(file), font=FONT_SMALL, fill=1)

    index = 0
    for file in menu:
      if file.is_dir():
        if file.samefile(highlighted_file):
          __print_highlighted_dir(0, index * LINE_HEIGHT, file.name)
        else:
          __print_normal_dir(0, index * LINE_HEIGHT, file.name)
      else:
        if file.samefile(highlighted_file):
          __print_highlighted_file(0, index * LINE_HEIGHT, file.name)
        else:
          __print_normal_file(0, index * LINE_HEIGHT, file.name)
      index = index + 1

    self.disp.image(image)
    self.disp.display()
  
  # draw a screen indicating empty directory
  def draw_empty_folder(self):
    # setup image canvas
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    draw = ImageDraw.Draw(image)

    mid_x = (DISPLAY_WIDTH / 2) - 1
    mid_y = (DISPLAY_HEIGHT / 2) - 1

    draw.text((mid_x, mid_y), "No Item", font=FONT_LARGE, fill=1, anchor="mm")

    self.disp.clear()
    self.disp.image(image)
    self.disp.display()

  def draw_script_output(self, script_name, script_outputs):
    # setup image canvas
    image = Image.new('1', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, DISPLAY_WIDTH-1, DISPLAY_HEIGHT-1), outline=1, fill=0)
    draw.rectangle((0, 0, DISPLAY_WIDTH-1, LINE_HEIGHT-1), outline=1, fill=1)
    draw.text((3, -1), script_name, font=FONT_SMALL, fill=0)

    idx = 1
    for line in script_outputs:
      draw.text((3, idx * LINE_HEIGHT), line, font=FONT_SMALL, fill=1)
      idx = idx +1
    
    self.disp.clear()
    self.disp.image(image)
    self.disp.display()

  # Clear OLED display
  def clear_display(self):
    self.disp.clear()
    self.disp.display()

  def off_display(self):
    # it's just clear the display actually
    self.clear_display()

  def sleep(self):
    self.is_sleep = True
    self.off_display()

  def wake_up(self):
    self.is_sleep = False
    if self.sleep_sec is not None:
      self.start_sleep_timer()

  def start_sleep_timer(self):
    if self.sleep_sec is not None:
      self.sleep_timer = Timer(self.sleep_sec, self.sleep)
      self.sleep_timer.start()

  def reset_sleep_timer(self):
    if self.sleep_sec is not None:
      self.sleep_timer.cancel()
      self.start_sleep_timer()

  def is_sleeping(self):
    return self.is_sleep
