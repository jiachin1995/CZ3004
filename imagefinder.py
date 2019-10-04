from camera import Camera

import numpy as np
import tensorflow as tf

import settings


class Imagefinder:
    camera = None
    model = None
    labels = None
    
    def __init__(self):
        self.camera = Camera()
        
        self.model = tf.keras.models.load_model('mymodel.h5')
        self.model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
        
        self.labels = ['4', '9', '8', '11', '10', '13', '12', '6', '7', '5', '14', '15',
        'default', '2', '1', '3']
       
        

    def predict(self, img):
        results = model.predict(img)
        id = self.labels[np.argmax(results)]
        
        return id

    def find(self):
        """
        outputs results
        
        0 - left
        1 - middle
        2 - right
        """
        image = self.camera.imageCapture()
        im = cv2.imread(image)
        
        left = im[649:1296, :int(im.shape[1]/3)]
        middle = im[649:1296, int(im.shape[1]/3):int(im.shape[1]/3*2)]
        right = im[649:1296, int(im.shape[1]/3*2):]
        
        
        images_list = [left,middle,right]
        for i in reversed(range(3)):        #process images right to left because new images are likely to be at right
            results = self.predict(images_list[i])
            if results == 'default':
                continue
            else:
                return [int(results), i]
                
        return None

