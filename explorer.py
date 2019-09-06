import time

import settings

class Explorer:
    robot = None
    state = "Initial"

    
    startTime = None
    timer = 500
    timeToReturn = 60       #buffer time to return to start, in seconds
    exploreLimit = 1.0

    def __init__(self, robot, timer=None, exploreLimit = None):
        self.robot = robot
        if settings.logging:  
            print("====== Starting Explorer =======")
            print("New State: " + self.state)
    
        if timer:
            self.setTime(timer)
            
        if exploreLimit:
            self.setExploreLimit(exploreLimit)
    
    def start(self):
        self.startTime = time.time()
    
        if self.state == "Initial": 
            self.hugleftwall()
    
        while not self.exploreDone():  
            if self.noTimeLeft():
                break
            self.spelunk()
        
        
        if self.noTimeLeft():
            self.state = "Out of time. Returning to start"
        else:
            self.state = "Exploration done. Returning to start"
           
        if settings.logging:
            print(self.state)
            print("Remaining Time left: " + str(self.getRemainingTime()))
            print(self.robot.pos)
            print(self.robot.orientation)

        self.robot.findpath(goal=[1,1])
        self.robot.faceDirection(0)
        
    def hugleftwall(self, turns = 0, startpos = None, endCondition=None):
        #return if out of time
        if self.noTimeLeft():
            return
            
        #return if explore limit reached:
        if self.exploreDone():
            return
    
        #run once when first called
        if startpos == None:
            if self.hugleftprep():
                startpos = self.robot.pos
            else: return             #prep failed. Cancel left wall hugging
        
        #if left is free, turn left, move forward once
        if not self.robot.sensors.isLeftBlocked():
            self.robot.turnLeft()                #no need to update map cause next step will update instead.
            self.robot.forward()   #in theory, there should be at least one row of free space. 
            turns = (turns + 3) % 4
            
        #elif if front is free, move forward (up to 3)
        elif not self.robot.sensors.isFrontBlocked():
            front,back = self.robot.sensors.getLeft()
            if front != 0: 
                steps = 1        #we go 1 step at a time to find where left wall ends
            else:
                front_terrain = self.robot.sensors.getFront()
                steps = min(front_terrain)      #go as far as possible
                if steps>3: steps = 3           #we do this as we have to check & hug left wall every 3 steps
            
                #check next tiles whether terminate condition is in next few tiles
                if steps>1:
                    result = self.hugleftcheckstepstoterminate(turns, startpos, endCondition=endCondition)
                    if result:
                        steps = result
            
            self.robot.forward(steps)

        #if both failed, turn right
        else:
            self.robot.turnRight()
            turns = (turns + 3) % 4

        #check terminate or continue. if turns == 0, it means robot is facing starting orientation.
        x,y = self.robot.pos
        if endCondition and eval(endCondition):
            return
        elif turns == 0 and [x,y] == startpos: 
            return
        else: 
            self.hugleftwall(turns = turns, startpos = startpos, endCondition=endCondition)
        
    def hugleftprep(self):
        """ Prepares robot for left wall hugging algorithm. 
            Expects an adjacent wall before starting.
            
        Args:
            none: no arguments

        Raises:
            Warning: Left Wall Hugging Cancelled. No adjacent walls found.
        """
    
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

    def hugleftcheckstepstoterminate(self, turns, startpos, endCondition=None):
        """check next tiles is in terminate condition"""
        x,y = self.robot.pos
        tileRange = self.robot.getTileRange()
        
        
        """if [x,y] in terminate: return distance"""
        for i in range(1,3):
            x,y = eval(tileRange)

            if endCondition and eval(endCondition):
                return i
            if turns == 0 and [x,y] == startpos: 
                return i
            
        return None
       
    def getRemainingTime(self):
        now = time.time()
        return (self.startTime+ self.timer) - now
       
    def noTimeLeft(self):
        now = time.time()
        if now > (self.startTime + self.timer - self.timeToReturn):
            return True
        else:
            return False
       
    def setTime(self, timer):
        if timer < self.timeToReturn:
            raise Exception("Time given less than return time. Give more time for exploration")
        
        self.timer = timer        

    def exploreDone(self):
        if self.robot.map.is_explored() >= self.exploreLimit:
            return True
        else:
            return False
       
    def setExploreLimit(self, exploreLimit):
        self.exploreLimit = exploreLimit
       
    def spelunk(self):
        self.state = "Spelunking"
        if settings.logging:  
              print("New State: " + self.state) 

        self.spelunkprep()        
        self._spelunking()
    
    def _spelunking(self):
        if not self.robot.sensors.isFrontBlocked():
            front_terrain = self.robot.sensors.getFront()
            steps = min(front_terrain)      #go as far as possible
            
            self.robot.forward(steps)
            
        else:
            endCondition = "y == " + str(self.robot.pos[1]) + " and not [x,y] == " + str(self.robot.pos)
            self.hugleftwall(endCondition=endCondition) #terminate condition: same row & not startpos


    def spelunkprep(self):
        x,y = self.robot.map.getUnexploredTile()
        
        if settings.logging:
            print("UNEXPLORED TILE")
            print([x,y])
            
            
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
            
