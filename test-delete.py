from gpiozero import Button
from signal import pause

def setup(pin_name, callback):
  button = Button(pin_name, bounce_time=1)
  button.when_pressed = callback
  return button

def print_hello():
  print("hello")

def main():
  btn = setup(19, print_hello)
  pause()

main()