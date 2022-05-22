#!/usr/bin/python
# function to read, format, and return the sensor data that we need

'''
This file is for function definitions only. Please import into a new python file in order to implement into main logic.
https://www.irjet.net/archives/V7/i5/IRJET-V7I51254.pdf
'''

## Import modules (gpio, libraries for reading data from sensors, etc)
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

## Set up GPIO pins and devices
calibration_light_pin = 26
dht11_pin = 13
barcodes_pin = 3
signal_light_pin = [22, 4, 6] # R pin, G pin, B pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(calibration_light_pin, GPIO.OUT)
p = GPIO.PWM(calibration_light_pin, 10) # channel = pin_num, frequency = freq
GPIO.setup(dht11_pin, GPIO.IN)
GPIO.setup(barcodes_pin, GPIO.IN)
GPIO.setup(signal_light_pin[0], GPIO.OUT)
GPIO.setup(signal_light_pin[1], GPIO.OUT)
GPIO.setup(signal_light_pin[2], GPIO.OUT)
dht11_device = adafruit_dht.DHT11(board.D13, use_pulseio=False)
# barcodes
scanner = BarcodeScanner("/dev/serial0")

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

def calibration_light():
    ## The transmitter is outputting a calibration light signal to indicate that data is being transmitted to the receiver.
    now = time.time()
    global p
    while (time.time() < now + 2):
        p.start(100)
        p.stop()
        print("blink")
        
def capture_photo():
    # take the photo and add to directory to be read
    camera = PiCamera()
    x = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    calibration_light()
    file_name = r'cam_data/image_{d}.jpg'.format(d=x)
    camera.capture(file_name)
    camera.close()
    return file_name
  
def camera_scanner():
    ## return values/data
    results = dict()
    time.sleep(0.2)
    # camera capture - get the last photo in photo directory
    file = open("file_log.txt", "r")
    file_name = file.readlines()[-1] # the only line should be the path of the most recent photo taken
    print(file_name)
    print(type(file_name))
    results["camera"] = file_name
    # barcode scanner
    global scanner
    timestamp = scanner.last_timestamp
    print("Looking for code")
    bcode = scanner.last_code
    #if (bcode == b''):
        #bcode = 1104086
    print(bcode)
    results["barcodes"] = [timestamp, bcode]
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
                                         
def food_by_barcode(code, temp, humidity):
    # https://thecleverprogrammer.com/2020/10/23/barcode-and-qr-code-reader-with-python/
    result = {"info":"", "freshness":0}
    if (code is None or code == b''):
        print("barcode cannot be read due to empty code")
        result["info"] = -1
        result["freshness"] = -1
        return result
    #todo
    data = code # look at upc api
    DEMO_KEY = "TfDLCvnjZoR2oyWIVIebJysr1TbYqi3PPDggY1Q8" # obtained from api.data.gov via email
    url = "https://api.nal.usda.gov/fdc/v1/food/{c}?api_key={d}".format(c=data, d=DEMO_KEY)
    food_code_info = requests.get(url)
    print("Status Code: "+str(food_code_info.status_code))
    if (food_code_info.status_code == 200 or food_code_info.status_code == 201):
        print("GET request worked")
        text = food_code_info.text
        result["info"] = text
    else:
        print("barcode cannot be read due to GET request issue (error or timeout): " + str(food_code_info.status_code))
        result["info"] = -1
        result["freshness"] = -1
        return result
    # the publicationDate field can be used, we can calculate a base "days left" using today's date minus publicationDate, then decay the number of days by looking at ambient conditions.
    today = datetime.datetime.now()
    pub_start = text.find("publicationDate")
    pub_date = text[pub_start + 18: pub_start + 28] 
    days_since = datetime.datetime.strptime(pub_date, "%m/%d/%Y") if pub_start != -1 else datetime.datetime.now() - datetime.timedelta(30) # assume that it just arrived to store in the past 30 days
    days_since_then = today - days_since
    print("days type = ", type(days_since_then.days))
    days_left = 730 - int(days_since_then.days)
    freshness = (days_left / 730) * 100 # look at upcfood api : exp date vs current day ratio: percentage per day left (730 days > implies 100% fresh)
    # we can also use basic facts about canned foods to set the freshness if it cannot be found; it takes about 2 years for the sell-by date to become unreliable on it's own if stored at 75 deg F and minimal humidity. temp and humidity affect this time. After this point, the person consuming or cooking the ingredient should be cautious. This is modeled based on predicted trends in bacteria growth dependent on these parameters.
    if (freshness == 0 or freshness is None) and temp != -1 and humidity != -1:
        temp_ideal = (temp >= 40 and temp <= 60)
        hum_ideal = (humidity <= 15)
        if temp_ideal and humidity_ideal:
            freshness = 100 # assume to be 100% fresh unless ambient conditions becom unideal
        elif temp_ideal and not humidity_ideal:
            freshness = 100 * ((100-humidity)/100)
        elif not temp_ideal and humidity_ideal:
            r = 2**48 # rate of bacterial grouth in a day
            t = days_left # in units of days
            rate_of_decay = 1 / (r**t)
            freshness = 100 * (rate_of_decay)
        else:
            r = 2**48 # rate of bacterial grouth in a day
            t = days_left # in units of days
            rate_of_decay_t = (1 / (r**t))
            rate_of_decay_h = ((100-humidity)/100)
            freshness = 100 * (rate_of_decay_h*rate_of_decay_t)
    result["freshness"] = freshness
    return result

def scale_lightness(rgb, scale_l):
    # convert rgb to hls
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # manipulate h, l, s values and return as rgb
    return colorsys.hls_to_rgb(h, min(1, l * scale_l), s = s)
                                         
def food_by_cam(img):
    # https://www.hackster.io/taifur/ripe-fruit-identification-9c8848
    # https://medium.com/@jamesthesken/detect-ripe-fruit-in-5-minutes-with-opencv-a1dc6926556c
    # https://docs.python.org/3/library/colorsys.html
    global objnum
    result = {"info":[], "freshness":[]}
    #todo
    image = cv2.imread(img)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
    f = 'apple.xml'
    fruit_data = cv2.CascadeClassifier(f)
    found = fruit_data.detectMultiScale(img_gray, minSize=(10, 10))
    print("Objects Found:")   
    amount_found = len(found)
    print("# Found: " + str(amount_found))  
    if amount_found > 0:
      for (x, y, width, height) in found:
        #cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
        print("found food")
        print("Location: {x1}, {y1}".format(x1=x, y1=y))
        print("Dimensions: {w} by {h}".format(w=width, h=height))   
        # restrict area of analysis to the apple
        apple = image[y:y+width, x:x+height]
        print(image.shape, apple.shape)
        c = r'cropped.jpg'
        cv2.imwrite(c, apple)
        read_image = Image.open(img)
        left = x.item()
        top = y.item()
        right = x.item()+height.item()
        bottom = y.item()+width.item()
        print("left: " , left)
        print("top: " , top)
        print("right: " , right)
        print("bottom: ", bottom)
        read_image = read_image.crop((left, top, right, bottom))
        read_image_rgb = read_image.convert("RGB")
        cw, ch = read_image_rgb.size
        center = (int((cw)/2),int((ch)/2))
        print("center:", center)
        rgb_pixel_value = read_image_rgb.getpixel(center)
        info_arr = [cv2.imread(c), rgb_pixel_value]  
        result["info"].append(info_arr)
        cv2.rectangle(img_rgb, (x, y), (x + height, y + width), (0, 255, 0), 5)
        print("info: "+str(result["info"]))
    else: # no items found, so nothing to analyze
        print("Since no objects were found, there is no information or freshness to analyze by view. Please add items to perform this analysis. Perhaps you might want to scan the barcodes of any canned items within?")
        result["info"] = -1
        result["freshness"] = -1
        return result
    item_arr = result["info"]
    result["info"] = f.split(".", 1)[0] #name of obj
    for obj in item_arr:
        ## Based on infolist, threshold colors via food_dict => https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f
        item_color = obj[1]
        #weaker = scale_lightness(item_color, 0.5)
        #stronger = scale_lightness(item_color, 1.5)
        weaker = np.array([0,0,0])#scale_lightness(item_color, 0.5)
        stronger = np.array([350,55,100])#scale_lightness(item_color, 1.5)
        # detect fruit color in img - we know that the color(s) which contrast the setting of the box are the object, so detect fruit as an obj, get matching color threshold from food_dict, and then analyze.
        print(type(obj[0]))
        mask = cv2.inRange(obj[0], weaker, stronger) #Threshold HSV image to obtain input color
        #calculate % of white content 
        white = cv2.countNonZero(mask) #number of non black pixels
        percentage = white/mask.size #white percentage 
        print("white = "+str(white))
        print("percentage white = "+str(percentage*100)+"%")
        # get all pixels contained in the obj area, use number of black in area (not white) by pixel
        # freshness = percent of black (black pixels of mask over total pixels in area).
        freshness = 1 - percentage #1 - percentage of white
        result["freshness"] = freshness*100
        print("freshness: "+str(result["freshness"]))
    #cv2.imshow('Image',img_rgb)
    #cv2.imshow('Result',mask)
    return result
  
def captureData():
    ## this function will be imported into the code that transmits the data, calls the functions defined above
    results = dict()
    results["timestamp_packet"] = str(datetime.datetime.now())
    try:
        ## formatting the data into a JSON -> work with dictionary
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
        ## Information for Recognized Food (name/type), ## Current Freshness of Food
        # for image scanner: using color analysis, we can compare the expected color of a dected object to the actual colors analyzed in the image in order to determine if an overwhelming part of the apperance indicates expiration. src: https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606      
        food_data = camera_scanner()
        print(food_data["barcodes"])
        path_file = food_data["camera"].strip()
        print(path_file)
        print(type(path_file))
        print(os.path.exists(path_file))
        print(os.listdir())
        if not os.path.exists(path_file):
            print("Path to photo cannot be found.")
            sys.exit(2)
        #food_img = Image.open(path_file, mode='r')
        bar_codes = food_data["barcodes"]
        print(bar_codes)
        if len(bar_codes) > 1 and bar_codes[1] != b'':
            b = food_by_barcode(bar_codes[1], results["temp_f"], results["humidity"])
            results["info"] = b["info"]
            results["freshness"] = b["freshness"]
        else:
            i = food_by_cam(path_file)
            results["info"] = i["info"]
            results["freshness"] = i["freshness"]               
        ## return data
        print(str(results))
        return results
    except:
        print("Quitting Program. Unexpected error: ", sys.exc_info())
        GPIO.cleanup()
        cv2.destroyAllWindows()
        sys.exit(2)
        quit()
  
def piTFT_disp(data):
    print(str(data))
    ## pygame
    global signal_light_pin
    global screen
    global WHITE
    global BLACK
    global screen
    global button_text
    global button_position
    global header_font
    global text_font
    global GPIO
    #quit button
    quit_surface = text_font.render(button_text,True,WHITE)
    quit_rect = quit_surface.get_rect(center = (button_position[0],button_position[1]))
    time.sleep(0.2)
    #while True:
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
                    cv2.destroyAllWindows()
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
    if (data["temp_flag"] or data["hum_flag"]):
        # red color
        print("Excess Temperature or Humidity Detected")
        GPIO.output(signal_light_pin[0], 255) # Red Pin Set
        GPIO.output(signal_light_pin[1], 0) # Green Pin Set
        GPIO.output(signal_light_pin[2], 255) # Blue Pin Set
    else: # neither
        # white color
        print("Optimal Temperature and Humidity Detected")
        GPIO.output(signal_light_pin[0], 0) # Red Pin Set
        GPIO.output(signal_light_pin[1], 255) # Green Pin Set
        GPIO.output(signal_light_pin[2], 0) # Blue Pin Set
    rightH_surface = text_font.render("Data",True,WHITE)
    rightH_rect = rightH_surface.get_rect(center = (275,50))
    print(data["temp_c"])
    print(data["temp_f"])
    print(data["humidity"])
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


