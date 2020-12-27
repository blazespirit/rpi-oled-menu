# #!/bin/bash

# check if python version is 3

# Install PIL
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

# Intall custon font
wget https://kottke.org/plus/type/silkscreen/download/silkscreen.zip
unzip silkscreen.zip # TODO - still need to clean up the folder

# Update i2c to higher speed
# https://www.raspberrypi-spy.co.uk/2018/02/change-raspberry-pi-i2c-bus-speed/

# TODO - finish the setup script !