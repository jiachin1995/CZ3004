from camera import Camera

import cv2
import numpy as np
import keras
from skimage import transform

import settings


class Imagefinder:
    camera = None
    model = None
    labels = None
    
    probability_threshold = 0.85         #only accept an image recognition result if its probability above this threshold
    
    
    def __init__(self):
        self.camera = Camera()
        
        self.model = keras.models.load_model('mymodel3.h5')
        self.model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
        
        self.labels = ['6', '9', 'default', '8', '7', '5', '4', '3', '2', '15', '14', '13',
       '12', '11', '10', '1']
       
        

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
        

    def find(self):
        """
        outputs results
        
        0 - left
        1 - middle
        2 - right
        """
        im = self.camera.imageCapture()
        
        left = im[160:320, :int(im.shape[1]/3)]
        middle = im[160:320, int(im.shape[1]/3):int(im.shape[1]/3*2)]
        right = im[160:320, int(im.shape[1]/3*2):]
        
        
        images_list = [left,middle,right]
        for i in reversed(range(3)):        #process images right to left because new images are likely to be at right
            results = self.predict(images_list[i])
            if results == 'default':
                continue
            else:
                location = i
                break
              
        print(results)
        print(location)
              
        left_bounding_box = [(50,200),(int(im.shape[1]/3-50), 280)]
        middle_bounding_box = [(int(im.shape[1]/3+50), 200),(int(im.shape[1]/3*2-50), 280)]
        right_bounding_box = [(int(im.shape[1]/3*2+50), 200),(int(im.shape[1]-50), 280)]
        
        boxes = [left_bounding_box,middle_bounding_box,right_bounding_box]
        cv2.rectangle(im,  boxes[location][0],  boxes[location][1],  (0, 20, 200),  10)
        
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
        cv2.imwrite('output.jpg', im)
        #cv2.imshow('Window', im)
        
