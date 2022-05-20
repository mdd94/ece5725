#!/bin/bash

script_full_path=$(dirname "$0")

#In order to avoid disrupting the system, we will first ensure that all system dependencies are installed, and install them if not, before proceeding.
time_lib = $(sudo pip3 show time)
serial_lib = $(sudo pip3 show serial)
sys_lib = $(sudo pip3 show sys)
datetime_lib = $(sudo pip3 show datetime)
gpio_lib = $(sudo pip3 show RPi.GPIO)
pygame_lib = $(sudo pip3 show pygame)
os_lib = $(sudo pip3 show os)
subprocess_lib = $(sudo pip3 show subprocess)
adafruit_dht_lib = $(sudo pip3 show adafruit_dht)
picamera_lib = $(sudo pip3 show picamera)
PIL_lib = $(sudo pip3 show PIL)
colorsys_lib = $(sudo pip3 show colorsys)
cv2_lib = $(sudo pip3 show cv2)
numpy_lib = $(sudo pip3 show numpy)
board_lib = $(sudo pip3 show board)
ws_barcode_scanner_lib = $(sudo pip3 show ws_barcode_scanner)
requests_lib = $(sudo pip3 show requests)

lib_array = (time_lib serial_lib sys_lib datetime_lib gpio_lib pygame_lib os_lib subprocess_lib adafruit_dht_lib picamera_lib os_lib PIL_lib colorsys_lib cv2_lib numpy_lib board_lib ws_barcode_scanner_lib requests_lib)

for lib in ${lib_array[@]}; do
	if [[ $lib ]]; then
	    echo "Library has been found in the system. We may proceed."
	elif [[$? != 0]]; then
		echo "Command failed."
		exit 0
	else
	    echo "$lib was not found in the system. Please install before proceeding."
	    exit 0
	fi
done

#The background processes will occur below (e.g., transmission of data to receiver device(s))

host_addr = "localhost" #subject to change, run IP command to check and then edit this code
host_port = "65432"

sudo python3 $script_full_path/transmit_server.py $host_addr $host_port &
sudo python3 $script_full_path/transmit_client.py $host_addr $host_port &

# Backup to GitHub
/home/pi/ece5725/push_changes.sh &

#The foreground processes will occur below (e.g., displaying data in RT on the PiTFT screen)

sudo python3 $script_full_path/main.py

