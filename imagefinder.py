try:
    from camera import Camera
    import keras
except ImportError:
    pass

import cv2
import numpy as np


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
        
        self.model = keras.models.load_model('mymodel.h5')
        self.model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
        
        self.labels = ['11', '12', '3', '1', '14', '13', '10', '2', '15', '4', '5', '6',
       '9', '7', '8', 'default']
       
        
        

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
        image = self.camera.imageCapture()
        #im = cv2.imread(image)
        #im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        
        left = im[649:1296, :int(im.shape[1]/3)]
        middle = im[649:1296, int(im.shape[1]/3):int(im.shape[1]/3*2)]
        right = im[649:1296, int(im.shape[1]/3*2):]

        return [left,middle,right]

    def find(self,checktiles=[0,1,2]):
        """
        outputs results
        
        0 - left
        1 - middle
        2 - right
        """
        if self.fakeRun:
            return
        
        
        if not checktiles:
            return None
        
        images_list = self.processimage()
        for i in reversed(range(3)):        #process images right to left because new images are likely to be at right
            if i not in checktiles:
                continue
            results = self.predict(images_list[i])
            if results == 'default':
                continue
            else:
                output = [int(results), i]
                if settings.save_images:
                    import os
                    filepath = os.path.join("detected images", "{}.jpg".format(output))
                    
                    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(filepath, im)
                
                return output
                
        return None
