from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
from time import time as t
import time as time
import pyaudio
import wave
from pydub import AudioSegment
import threading as th

#Pre Definitions 
#Speech Detection Settings
timeoutms = 1500 #THIS IS FOR TIMEOUT AFTER TEXT DETECTED
waitforspeechtimeout = 5000 #THIS IS FOR TIMEOUT IF SPEECH IS NOT DETECTED
waitforstreamload = 500 #some buffer time to load the stream
AUDIO_BOOST = 23 #boosting cus my computer mic is too soft
SPEECH_DETECTION_LEVEL = 65 #Well the original level i set it at was 10 uh it works in mysterious ways

#PYAUDIO & OTHER SETTINGS
audiosavepath = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Speech Recognition\temp"
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

#Storage Variables
audiodata = []
audioWrite = True
volume_norm = 0.0

#Speech to text ai
model_size = "tiny.en"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

#Code
def getMillis(): #Returns Millis 
    read = int(t()*1000)
    return read

def audio_callback(indata, frames, time, status): #This is the function for detecting timeout
    global audioWrite
    global initialMillis
    global volume_norm
    volume_norm = np.linalg.norm(indata) * 100
    #print("[VOICE] LEVEL | %.3f" %volume_norm, end="\r")
    
    if volume_norm > SPEECH_DETECTION_LEVEL: #speech detected
        audioWrite = True
        initialMillis = getMillis()
        
    
    if (getMillis() - initialMillis) > timeoutms and audioWrite == True: #this timeout only triggers if text has already been started saying
        print("\n[VOICE] Phrase Finished!")
        initialMillis = getMillis() #reset back
        audioWrite = False
        speechTimeout.set()
    
    elif (getMillis() - initialMillis > waitforspeechtimeout and audioWrite == False):
        print("[VOICE] No speech detected")
        waitTimeout.set()
        # stream.stop()
        # stream.close()
        
        
#Streaming & PyAudio
pa = pyaudio.PyAudio()
pstream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)
stream = sd.InputStream(callback=audio_callback)

initialMillis = getMillis()
speechTimeout = th.Event() #after speech waiting for more
waitTimeout = th.Event() #waiting for speech

#stream is almost like a thread, and hence you need to start and stop it. 
def main():
    global initialMillis
    global audioWrite
    global audiodata
    global path
    
    if input("Test? (y/n): ") == "y":
        stream.start()
        
        initialMillis = getMillis()
        while (getMillis() - initialMillis) < waitforstreamload:
            pass
        
        print("[VOICE] Stream Started")
        
        while True:
            if audioWrite == True:
                audiodata.append(pstream.read(FRAMES_PER_BUFFER))
                
            elif speechTimeout.is_set(): 
                path = audiosavepath + "\\" + f"detectedspeech.wav" #in voice extraction tests we want to save them as different files for testing, but now we just want to find exactly when we spoke
                obj = wave.open(path, 'wb')
                obj.setnchannels(CHANNELS)
                obj.setsampwidth(pa.get_sample_size(FORMAT))
                obj.setframerate(RATE)
                obj.writeframes(b''.join(audiodata))
                obj.close()
                
                file = AudioSegment.from_wav(path)
                boostedfile = file + AUDIO_BOOST

                boostedfile.export(path, format="wav")
                
                audioWrite = False
                audiodata = []
                
                segments, _= model.transcribe(path, beam_size=5)
                
                for segment in segments:
                    print(f"[STT] Speech Detected: {segment.text}")
                
                break #have to remove this later


            elif waitTimeout.is_set():
                break
            
        speechTimeout.clear()
        waitTimeout.clear()
        audioWrite = False
        stream.stop()
        
while __name__ == "__main__":
    main()