'''

Transmitter Main Screen Implementation - ECE 5725, W grp 3
# transmitting the data will be run in background in the main batch file rather than here to not have the PiTFT process block it.
This file main.py will take care of the data display on the transmitter (pi) side.

'''
import time
import data_to_send # import file with sensor and display functions defined
import sys
import RPi.GPIO as GPIO
import json

# quit btn - consistent with data_to_send.py
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def gpio17_cb(channel):
    GPIO.cleanup()
    sys.exit(0)
    quit()
GPIO.add_event_detect(17, GPIO.FALLING, callback=gpio17_cb, bouncetime=400)
# main loop
play = 1
while True:#for i in range(play):
  current_data = data_to_send.captureData() # this data capture will be shown in Real Time on the PiTFT. Because of issues with blocking the system for transmission for too long, the data transmission with be done in a separate instance as a background processes. However, we expect that as the environment remains fairly constant, the system data at the receiver will be fairly consistent.
  print(str(current_data))
  # load the data unto the PiTFT
  data_to_send.piTFT_disp(current_data)
  # send data to json
  data_string = json.dumps(current_data) #data serialized (dict -> str obj)
  data_dict = str.encode(data_string) # converts serialized data to bytes from str obj
  # also write json to file to access, keep appending data to data_all, replace for data
  try:
    print("Writing data to full log -> json")
    f_all = open("/home/pi/ece5725/receiver/data_all.json", "a")
    f_all.write(data_string)
    f_all.close()
    print("Data was written to full log -> json. \n Now writting data to single json.")
    f = open("/home/pi/ece5725/receiver/data.json", "w")
    f.write(data_string)
    f.close()
    print("Data was written to single log -> json.")
  except:
    print("not saved, error occured")
    print("Error: "+sys.exc_info())
    sys.exit(2)

