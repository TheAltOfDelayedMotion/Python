import pvporcupine
from pvrecorder import PvRecorder
import serial 
import time
import threading as th
import turtle

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

#Variables
state = "sleep"

#Serial
class Serial:
    global state
    def serialUpdate():
        global state
        while True:
            recieved = str(arduino.readline().decode("utf-8"))
            #recieved = recieved.strip() #stripping data with \r\n characters (it doesnt work rn)
            dataToPython = recieved.split("=")
            if dataToPython[0] != recieved: #if data is indeed split and seperated (pos 0 will not be the same as recieved)
                #print(f'[PYDEBUG] {dataToPython}')
                if dataToPython[0] == "[STATE]":
                    state = dataToPython[1].strip() #when read, the end of the data is actually read as \r\n
                    print(f"[STATE] PYSTATE changed to: {state}")
                
            if recieved != "":
                print(recieved, end = "")
            
            #return recieved
        
    def write(x):
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)

    def getwriteInput():
        while True:
            writeinput = turtle.Screen()
            writeinput.setup(400, 500)
            print("[PYTHON] Getting Input")
            datawrite = turtle.textinput("Python -> C++ Input", "Dataline")
            print(datawrite)
            
            if datawrite != "":
                Serial.write(datawrite)   
                
            print("[PYTHON] Done")     
            
    def deepSleepInput():
        global state
        while True:
            writeinput = turtle.Screen()
            writeinput.setup(400, 500)
            
            datawrite = turtle.textinput("Python -> C++ Input", "Dataline")
            print("[PYTHON] Turtle Window awaiting input... ")
            
            if datawrite == "wake":
                state = "sleep"
                break
                
            elif datawrite != "":
                Serial.write(datawrite)

def wakeword():
    keyword_dictionary = {"1": ["Hey CT", r'C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\Hey-Cee-Tee_en_windows_v3_0_0.ppn'], 
                   "2": ["Yo CT", r'C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\yo-cee-tee_en_windows_v3_0_0.ppn']}
    access_key = '5XYibmnYr83z6EscaHDRMx7ERgAnRBf1T71w007c+xADuXcb3PhsOg=='
    keyword_paths = []
    
    # for i, device in enumerate(PvRecorder.get_available_devices()):
    #     print('Device %d: %s' % (i, device))
    #     #Device 0: Microphone (Realtek(R) Audio)
        
    for keyword in keyword_dictionary: 
        keyword_paths.append(keyword_dictionary[keyword][1])
        #print(f'Keywords paths {keyword_paths}')
        
    #creating the porcupine object
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=keyword_paths,
        sensitivities=[0.5, 0.5])

    #recording audio
    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=0)
    recorder.start()
    print('[AUDIO] Command Armed... ')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            
            if result >= 0:
                print(f'[WAKE] Detected Keyword: {keyword_dictionary[str(result+1)][0]}')

                wakeEvent.set()
                #print("[EVENT] wakeEvent True")
                #print(f"[PYDEBUG] EVENT {wakeEvent.is_set()}")
                
    except KeyboardInterrupt:
        print('[STATE] Forcing Deep Sleep...')
        
    finally:
        recorder.delete()
        porcupine.delete()
        print("[AUDIO] Audio Engine shutdown")

def sleep():
    global state
    #print(f"[PYDEBUG] EVENT {wakeEvent.is_set()}")
    if wakeEvent.is_set() == True:
        print("[EVENT] wakeEvent Detected")
        Serial.write("00/idle")
        wakeEvent.clear()
        state = "idle"
        
def deepsleep():
    global state
    getInput_Thread = th.Thread(target=Serial.deepSleepInput) #special input prompt such that if wake is passed, robot goes into sleep
    getInput_Thread.daemon = True
    
    if getInput_Thread.is_alive(): #so that it doesnt keep starting this thread over and over again until the program closes (leaves deep sleep)
        getInput_Thread.start()

#Threading
serialUpdate_thread = th.Thread(target=Serial.serialUpdate)
serialUpdate_thread.start()

serialUpdate_thread = th.Thread(target=wakeword)
serialUpdate_thread.daemon = True
serialUpdate_thread.start()

wakeEvent = th.Event() #if wakeword is called... 

def main():
    #Clearing of the wakeword event if state is not sleep (change if needed later)
    if wakeEvent.isSet() == True and state != "sleep":
        wakeEvent.clear()
    
    if state == "idle":
        #print("IDLE")
        pass
    
    elif state == "sleep":
        #print("SLEEP")
        sleep()
        
    elif state == "deepsleep":
        deepsleep()
    
while __name__ == "__main__":
    main()