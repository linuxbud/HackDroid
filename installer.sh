#!/bin/bash

sudo apt update;
sudo apt install adb scrcpy -y;
chmod +x androhack.py
sudo cp androhack.py /usr/bin/androhack;
mkdir ~/.androhack
cp logo.txt shodan_api_key.txt ~/.androhack
pip3 install -r requirements.txt
cd ~/.androhack
touch ip_list.txt
touch hackable_ip_list.txt
cd ~

echo "



        Installation Done ...
        Mr. Garbage says, "You're welcome $USER"



"

exit