#!/bin/bash

#Run both the transmitter and receiver bash scripts in one go:
runs=1
while true
do
  echo "======= Run #$runs ======="
  echo "====== Run Transmitter ======"
  #Transmitter runs, background
  sudo python3 /home/pi/ece5725/transmitter/run_transmitter.sh &
  echo "====== Run Receiver ======"
  #Receiver runs, background
  sudo python3 /home/pi/ece5725/receiver/run_receiver.sh &
  let runs++
done

