import picamera
import picamera.array
import cv2
import threading
import time
from copy import deepcopy

class faceDetection():
    def __init__(self):
        self.frameWidth = 320
        self.frameHeight = 240
        self.classifier = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.classifier)
        self.stopThread = False
        self.faces = None
        self.lock = threading.Lock()
        #start the thread controlling the camera
        try:
            t = threading.Thread(target=self.__detectFace__)
            t.start()
            time.sleep(2) #time to launch the camera
        except:
            print 'Error launching stepper thread'

    def stopDetection(self):
        self.stopThread = True

    def getFrameWidth(self):
        return self.frameWidth

    def getFrameHeight(self):
        return self.frameHeight

    def __detectFace__(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (self.frameWidth,self.frameHeight)
            with picamera.array.PiRGBArray(camera) as stream:
	        while not self.stopThread:
	            camera.capture(stream, 'bgr', use_video_port=True)
		    frame = stream.array
		    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		    faces = self.face_cascade.detectMultiScale(gray,1.3,1)

                    self.lock.acquire()
		    self.faces = faces
                    self.lock.release()

		    #for (x,y,w,h) in faces:
                    #    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),4)
		    #    print "face found"
		    stream.seek(0)
	            stream.truncate()

    def getDetectedFaces(self):
        self.lock.acquire()
        faces = deepcopy(self.faces)
        self.lock.release()
        return faces

if __name__ == '__main__':
    faceDetector = faceDetection()
    for i in range(10):
        print faceDetector.getDetectedFaces()
        time.sleep(1)
    faceDetector.stopDetection()