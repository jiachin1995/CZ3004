from sensors import Sensors
from map import Map
from explorer import Explorer
from coordinator import Coordinator

import settings

class Robot:
    """
    Robot class. Represents the virtual robot.
         
    Attributes:
        pos: a 15x20 array. Contains None, 0 or 1 as values.
        orientation: Centre of 3x3 start area. Default = [1,1]
        explore: if True, update map after every movement
        map: Map object. Refer to Map.py
        sensors: Sensors object. Refer to sensors.py
        coordinator: Coordinator object. Refer to coordinator.py
    """
    pos = [1,1]
    orientation = 0
    explore = True
    map = Map()
    sensors = Sensors()
    coordinator = Coordinator()
    
    def __init__(self, fakeRun= False, fakeMap=None, **kwargs):  
        """ Constructor. Accepts attributes as kwargs.
            
        Args:
            fakeRun: set True if running simulation. Remember to give fake map as input. I.e: fakeMap = fakemap
            fakeMap: set simulation map. If left empty, creates an empty arena.
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
            
        if fakeRun:
            from sensors_fake import Sensors
            self.sensors = Sensors(self, fakeMap)    #fake sensors for simulation
            
        #update map
        self.updatemap()
    
            
    def explore(self):        
        dora  = Explorer(self)
    
    def forward(self, steps = 1, updatemap=False):
        self.coordinator.forward(steps)
        
        x,y = self.pos
        newpos_dict = {
            0: "[x, y+steps]", 
            1: "[x+steps,y]",
            2: "[x, y-steps]",
            3: "[x-steps,y]"
        }
        self.pos = eval(
                newpos_dict[self.orientation]
            )
        
        if self.explore: self.updatemap()
        
        if settings.logging:
            print("Movement: Robot goes forward " +str(steps)+ " steps")
        
    def getBaseLine(self):
        """
        baseline refers to the left,middle & right (from the robot's perspective) tiles 
            immediately in front of robot and the 3x3 space the robot is occupying. 
        baseline_dict contains the tiles to search. For example, if facing right, search top, middle & bottom tiles
        """
        x,y =self.pos        
        baseline_dict = {
            0: "[[x-1,y+2],[x,y+2],[x+1,y+2]]",
            1: "[[x+2,y+1],[x+2,y],[x+2,y-1]]",
            2: "[[x+1,y-2],[x,y-2],[x-1,y-2]]",
            3: "[[x-2,y-1],[x-2,y],[x-2,y+1]]"
        }
        baseline_str = eval(
                baseline_dict[self.orientation]
            )
            
        return baseline_str
  
    def getBaseLineVert(self):
        """
        baseline_vert refers to baseline, but vertical. Refer to getBaseLine() above
        """
        x,y =self.pos    
        baseline_vert_dict = {
            0: "[[x-2,y+1],[x-2,y-1]]",
            1: "[[x+1,y+2],[x-1,y+2]]",
            2: "[[x+2,y-1],[x+2,y+1]]",
            3: "[[x-1,y-2],[x+1,y-2]]"
        }
        baseline_vert = eval(
                baseline_vert_dict[self.orientation]
            )
    
        return baseline_vert
        
    def getTileRange(self):
        """
        direction of tiles to search. if facing right, search range of tiles right of robot.
        """
    
        tileRange_dict = {
            0: "[x,y+1]",
            1: "[x+1,y]",
            2: "[x,y-1]",
            3: "[x-1,y]",
        }
        tileRange = tileRange_dict[self.orientation]
    
        return tileRange
        
    def getTileRangeVert(self):
        """
            Same as getTileRange() above, but search range of tiles to left of robot
        """
        tileRange_vert_dict = {
            0: "[x-1,y]",
            1: "[x,y+1]",
            2: "[x+1,y]",
            3: "[x,y-1]",
        }
        tileRange_vert = tileRange_vert_dict[self.orientation]    
    
        return tileRange_vert
  
    def setAttributes(self, **kwargs):
        # kwargs is a dict of the keyword args passed to the function. Expected to contain robot attributes
        for key, value in kwargs:
            concat = "self."+key+" = " + value
            eval(concat)                    #Set attributes. Evaluate self.key = value  
            
    def turnLeft(self, updatemap=False):
        self.coordinator.turnLeft()
        self.orientation = (self.orientation + 3) % 4

        if self.explore: self.updatemap()
        
        if settings.logging:
            print("Movement: Robot Turns Left")
    
    def turnRight(self, updatemap=False):
        self.coordinator.turnRight()
        self.orientation = (self.orientation + 1) % 4

        if self.explore: self.updatemap()
 
        if settings.logging:
            print("Movement: Robot Turns Right")
 
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
        front_terrain = self.sensors.getFront()
        
        baseline = self.getBaseLine()
        tileRange = self.getTileRange()
        
        for terr in front_terrain:              #for every column in front_terrain
            x,y = baseline.pop(0)
            for i in range(0, terr):            
                freeTiles.append([x,y])
                valuelist += [0]
                
                x,y = eval(tileRange)
                
            if terr < self.sensors.front_sensors_range - 1:
                freeTiles.append([x,y])
                valuelist += [1]                #obstacle detected. Add to map
            
        
        #update map with left sensors
        left_terrain = self.sensors.getLeft()
        
        baseline_vert = self.getBaseLineVert()
        tileRange_vert = self.getTileRangeVert()
        
        for terr in left_terrain:              #for every column in left_terrain
            x,y = baseline_vert.pop(0)
            for i in range(0, terr):            
                freeTiles.append([x,y])
                valuelist += [0]
                
                x,y = eval(tileRange_vert)
                
            if terr < self.sensors.front_sensors_range - 1:
                freeTiles.append([x,y])
                valuelist += [1]                #obstacle detected. Add to map
        
        #TODO-update map with right sensors
        
        if settings.logging:
            print("=======Robot updatemap()=======")
            print(freeTiles)
            print(valuelist)
        
        
        self.map.setTiles(freeTiles, valuelist)
     
    