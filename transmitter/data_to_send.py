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
button_position = (160,200)

print('serial test start ...')
if ser is not None:
    print('serial ready...')
else:
    print('serial not ready')
    sys.exit()

ser.timerout = 1  # read time out
ser.writeTimeout = 0.5  # write time out.

food_dict = {}

def calibration_light():
    ## The transmitter is outputting a calibration light signal to indicate that data is being transmitted to the receiver.
    global p
    p.start(50)
    print("blinky")
    p.stop()
    print("no blinky")
  
def camera_scanner():
    ## return values/data
    results = dict()
    # camera capture
    global camera
    camera.start_preview()
    x = datetime.datetime.now()
    sleep(5)
    file_name = '/home/pi/ece5725/image_{date}.jpg'.format(date=x)
    camera.capture(file_name)
    camera.stop_preview()
    results["camera"] = file_name
    # barcode scanner
    global ser
    
    results["barcodes"] = 
    return results
  
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
    global food_dict # expected average colors of a list of fruits
    results = dict()
    try:
        ## formatting the data into a JSON -> work with dictionary
        ## Information for Recognized Food (name/type)
        food_imgs = camera_scanner()
        results["info"] =
        ## Current Freshness of Food
        # for image scanner: using color analysis, we can compare the expected color of a dected object to the actual colors analyzed in the image in order to determine if an overwhelming part of the apperance indicates expiration. src: https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606 
        results["freshness"] = 
        ## Ambient Temperature of Demo Environment & Ambient Humidity of Demo Environment
        temp_hum_dt = temp_and_hum_capture()
        results["temp_c"] = temp_hum_dt["temp_c"]
        results["temp_f"] = temp_hum_dt["temp_f"]
        results["humidity"] = temp_hum_dt["humidity"]
        if results["temp_c"] == -1 and results["humidity"] == -1:
            results["temp_flag"] = True
            results["hum_flag"] = True
        elif results["temp_c"] != -1 and results["humidity"] == -1:
            standard_rt = 21 # in celcius
            threshold_rt = abs((results["temp_c"] - standard_rt)/standard_rt) * 100
            results["temp_flag"] = False if threshold_rt <= 30 else True
            results["hum_flag"] = True
        elif results["temp_c"] == -1 and results["humidity"] != -1:
            results["hum_flag"] = False if results["humidity"] >= 40 and results["humidity"] <= 60 else True
            results["hum_flag"] = True
        else:
            ## Temperature Threshold Flag - The transmitter is outputting the light signals for the environment if the temperature lies outside of 30% of the standard room temperature range (“Temperature Threshold Flag”)
            standard_rt = 15.5556 # in celcius, healthy average food pantry storage temp for dry, non refrigerated foods
            threshold_rt = abs((results["temp_c"] - standard_rt)/standard_rt) * 100
            results["temp_flag"] = False if threshold_rt <= 30 else True
            ## Humidity Threshold Flag - The transmitter is outputting the light signals for the environment if the humidity lies outside the optimal room humidity range (“Humidity Threshold Flag”).
            results["hum_flag"] = False if results["humidity"] >= 40 and results["humidity"] <= 60 else True 
        ## return data
        return results
    except:
        print("Unexpected error:", sys.exc_info())
        return {"food info":-1, "freshness":-1, "temp_c":-1, "temp_f":-1, } # params should equal -1 to indicate no valid reading
  
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
        leftH_surface = text_font.render("Fields",True,WHITE)
        leftH_rect = leftH_surface.get_rect(center = (50,50))
        leftN_surface = text_font.render("Temperature (C)",True,WHITE)
        leftN_rect = leftN_surface.get_rect(center = (50,100))
        leftM_surface = text_font.render("Temperature (F)",True,WHITE)
        leftM_rect = leftM_surface.get_rect(center = (50, 150))
        leftO_surface = text_font.render("Humidity (%)",True,WHITE)
        leftO_rect = leftO_surface.get_rect(center= (50, 200))
        temp_flag = (0, 255, 0) if not data["temp_flag"] else (255, 0, 0)
        hum_flag = (0, 255, 0) if not data["hum_flag"] else (255, 0, 0)
        rightH_surface = text_font.render("Data",True,WHITE)
        rightH_rect = rightH_surface.get_rect(center = (275,50))
        rightN_surface = text_font.render(str(data["temp_c"]),True,temp_flag) # temp c
        rightN_rect = rightN_surface.get_rect(center = (275, 100))
        rightM_surface = text_font.render(str(data["temp_f"]),True,temp_flag) # temp f
        rightM_rect = rightM_surface.get_rect(center = (275, 150))
        rightO_surface = text_font.render(str(data["humidity"]),True,hum_flag) # humidity
        rightO_rect = rightO_surface.get_rect(center = (275, 200))
        screen.blit(leftH_surface, leftH_rect)
        screen.blit(rightH_surface, rightH_rect)
        screen.blit(leftN_surface,leftN_rect)
        screen.blit(rightN_surface, rightN_rect)
        screen.blit(leftM_surface, leftM_rect)
        screen.blit(rightM_surface, rightM_rect)
        screen.blit(leftO_surface, leftO_rect)
        screen.blit(rightO_surface, rightO_rect)
        pygame.display.flip()
        
