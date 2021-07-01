# CM3267 Lab Instruction for Weather Station

Welcome to this module! To get things started, setup your Raspberry Pi (RPi) with the correct Raspbian version. You can use [RPi Imager Software](https://www.raspberrypi.org/software/ "enter this website to download the software") to flash the **recommended** 32-bit Raspbian OS onto your 16/32 GB micro-SD (uSD) card.

Once you pluck the uSD card into the RPi board, boot it and continue setting up the desired language, US keyboard type and location. **MAKE SURE NOT** to update the OS when the update request prompts out.

NOTE:

- To check if you have the right OS version on the RPi, open a terminal and type `uname -r`.
- _5.10.17-v7+_ should be the output. Otherwise, install the OS manually (on PC) through the image provided [here](https://downloads.raspberrypi.org/raspios_armhf/images/raspios_armhf-2021-05-28/2021-05-07-raspios-buster-armhf.zip "5.10.17-v7+ OS image download") and flash it once more with RPi Imager software.

## Download the repo and necessary packages

Open up a terminal and follow the commands below:

```
cd ~
git clone https://github.com/Nntsyeo/weather_station.git
```

You should now have a folder named _weather_station_ in your home directory. Next, you will need to install the python packages through the terminal.

```
sudo apt-get update
sudo pip3 install Adafruit_DHT matplotlib datetime
sudo pip install pyserial Adafruit_DHT schedule datetime matplotlib
sudo apt-get install -y python-matplotlib
```

Now, you should be able to execute the python scripts accordingly:

```
sudo python V2_weather.py
sudo python3 DHT22_cal.py
sudo python3 weatherplot.py
```

NOTE:

- _V2_weather.py_ uses the particle sensor on port _/dev/ttyUSB0_. Thus, to make sure the particle sensor is active on RPi, simply type `ls \dev\tty*` on the terminal and check if _/dev/ttyUSB0_ is present (usually at the end of the list).

@1 ----- If _/dev/ttyUSB0_ is not present, try using the particle sensor on another USB port. <br>
@2 ----- If a different portname is present (for e.g., _/dev/ttyUSB2_), simply use Thonny to edit the portname within the _V2_weather.py_ at line 46 to `_/dev/ttyUSB<port_number>_`.

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
