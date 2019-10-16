from islandsfinder import Islandsfinder

import time

import settings

class Explorer:
    """
        Explorer class. Used during exploration
        
            
        Attributes:
            robot: An instance of the Robot Object. Expects a robot object during initialisation
            state: String. Shows current exploration state. Possible states are:
                "Initial" - initial state when explorer is just created.
                "LeftWallHugging" - Robot is performing left wall hugging algorithm
                "Spelunking" - Robot traverses to unexplored tiles in centre of map
                "Out of time" - Out of time. Robot returns to starting position.
                "Exploration done" - Exploration done. Robot returns to starting position.
            startTime: Time object. Time when exploration started. If exploration has not started, returns None.
            timer: Integer. Defaults 500. Total time allowed for exploration in seconds. Includes timeToReturn. Thus, timer must be more than timeToReturn.
            timeToReturn: Integer. Defaults to 60. Time given to robot to return to start. Occupies timer. Thus, timer must be more than timeToReturn.
            exploreLimit: Float. Defaults to 1.0. Percentage of map to explore. Cancels exploration if percentage reached.
            
    """
    robot = None
    state = "Initial"

    startTime = None
    timer = 360
    timeToReturn = 60       #buffer time to return to start, in seconds
    exploreLimit = 1.0

    prevUnexploredTile = None           #used to escape from spelunking to same unexplored tile recursion
    prevMoveLeftTurn = False            #used to escape from left turn recursion

    def __init__(self, robot):
        """
        Constructor. Expects a robot argument
        
        Args:
            robot: Robot Object. 
            timer: Integer. Total time in seconds for robot to complete exploration.
            exploreLimit: Float. Percentage of map to explore before returning to start
        """
        self.robot = robot
        if settings.logging:  
            print("====== Starting Explorer =======")
            print("New State: " + self.state)
    
    
    def start(self):
        """
        Call this method to begin exploration
        """
        self.startTime = time.time()
    
        if self.state == "Initial": 
            self.hugleftwall()
    
        if settings.logging:
            self.robot.map.printmap()
            print(self.robot.map.convert())
    
        while not self.exploreDone():
            if settings.giveupspelunk:
                break
            if self.noTimeLeft():
                break
            self.spelunk()
        
        if settings.findallimages == 2:
            finder = Islandsfinder(self.robot.map)
            iterator = finder.nextIsland()
                
            while len(self.robot.images) < settings.images_threshold:
                if self.noTimeLeft():
                    break
                
                results = next(iterator, None)      #results contain pos & orient. Or None
                if results is None:
                    print("All islands searched. Stopping exploration")
                    break
                
                pos, orient = results
                self.robot.findpath(goal=pos)
                self.robot.faceDirection(orient)
                
                endCondition = "len(self.robot.images) >= settings.images_threshold" 
                self.hugleftwall(endCondition=endCondition, checkexplore=False)
                
        
        if self.noTimeLeft():
            self.state = "Out of time"
        else:
            self.state = "Exploration done"
           
        if settings.logging:
            print(self.state)
            print("Returning to start")
            print("Remaining Time left: " + str(self.getRemainingTime()))
            print(self.robot.pos)
            print(self.robot.orientation)

        self.robot.findpath(goal=[1,1])
        self.robot.faceDirection(0)
       
        
    def hugleftwall(self, startorient = None, startpos = None, endCondition=None, checkexplore=True):
        """
        Recursive function. Ends when robot is back to initial starting position and orientation.
        Also accepts a different end condition as argument.
        
        Args:
            startorient: Integer. Do not provide an argument. Starting orientation of robot when function was first called. 
            startpos: [x,y] coordinates. Do not provide an argument. Starting pos of robot when function was first called. 
            endCondition: String. Expects a boolean string. Calls eval() on string to determine True/False. If True, end function.
        """
        #return if out of time
        if self.noTimeLeft():
            return
            
        #return if explore limit reached:
        if checkexplore and self.exploreDone():
            return
    
        #run once when first called
        if startpos == None:
            if self.hugleftprep():
                startorient = self.robot.orientation
                startpos = self.robot.pos
            else: return             #prep failed. Cancel left wall hugging
        
        #if left is free, turn left, move forward once
        if not self.robot.sensors.isLeftBlocked() and not self.robot.isLeftBlocked():
            if self.prevMoveLeftTurn:
                print("Warning: Infinite Loop detected. Attempting to recover.")
                self.robot.turnRight()
                
                self.prevMoveLeftTurn = False
              
            else:
                self.robot.turnLeft()                #no need to update map cause next step will update instead.
                self.robot.forward(findImage=True)   #in theory, there should be at least one row of free space. 
                
                self.prevMoveLeftTurn = True
            
        #elif if front is free, move forward (up to 3)
        elif not self.robot.sensors.isFrontBlocked():
            self.robot.forward(findImage=True)
        
            self.prevMoveLeftTurn = False
        
            """Unused as it causes exploration to occasionally skip detection of certain walls on left."""
            # front,back = self.robot.sensors.getLeft()
            # if front != 0: 
                # steps = 1        #we go 1 step at a time to find where left wall ends
            # else:
                # front_terrain = self.robot.sensors.getFront()
                # steps = min(front_terrain)      #go as far as possible
                # if steps>3: steps = 3           #we do this as we have to check & hug left wall every 3 steps
            
                # #check next tiles whether terminate condition is in next few tiles
                # if steps>1:
                    # result = self._hugleftcheckstepstoterminate(turns, startpos, endCondition=endCondition)
                    # if result:
                        # steps = result
            
            # self.robot.forward(steps)

        #if both failed, turn right
        else:
            self.robot.turnRight(findImage=True)
            
            self.prevMoveLeftTurn = False
 
        #check terminate or continue. 
        x,y = self.robot.pos
        if endCondition and eval(endCondition):
            return
        elif startorient == self.robot.orientation and [x,y] == startpos: 
            return
        else: 
            self.hugleftwall(startorient = startorient, startpos = startpos, endCondition=endCondition)
        
    def hugleftprep(self):
        """ 
        Prepares robot for left wall hugging algorithm. 
        Expects an adjacent wall before starting.
            
        Raises:
            Warning: Left Wall Hugging Cancelled. No adjacent walls found.
        """
        self.prevMoveLeftTurn = False
    
    
        self.state = "LeftWallHugging"
        if settings.logging:  
              print("New State: " + self.state)   
            
        #if left wall exists, return true
        if self.robot.sensors.isLeftBlocked():
            return True
        #elif front wall exists, turn right and return true
        elif self.robot.sensors.isFrontBlocked():    
            #Check for T-blocks, move forward by 1 so that left-back sensor can detect wall
            left, middle, right = self.robot.sensors.getFront()
            if middle==0 and left != 0 and right !=0:
                self.robot.turnRight()
                self.robot.forward()
            else: self.robot.turnRight()
        
            return True
        else:
            if settings.logging:  
                print("Warning: Left Wall Hugging Cancelled. No adjacent walls found.")
            return False

    def _hugleftcheckstepstoterminate(self, startorient, startpos, endCondition=None):
        """
        Before moving forward multiple tiles in hugleftwall(), check next few tiles are not in end condition.
        If in end condition, return distance of tile to move.
        
        Args:
            startorient: Integer. Do not provide an argument. Starting orientation of robot when hugleftwall() was first called. 
            startpos: [x,y] coordinates. Do not provide an argument. Starting pos of robot when hugleftwall() was first called. 
            endCondition: String. Expects a boolean string. Calls eval() on string to determine True/False. 
        """
        x,y = self.robot.pos
        tileRange = self.robot.getTileRange()
        
        
        """if [x,y] in terminate: return distance"""
        for i in range(1,3):
            x,y = eval(tileRange)

            if endCondition and eval(endCondition):
                return i
            if startorient == self.robot.orientation and [x,y] == startpos: 
                return i
            
        return None
       
    def getRemainingTime(self):
        """
        Returns time object showing remaining exploration time left.
        """
        now = time.time()
        return (self.startTime+ self.timer) - now
       
    def noTimeLeft(self):
        """
        Returns True if out of time. Includes time to return in calculations.
        """
        now = time.time()
        if now > (self.startTime + self.timer - self.timeToReturn):
            return True
        else:
            return False
       
    def setTime(self, timer):
        """
        Sets self.timer
        
        Args:
            timer: Integer. Time for exploration in seconds.
        """
        if timer is None:
            return
        
        if timer < self.timeToReturn:
            raise Exception("Time given less than return time. Give more time for exploration")
        
        self.timer = timer        

    def exploreDone(self):
        """
        Return True if exploration done or exploration > exploreLimit.
        """
        if self.robot.map.explored_percent() >= self.exploreLimit:
            return True
        else:
            return False
       
    def setExploreLimit(self, exploreLimit):
        """
        sets self.exploreLimit
        
        Args:
            exploreLimit: Float. Percentage of map to explore
        """
        if exploreLimit is None:
            return
            
        if exploreLimit < 0.0 or exploreLimit > 1.0:
            raise Exception("Explore Limit out of range. Please input between 0.0 and 1.0")
        
        self.exploreLimit = exploreLimit
       
    def spelunk(self):
        """
        Algorithm for robot to explore unexplored tiles in centre of arena.
        """
        self.state = "Spelunking"
        if settings.logging:  
              print("New State: " + self.state) 

        self.spelunkprep()        
        self._spelunking()
    
    def _spelunking(self):
        """
        After calling spelunkprep, moves robot forward to explore y-axis. If obstacle is found, sets the robot to perform left wall hug.
        """
        if not self.robot.sensors.isFrontBlocked():
            front_terrain = self.robot.sensors.getFront()
            steps = min(front_terrain)      #go as far as possible
            
            self.robot.forward(steps)
            
        else:
            endCondition = "y == " + str(self.robot.pos[1]) + " and not [x,y] == " + str(self.robot.pos)
            self.hugleftwall(endCondition=endCondition) #terminate condition: same row & not startpos


    def spelunkprep(self):
        """
        Part of spelunking algorithm. Prepares the robot for spelunking.
        
        Finds unexplore Tile and moves robot to the same y-axis as Tile. Sets the robot to face unexplored tile.
        """
        x,y = self.robot.map.getUnexploredTile()
        
        if settings.logging:
            print("UNEXPLORED TILE")
            print([x,y])
            
        #escape function
        if [x,y] == self.prevUnexploredTile:
            goal, dir = self.robot.map.findAdjacentFreeSpace([x,y])
            
            self.robot.findpath(goal=goal)
            self.robot.faceDirection(dir)
            return
            
        self.prevUnexploredTile = [x,y]
            
        if self.robot.pos[1] != y:
            #move to unexplored Tile's y-axis
            if self.robot.pos[0]  <8:
                toRight=True
            else:
                toRight=False
            goal = self.robot.map.findSpaceInRow(y+1,toRight=toRight)     
            
            self.robot.findpath(goal=goal, rowgoal = goal[1])
        
        if x > self.robot.pos[0]:
            self.robot.faceDirection(1)
        else:
            self.robot.faceDirection(3)
            
