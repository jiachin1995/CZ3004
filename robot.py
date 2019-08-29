from sensors import Sensors
from map import Map
from explorer import Explorer
from coordinator import Coordinator


class Robot:
    """
    Robot class. Represents the virtual robot.
         
    Attributes:
        pos: a 15x20 array. Contains None, 0 or 1 as values.
        orientation: Centre of 3x3 start area. Default = [1,1]
        map: Map object. Refer to Map.py
        sensors: Sensors object. Refer to sensors.py
        coordinator: Coordinator object. Refer to coordinator.py
    """
    pos = [1,1]
    orientation = 0
    map = Map()
    sensors = Sensors()
    coordinator = Coordinator()
    
    def __init__(self, **kwargs):  
        """ Constructor. Accepts attributes as kwargs.
            
        Args:
            pos: a 15x20 array. Contains None, 0 or 1 as values.
            orientation: Centre of 3x3 start area. Default = [1,1]
            map: Map object. Refer to Map.py
            sensors: Sensors object. Refer to sensors.py
            coordinator: Coordinator object. Refer to coordinator.py
        """    
        # kwargs is a dict of the keyword args passed to the function. Expected to contain robot attributes
        for key, value in kwargs:
            concat = "self."+key+" = " + value
            eval(concat)                    #Initialise attributes. Evaluate self.key = value
            
        #update map
        self.updatemap()
    
            
    def explore(self):        
        dora  = Explorer(self)
    
    def forward(self, steps = 1, updatemap=False):
        self.coordinator.forward(steps)
        newpos_dict = {
            0: [x, y+steps], 
            1: [x+steps,y],
            2: [x, y-steps],
            3: [x-steps,y]
        }
        if updatemap: self.updatemap()
        
  
    def setAttributes(self, **kwargs):
        # kwargs is a dict of the keyword args passed to the function. Expected to contain robot attributes
        for key, value in kwargs:
            concat = "self."+key+" = " + value
            eval(concat)                    #Set attributes. Evaluate self.key = value  
            
    def turnLeft(self, updatemap=False):
        self.coordinator.turnLeft()
        self.orientation = (self.orientation + 3) % 4
        if updatemap: self.updatemap()

    
    def turnRight(self, updatemap=False):
        self.coordinator.turnRight()
        self.orientation = (self.orientation + 1) % 4
        if updatemap: self.updatemap()
              
    def updatemap(self):
        #update robot's position as free space on map
        x,y = self.pos        
        freeTiles = [
            [x-1,y+1],[x,y+1],[x+1,y+1],
            [x-1,y],  [x,y],  [x+1,y],
            [x-1,y-1],[x,y-1],[x+1,y-1],
        ]
        valuelist = [0]*len(freeTiles)
   
   
        #update map with front sensors
        left, middle, right = sensors.getFront()
   
        #baseline refers to the left,middle & right (from the robot's perspective) tiles the robot is occupying. 
        #baseline_dict contains the tiles to search. For example, if facing right, search top, middle & bottom tiles
        baseline_dict = {
            0: [[x-1,y],[x,y],[x+1,y]],
            1: [[x,y+1],[x,y],[x,y-1]],
            2: [[x+1,y],[x,y],[x-1,y]],
            3: [[x,y-1],[x,y],[x,y+1]]
        }
        baseline = baseline_dict[robot.orientation]
        
        
        
        #update map with left sensors
        #update map with right sensors
        
        map.setTiles(freeTiles, valuelist)
     
    