#!/bin/bash

script_full_path=$(dirname "$0")

requests_lib = $(sudo pip3 show requests)
bs4_lib = $(sudo pip3 show bs4)
requests_html_lib = $(sudo pip3 show requests_html)
datetime_lib = $(sudo pip3 show datetime)
glob_lib = $(sudo pip3 show glob)
os_lib = $(sudo pip3 show os)
socket_lib = $(sudo pip3 show socket)
sys_lib = $(sudo pip3 show sys)

lib_array = (requests_lib bs4_lib requests_html_lib datetime_lib glob_lib os_lib socket_lib sys_lib)

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

#The foreground processes will occur below

sudo python3 $script_full_path/receiver.py
