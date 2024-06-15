from time import time as t
import time as time
import pyaudio
import wave
from pydub import AudioSegment

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

recordingtime = 5000 #5s
audiodata = []

pa = pyaudio.PyAudio()

stream = pa.open(
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

while (getMillis() - initialMillis < recordingtime):
    audiodata.append(stream.read(FRAMES_PER_BUFFER))
    
stream.stop_stream()
stream.close()
pa.terminate()

obj = wave.open('lemaster_tech.wav', 'wb')
obj.setnchannels(CHANNELS)
obj.setsampwidth(pa.get_sample_size(FORMAT))
obj.setframerate(RATE)
print(audiodata)
obj.writeframes(b''.join(audiodata))
obj.close()

file = AudioSegment.from_wav(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\lemaster_tech.wav")
boostedfile = file + 25

boostedfile.export("save.wav", format="wav")