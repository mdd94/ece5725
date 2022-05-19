'''

This file defines the functions that intake, read and process the data packets that have been sent to the receiver program.
They will be called in the main program.

Sources:
https://realpython.com/beautiful-soup-web-scraper-python/#static-websites
https://github.com/psf/requests-html

'''

import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession
import datetime
import glob
import os
import socket
import sys

## Reading Data Functions

def read_in(HOST, PORT):
	# receive packet, read, return it as dict structure
	if HOST is None:
	    HOST = "127.0.0.1"  # The server's hostname or IP address
	if PORT is None:
	    PORT = 65432  # The port used by the server
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    	s.connect((HOST, PORT))
    	data = s.recv(1024)
    	s.close()
	print(f"Received {data!r}")
	return data # expecting JSON

## Processing Data Functions

def websc_recipes(food):
	## use food argument to do a Google search for recipes and return resulting links as well as search query link.
	recipes = dict()
	search_URL_g = "https://www.google.com/search?q=recipes+with+{ingredient}".format(ingredient=food)
	search_URL = "https://www.bbcgoodfood.com/recipes/collection/{ingredient}-recipes".format(ingredient=food)
	# The original search URLs are always an element of recipes, guarrenteeing that length(search_URL) >= 1
	recipes["food_ingredient"] = food
	recipes["g_search_url"] = search_URL_g
	recipes["bbc_search_url"] = search_URL
	session = HTMLSession()
	page_web = session.get(search_URL)
	page_web.html.render()
	results_bbc = page_web.html.search(food.lower())[0]
	print(results_bbc)
	recipes["results_bbc_raw"] = results_bbc
	page_google = session.get(search_URL_g)
	page_google.html.render()
	results_g = page_google.html.search(food.lower())[0]
	print(results_g)
	recipes["results_google_raw"] = results_g
	# having the raw data is good, but it would be better to get the target data...for google, the title and link would suffice; for bbc, the description with each link would be great in addition to the same components as the google one
	# google
	title_g = [element.text for element in page_google.html.find('.title')]
	link_g = [element.text for element in page_google.html.find('.link')]
	recipe_data_google = dict(zip(title_g, link_g))
	recipes["results_google_processed"] = recipe_data_google
	# bbc
	title_b = [element.text for element in page_web.html.find('.title')]
	link_b = [element.text for element in page_web.html.find('.link')]
	desc_b = [element.text for element in page_web.html.find('.description')]
	recipe_data_bbc = dict(zip(title_b, link_b, desc_b))
	recipes["results_bbc_processed"] = recipe_data_bbc
	return recipes


## Outputting HTML dashboard with data Functions

# display info on inventory, expecting JSON input
def inventory(read):
	print(read)
	info = "<h2>Information about the food in the Inventory</h2>\n"
	info += "<p>{data}</p>".format(data=read)
	return info

# get data for humidity, expecting JSON input
def hum_data(read):
	print(read)
	info = "<h2>Information about the humidity of the storage unit</h2>\n"
	info += "<p>Current Humidity: {data}%</p>".format(data=read)
	return info

# get data for temp, expecting JSON input
def temp_data(read):
	print(read)
	info = "<h2>Information about the temperature of the storage unit</h2>\n"
	info += "<p>Current Temperature: {data_c}°C</p> \n <p>Current Temperature: {data_f}°F</p>".format(data_c=read["temp_c"], data_f=read["temp_f"])
	return info

# get freshness of food graph trend, expecting JSON input
def fresh_data(read):
	print(read)
	info = "<h2>Information about the freshness of the food contained in the storage unit</h2>\n"
	info += "<p>Food freshness: {data}</p>".format(data=read)
	return info

# format recipe information, expecting dict input
def recipe_book(read):
	print(read)
	html_out = "\n<h2>Recipe(s) for Inventory Items</h2>\n<p>For the items identified in the pantry, we have found a few recipes that you can follow in order to use the food while it is still fresh. These recipes were sourced from bbcgoodfood and Google at the time of compliation.</p>\n"
	for key, value in read.items():
		if key == "food_ingredient":
			new_info = "<p>The item in our inventory that we will be analyzing is {v} [arg={k}].</p>\n".format(k=key, v=value)
		elif key == "g_search_url": 
			new_info = "<p>To search for recipes for this food ingredient on Google, we can navigate to the following <a href='{v}'>link</a> [arg={k}].</p>\n".format(k=key, v=value)
		elif key == "bbc_search_url": 
			new_info = "<p>We can also search for this food ingredient on BBC Good Food to find a recipe, by navigating to the following <a href='{v}'>link</a> [arg={k}].</p>\n".format(k=key, v=value)
		else: # other data
			for key1, value1 in value.items():
				new_info = "<h4>Recipe Data from Webscrapping:</h4>\n<p>{v}</p>\n".format(k=key1, v=value1)
		html_out += new_info
	return html_out

# construct html dashboard with the info obtained via the previous helper functions
# expect all info to be put into array to be written into HTML in function
def construct_dashboard(info):
	dashboard = open("dashboard_{d}.html".format(d=datetime.now()),"w")
	# format beginning
	dashboard.write("<!DOCTYPE html> \n<html> \n<head> \n<title>Food Mgmt Dashboard</title> \n<style> \n.all-browsers {margin: 0; padding: 5px; background-color: rgb(240, 250, 255);} \n.all-browsers > h1, \n.browser {margin: 10px;  padding: 5px;} \n.browser {background: white;} \n.browser > h2, p {  margin: 4px;  font-size: 90%;} \nfooter { text-align: center; padding: 3px; background-color: lightgray; color: white;}\n</style>\n</head> <body>\n")
	dashboard.write("<h1>IoT Food Management System Dashboard</h1>\n")
	dashboard.write("<p>This dashboard reports trends in temperature and humidity over time as it relates to food item freshness for each item logged in inventory.</p>\n")
	for piece in info:
		print(piece)
		dashboard.write(piece)
	# format ending
	dashboard.write("</body>\n</html>\n")
	# traverse whole directory
	dashboard.write("<footer>\n")
	dashboard.write("<h2>Past Dashboard Entries</h2>\n")
	for root, dirs, files in os.walk(r'./reciever'):
	    # select file name
	    for file in files:
	        # check the extension of files
	        if file.endswith('.html'):
	            # print whole path of files
	            file_path = os.path.join(root, file)
	            print(file_path)
	            dashboard.write("<p><a href='{link}'>{file_name}</a></p>\n".format(file_name=file, link=file_path))
	dashboard.write("<p>ECE 5725 - Spring 2022 | IoT Food Management System</p>\n<p>Group 3, Wednesday Night Lab</p>\n")
	dashboard.write("</footer>")
	dashboard.close() # finished writing file

