# This file is the first working code which is able to extract the voice from the microphone and automatically save only the voice in a wave file.
# Running this code, it will recognise/save based on the timeouts for five times. read through and you shld be able to understand 

from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
from time import time as t
import time as time
import pyaudio
import wave
from pydub import AudioSegment

timeoutms = 1000 #a second
audiosavepath = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Speech Recognition\temp"
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
audiodata = []
audioWrite = True
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

initialMillis = getMillis()

def audio_callback(indata, frames, time, status):
    global audioWrite
    global initialMillis
    volume_norm = np.linalg.norm(indata) * 100
    
    if volume_norm > SPEECH_DETECTION_LEVEL: #speech detected
        audioWrite = True
        initialMillis = getMillis()
        print(volume_norm)
    
    if (getMillis() - initialMillis) > timeoutms:
        print("timeout triggered")
        initialMillis = getMillis() #reset back
        audioWrite = False
    # if audioWrite == True:
    #     audiodata.append(stream.read(FRAMES_PER_BUFFER))
duration = 5 #in seconds
stream = sd.InputStream(callback=audio_callback)

print("Stream Starting")
stream.start()

count = 0

while True:
    if audioWrite == True:
        audiodata.append(pstream.read(FRAMES_PER_BUFFER))
        
    else: 
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
        
        audioWrite = True
        audiodata = []
        
        if count >= 5: break