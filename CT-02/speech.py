import speech_recognition as sr
import time

r = sr.Recognizer()
    
def setup():
    print("[SETUP] Calibrating for Ambient Noise...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels

def listen():
    with sr.Microphone() as source:
        print("[EXECUTE] Listening.... ")
        audio = r.listen(source)
        
    try:
        print("[EXECUTE] Processing....")
        #speech = r.recognize_whisper(audio, language="english") #Whisper
        speech =  r.recognize_google(audio)
        return speech 
    
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Request error; {0}".format(e))

setup()
text = listen()
print(text)