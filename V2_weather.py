#!/usr/bin/python -u
import RPi.GPIO as GPIO
import serial
import time, struct
import schedule
import Adafruit_DHT
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

#############################################
"INPUT SECTION"
#############################################

delay = 10                                  #interval of recording data (in seconds) used in the function 'recording()' below

"""Change filename"""

filename = "Finaltest"                      #<< Change the filename

"""Change filename"""

#############################################
"CHANNEL CREATION OF HUMIDITY AND TEMPERATURE DHT22 SENSOR"
#############################################

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4                               ### Pin number can change with your preference, check GPIO pinout for reference

#############################################
"CHANNEL CREATION OF NOVA PM SENSOR"
#############################################

DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1
PERIOD_CONTINUOUS = 0

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600
ser.open()
ser.flushInput()

byte, data = 0, ""

def read_response():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    return [pm25, pm10]

def cmd_query_data():
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    values = []
    if d[1] == "\xc0":
        values = process_data(d)
    return values

def cmd_set_sleep(sleep):
    mode = 0 if sleep else 1
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()
    
def cmd_set_mode(mode=MODE_QUERY):
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()
    
def cmd_set_working_period(period):
    ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()

cmd_set_sleep(0)
cmd_set_working_period(PERIOD_CONTINUOUS)
cmd_set_mode(MODE_QUERY);



#############################################
"FUNCTIONS FOR READING AND RECORDING SENSORS"
#############################################

def weather():
    try:
##       {Choice of interval selection to run script}
        """Best to keep interval in whole 'hour' format as seen below."""
        """Graph plotting script handles data in hours exclusively"""
        """Change the schedule only if you are mindful of data processing"""
        """e.g at the 15/30/45th minute of every hour works too."""
        """Any other denomination would be tedious though i.e last 3 options"""

##        schedule.every().hour.at(":30").do(recording)
#         schedule.every().hour.at(":00").do(recording)
        
        print("recording data...")
#         schedule.every(1).minutes.do(recording)
##        schedule.every().day.do(recording)
        schedule.every(5).seconds.do(recording)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print("Program end")

def recording():
    cmd_set_sleep(0)
    humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    """BASED ON YOUR CALIBRATION OR THE DETERMINATION OF ERROR, CHANGE THE HUMIDITY AND TEMPERATURE ACCORDINGLY BY ADDING AN EQUATION"""
    """e.g HUM = humidity + 0.3. Then change the defined humidity and temperature terms in the script below respectively"""
        
    values = cmd_query_data();
    if values is not None and len(values) == 2 and humidity is not None and temperature is not None:
        f = open(filename+".csv", 'a')
        m = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        x = datetime.strptime(m, '%Y-%m-%d %H:%M:%S')
        xs = matplotlib.dates.date2num(x)
        h = datetime.now().hour
        
        """ Change humidity and temperature according to conclusions from calibration"""
        
        data_pt = "{:1}{:15.6f}{:7.2f}{:7.2f}{:7.2f}{:7.2f}\n".format(h, xs, values[0], values[1], temperature, humidity)
        
        """ Change humidity and temperature according to conclusions from calibration"""
        
        ###############################################
        ###Format of {} above:###
        ###{'Column/printing index':'Space between columns'.'Number of decimal places'f} , f = float i.e numbers with decimals ###
        ###############################################
        f.write(data_pt)
        print(m)
        print("Hour= {:1} PM2.5= {:1.2f}ug/m^3 PM10= {:1.2f}ug/m^3 Temp= {:1.2f}*C  Humidity= {:1.2f}%".format(h, values[0],values[1],temperature,humidity))
        time.sleep(delay)
    elif values is None:
        print("Problem occurred with Air Quality sensor")
    elif humidity is None:
        print("Problem occurred with DHT22 sensor")
    elif temperature is None:
        print("Problem occurred with DHT22 sensor")
    else:
        print ("Failed to retrieve data from sensors")

#############################################
"EXECUTION OF WEATHER STATION"
#############################################

weather()

