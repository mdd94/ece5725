#!/usr/bin/python
# function to read, format, and return the sensor data that we need

## Import modules (gpio, libraries for reading data from sensors, etc)
import time
import sys
import datetime
import time
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import os
import subprocess
import adafruit_dht

## Set up GPIO pins
calibration_light_pin = 1
dht11_pin = 2
barcodes_pin = 3
signal_light_pin = [4, 5, 6] # R pin, G pin, B pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(calibration_light_pin, GPIO.OUT)
GPIO.setup(dht11_pin, GPIO.IN)
GPIO.setup(barcodes_pin, GPIO.IN)
GPIO.setup(signal_light_pin[0], GPIO.OUT)
GPIO.setup(signal_light_pin[1], GPIO.OUT)
GPIO.setup(signal_light_pin[2], GPIO.OUT)
dht11_device = adafruit_dht.DHT11(dht11_pin, use_pulseio=False)

def calibration_light():
  ## The transmitter is outputting a calibration light signal to indicate that data is being transmitted to the receiver.
  
def camera_scanner():
  ## return values/data
  
def temp_and_hum_capture():
  ## return values
  
  

def captureData():
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

def pygame_setup():
  ## set up for pygame
  
def piTFT_disp():
  ## pygame
  
  
## main: use data for display
