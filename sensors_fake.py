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
        tiles_array = self.robot.getBaseLineRange(length = self.front_sensors_range)
        results = []
        
        for row in tiles_array:
            count = 0
            for tile in row:
                if self.map.getTile(tile) == 1 or self.map.getTile(tile) == -1:
                    break
                else:
                    count += 1
            results.append(count)
            
        return results
            
            
    def getLeft(self):
        """
        Returns left terrain in the form of a list, containing [front, back].
        front,back are integers.
        
        Similar to getFront(). Refer to getFront() above.
        
        Fake sensors does this by reading robot's position and orientation and compares it with fake map.

        """
        tiles_array = self.robot.getBaseLineVertRange(length = self.left_sensors_range)
        results = []
        
        for row in tiles_array:
            count = 0
            for tile in row:
                if self.map.getTile(tile) == 1 or self.map.getTile(tile) == -1:
                    break
                else:
                    count += 1
            results.append(count)
            
        return results

        
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