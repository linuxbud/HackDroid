#!/bin/sh

sudo apt install adb scrcpy -y ;
chmod +x androhack ;
sudo mv androhack /usr/bin ;
androhack ;
exit
