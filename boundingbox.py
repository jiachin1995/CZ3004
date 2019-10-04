from camera import Camera

import cv2
import numpy as np
import keras

import settings


class Imagefinder:
    camera = None
    model = None
    labels = None
    
    def __init__(self):
        self.camera = Camera()
        
        self.model = keras.models.load_model('mymodel.h5')
        self.model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
        
        self.labels = ['4', '9', '8', '11', '10', '13', '12', '6', '7', '5', '14', '15',
        'default', '2', '1', '3']
       
        

    def predict(self, img):
        np_image = np.array(img).astype('float32')/255
        np_image = transform.resize(np_image, (24, 32, 3))
        np_image = np.expand_dims(np_image, axis=0)

        results = self.model.predict(np_image)
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
        
        left = im[449:1096, :int(im.shape[1]/3)]
        middle = im[449:1096, int(im.shape[1]/3):int(im.shape[1]/3*2)]
        right = im[449:1096, int(im.shape[1]/3*2):]
        
        
        images_list = [left,middle,right]
        for i in reversed(range(3)):        #process images right to left because new images are likely to be at right
            results = self.predict(images_list[i])
            if results == 'default':
                continue
            else:
                location = i
                break
                
        left_bounding_box = [(550,100),(996, im.shape[1]/3-100)]
        middle_bounding_box = [(550,im.shape[1]/3+100)),(996, im.shape[1]/3*2-100))]
        right_bounding_box = [(550, im.shape[1]/3*2+100)),(99,6 im.shape[1]-100))]
        
        boxes = [left_bounding_box,middle_bounding_box,right_bounding_box]
        cv2.rectangle(im, boxes[location][0], boxes[location][1], (0, 20, 200), 10)
        
        cv2.imshow('Window', im)
        
        
