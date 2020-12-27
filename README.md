Raspberry Pi OLED display menu
----------------------------------------

This is a simple menu GUI displayed on a 128x64 OLED display

Setup
----------------------------------------
1. Check if your Python version is 3.7.0 or above
```
python --version
```

2. Install necessary packages
```
sudo apt install -y python3-dev
sudo apt install -y python-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-pip
sudo apt install -y python3-setuptools
sudo apt install -y python3-rpi.gpio
sudo apt install python3-gpiozero
```
more info: https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/

3. Enable I2C interface
```
sudo raspi-config
```
additional info: https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/

4. There is a script to read temperature from 4 DS18B20 sensors, so you will need to enable the 1-wire protocal
```
dtoverlay=w1-gpio
```
add the aboce line to `/boot/config.txt`

References
----------------------------------------
* Adafruit Python SSD1306 library: https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/README.md
* Setup guide: https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/
* Remote development on Pi (Pi Zero not supported yet as the time of writing): https://electrobotify.wordpress.com/2019/08/16/remote-development-on-raspberry-pi-with-vs-code/

Other notes
----------------------------------------

Recommended Python version 3.7.3

python script must handle SIGTERM properly

Must use GPIO PinMode = BCM, not BOARD
