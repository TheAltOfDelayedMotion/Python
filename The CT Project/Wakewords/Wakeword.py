# REFERENCE FILE
# This file is not used as a module for CT-02. 
# Wakeword detection is already integrated into main.py

import pvporcupine
from pvrecorder import PvRecorder

def main():
    keyword_dictionary = {"1": ["Hey CT", r'C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\Datafiles\Hey-Cee-Tee_en_windows_v3_0_0.ppn'], 
                   "2": ["Yo CT", r'C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Wakewords\Datafiles\yo-cee-tee_en_windows_v3_0_0.ppn']}
    access_key = '5XYibmnYr83z6EscaHDRMx7ERgAnRBf1T71w007c+xADuXcb3PhsOg=='
    keyword_paths = []
    
    for i, device in enumerate(PvRecorder.get_available_devices()):
        print('Device %d: %s' % (i, device))
        #Device 0: Microphone (Realtek(R) Audio)
        
    for keyword in keyword_dictionary: 
        keyword_paths.append(keyword_dictionary[keyword][1])
        print(f'Keywords paths {keyword_paths}')
        
    
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=keyword_paths,
        sensitivities=[0.5, 0.5])

    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=0)
    recorder.start()

    print('Listening ... (press Ctrl+C to exit)')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            
            if result >= 0:
                print(f'[WAKE] Detected Keyword: {keyword_dictionary[str(result+1)][0]}')
                
    except KeyboardInterrupt:
        print('Stopping ...')
        
    finally:
        recorder.delete()
        porcupine.delete()

if __name__ == '__main__':
    main()