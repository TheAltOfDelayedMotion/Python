#Modules
import serial 
import time
import threading as th
import turtle

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

def serialUpdate():
    recieved = arduino.readline().decode("utf-8")
    if recieved != "":
        print(recieved, end = "")
    
    return recieved

def getInput():
    while True:
        writeinput = turtle.Screen()
        writeinput.setup(400, 500)
        print("Getting Input")
        datawrite = turtle.textinput("Python -> C++ Input", "Dataline")
        print(datawrite)
        if datawrite != "":
            write(datawrite)   
            
        print("Done")     

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

getInput_Thread = th.Thread(target=getInput)
getInput_Thread.daemon = True
getInput_Thread.start()
while __name__ == "__main__":
    serialUpdate()
    
