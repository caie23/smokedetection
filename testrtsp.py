import cv2

if __name__ == '__main__':
    print("start capturing")
    cap = cv2.VideoCapture("rtsp://zephyr.rtsp.stream/movie?streamKey=4695560b83ff1e810afbef52789613de")
    ret,frame = cap.read()
    print(ret)
    while ret:
        ret,frame = cap.read()
        cv2.imshow("frame",frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()
