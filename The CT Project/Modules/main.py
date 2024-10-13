print("[PYTHON] CT-02 Starting... \n")

import cv2
import time
import dlib
import sys
import turtle
import serial #custom serial library is not needed (see class: serial)
import pygame
import pvporcupine
import threading as th
import lib_spotify as spotify
from pvrecorder import PvRecorder
from lib_stt import recognizer as SST
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

#Variables
state = "sleep"
speech = None
WAKEWORDPATH1 = r'C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\Datafiles\Hey-Cee-Tee_en_windows_v3_0_0.ppn'
WAKEWORDPATH2 = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\Datafiles\yo-cee-tee_en_windows_v3_0_0.ppn"
MIC_ID = 1

#Face Tracking
WIDTH = 1280
HEIGHT = 720
VISION_Y = 480
truecentre = WIDTH/2
vision_offset = 30
movement_pix_sens = 32
detector = dlib.get_frontal_face_detector()

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
        arduino.write(bytes((x+'\n'), 'utf-8'))
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
        writeinput = turtle.Screen()
        writeinput.setup(100, 100)
        
        while True:
            datawrite = turtle.textinput("Python -> C++ Input", "Dataline")
            print(f"[PYTHON] Command Recieved: {datawrite}")
            
            if datawrite == "wake":
                state = "sleep"
                print(f"[PYTHON] Starting Up CT-02...")
                pygame.init()
                display = pygame.display.set_mode((300, 300))
                Serial.write("00/sleep")
                
                writeinput.clear()
                writeinput.reset()
                writeinput.bye()
                break
                
            elif datawrite != "":
                Serial.write(datawrite)

#Functions
def wakeword():
    keyword_dictionary = {"1": ["Hey CT", WAKEWORDPATH1], 
                   "2": ["Yo CT", WAKEWORDPATH2]}
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
    recorder = PvRecorder(frame_length=porcupine.frame_length, device_index=MIC_ID)
    recorder.start()
    print('[AUDIO] Command Armed... ')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            
            if result >= 0:
                print(f'[PYTHON] Detected Keyword: {keyword_dictionary[str(result+1)][0]}')
                wakeEvent.set()
                
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
        #print("[EVENT] wakeEvent Detected")
        Serial.write("00/awake")
        wakeEvent.clear()
        SST.stopRecording.clear()
        state = "awake"
        
def deepsleep():
    global state
    getInput_Thread = th.Thread(target=Serial.deepSleepInput) #special input prompt such that if wake is passed, robot goes into sleep
    getInput_Thread.daemon = True
    
    if getInput_Thread.is_alive() == False and state == "deepsleep": #so that it doesnt keep starting this thread over and over again until the program closes (leaves deep sleep)
        print("[PYTHON] Deep Sleep threading started")
        getInput_Thread.run()

def listen():
    global speech
    print("[PYSST] Listening")
    SST.stopRecording.clear()
    speech_detected.clear()
    speech = SST.recognize()
    
    if speech != None:
        #print(f"[PYSST] {speech}")
        SST.stopRecording.clear()
        speech = speech.lower()
        speech_detected.set() 
        #to do: need to clear speech as a global variable and also clear Speech detected
    
    # else: #I genuinely don't know why i keep repeating it
    #     SST.stopRecording.clear()

def textToAction():
    global speech
    if speech != None:
        #print(f"[PYSST] {speech}")
        if speech.find("play") >= 0:
            spotify.play()
        
        elif speech.find("pause") >= 0:
            spotify.pause()
        
        speech = None

#Threading
serialUpdate_thread = th.Thread(target=Serial.serialUpdate)
serialUpdate_thread.daemon = True #when error surfaces or program exits serial stops updating
serialUpdate_thread.start()

wakeword_thread = th.Thread(target=wakeword)
wakeword_thread.daemon = True
wakeword_thread.start()
wakeEvent = th.Event() #if wakeword is called... 

speech_detected = th.Event()

#Main
def main():
    global speech
    global state
    
    #Clearing of the wakeword event if state is not sleep (change if needed later)
    if wakeEvent.is_set() == True and state != "sleep":
        wakeEvent.clear()
    
    if state == "idle":
        SST.stopRecording.clear()
        #print("[SST] RECOGNIZE")
        speech = SST.recognize()
        
        if speech != None:
            print(f"[PYSST] {speech}")
            SST.stopRecording.clear()
            
            speech = speech.lower()
            
            #i just want to do this for fun
            if speech.find("play") >= 0:
                spotify.play()
            
            elif speech.find("pause") >= 0:
                spotify.pause()
        else:
            SST.stopRecording.clear()
    
    if state == "awake":
        count = 0
        prev_frame_time = 0
        new_frame_time = 0
        prev_face_x = 0
        face_x = 0
        face_y = 0
        
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        
        #start recording (one thread)
        listening_thread = th.Thread(target=listen)
        listening_thread.daemon = True
        listening_thread.start()
        
        while state == "awake": #while loop for repeat
            #see if listening thread had detected speech
            if speech_detected.is_set() == True:
                speech_detected.clear()
                
                textToAction_thread = th.Thread(target=textToAction)
                textToAction_thread.daemon = True
                textToAction_thread.start()
                
            elif (listening_thread.is_alive() == False) and (speech_detected.is_set()) == False:
                listening_thread = th.Thread(target=listen)
                listening_thread.daemon = True
                listening_thread.start()
            
            ret, frame = vid.read()
            if not ret:
                break
            
            frame = frame[int((HEIGHT/2)-(VISION_Y/2)):int((HEIGHT/2)+(VISION_Y/2)), 0:WIDTH] #FULL WIDTH, HALF HEIGHT
            faces = detector(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            cv2.circle(frame, (int(WIDTH/2), int(VISION_Y/2)), 20, (0,0,0), 3)
            
            for face in faces:
                count += 1
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()
                
                centrex = (x1 + x2)/2
                centrey = (y1 + y2)/2
                #boxarea = (x2 - x1) * (y2 - y1)
                
                cv2.circle(frame, (int(round(centrex)), int(round(centrey))), 10, (0,0,255), 3)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                
                face_x = round(centrex)
                face_y = round(centrey)
        
            new_frame_time = time.time() 
            fps = 1/(new_frame_time-prev_frame_time)     
            if (new_frame_time-prev_frame_time) >= 0.1:
                prev_frame_time = new_frame_time 
                fps = int(fps) 
                
                if (face_x != 0) or (face_y != 0):
                    #print(f"FPS: {fps} | X{face_x} Y{face_y}")
                    if (abs(face_x - prev_face_x) > movement_pix_sens):
                        Serial.write(f"09/{face_x}")
                        print(f"\n[PYTHON] Sent: 09/{face_x} | FPS: {fps}")

                        prev_face_x = face_x
                        
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("Quitting...")
                vid.release() 
                cv2.destroyAllWindows() 
                time.sleep(0.5)
                state = "sleep"
                Serial.write("03/sw/98/10")
                Serial.write("00/sleep")
                break  
            
            face_x = 0
            face_y = 0
    
    elif state == "sleep":
        #print("SLEEP")
        sleep()
        
    elif state == "deepsleep":
        speech = None
        deepsleep()

pygame.init()
display = pygame.display.set_mode((300, 300))

print("\n[PYTHON] CT-02 Online")
while __name__ == "__main__":
    main()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            Serial.write("00/sleep")
            sys.exit()
         
        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("[PYTHON] ESC Forcing Deep Sleep...")
                Serial.write("00/deepsleep")
                state = "deepsleep"
       