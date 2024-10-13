# Usage notes for Timer

# startTimer()
# Arguements:
# 1. <time> (List) 
# ["10H", "20M", "0S", "2000MS"]
# ["30S"]
# ["20M"]
# ["3500MS"] Milliseconds
# ["1H", "30S"]

# checkTimerStatus()
# No Arguements!
# bool = checkTimerStatus()
# if the timer is finished, bool = True, else, False.

#This is a really old version, i plan to change it by using threading events and the Millis library, its simply more accurate, rather than starting a whole damn thing

import threading as th
logfilePATH = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\CT-02\timerlog.txt"

#Global Variables
status = False #Timer Status
start_time = 0 
elapsed_time = 0
time_left = 0

#Changes the status of the Timer to completed 
def handling():
    global status
    status = True #Status = Completed
    writeLog(["Complete"])

#Updates the Log every second
def updateLog():
    #Editing Global Variables
    global elapsed_time
    global time_left
    global status
    
    if status == False:
        updatethread = th.Timer(1, updateLog) #Start a thread every second to update the log
        updatethread.start()
    
        writeLog(["Pending", "\n", str(elapsed_time), "\n", str(time_left)]) #Writes as ["Pending", "<elapsed time>", "<time left>"]
        elapsed_time += 1
        time_left -= 1
    
#Main Function
def startTimer(rawtime):
    global start_time
    global time_left
    
    time = intoSeconds(rawtime) #Converting H, M, S into Seconds only

    timerthread = th.Timer(time, handling)
    timerthread.start()

    #Logging
    print("[EXECUTE] Timer Started")
    time_left = time
    updateLog()
    
def writeLog(lines):
    with open(logfilePATH, "w") as logfile:
        logfile.seek(0)
        logfile.writelines(lines)
        logfile.close()

def readLog():        
    with open(logfilePATH, "r") as logfile:     
        try:
            data = logfile.readlines()
            index = 0
            
            for datas in data:
                #print(f"Original String: {datas}")
                if ("\n" in datas):
                    datas = datas.replace("\n", "")
                    #print(f"Modified String: {datas}")
                    data[index] = datas
                index += 1
                
            logfile.close()
            #print(data)
            
        except IndexError:
            print("[ERROR] IndexError!")
    
    return data

def checkTimerStatus():
    timerfinished = False
    data = readLog()
    
    for datas in data:
        if (datas == "Complete"):
            timerfinished = True
        
    return timerfinished

def intoSeconds(input):
    timeinhours = 0
    timeinminutes = 0
    timeinseconds = 0    
    timeinmilliseconds = 0
    
    for inputs in input:
        if (("M" in inputs) and ("S" in inputs)): 
            inputs = inputs.replace("MS", "")
            timeinmilliseconds += int(inputs)/1000
            
        if "H" in inputs:
            inputs = inputs.replace("H", "")
            timeinhours += int(inputs) * 60 * 60
            
        if "M" in inputs:
            inputs = inputs.replace("M", "")
            timeinminutes += int(inputs) * 60
            
        if "S" in inputs:
            inputs = inputs.replace("S", "")
            timeinseconds += int(inputs) 

    print(f"{timeinhours}S + {timeinminutes}S + {timeinseconds}S + {timeinmilliseconds}S")
    output = timeinhours + timeinminutes + timeinseconds + timeinmilliseconds
    return output
    
def mainTest():
    tf = True
    timertime = ["0H", "0M", "10S","3000MS"]
    startTimer(timertime)
    
    while tf:
        status = checkTimerStatus()
        if status == True:
            tf = False
            print("[EXECUTE] Timer Completed")
            
mainTest()