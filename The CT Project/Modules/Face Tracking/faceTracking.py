print("[SETUP]")
import cv2
from time import sleep
import dlib
import time
import serialcomms as s
WIDTH = 1280
HEIGHT = 720
VISION_Y = 480
truecentre = WIDTH/2
vision_offset = 30
movement_pix_sens = 32
#Resize is 1280, 384
#Boundaries
#270 - 370
#190 - 290

vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
detector = dlib.get_frontal_face_detector()


prev_frame_time = 0
new_frame_time = 0
prev_face_x = 0
face_x = 0
face_y = 0

command = ""

s.write("00/awake")
# sleep(2)
print("[START]")

while True:
    s.serialUpdate()
    count = 0
    locations = []
    locationdata = []
    
    ret, frame = vid.read()
    if not ret:
        break
    
    frame = frame[int((HEIGHT/2)-(VISION_Y/2)):int((HEIGHT/2)+(VISION_Y/2)), 0:WIDTH] #FULL WIDTH, HALF HEIGHT
    faces = detector(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # Loop through list (if empty this will be skipped) and overlay green bboxes
    cv2.circle(frame, (int(WIDTH/2), int(VISION_Y/2)), 20, (0,0,0), 3)
    
    
    for face in faces:
        count += 1
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        
        centrex = (x1 + x2)/2
        centrey = (y1 + y2)/2
        boxarea = (x2 - x1) * (y2 - y1)
        #locations.append(x1, y1, x2, y2)
        
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
                s.write(f"09/{face_x}")
                print(f"\n[PYTHON] Sent: 09/{face_x} | FPS: {fps}")

                prev_face_x = face_x
                
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frames
    # if the `q` key was pressed, break from the loop

    if key == ord("q"):
        print("Quitting...")
        vid.release() 
        cv2.destroyAllWindows() 
        
        break  
    
    face_x = 0
    face_y = 0
    
