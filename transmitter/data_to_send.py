#!/usr/bin/python
# function to read, format, and return the sensor data that we need

'''
This file is for function definitions only. Please import into a new python file in order to implement into main logic.

'''

## Import modules (gpio, libraries for reading data from sensors, etc)
import time
import serial
import sys
import datetime
import time
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import os
import subprocess
import adafruit_dht
from picamera import PiCamera
import datetime
import os

## Set up GPIO pins and devices
calibration_light_pin = 1
dht11_pin = 2
barcodes_pin = 3
signal_light_pin = [4, 5, 6] # R pin, G pin, B pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(calibration_light_pin, GPIO.OUT)
p = GPIO.PWM(calibration_light_pin, 10) # channel = pin_num, frequency = freq
GPIO.setup(dht11_pin, GPIO.IN)
GPIO.setup(barcodes_pin, GPIO.IN)
GPIO.setup(signal_light_pin[0], GPIO.OUT)
GPIO.setup(signal_light_pin[1], GPIO.OUT)
GPIO.setup(signal_light_pin[2], GPIO.OUT)
dht11_device = adafruit_dht.DHT11(dht11_pin, use_pulseio=False)
camera = PiCamera()
# barcodes
ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5)
# PiTFT
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
pygame.init()
pygame.mouse.set_visible(True)
WHITE=255,255,255
BLACK=0,0,0
screen = pygame.display.set_mode((320,240))
screen.fill(BLACK)
header_font = pygame.font.Font(None, 30)
text_font = pygame.font.Font(None,20) 
button_text = 'CLOSE'
button_position = (160,240)

print('serial test start ...')
if ser is not None:
    print('serial ready...')
else:
    print('serial not ready')
    sys.exit()

ser.timerout = 1  # read time out
ser.writeTimeout = 0.5  # write time out.

def calibration_light():
  ## The transmitter is outputting a calibration light signal to indicate that data is being transmitted to the receiver.
  global p
  p.start(50)
  print("blinky")
  p.stop()
  print("no blinky")
  
def camera_scanner():
  ## return values/data
  # camera capture
  global camera
  camera.start_preview()
  for i in range(5):
      x = datetime.datetime.now()
      sleep(5)
      camera.capture('/home/pi/ece5725/image{index}s_{date}.jpg'.format(index=i, date=x))
  camera.stop_preview()
  # barcode scanner
  global ser
  
  
  
def temp_and_hum_capture():
  global dht11_device
  ## return values
  try:
    # Print the values to the serial port
    temp_c = dht11_device.temperature
    temp_f = temp_c * (9 / 5) + 32
    humidity = dht11_device.humidity
    print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temp_f, temp_c, humidity))
    results = {"temp_f":temp_f, "temp_c":temp_c, "humidity":humidity}
    return results
  except RuntimeError as error:
    # Error handling in sensor read
    print(error.args[0])
    return {"temp_f":-1, "temp_c":-1, "humidity":-1}
  except Exception as error:
    dht11_device.exit()
    raise error
  
def captureData():
  ## this function will be imported into the code that transmits the data, calls the functions defined above
  try:
    ## formatting the data into a JSON -> work with dictionary
    ## Information for Recognized Food (name/type)
    ## Current Freshness of Food
    ## Ambient Temperature of Demo Environment
    ## Ambient Humidity of Demo Environment
    ## Temperature Threshold Flag - The transmitter is outputting the light signals for the environment if the temperature lies outside of 30% of the standard room temperature range (“Temperature Threshold Flag”).
    ## Humidity Threshold Flag - The transmitter is outputting the light signals for the environment if the humidity lies outside of 30% of the standard room humidity range (“Humidity Threshold Flag”).
    ## return data
  except:
    print("Unexpected error:", sys.exc_info())
    return -1
  
def piTFT_disp(data):
    ## pygame
    global screen
    global WHITE
    global BLACK
    global screen
    global button_text
    global button_position
    global header_font
    global text_font
    #quit button
    quit_surface = my_font.render(button_text,True,WHITE)
    quit_rect = quit_surface.get_rect(center = (button_position[0],button_position[1]))
    time.sleep(0.2)
    while True:
        screen.fill(BLACK)
        screen.blit(quit_surface, quit_rect)
        # check close screen btn
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                x,y = pos
                print(pos)
                if (y >= button_position[1] - 20 and y <= button_position[1] + 20):
                    if (x >= button_position[0] - 10 and x <= button_position[0] + 10):
                        # pushed close btn
                        GPIO.cleanup()
                        quit()
        # draw data to screen
        
        pygame.display.flip()
        
