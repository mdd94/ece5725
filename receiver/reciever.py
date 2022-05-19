'''
Main Receiver Logic

'''
import get_data
import json

# read data in from the json
f = open("data.json", "r")
data = json.load(f)
print(f.read())


