from picamera import PiCamera

class Camera:
    def __init__(self):
        """
            Initializing all the variables required for the PiCamera module.

            Only importing up image here, then using rotation to save memory space.
        """
        self.camera = PiCamera()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.rawCapture = None
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(rs, rs))

    def imageCapture(self):

        # Capturing an image
        frame = self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        image = self.rawCapture.array
        
        return image
        