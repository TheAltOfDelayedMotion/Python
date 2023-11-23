#Modules
import serial 
import time
import threading as th

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

def write(x):
    print(x)
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

    while True:
        if returndata != "":
            returndata = arduino.readline() 
            print(returndata)

        else: 
            print("data finished")
            return False

def blink(y):
    print(y)


while True:
    #testtimer = th.Timer(0.3, write("01/blink"))
    #testtimer.start()

    data = input("Please enter data: ")
    if data == "exit":
        exit()

    write(data)
