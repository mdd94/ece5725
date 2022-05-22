#!/bin/bash

#quit functionality
set -e

script_full_path=$(dirname "$0")

#The background processes will occur below (e.g., transmission of data to receiver device(s))

#Capture camera photo
echo "taking photo"
#first refresh cam dir to avoid clutter
rm -rf $script_full_path/cam_data/*
timeout 30 sudo python3 $script_full_path/photo.py > $script_full_path/file_log.txt
cat $script_full_path/file_log.txt

#echo "Transmission Activated. Data saving to json"
#host_addr="localhost" #subject to change, run IP command to check and then edit this code
#host_port="65432"

#sudo python3 $script_full_path/transmit_server.py $host_addr $host_port &
#timeout 30 sudo python3 $script_full_path/transmit_client.py $host_addr $host_port &
#echo "Transmission Done. Data saved to json"

#The foreground processes will occur below (e.g., displaying data in RT on the PiTFT screen)
echo "main script activated"
sudo python3 $script_full_path/main.py
echo "main executed, program is done."

# Backup to GitHub
echo "push initiated"
timeout 30 /home/pi/ece5725/push_changes.sh &
echo "push is commenced, moving on..."

read -t 3 -n 1 keyinput
if [ $? = 0 ] ; then
	exit;
fi

