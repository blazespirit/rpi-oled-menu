from gpiozero import PWMLED

class LED_Manager():
  def setup(self, pin):
    led = PWMLED(pin)
    # Override with custom pulse pattern
    led.pulse = lambda: led.blink(on_time=0.1, off_time=0.1, fade_in_time=0.1, fade_out_time=0.7)
    return led