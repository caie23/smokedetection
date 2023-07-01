import cv2
import time
from smokedetection import detectsmoke

if __name__ == '__main__':
    vidcap = cv2.VideoCapture('testvideo.mp4') # add a video for testing in the directory and name it "testvideo.mp4"

    success, frame = vidcap.read()
    count = 0
    start_time = time.time()
    while success:
        success, frame = vidcap.read()
        if time.time()-start_time > 0.5: # capture every 0.5 sec
            framename = f"frame{count}.jpg"
            print(f"capture: {framename}")
            cv2.imwrite("framesin/"+framename, frame)
            # result = detectsmoke('v8best.onnx', framename)
            count += 1
            start_time = time.time()

    vidcap.release()
    cv2.destroyAllWindows()
    print(f"total frame count: {count}")
