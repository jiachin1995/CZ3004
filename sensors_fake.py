from map import Map

import settings

class Sensors:
    """
    Fake Sensors class. Returns fake sensor input by reading a fakemap. Fake map should be 100% explored.
    
    Attributes:
        front_sensors_range: Integer. Defaults to 4. Maximum range that sensor can read
        left_sensors_range: Integer. Defaults to 4. Maximum range that sensor can read
        map: Map object. Fake map used to output fake sensor inputs.
        robot: Robot object. Required to read current pos and orientation.
    """

    front_sensors_range = 4
    left_sensors_range = 4
    map = None
    robot = None

    def __init__(self, robot, fakemap):
        """
        Constructor.  
        
        Args:
            robot: Robot object. Required to read current pos and orientation.
            fakemap: Map object. Fake map used to output fake sensor inputs.
        """
        self.robot = robot
        
        if fakemap is None:
            map = [[0 for _ in range(15)] for _ in range(20)]
            self.map = Map(map)
        else: self.map = fakemap
        
    def getFront(self):
        """
        Returns front terrain in the form of a list, containing [left,middle,right].
        Left,middle,right are integers.
        if left == 0, it means there is a wall directly in front of robot, on the left side
        if middle == 2, it means there is a wall 2 steps in front of robot, at the middle
        
        For example, if front obstacle is T-shaped, getFront() might return 1, 0, 1.
        
        Fake sensors does this by reading robot's position and orientation and compares it with fake map.
        """
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
                
                
        return [left, middle, right]
            
    def getLeft(self):
        """
        Returns left terrain in the form of a list, containing [front, back].
        front,back are integers.
        
        Similar to getFront(). Refer to getFront() above.
        
        Fake sensors does this by reading robot's position and orientation and compares it with fake map.

        """
        x, y = self.robot.pos

        baseline_vert = self.robot.getBaseLineVert()
        baseline_vert.pop(1)
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
        """
        Returns True if any tiles immediately in front of robot is occupied.
        
        If any terrain in getFront() is 0, return False.
        """
        for val in self.getFront():
            if val == 0:
                return True
        return False
        
    def isLeftBlocked(self):
        """
        Returns True if any tiles immediately left of robot is occupied.
        
        If any terrain in getLeft() is 0, return False.
        """
        for val in self.getLeft():
            if val == 0:
                return True
        return False