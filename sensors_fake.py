from map import Map

class Sensors:
    front_sensors_range = 4
    left_sensors_range = 4

    def __init__(self, robot, fakemap):
        self.robot = robot
        
        if fakemap is None:
            map = [[0 for _ in range(15)] for _ in range(20)]
            self.map = Map(map)
        else: self.map = fakemap
        
    def getFront(self):
        x, y = self.robot.pos
        #baseline refers to the left,middle & right (from the robot's perspective) tiles the robot is occupying. 
        #baseline_dict contains the tiles to search. For example, if facing right, search top, middle & bottom tiles
        baseline_dict = {
            0: [[x-1,y],[x,y],[x+1,y]],
            1: [[x,y+1],[x,y],[x,y-1]],
            2: [[x+1,y],[x,y],[x-1,y]],
            3: [[x,y-1],[x,y],[x,y+1]]
        }
        baseline = baseline_dict[self.robot.orientation]
        
        #range of tiles to check
        tileRange_dict = {
            0: "y+i",
            1: "x+i",
            2: "y-i",
            3: "x-i",
        }
        tileRange = tileRange_dict[self.robot.orientation]
        
        x,y = baseline.pop(0)
        left = 0
        for i in range(2, self.front_sensors_range+2):      # +2 because the Tiles we want to check are 2 tiles away. 
            eval(tileRange)
            
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                left += 1
                
        x,y = baseline.pop(0)
        middle = 0
        for i in range(2, self.front_sensors_range+2):      # +2 because the Tiles we want to check are 2 tiles away. 
            eval(tileRange)
            
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                middle += 1        

        x,y = baseline.pop(0)
        right = 0
        for i in range(2, self.front_sensors_range+2):      # +2 because the Tiles we want to check are 2 tiles away. 
            eval(tileRange)
            
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                right += 1                     
                
        return [left, middle, right]
            
    def getLeft():
        x, y = self.robot.pos
        #baseline_vert refers to baseline, but vertical. Refer to above
        baseline_vert_dict = {
            0: [[x,y+1],[x,y-1]],
            1: [[x+1,y],[x-1,y]],
            2: [[x,y-1],[x,y+1]],
            3: [[x-1,y],[x+1,y]]
        }
        baseline_vert = baseline_vert_dict[self.robot.orientation]
        
        #range of tiles to check
        tileRange_dict = {
            0: "x-i",
            1: "y+i",
            2: "x+i",
            3: "y-i",
        }
        tileRange = tileRange_dict[self.robot.orientation]
        
        x,y = baseline_vert.pop(0)
        front = 0
        for i in range(2, self.left_sensors_range+2):      # +2 because the Tiles we want to check are 2 tiles away. 
            eval(tileRange)
            
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y] == -1):
                break
            else:
                front += 1
                
        x,y = baseline_vert_dict.pop(0)
        back = 0
        for i in range(2, self.left_sensors_range+2):      # +2 because the Tiles we want to check are 2 tiles away. 
            eval(tileRange)
            
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y] == -1):
                break
            else:
                back += 1                
        
        return [front, back]
        
    def isFrontBlocked():
        for val in self.getFront():
            if val == 0:
                return True
        return False
        
    def isLeftBlocked():
        for val in self.getFront():
            if val == 0:
                return True
        return False