'''

Transmitter Main Screen Implementation - ECE 5725, W grp 3
# transmitting the data will be run in background in the main batch file rather than here to not have the PiTFT process block it.
This file main.py will take care of the data display on the transmitter (pi) side.

'''
import time
import data_to_send # import file with sensor and display functions defined
import sys
import RPi.GPIO as GPIO

# quit btn - consistent with data_to_send.py

# main loop
while True:
  current_data = data_to_send.captureData() # this data capture will be shown in Real Time on the PiTFT. Because of issues with blocking the system for transmission for too long, the data transmission with be done in a separate instance as a background processes. However, we expect that as the environment remains fairly constant, the system data at the receiver will be fairly consistent.
  # load the data unto the PiTFT
  data_to_send.piTFT_disp(current_data)

