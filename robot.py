from sensors import Sensors
from map import Map
from explorer import Explorer
from coordinator import Coordinator
from pathfinder import Pathfinder

import settings

class Robot:
    """
    Robot class. Represents the virtual robot.
         
    Orientation refers to where the robot is facing:
        0. Top
        1. Right
        2. Bottom
        3. Left
 
         
    Attributes:
        pos: a 15x20 array. Contains None, 0 or 1 as values.
        orientation: Centre of 3x3 start area. Default = [1,1]
        explore: if True, update map after every movement. Explorer sets this to False after finishing exploration.
        map: Map object. Refer to Map.py
        sensors: Sensors object. Refer to sensors.py
        coordinator: Coordinator object. Refer to coordinator.py
        pathfinder: Pathfinder object. Refer to pathfinder.py
        explorer: Explorer Object. Refer to explorer.py
    """
    pos = [1,1]
    orientation = 0
    explore = True
    map = Map()
    sensors = None
    coordinator = Coordinator()
    pathfinder = None
    explorer = None

    
    def __init__(self, arduino = None, fakeRun= False, fakeMap=None, stepsPerSec=1, **kwargs):  
        """ 
        Constructor. Accepts attributes as kwargs.
            
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
            self.coordinator.fakeRun = True
            self.coordinator.stepsPerSec = stepsPerSec
        elif arduino is None:
            raise Exception("Real run requires arduino to be present")
        else:
            self.sensors = Sensors(arduino)
            self.coordinator.arduino = arduino
            
        #update map
        self.updatemap()
        
        #initialise pathfinder
        self.pathfinder = Pathfinder(self.map)
    
        #initialise explorer
        self.explorer = Explorer(self)

    def backward(self):
        """ 
        Moves the robot backward.
        """  
        self.coordinator.backward()
        
        x,y = self.pos
        newpos_dict = {
            0: "[x, y-1]", 
            1: "[x-1,y]",
            2: "[x, y+1]",
            3: "[x+1,y]"
        }
        self.pos = eval(
                newpos_dict[self.orientation]
            )
        
        if self.explore: self.updatemap()
        
        if settings.logging:
            print("Movement: Robot goes backward")


        
    def explore(self, timer = None, exploreLimit = None): 
        """ 
        Starts exploration.
        
        Args:
            timer: Integer. Time in seconds. Total time for robot to explore. Includes time to return
            exploreLimit: Float. Between 0.0 to 1.0. Percentage of map to explore before exploration is declared done.
        """      
        self.explorer.setTime(timer)
        self.explorer.setExploreLimit(exploreLimit)
        
        self.explorer.start()

    def faceDirection(self, orient):
        """
        Turns the robot to face the given direction.
        
        Args:
            orient: Integer. Direction for robot to face.
        """
        if orient == self.orientation:
            return
        elif orient == (self.orientation + 1) % 4:
            self.turnRight()
        elif orient == (self.orientation + 3) % 4:
            self.turnLeft()
        else:
            self.turnRight()
            self.turnRight()
  
    def findpath(self, start=None, goal=[13,18], waypoint=None, move=True, rowgoal=None):
        """
        Method for robot to find shortest path.
        
        Args:
            start: [x,y] coordinates. Defaults to current robot position.
            goal:  [x,y] coordinates. Defaults to [13,18].
            waypoint:  [x,y] coordinates. Defaults to None.
            move: Boolean. Defaults True. If True, moves robot after finding shortest path.
            rowgoal: Integer. y-axis. Defaults None. Ends findpath() early if y-axis is reached.
        """
        if start is None:
            start = self.pos
            orientation = self.orientation
        path,directions = self.pathfinder.findpath(start, goal, waypoint, orientation)
        
        if move:
            instructions = self.readDirections(directions)
            
            for i in instructions:
                if rowgoal and self.pos[1] == rowgoal: break
                exec(i)
            
        if settings.logging:
            print("Movement: findpath() to " + str(goal)+ " with rowgoal " + str(rowgoal))
            
            
        return [path, directions]
    
    def forward(self, steps = 1):
        """ 
        Moves the robot forward.
        
        Args:
            steps: Integer. Defaults to 1. Number of steps forward to take
        """  
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
        Baseline refers to the left,middle & right (from the robot's perspective) tiles 
        immediately in front of robot and the 3x3 space the robot is occupying. 
        
        Returns a string compatible for eval(). Expects [x,y] to be declared beforehand.
        
        Example string:
        "[[x-1,y+2],[x,y+2],[x+1,y+2]]"
        
        Example usage:
        x,y = self.pos
        baseline = getBaseLine()
        tilelist = eval(baseline)
        
        """
        #baseline_dict contains the tiles to search. For example, if facing right, search top, middle & bottom tiles
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
        baseline_vert refers to baseline, but vertical. Refer to getBaseLine() above.
        """
        x,y =self.pos    
        baseline_vert_dict = {
            0: "[[x-2,y+1], [x-2,y], [x-2,y-1]]",
            1: "[[x+1,y+2], [x,y+2], [x-1,y+2]]",
            2: "[[x+2,y-1], [x+2,y], [x+2,y+1]]",
            3: "[[x-1,y-2], [x,y-2], [x+1,y-2]]"
        }
        baseline_vert = eval(
                baseline_vert_dict[self.orientation]
            )
    
        return baseline_vert
        
    def getTileRange(self):
        """
        Range of tiles to search. If facing right, search range of tiles right of robot.
        
        Returns a string compatible for eval(). Expects [x,y] to be declared beforehand.
        
        Example string:
        "[x,y+1]"
        
        Example usage:
        x,y = self.pos
        tilerange=getTileRange
        
        for i in range(0,5):
            nextTile = eval(tilerange)
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
        Search range of tiles to left of robot. Refer to getTileRange() above.
        """
        tileRange_vert_dict = {
            0: "[x-1,y]",
            1: "[x,y+1]",
            2: "[x+1,y]",
            3: "[x,y-1]",
        }
        tileRange_vert = tileRange_vert_dict[self.orientation]    
    
        return tileRange_vert
  
    def isLeftBlocked(self):
        """
        Checks whether left side is blocked by reading map.
        """
        x,y = self.pos
        
        tiles = self.getBaseLineVert()
        
        for pos in tiles:
            if self.map.getTile(pos) == 1:
                return True
        
        return False
  
    def readDirections(self, directions):
        """
        Reads a list of directions and converts it into instructions like forward, turn left, etc.
        
        Args:
            directions: list of directions/integers. 
        """
        prev = self.orientation
        steps = 0
        
        instructions=[]
        
        for d in directions:
            if d == prev:
                steps += 1
                prev = d
            elif d == (prev+1) % 4:     #turn right
                if steps >0:
                    instructions.append("self.forward("+ str(steps) +")")
                instructions.append("self.turnRight()")
                instructions.append("self.forward()")
                
                steps=0
                
            elif d == (prev+2) % 4:     #U-turn
                if steps >0:
                    instructions.append("self.forward("+ str(steps) +")")
                instructions.append("self.turnRight()")
                instructions.append("self.turnRight()")
                instructions.append("self.forward()")
                
                steps=0
            else:                       #turn right
                if steps >0:
                    instructions.append("self.forward("+ str(steps) +")")
                instructions.append("self.turnLeft()")
                instructions.append("self.forward()")
                
                steps=0
            prev = d
            
                
        if steps >0:
            instructions.append("self.forward("+ str(steps) +")")     
        
        if settings.logging:
            print("=======Read Instructions Output========")
            print(instructions)
                     
        return instructions
        
  
    def setAttributes(self, **kwargs):
        """
        Set class attributes. Accepts kwargs of robot attributes.
        """
        for key, value in kwargs:
            concat = "self."+key+" = " + value
            eval(concat)                    #Set attributes. Evaluate self.key = value  
            
    def turnLeft(self):
        """
        Turns the robot left.
        """
        self.coordinator.turnLeft()
        self.orientation = (self.orientation + 3) % 4

        if self.explore: self.updatemap()
        
        if settings.logging:
            print("Movement: Robot Turns Left")
    
    def turnRight(self):
        """
        Turns the robot right.
        """
        self.coordinator.turnRight()
        self.orientation = (self.orientation + 1) % 4

        if self.explore: self.updatemap()
 
        if settings.logging:
            print("Movement: Robot Turns Right")
 
    def updatemap(self):
        """
        Updates map by reading sensors.
        """
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
        baseline_vert.pop(1)
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
        
        
        self.map.setTiles(freeTiles, valuelist)
     
        if self.map.is_explored(): self.explore = False
            
