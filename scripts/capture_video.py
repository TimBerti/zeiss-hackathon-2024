import cv2

def capture_video():
    gst_str = ("nvarguscamerasrc ! "
               "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! "
               "nvvidconv flip-method=0 ! "
               "video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! "
               "videoconvert ! "
               "video/x-raw, format=(string)BGR ! appsink")

    cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
