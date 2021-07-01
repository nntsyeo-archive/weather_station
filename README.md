# CM3267 Lab Instruction for Weather Station

Welcome to this module! To get things started, setup your Raspberry Pi (RPi) with the correct Raspbian version. You can use [RPi Imager Software](https://www.raspberrypi.org/software/ "enter this website to download the software") to flash the **recommended** 32-bit Raspbian OS onto your 16/32 GB micro-SD (uSD) card.

Once you pluck the uSD card into the RPi board, boot it and continue setting up the desired language, US keyboard type and location. **MAKE SURE NOT** to update the OS when the update request prompts out.

NOTE:

- To check if you have the right OS version on the RPi, open a terminal and type `uname -r`.
- _5.10.17-v7+_ should be the output. Otherwise, install the OS manually (on PC) through the image provided [here](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip "5.10.17-v7+ OS image download") and flash it once more with RPi Imager software.

## Install the necessary packages for the python scripts

```
sudo apt-get update
sudo pip3 install Adafruit_DHT matplotlib datetime
sudo pip install pyserial Adafruit_DHT schedule datetime matplotlib
sudo apt-get install -y python-matplotlib
```

cd ~
git clone https://github.com/Nntsyeo/weather_station.git

## Potential error during the python execution

1. For _V2_weatherplot.py_:

- Error output:
  "RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd"
  Try doing this:

```
sudo apt-get install -y libatlas-base-dev
sudo pip3 install numpy --upgrade
cd ~/weather_station
sudo python3 V2_weatherplot.py
```
