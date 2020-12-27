import time
import sys
from signal import signal, SIGTERM

exit_flag = False

def signal_handler(signal_received, frame):
  global exit_flag
  exit_flag = True

def main():
  signal(SIGTERM, signal_handler)
  try:
    for x in range(50):
      global exit_flag
      if exit_flag:
        print('Exiting...')
        break
      print("logging ... " + str(x))
      time.sleep(0.5)
  except KeyboardInterrupt:
    print("Exit dummy-logger")
  print("dummy-logger completed")
  sys.exit(0)

main()
