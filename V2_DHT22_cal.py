import Adafruit_DHT
import time
import numpy as np

"""FOR DHT22 SENSOR CALIBRATION, YOU CAN USE THIS SCRIPT OR EXCEL, WHICHEVER IS MORE COMFORTABLE"""
"""THE DATA PROCESSING CALCULATES THE MEAN ABSOLUTE DIFFERENCE"""
"""IF YOU WANT TO GET A CALIBRATION GRAPH OR ANY OTHER ERROR MEASUREMENT TO CALIBRATE THE DHT22 SENSOR, TWEAK THE FUNCTIONS BELOW OR USE EXCEL TO LOG AND PROCESS"""

#############################################
"CHANNEL CREATION OF HUMIDITY AND TEMPERATURE DHT22 SENSOR"
#############################################
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4                               ### Pin number can change with your preference, check GPIO pinout for reference


#############################################
"SELECTION QUALIFIERS"
#############################################

yesChoice = ['Y', 'y',]
noChoice = ['N', 'n']
humidChoice = ['H', 'h']
tempChoice = ['T', 't']
processChoice = ['P', 'p']
caliChoice = ['C', 'c']


#############################################
"FUNCTIONS"
#############################################

def cORp():
    print("This is to process measurements or calibrate the Humidity / Temperature of DHT22 sensor. Press CTRL + C to exit")
    cek = input("Calibrate or process results? (c/p): ")
    if cek in processChoice:
        MOD()
    elif cek in caliChoice:
        which()
    else:
        print("Input error")

def MOD():
    check = input("Want to find the mean of difference? (y/n):")
    if check in yesChoice:
        fname = input("Please enter the calibration file name for processing: ")
        data = np.loadtxt(fname+".csv")
        Diff = np.abs(data[1] - data[0])
        aveDiff = np.mean(Diff)
        print ("Mean of difference = {:0.2f}".format(aveDiff))
    elif check in noChoice:
        print("Alright then.")

def which():
    select = input("Which to calibrate, Humidity or Temperature? (h/t): ")
    if select in humidChoice:
        HUcal()
    elif select in tempChoice:
        TEcal()
    else:
        print("Error. Will exit please start again")

def HUcal():
    print("Let's calibrate the HUMIDITY measurement. ")
    filename = input("Please enter a/the calibration file name: ")
    f = open(filename+".csv", 'a')
    Data = int(input("How many humidity intervals to measure?: "))
    for x in range (0,Data):
        print("Place DHT22 sensor in the air tight jar. ")
        JAR = float(input("Digital Hygrometer humidity value: "))      ## Humidity level read by hygrometer
        Read = Hquery()                                                ## Humidity level read by DHT22 sensor
        f = open(filename+".csv", 'a')
        cal_pt = "{:10.2f}{:10.2f}\n".format(Read,JAR)
        f.write(cal_pt)
        print("DHT22 Humidity= {:0.2f}% Jar Humidity= {:0.2f}%".format(Read,JAR))
    MOD()                                                              ## Immediately asks to find mean absolute difference

def Hquery():
    while True:
        humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        H = humidity
##        print("DHT22 Humidity reading = {:10.2f}%".format(H))
        query_str = input("Take this voltage? (y/n) : ")
        if query_str in yesChoice:
            break
    return H

def TEcal():
    print("Let's calibrate the TEMPERATURE measurement. ")
    filename = input("Please enter a/the calibration file name: ")
    f = open(filename+".csv", 'a')
    Data = int(input("How many temperature levels to measure?: "))
    for x in range (0,Data):
        print("Place DHT22 sensor in a waterproof bag and submerge in waterbath. ")
        BATH = float(input("Waterbath thermometer temperature?: "))    ## Temperature read by external thermometer
        TRead = Tquery()                                               ## Temperature read by DHT22 sensor
        f = open(filename+".csv", 'a')
        cal_pt = "{:10.2f}{:10.2f}\n".format(TRead,BATH)
        f.write(cal_pt)
        print("DHT22 Temperature= {:0.2f}oC Water bath Temperature= {:0.2f}oC".format(TRead,BATH))
    MOD()                                                              ## Immediately asks to process and find mean absolute difference

def Tquery():
    while True:
        humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        T = temperature
        print("DHT22 Temperature reading = {:10.2f}*C".format(T))
        query_str = input("Take this Temperature? (y/n) : ")
        if query_str in yesChoice:
            break
    return T 

#############################################
"CALLING OF FUNCTION"
#############################################
cORp()   
    
    
    
    
    
        

    