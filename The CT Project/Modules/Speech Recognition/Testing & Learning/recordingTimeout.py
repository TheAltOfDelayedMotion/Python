import numpy as np
import sounddevice as sd
from time import time as t
import time as time

timeoutms = 1000 #a second

def getMillis():
    read = int(t()*1000)
    return read

initialMillis = getMillis()

def audio_callback(indata, frames, time, status):
    global initialMillis
    volume_norm = np.linalg.norm(indata) * 100
    
    if volume_norm > 65: #speech detected
        initialMillis = getMillis()
        print(volume_norm)
    
    if (getMillis() - initialMillis) > timeoutms:
        print("timeout triggered")
        initialMillis = getMillis() #reset back
        
duration = 5 #in seconds
stream = sd.InputStream(callback=audio_callback, device=1)
stream.start()

while True:
    pass
    
