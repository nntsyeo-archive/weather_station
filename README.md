
# install necessary packages to setup for weather station program
sudo apt-get update
sudo pip3 install Adafruit_DHT matplotlib datetime 
sudo pip install pyserial Adafruit_DHT schedule datetime matplotlib
sudo apt-get install python-matplotlib

cd ~
git clone https://github.com/Nntsyeo/weather_station.git
