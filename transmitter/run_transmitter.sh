#!/bin/bash

script_full_path=$(dirname "$0")

#The background processes will occur below (e.g., transmission of data to receiver device(s))

host_addr = "localhost" #subject to change, run IP command to check and then edit this code
host_port = "65432"

sudo python3 $script_full_path/transmit_server.py $host_addr $host_port &
sudo python3 $script_full_path/transmit_client.py $host_addr $host_port &

# Backup to GitHub
/home/pi/ece5725/push_changes.sh &

#The foreground processes will occur below (e.g., displaying data in RT on the PiTFT screen)

sudo python3 $script_full_path/main.py

