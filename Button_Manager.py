import RPi.GPIO as GPIO

class Button_Manager():
  def setup(self, button, callback):
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button, GPIO.FALLING, callback=callback, bouncetime=250)
