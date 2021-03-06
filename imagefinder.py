try:
    from camera import Camera
    import keras
except ImportError:
    pass

import cv2
import numpy as np
from skimage import transform
import tensorflow as tf

import settings


class Imagefinder:
    camera = None
    model = None
    labels = None
    
    
    fakeRun = False
    
    probability_threshold = 0.85         #only accept an image recognition result if its probability above this threshold
    
    def __init__(self, fakeRun=False):
        if fakeRun:
            self.fakeRun = True
            return

        self.camera = Camera()
        

        self.model = keras.models.load_model('JCM_mdp22.h5')
        self.model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
              
        self.model._make_predict_function()
            
        
        
        self.labels = ['9', 'default', '8', '6', '7', '5', '4', '3', '2', '15', '14', '13', '12', '11', '10', '1']
       


    def predict(self, img):
        np_image = np.array(img).astype('float32')/255
        np_image = transform.resize(np_image, (24, 32, 3))
        np_image = np.expand_dims(np_image, axis=0)

        results = self.model.predict(np_image)

        index = np.argmax(results)
        id = self.labels[index]
        
        probability = results[0][index]
        if probability>self.probability_threshold:
            print("Image {} found. Probability is {}".format(id, probability))
            return id
        else:
            return 'default'


    def processimage(self):
        print('taking image')
        im = self.camera.imageCapture()
        #im = cv2.imread(image)
        #im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        print('processing')
        left = im[160:320, :int(im.shape[1]/3)]
        middle = im[160:320, int(im.shape[1]/3):int(im.shape[1]/3*2)]
        right = im[160:320, int(im.shape[1]/3*2):]

        return [right,middle,left]          #same order as baseline_vert

    def find(self,checktiles=[0,1,2]):
        """
        outputs results
        
        0 - right
        1 - middle
        2 - left
        """
        if self.fakeRun:
            return
        
        print(checktiles)
        
        if not checktiles:
            return None
        
        images_list = self.processimage()
        for i in checktiles:        #process images right to left because new images are likely to be at right
            results = self.predict(images_list[i])
            if results == 'default':
                continue
            if settings.skipwhiteimages and (results in ["1","9","13"]):
                print("Warning: White images found but setting to skip white images is true.")
                continue
            if results not in settings.imageslabels:
                print("Warning: Result is an image but not in images labels list")
                continue
                
            else:
                output = [int(results), i]
                if settings.save_images:
                    import os

                    #output = cv2.cvtColor(converted_output , cv2.COLORBGR2RGB)
                    filepath = os.path.join("detected images", "{}.jpg".format(str(output)))
                    
                    bgrimage = cv2.cvtColor(images_list[i], cv2.COLOR_RGB2BGR)
                    cv2.imwrite(filepath, bgrimage)

                    print("saving {}".format(filepath))
                
                return output
                
        return None
