from picamera import PiCamera
from picamera.array import PiRGBArray
import os
import cv2
import time
import numpy as np

class Camera:
    def __init__(self, image_d = 1):
        """
            Initializing all the variables required for the PiCamera module.

            Only importing up image here, then using rotation to save memory space.
        """
       
        self.camera = PiCamera()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.rawCapture = None
        self.camera.resolution = (640, 480)
        self.camera.vflip = True
        self.camera.framerate = 15
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))

        print("Picamera loaded")
        time.sleep(1)
                                                     

    def imageCapture(self):


        # Capturing an image
        image = self.camera.capture(self.rawCapture,format='rgb', use_video_port=True)
        frame = self.rawCapture.array

        if frame is None:
            raise Exception('no image taken here')

        print(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        print("after conversion")
        print(frame)
       
        self.rawCapture.truncate(0)
        
        return frame
