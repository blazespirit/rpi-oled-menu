from Directory_Manager import Directory_Manager
from Display_Manager import Display_Manager
from Button_Manager import Button_Manager # TODO - maybe group these manager into Utils

from pathlib import Path
from subprocess import Popen, PIPE
from threading import Thread, Timer
from signal import pause
import time

ROW_PER_PAGE = 7
DISP_OFF_SEC = 5

# Buttons pin number (BOARD)
# BUTTON_UP      = 37
# BUTTON_DOWN    = 35
# BUTTON_CANCEL  = 33
# BUTTON_CONFIRM = 31

# Buttons pin number (BCM)
BUTTON_UP      = 26
BUTTON_DOWN    = 19
BUTTON_CANCEL  = 13
BUTTON_CONFIRM = 6

directory_manager = None
display_manager = None
button_manager = None
running_script = None
running_thread = None
is_display_off = False
display_off_timer = None

def setup_directory_manager():
  cwd_path = Path.cwd()
  script_folder_path = cwd_path.joinpath('scripts-menu')
  global directory_manager
  directory_manager = Directory_Manager(script_folder_path, ROW_PER_PAGE)

def setup_display_manager():
  global display_manager
  display_manager = Display_Manager()

def setup_buttons():
  global button_manager
  button_manager = Button_Manager()

  def is_script_running():
    global running_script
    global running_thread
    if running_script is not None and running_thread is not None:
      return True
    else:
      return False

  def btn_up_callback(channel):
    global is_display_off
    if is_display_off is True:
      is_display_off = False
      display_updated_menu()
      restart_display_off_timer()
      return

    restart_display_off_timer()

    # no-op when scripts is running
    if is_script_running() is True:
      return
    directory_manager.highlight_previous_file()
    display_updated_menu()

  def btn_down_callback(channel):
    if is_script_running() is True:
      return
    directory_manager.highlight_next_file()
    display_updated_menu()

  def btn_confirm_callback(channel):
    if is_script_running() is True:
      return
    if directory_manager.is_highlighted_path_directory():
      directory_manager.go_into_folder()
      display_updated_menu()
    else:
      # execute script
      current_path = directory_manager.get_current_dir_path()
      script_path = directory_manager.get_highlighted_path()
      execute_script(script_path, current_path)
  
  def btn_cancel_callback(channel):
    global running_script
    global running_thread
    if is_script_running() is True:
      running_script.terminate()
      running_script.communicate()
      running_thread.join()

      running_script = None
      running_thread = None
      display_updated_menu()
    else: 
      directory_manager.go_out_from_folder()
      display_updated_menu()
  
  button_manager.setup(BUTTON_UP,      btn_up_callback)
  button_manager.setup(BUTTON_DOWN,    btn_down_callback)
  button_manager.setup(BUTTON_CONFIRM, btn_confirm_callback)
  button_manager.setup(BUTTON_CANCEL,  btn_cancel_callback)

def display_updated_menu():
  menus = directory_manager.get_menus()
  highlighted_file = directory_manager.get_highlighted_path()

  if len(menus) > 0:
    display_manager.draw_menu(menus, highlighted_file)
  else:
    display_manager.draw_empty_folder()

def execute_script(script_path, working_path):
  global running_script
  if script_path.suffix == ".py":
    running_script = Popen(["python", "-u", script_path], cwd=working_path, stdout=PIPE, bufsize=1, universal_newlines=True)
  elif script_path.suffix == ".sh":
    running_script = Popen(["sh", script_path], cwd=working_path, stdout=PIPE, bufsize=1, universal_newlines=True)

  def print_script_output_to_display(running_script, display_fnc, script_name):
    output_lines = []
    while running_script.poll() is None:
      output_buf = running_script.stdout.readline()
      output_lines.append(output_buf)
      if len(output_lines) > 6:
        output_lines.pop(0)
      display_fnc(script_name, output_lines)

  script_thread = Thread(target=print_script_output_to_display, args=(running_script, display_manager.draw_script_output, script_path.name), daemon=True)
  script_thread.start()

  global running_thread
  running_thread = script_thread

def start_display_off_timer():
  def off_disp_callback():
    print("off display")
    display_manager.off_display()
    global is_display_off
    is_display_off = True
  
  global display_off_timer
  display_off_timer = Timer(DISP_OFF_SEC, off_disp_callback)
  display_off_timer.start()

def cancel_display_off_timer():
  display_off_timer.cancel()

def restart_display_off_timer():
  cancel_display_off_timer()
  start_display_off_timer()

# ==================================================================
# Test LED
def test_led():
  from gpiozero import PWMLED, Button

  led = PWMLED("GPIO5")
  # led.blink(on_time=0.1, off_time=0.1, fade_in_time=0.1, fade_out_time=0.7)

  # def blink_fast():
  #   led.blink(on_time=0.1, off_time=0.1, fade_in_time=0.1, fade_out_time=0.7)

  led.pulse = lambda: led.blink(on_time=0.1, off_time=0.1, fade_in_time=0.1, fade_out_time=0.7)
  led.pulse()


# ==================================================================

def main():
  try:
    setup_directory_manager()
    setup_display_manager()
    setup_buttons()
    
    # display initial menus
    display_updated_menu()
    # test_led()

    start_display_off_timer()

    pause()
  except KeyboardInterrupt:
    display_manager.off_display()

main()


# TODO - off display after some timeout
