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
from PIL import Image
import colorsys
import cv2 
import numpy as np

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
	# to do
	results["barcodes"] = ""
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
										 
def food_by_barcode(code):
	# https://thecleverprogrammer.com/2020/10/23/barcode-and-qr-code-reader-with-python/
	result = {"info":"", "freshness":0}
	#todo
	return result
										 
def food_by_cam(img):
	# https://www.hackster.io/taifur/ripe-fruit-identification-9c8848
	# https://medium.com/@jamesthesken/detect-ripe-fruit-in-5-minutes-with-opencv-a1dc6926556c
	# https://docs.python.org/3/library/colorsys.html		
	# define color thresholds tones in HSV
	food_dict = {"Red":[(345, 89.1, 50.6), (12, 69.5, 86.3)],
			"Deep_Orange":[(19, 93.1, 79.6), (20, 71.0, 100.0)],
			"Orange":[(33, 98.6, 81.2), (35, 75.3, 100.0)],
			"Ripe_Mango":[(44, 97.3, 88.2), (50, 74.1, 100.0)],
			"Bright_Yellow":[(56, 100.0, 88.2), (60, 88.2, 100.0)],
			"Green_Apple":[(103, 72.7, 58.8), (103, 51.9, 82.4)],
			"Kiwi":[(91, 83.4, 78.0), (102, 63.5, 100.0)],
			"Blueberry":[(240, 100.0, 50.2), (240, 20.0, 100.0)],
			"Blue_Violet":[(282, 100.0, 28.6), (300, 45.4, 93.3)]}
	result = {"info":[], "freshness":[]}
	#todo
	image = cv2.imread(img)
	img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)						    
	# detect fruit color in img - we know that the color(s) which contrast the setting of the box are the object, so detect fruit as an obj, get matching color threshold from food_dict, and then analyze.									 
	img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	fruit_data = cv2.CascadeClassifier('fruit_data.xml')
	found = stop_data.detectMultiScale(img_gray, minSize=(10, 10))	
	print("Objects Found:")						    
	for obj in found:
		print(obj)					    
	amount_found = len(found)
	print("# Found: " + str(amount_found))						    
	if amount_found != 0:
	  for (x, y, width, height) in found:
			#cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
			print("found food")
			print("Location: {x1}, {y1}".format(x1=x, y1=y))
			print("Dimensions: {w} by {h}".format(w=width, h=height))					    
			# which food?
			red_image = PIL.Image.open(img)
			red_image_rgb = red_image.convert("RGB")
			rgb_pixel_value = red_image_rgb.getpixel((x,y))
			food_name = ""
			info_arr = [food_name, rgb_pixel_value]					    
			result["info"].append(info_arr)
			cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
	#result["freshness"].append()
	#item_color = food_dict["red"]						    
	#weaker = item_color[0]
	#stronger = item_color[1]
	mask = cv2.inRange(img_hsv, weaker, stronger) #Threshold HSV image to obtain input color 
	cv2.imshow('Image',img_rgb)
	cv2.imshow('Result',mask) 
	return result
  
def captureData():
	## this function will be imported into the code that transmits the data, calls the functions defined above
	results = dict()
	try:
		## formatting the data into a JSON -> work with dictionary
		## Information for Recognized Food (name/type), ## Current Freshness of Food
		# for image scanner: using color analysis, we can compare the expected color of a dected object to the actual colors analyzed in the image in order to determine if an overwhelming part of the apperance indicates expiration. src: https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606      
		food_data = camera_scanner()
		food_img = Image.open(food_data["camera"])
		bar_codes = food_data["barcodes"]
		if len(bar_codes) > 0:
			b = food_by_barcode(bar_codes)
			results["info"] = b["info"]
			results["freshness"] = b["freshness"]
		else:
			i = food_by_cam(food_img)
			results["info"] = i["info"]
			results["freshness"] = i["freshness"]               
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
		return {"food info":-1, "freshness":-1, "temp_c":-1, "temp_f":-1, "humidity":-1, "temp_flag":-1, "hum_flag":-1} # params should equal -1 to indicate no valid reading
  
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
		
