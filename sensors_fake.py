from map import Map

import settings

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

        baseline = self.robot.getBaseLine()
        tileRange = self.robot.getTileRange()
        
        x,y = baseline.pop(0)
        left = 0
        for i in range(0, self.front_sensors_range):      
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                left += 1
                x,y = eval(tileRange)

             
        x,y = baseline.pop(0)
        middle = 0
        for i in range(0, self.front_sensors_range):  
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                middle += 1
                x,y = eval(tileRange)

        x,y = baseline.pop(0)
        right = 0
        for i in range(0, self.front_sensors_range):    
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                right += 1
                x,y = eval(tileRange)                
                
        if settings.logging:
            print("=======Sensors getFront() Output=======")
            print([left, middle, right])
                
        return [left, middle, right]
            
    def getLeft(self):
        x, y = self.robot.pos

        baseline_vert = self.robot.getBaseLineVert()
        tileRange_vert = self.robot.getTileRangeVert()
        
        x,y = baseline_vert.pop(0)
        front = 0
        for i in range(0, self.left_sensors_range):    
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                front += 1
                x,y = eval(tileRange_vert)   
                
        x,y = baseline_vert.pop(0)
        back = 0
        for i in range(0, self.left_sensors_range):    
            if self.map.getTile([x,y]) == 1 or self.map.getTile([x,y]) == -1:
                break
            else:
                back += 1
                x,y = eval(tileRange_vert)                
        
        return [front, back]
        
    def isFrontBlocked(self):
        for val in self.getFront():
            if val == 0:
                return True
        return False
        
    def isLeftBlocked(self):
        for val in self.getLeft():
            if val == 0:
                return True
        return False