from sensors import Sensors
from map import Map
from explorer import Explorer
from coordinator import Coordinator

class Robot:
    pos = [1,1]
    orientation = 0
    map = Map()
    sensors = Sensors()
    coordinator = Coordinator
    
    def __init__(self, **kwargs):      
        # kwargs is a dict of the keyword args passed to the function. Expected to contain robot attributes
        for key, value in kwargs:
            concat = "self."+key+" = " + value
            eval(concat)                    #Initialise attributes. Evaluate self.key = value
            
    def explore(self):        
        dora  = Explorer(self)
    
    
    def setAttributes(self, **kwargs):
        # kwargs is a dict of the keyword args passed to the function. Expected to contain robot attributes
        for key, value in kwargs:
            concat = "self."+key+" = " + value
            eval(concat)                    #Set attributes. Evaluate self.key = value  
            
    
                 
    