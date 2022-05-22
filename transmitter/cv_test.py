import time
import serial
import sys
import datetime
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import os
import subprocess
import adafruit_dht
from picamera import PiCamera
from PIL import Image
import colorsys
import cv2 
import numpy as np
import board
from ws_barcode_scanner import BarcodeScanner
objnum = 1
import requests
from pathlib import Path

def scale_lightness(rgb, scale_l):
    # convert rgb to hls
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # manipulate h, l, s values and return as rgb
    return colorsys.hls_to_rgb(h, min(1, l * scale_l), s = s)

im = "image_2022_05_22_00_06_39.jpg"
img = cv2.imread(im)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_gray = cv2.equalizeHist(img_gray)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#cv.imshow("reg",img)
#cv.imshow("gray", img_gray)
#cv.imshow("hsv", img_hsv)
#cv.imshow("rgb", img_rgb)


#cv2.waitKey(0)
result = {"info":[], "freshness":[]}
    #todo
    #todo
f = 'apple.xml'
fruit_data = cv2.CascadeClassifier(f)
found = fruit_data.detectMultiScale(img_gray, minSize=(100, 100))
print("Objects Found:")   
amount_found = len(found)
print("# Found: " + str(amount_found))  
if amount_found != 0:
	for (x, y, width, height) in found:
		#cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
		print("found food")
		print("Location: {x1}, {y1}".format(x1=x, y1=y))
		print("Dimensions: {w} by {h}".format(w=width, h=height))   
		# which food?
		red_image = Image.open(im)
		red_image_rgb = red_image.convert("RGB")
		rgb_pixel_value = red_image_rgb.getpixel((x,y))
		info_arr = [found, rgb_pixel_value]  
		result["info"].append(info_arr)
		cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
		
		#just the apple
		apple = img[x:x+height, y:y+width]
		
item_arr = result["info"]
result["info"] = f.split(".", 1)[0] #name of obj
for obj in item_arr:
	## Based on infolist, threshold colors via food_dict => https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f
	item_color = obj[1]
	weaker = np.array([0,0,0])#scale_lightness(item_color, 0.5)
	stronger = np.array([350,55,100])#scale_lightness(item_color, 1.5)
	mask = cv2.inRange(img_rgb, weaker, stronger) #Threshold HSV image to obtain input color
	#calculate % of white content 
	white = cv2.countNonZero(mask) #number of non black pixels
	percentage = white/mask.size #white percentage 
	print("white = "+str(white))
	print("percentage white = "+str(percentage*100))
	# get all pixels contained in the obj area, use number of black in area (not white) by pixel
	# freshness = percent of black (black pixels of mask over total pixels in area).
	freshness = 1 - percentage #1 - percentage of white
	result["freshness"] = freshness*100
	print("freshness: "+str(result["freshness"]))
	
cv2.imshow('Image',img)
cv2.imshow('Result',mask) 

cv2.waitKey(0)

