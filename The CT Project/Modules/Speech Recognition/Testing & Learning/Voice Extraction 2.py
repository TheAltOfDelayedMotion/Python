from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
from time import time as t
import time as time
import pyaudio
import wave
from pydub import AudioSegment
import threading as th

#Speech to text ai
#model_size = "tiny.en"
#model = WhisperModel(model_size, device="cpu", compute_type="int8")
#segments, _= model.transcribe(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\audio.mp3", beam_size=5)

timeoutms = 1500 #THIS IS FOR TIMEOUT AFTER TEXT DETECTED
waitforspeechtimeout = 5000 #THIS IS FOR TIMEOUT IF SPEECH IS NOT DETECTED
audiosavepath = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Speech Recognition\temp"
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
audiodata = []
audioWrite = False
AUDIO_BOOST = 23
SPEECH_DETECTION_LEVEL = 8 #Well the original level i set it at was 10 uh it works in mysterious ways

pa = pyaudio.PyAudio()

pstream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

def getMillis():
    read = int(t()*1000)
    return read

def audio_callback(indata, frames, time, status):
    global audioWrite
    global initialMillis
    global waitforspeechtimeoutbool
    volume_norm = np.linalg.norm(indata) * 100
    
    if volume_norm > SPEECH_DETECTION_LEVEL: #speech detected
        audioWrite = True
        initialMillis = getMillis()
        print(volume_norm)
    
    if (getMillis() - initialMillis) > timeoutms and audioWrite == True: #this timeout only triggers if text has already been started saying
        print("timeout triggered")
        initialMillis = getMillis() #reset back
        audioWrite = False
        speechTimeout.set()
    
    elif (getMillis() - initialMillis > waitforspeechtimeout and audioWrite == False):
        print("No speech detected, quitting... ")
        waitTimeout.set()
        # stream.stop()
        # stream.close()
        
stream = sd.InputStream(callback=audio_callback)

print("Stream Starting")
#stream.start()

count = 0
    
initialMillis = getMillis()
speechTimeout = th.Event() #after speech waiting for more
waitTimeout = th.Event() #waiting for speech
    
while __name__ == "__main__":
    if input("Test Y/n") == "y":
        stream.start()
        initialMillis = getMillis()
        
        while True:
            if audioWrite == True:
                audiodata.append(pstream.read(FRAMES_PER_BUFFER))
                
            elif speechTimeout.is_set(): 
                count += 1
                path = audiosavepath + "\\" + f"speech_{count}.wav"
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
                
                break
            
            elif waitTimeout.is_set():
                break
            
        speechTimeout.clear()
        waitTimeout.clear()
        audioWrite = False
        stream.stop()