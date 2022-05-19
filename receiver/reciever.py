'''
Main Receiver Logic

'''
import get_data
import json
import matplotlib.pyplot as plt

# read single data entry in from the json
f = open("data.json", "r")
data = json.load(f)
print(f.read())

# food inventory information {info}
information = 

# temperature and humidity data
temperature = 
humidity = 

# freshness of the food
freshness = 

# recipe book data
recipe = 

# dashboard construction for date
info = [information, temperature, humidity, freshness, recipe]
get_data.construct_dashboard(info) # check directory for output

# create file with all data, historical html
f_all = open("data_all.json", "r")
data_all = json.load(f_all)
print(f_all.read())
i_info = []
i_temp = []
i_humi = []
i_fresh = []
i_rep = []
for entries in data_all['data_string']:
  print(entries)
  if (entries['info'] != -1 and entries['temp_c'] != -1 and entries['temp_f'] != -1 and entries['humidity'] != -1 and entries['freshness'] != -1):
    info = i_info.append(entries['info'])
    temperature_c = i_temp.append(entries['temp_c'])
    temperature_f = i_temp.append(entries['temp_f'])
    humidity = i_humi.append(entries['humidity'])
    freshness = i_fresh.append(entries['freshness'])
    recipe = get_data.recipe_book(entries['info'])
    i_rep.append(recipe)
all_datapg = open("historical_data.html","w")
pg = "<!DOCTYPE html> \n<html> \n<head> \n<title>Food Mgmt Dashboard</title> \n<style> \n.all-browsers {margin: 0; padding: 5px; background-color: rgb(240, 250, 255);} \n.all-browsers > h1, \n.browser {margin: 10px;  padding: 5px;} \n.browser {background: white;} \n.browser > h2, p {  margin: 4px;  font-size: 90%;} \nfooter { text-align: center; padding: 3px; background-color: lightgray; color: white;}\n</style>\n</head> <body>\n"
pg += "<p>Welcome to the IoT Food Management System! Data is graphed below.</p>\n"
pg += "<h2> Food Inventory Log </h2>\n"
for i in i_info:
  pg += "<p>{info_a}</p>\n".format(info_a=i)
pg += "<h2> Temperature Graph over Time </h2>"
plt.plot()
plt.savefig()
plt.plot()
plt.savefig()
pg += "<p></p>"
pg += "<p></p>"
pg += "<h2> Humidity Graph over Time </h2>"
plt.plot()
plt.savefig()
pg += "<p></p>"
pg += "<h2> Freshness Graph over Time </h2>"
plt.plot()
plt.savefig()
pg += "<p></p>"
for r in i_rep:
  pg += r
pg += "</body>\n</html>\n"
pg += "<footer>\n"
pg += "<p>This project was developed in the Spring of 2022 for ECE 5725 by Michelle Davies (mdd94) and Myles Cherebin (mac497), Wednesday Group 3 Lab.<p>\n"
pg += "</footer>"
all_datapg.write(pg)
all_datapg.close()


# create index file with all data linked
index = open("index.html","w")
page = "<!DOCTYPE html> \n<html> \n<head> \n<title>Food Mgmt Dashboard</title> \n<style> \n.all-browsers {margin: 0; padding: 5px; background-color: rgb(240, 250, 255);} \n.all-browsers > h1, \n.browser {margin: 10px;  padding: 5px;} \n.browser {background: white;} \n.browser > h2, p {  margin: 4px;  font-size: 90%;} \nfooter { text-align: center; padding: 3px; background-color: lightgray; color: white;}\n</style>\n</head> <body>\n"
page += "<p>Welcome to the IoT Food Management System! Past dashboard data entries for specific dates are linked below.</p>\n"
page += "<h2> Dashboard Entries</h2>\n"
for root, dirs, files in os.walk(r'./reciever'):
	    # select file name
	    for file in files:
	        # check the extension of files
	        if file.endswith('.html') and file != 'index.html':
	            # print whole path of files
	            file_path = os.path.join(root, file)
	            print(file_path)
	            page += "<p><a href='{link}'>{file_name}</a></p>\n".format(file_name=file, link=file_path)
page += "</body>\n</html>\n"
page += "<footer>\n"
page += "<p>This project was developed in the Spring of 2022 for ECE 5725 by Michelle Davies (mdd94) and Myles Cherebin (mac497), Wednesday Group 3 Lab.<p>\n"
page += "</footer>"
index.write(page)
index.close()
