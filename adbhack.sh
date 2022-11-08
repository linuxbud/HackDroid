#!/bin/bash

#Hack android via adb over Internet
#Requirements : adb & scrcpy. First install them.

echo ""
echo ""
echo -e "\e[1;33m             ##      Hack Android over Internet    ##     \e[0m"
echo ""
echo ""
adb kill-server;
adb start-server;
adb tcpip 5555;
echo ""
echo -e "\e[1;32m Put Ip Addr: \e[0m"
# IP input prompt
read -p "=>" IP;
adb connect $IP;
echo ""
echo -e "\e[1;32m Put Fps rate: [less than 15 for performace] \e[0m"
# Fps input prompt
read -p "=>" FPS;
scrcpy -b2M -m800 --max-fps $FPS;
echo ""
echo -e "\e[1;33m Press ENTER to run it again \e[0m"
echo ""
echo -e "\e[1;31m Press Zero (0) to exit \e[0m"
echo ""
read -p "=>" ANS
if [ $ANS -eq 0 ]
then
	exit
else
	./$0
fi

