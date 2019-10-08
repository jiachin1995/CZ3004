from coordinator import Coordinator
from explorer import Explorer
from imagefinder import Imagefinder
from map import Map
from pathfinder import Pathfinder
from sensors import Sensors



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
    imagefinder = None
    
    images = []
    camera_counter = 0
    sendimages = False
    android = None

    
    def __init__(self, arduino = None, fakeRun= False, fakeMap=None, android=None, stepsPerSec=1, **kwargs):  
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
            self.imagefinder = Imagefinder(fakeRun=True)
        elif arduino is None:
            raise Exception("Real run requires arduino to be present")
        else:
            from sensors import Sensors
            self.sensors = Sensors(self, arduino)
            self.coordinator.arduino = arduino
            self.imagefinder = Imagefinder()

        self.android = android
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
  
    def detectImage(self, reset_counter = False):
        if reset_counter:
            self.camera_counter = 0
        
        if self.isDetectImageCancelled():
            return
            
        #only check tiles that have obstacles
        checktiles = []
        baseline_vert = self.getBaseLineVert()
        for i in range(3):
            if self.map.getTile(baseline_vert[i]) == 1:
                checktiles.append(i)
        
        results = self.imagefinder.find(checktiles=checktiles)
        if results is None:
            return
        
        id, location = results
        
        pos = baseline_vert[location]
        for img in self.images:
            if pos == img[1]:
                print("WARNING. Found image {} at {} but position already has an image".format(id, pos))
                return
        
        print("images found")
        self.images.append([id, pos])
        self.sendimages = True
        
    def isDetectImageCancelled(self):
        """method to minimise image recognition calls"""
        #cancelled because settings is find no image
        if settings.findallimages == 0:
            return True
        
        #cancelled because all images found
        if len(self.images) == settings.images_threshold:
            return True
            
        #reduce camera usage by only taking once every 3 steps
        if self.camera_counter != 0:
            self.camera_counter = (self.camera_counter + 1) % 3
            return True
        else:
            self.camera_counter = (self.camera_counter + 1) % 3
        
        #if next to arena walls, cancel image recognition
        #format is [x,y,orientation]
        conditions = [          
            [1,-1, 0],
            [-1,18,1],
            [13,-1,2],
            [-1,1,3]
        ]
        
        for cond in conditions:
            x,y,orient = cond
            if (self.pos[0] == x or self.pos[1] == y) and self.orientation == orient:
                return True
        
        
        return False
  
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
    
    def forward(self, steps = 1, findImage=False):
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
        
        if findImage: self.detectImage()
        
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
        baseline = eval(
                baseline_dict[self.orientation]
            )
            
        return baseline
  
    def getBaseLineRange(self, length=1):
        baseline = self.getBaseLine()
        tileRange = self.getTileRange()
        results = []
        
        for tile in baseline:
            x,y = tile
            tiles = []
            for i in range(length):
                tiles.append([x,y])
                x,y = eval(tileRange)
            results.append(tiles)
            
        return results
                
            
  
    def getBaseLineVert(self, right=False):
        """
        baseline_vert refers to baseline, but vertical. Refer to getBaseLine() above.
        """
        x,y =self.pos  
        if right:
            baseline_vert_dict = {
                0: "[[x+2,y+1], [x+2,y], [x+2,y-1]]",
                1: "[[x+1,y-2], [x,y-2], [x-1,y-2]]",
                2: "[[x-2,y-1], [x-2,y], [x-2,y+1]]",
                3: "[[x-1,y+2], [x,y+2], [x+1,y+2]]"
            }

        else:
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
        
    def getBaseLineVertRange(self, length=1, exclude_mid = True, toRight=False):
        baseline_vert = self.getBaseLineVert(right=toRight)
        if exclude_mid: baseline_vert.pop(1)
        tileRange_vert = self.getTileRangeVert(toRight=toRight)
        results = []
        
        for tile in baseline_vert:
            x,y = tile
            tiles = []
            for i in range(length):
                tiles.append([x,y])
                x,y = eval(tileRange_vert)
            results.append(tiles)
            
        return results
        
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
        
    def getTileRangeVert(self, toRight=False):
        """
        Search range of tiles to left of robot. Refer to getTileRange() above.
        """
        if toRight:
            tileRange_vert_dict = {
                0: "[x+1,y]",
                1: "[x,y-1]",
                2: "[x-1,y]",
                3: "[x,y+1]",
            }
        else:
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
            
    def turnLeft(self, findImage=False):
        """
        Turns the robot left.
        """
        self.coordinator.turnLeft()
        self.orientation = (self.orientation + 3) % 4

        if self.explore: self.updatemap()
        
        if findImage: self.detectImage()
        
        if settings.logging:
            print("Movement: Robot Turns Left")
    
    def turnRight(self, findImage=False):
        """
        Turns the robot right.
        """
        if findImage: self.detectImage(reset_counter = True)         #called before and after movement
        
        self.coordinator.turnRight()
        self.orientation = (self.orientation + 1) % 4

        if self.explore: self.updatemap()
 
        if findImage: self.detectImage(reset_counter = True)            
 
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
        tiles_array = self.getBaseLineRange(length = self.sensors.front_sensors_range)
        
        for row in tiles_array:                     #for each row - left, middle, right
            terr = front_terrain.pop(0)
            for i in range(0, terr):            
                freeTiles.append(row[i])
                valuelist += [0]
                
            if terr < self.sensors.front_sensors_range:
                freeTiles.append(row[terr])
                valuelist += [1]                   #obstacle detected. Add to map
            
        
        #update map with left sensors
        left_terrain = self.sensors.getLeft()
        tiles_array = self.getBaseLineVertRange(length = self.sensors.left_sensors_range)
        
        for row in tiles_array:                     #for each row - front, back
            terr = left_terrain.pop(0)
            for i in range(0, terr):            
                freeTiles.append(row[i])
                valuelist += [0]
                
            if terr < self.sensors.left_sensors_range:
                freeTiles.append(row[terr])
                valuelist += [1]                   #obstacle detected. Add to map
        

        
        #update map with right sensors
        right_terrain = self.sensors.getRight()
        tiles_array = self.getBaseLineVertRange(
                length = self.sensors.right_sensors_range,
                exclude_mid=False,
                toRight=True
            )
        row = tiles_array.pop(self.sensors.right_sensors_position)
           
        terr = right_terrain.pop(0)
        if terr != -1:
            for i in range(0, terr):            
                freeTiles.append(
                row[i]
                )
                valuelist += [0]
                
            if terr < self.sensors.right_sensors_range:
                freeTiles.append(row[terr])
                valuelist += [1]                   #obstacle detected. Add to map
        
        self.map.setTiles(freeTiles, valuelist)
     
        if self.map.is_explored(): self.explore = False
            
