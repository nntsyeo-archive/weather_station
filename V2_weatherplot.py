import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator
from datetime import datetime
import numpy as np

## In this script, there are a few options to plot your graphs depending on your analysis requirements.
## The flow is as follows:
## 1) It asks if you want either 1 or 2 parameters against time on the same graph. for e.g (Time + Humidity OR Time + Humidity + PM2.5 )
## 2) It asks if you'd want a continuous time plot or specific durations (continuous, full days starting from 00 00, 24h from random start time)
## 3) It asks which parameters to plot against time
## 4) Graph is produced

###########################
"SELECTION QUALIFIERS"
###########################
yesChoice = ['Y', 'y',]
noChoice = ['N', 'n']
fiveChoice = ['F', 'f']
tenChoice = ['T', 't']
HumidChoice = ['H', 'h']
warmChoice = ['W', 'w']
SingleChoice = ['S', 's']
DoubleChoice = ['D', 'd']
ContiChoice = ['C', 'c']
BracketChoice = ['B', 'b']
TwofourChoice = ['R', 'r']

###########################
"FUNCTIONS TO CALL"
###########################

def check():
    cek = input("Do you want to plot? (y/n): ")
    if cek in yesChoice:
        query()
    elif cek in noChoice:
        print("Alright then, bye. ")
    else:
        print("Input error. Will Exit.")

def query():
    SorD = input("Single plot? (e.g Just PM2.5 vs time) OR Double plot?(e.g PM2.5 + PM10/Humidity/Temperature vs time?) Enter (s/d): ")
    if SorD in SingleChoice:
        single()
    elif SorD in DoubleChoice:
        double()
    else:
        print("Error, will exit. ")

###########################
"SINGLE PARAMETER SELECTION"
###########################

def single():
    fname = input("Which datafile would you like to access?: ")
    data = np.loadtxt(fname+".csv")
    newfile = input ("Give this plot a filename!: ")
    contiORtime = input ("Continuous, fixed bracket or 24h-cycle plots? Enter (c/b/r): ")
    MHT1 = input("Which data? PM2.5 (f) / PM10(t) / humidity(h) / temperature(w)? Enter (f/t/h/w): ")
    
    if MHT1 in fiveChoice:
        colnum = 2
        plotname = "PM2.5 vs Time"
        yname = "PM2.5"
        
    elif MHT1 in HumidChoice:
        colnum = 3
        plotname = "PM10 vs Time"
        yname = "PM10"
        
    elif MHT1 in HumidChoice:
        colnum = 5
        plotname = "Humidity vs Time"
        yname = "Humidity"
        
    elif MHT1 in warmChoice:
        colnum = 4
        plotname = "Temperature vs Time"
        yname = "Temperature"
        
    else:
        print("Input Error. No column selected. Will exit. ")
    
    if contiORtime in ContiChoice:
        Typename = "Continuous "
        
        x = []
        y = []
        
        if np.shape(data) == (4,):
            x.append(data[1])
            y.append(data[colnum])
        else:
            for i in range(0,len(data)): 
                x.append(data[i,1]) 
                y.append(data[i,colnum])
    
    elif contiORtime in BracketChoice:
        Typename = "Bracket "
        Hday = input("Did the first day begin at midnight?: (y/n): ")
        if Hday in noChoice:
            dayhours = int(input("How many hours were recorded in the first day?: "))
        elif Hday in yesChoice:
            dayhours = 0
        startdate = int(input("Plot from which day? Enter integer: "))
        lastday = input("Are you including the last day? (y/n): ")
        
        if lastday in yesChoice:
                        
            startrownum = int((startdate-1)*24-dayhours)
            
            x = []
            y = []
            
            x.append(data[startrownum:,1])
            y.append(data[startrownum:,colnum])
            
        elif lastday in noChoice:
            enddate = int(input("Plot till end of which day? Enter integer: "))            
            startrownum = int((startdate-1)*24-dayhours)
            endrownum = int(enddate*24-dayhours)
            
            x = []
            y = []
            
            x.append(data[startrownum:endrownum,1])
            y.append(data[startrownum:endrownum,colnum])              
    
    elif contiORtime in TwofourChoice:
        Typename = "24h "
        
        startrownum = int((startdate-1)*24)
        endrownum = int(enddate*24)
        
        x = []
        y = []
        
        x.append(data[startrownum:endrownum,1])
        y.append(data[startrownum:endrownum,colnum])

    hfmt = matplotlib.dates.DateFormatter('%m-%d\n%H:%M:%S')
       
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.xaxis.set_major_formatter(hfmt)
    ax1.set_title(Typename + plotname + " plot")
    ax1.set_xlabel('Time')
    ax1.set_ylabel(yname, color = color)
    
    """Change the major and minor time locators below. This gives different x-axis grids and labelling"""
    
##    ax1.xaxis.set_major_locator(HourLocator())
    ax1.xaxis.set_major_locator(DayLocator()) # Other inputs for you to choose the resolution of grids
    ax1.xaxis.set_minor_locator(HourLocator(range(0, 25, 4))) # range from 0 to 25 not including 25th hour, with every 4 hours as a minor x-axis grid line
    ax1.plot(x, y, linewidth=1, color = color)
    ax1.scatter(x, y)
    fig.tight_layout()
    plt.grid()
    plt.savefig(newfile+ ".png")
    print("Exit image to end program. ")
    plt.show()

###########################
"DOUBLE PARAMETER SELECTION"
###########################

def double():
    fname = input("Which datafile would you like to access?: ")
    data = np.loadtxt(fname+".csv")
    newfile = input ("Give this plot a filename!: ")
    contiORtime = input ("Continuous, full-day brackets or 24h-cycles? Enter (c/b/r): ")
    MHT1 = input("First data? PM2.5 / PM10 / humidity / temperature? Enter (f/t/h/w): ")
    MHT2 = input("Second data? PM2.5 / PM10 / humidity / temperature? Enter f/t/h/w: ")
    
    while MHT2 == MHT1:
        MHT1 = input("First data? PM2.5 / PM10 / humidity / temperature? Enter (f/t/h/w): ")
        MHT2 = input("Second data? PM2.5 / PM10 / humidity / temperature? Enter (f/t/h/w): ")
        
    if MHT1 in fiveChoice:
        colnum1 = 2
        yx1 = "PM2.5 ug/m^3"
        
    elif MHT1 in tenChoice:
        colnum1 = 3
        yx1 = "PM10 ug/m^3"
    
    elif MHT1 in HumidChoice:
        colnum1 = 5
        yx1 = "Relative Air Humidity (%)"
        
    elif MHT1 in warmChoice:
        colnum1 = 4
        yx1 = "Air Temperature (*C)"
    
    else:
        print("Input Error. ")
    
    if MHT2 in fiveChoice:
        colnum2 = 2
        yx2 = "PM2.5 ug/m^3"
        
    elif MHT2 in tenChoice:
        colnum2 = 3
        yx2 = "PM10 ug/m^3"
    
    elif MHT2 in HumidChoice:
        colnum2 = 5
        yx2 = "Relative Air Humidity (%)"
        
    elif MHT2 in warmChoice:
        colnum2 = 4
        yx2 = "Air Temperature (*C)"
    
    else:
        print("Input Error. ")
    
    if contiORtime in ContiChoice:
        Typename = "Continuous "
        
        x = []
        y = []
        z = []
        
        if np.shape(data) == (4,):
            x.append(data[1])
            y.append(data[colnum1])
            z.append(data[colnum2])
        else:
            for i in range(0,len(data)): 
                x.append(data[i,1]) 
                y.append(data[i,colnum1])
                z.append(data[i,colnum2])
    
    elif contiORtime in BracketChoice:
        Typename = "Bracket "
        Hday = input("Did the first day begin at midnight? (y/n): ")
        if Hday in noChoice:
            dayhours = int(input("How many hours were recorded in the first day?: "))
        elif Hday in yesChoice:
            dayhours = 0

        startdate = int(input("Plot from which day? Enter integer: "))
        lastday = input("Are you including the last day? (y/n): ")
        
        if lastday in yesChoice:
                        
            startrownum = int((startdate-1)*24-dayhours)
            
            x = []
            y = []
            z = []
            
            x.append(data[startrownum:,1])
            y.append(data[startrownum:,colnum1])
            z.append(data[startrownum:,colnum2])
            
        elif lastday in noChoice:
            enddate = int(input("Plot till end of which day? Enter integer: "))            
            startrownum = int((startdate-1)*24-dayhours)
            endrownum = int(enddate*24-dayhours)
            
            x = []
            y = []
            z = []
            
            x.append(data[startrownum:endrownum,1])
            y.append(data[startrownum:endrownum,colnum1])
            z.append(data[startrownum:endrownum,colnum2]) 
    
    elif contiORtime in TwofourChoice:
        Typename = "24h "
        lastday = input("Are you including the last day? (y/n): ")
        
        if lastday in yesChoice:
                        
            startrownum = int((startdate-1)*24)
            
            x = []
            y = []
            z = []
            
            x.append(data[startrownum:,1])
            y.append(data[startrownum:,colnum1])
            z.append(data[startrownum:,colnum2])
            
        elif lastday in noChoice:
            enddate = int(input("Plot till end of which day? Enter integer: "))            
            startrownum = int((startdate-1)*24)
            endrownum = int(enddate*24)
            
            x = []
            y = []
            z = []
            
            x.append(data[startrownum:endrownum,1])
            y.append(data[startrownum:endrownum,colnum1])
            z.append(data[startrownum:endrownum,colnum2])

    hfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
       
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.xaxis.set_major_formatter(hfmt)
    ax1.set_title(Typename + "time plot")
    ax1.set_xlabel('Time')
    ax1.set_ylabel(yx1, color = color)
    
    """Change the major and minor time locators below. This gives different x-axis grids and labelling"""
##    ax1.xaxis.set_major_locator(HourLocator())
    ax1.xaxis.set_major_locator(DayLocator()) # Other inputs for you to choose the resolution of grids
    ax1.xaxis.set_minor_locator(HourLocator(range(0, 25, 4))) # range from 0 to 25 hours not including 25th hour, with every 4 hours as a minor x-axis grid line
    
    ax1.plot(x, y, linewidth=1, color = color)
    ax1.scatter(x, y)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.xaxis.set_major_formatter(hfmt)
    ax2.set_ylabel(yx2, color=color)  # we already handled the x-label with ax1
    ax2.xaxis.set_major_locator(HourLocator())
    ax2.plot(x, z, linewidth=1, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
##    fig.tight_layout()
    plt.grid()
    plt.savefig(newfile+ ".png")
    print("Exit image to end program. ")
    plt.show()

###########################
"CALLING OF SCRIPT"
###########################
check()


    
    