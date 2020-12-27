# Sensor ID
DS18B20_0_ID = '28-3c01b556e347'
DS18B20_1_ID = '28-3c01b556fcc3'
DS18B20_2_ID = '28-3c01b55658e4'
DS18B20_3_ID = '28-3c01b5562d72'

# Sensor read interval in seconds
READ_INTERVAL_SEC = 1

from signal import signal, SIGINT
from sys import exit
from datetime import datetime
import time
import csv

exit_flag = False

def signal_handler(signal_received, frame):
    global exit_flag
    exit_flag = True

# Read temperature value from file
def get_temp_from_file(sensor_id):
    temp_file = open('/sys/bus/w1/devices/' + sensor_id + '/w1_slave')
    raw_value = temp_file.read()
    temp_file.close()
    return raw_value

# Process raw input to temp celcius in 'C
def raw_str_to_temp(raw_str):
    splited_lines = raw_str.split('\n')
    line_1, line_2 = splited_lines[0], splited_lines[1]
    tempInCelcius = 0
    if line_1.split(' ')[11] == 'YES':
        raw_temp = line_2.split(' ')[9]
        raw_temp = float(raw_temp[2:])
        temp_in_celcius = raw_temp / 1000
    return temp_in_celcius

# ========= Start here =========
print('temp-logger started')

signal(SIGINT, signal_handler)

now = datetime.now()
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# with open(date_time + '.csv', 'w', newline='') as temp_logs:
with open('temp_logs/' + date_time + '.csv', 'w') as temp_logs:
    writer = csv.writer(temp_logs)
    writer.writerow(['time', 'temp_0', 'temp_1', 'temp_2', 'temp_3'])

    while True:
        raw_value_0 = get_temp_from_file(DS18B20_0_ID)
        raw_value_1 = get_temp_from_file(DS18B20_1_ID)
        raw_value_2 = get_temp_from_file(DS18B20_2_ID)
        raw_value_3 = get_temp_from_file(DS18B20_3_ID)

        temp_0 = raw_str_to_temp(raw_value_0)
        temp_1 = raw_str_to_temp(raw_value_1)
        temp_2 = raw_str_to_temp(raw_value_2)
        temp_3 = raw_str_to_temp(raw_value_3)

        read_time = datetime.now()
        timestamp = read_time.strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow([
          timestamp,
          temp_0,
          temp_1,
          temp_2,
          temp_3
        ])

        print(timestamp, temp_0, temp_1, temp_2, temp_3)

        time.sleep(READ_INTERVAL_SEC)

        if exit_flag:
            print('Exiting...')
            break

exit(0)
