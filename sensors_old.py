import time
import settings
        

class Sensors:
    """
    Sensors class. Reads sensors input.
    
    """
    arduino = None
    robot=None
    instructions = {
        "getFront": "get front sensors",
        "getLeft": "get left sensors",
        "getAllexceptRight": "z",
        "getRight": "y"
    }
    check_rate = 0.01
    
    front_sensors_range = settings.front_sensors_range     #biggest integer that sensors will return to algo
    left_sensors_range = settings.left_sensors_range
    right_sensors_range = settings.right_sensors_range
    
    right_sensors_position = settings.right_sensors_position
    
    
    
    def __init__(self, robot, arduino):
        self.robot = robot
        self.arduino = arduino
    
    def getAll(self):
        if self.isFrontExplored() and self.isLeftExplored():
            front = self.getFront()
            left = self.getLeft()
            #Excluding right
            
            return front + left
    
        instr = self.instructions["getAllexceptRight"]
        
        self.arduino.write(instr)
        
        while True:
            msg = self.arduino.read()
            if msg == None:
                print("[#] nothing to read [read_from_serial]")
                
            else:
                front_mid,front_left, front_right,left_front, left_back = msg.split(',')
                break
                
            time.sleep(self.check_rate)
        
        return [int(front_left), int(front_mid), int(front_right), int(left_front), int(left_back)]
    
    def getFront(self):
        """
        Returns front terrain in the form of a list, containing [left,middle,right].
        Left,middle,right are integers.
        if left == 0, it means there is a wall directly in front of robot, on the left side
        if middle == 2, it means there is a wall 2 steps in front of robot, at the middle
        
        For example, if front obstacle is T-shaped, getFront() might return 1, 0, 1.
        """
        #check if map explored, return obstacles
        if self.isFrontExplored():
            results = []
            tiles_array = self.robot.getBaseLineRange(length = self.front_sensors_range)
            
            for row in tiles_array:
                count = 0
                for tile in row:
                    if self.robot.map.getTile(tile) == 1 or self.robot.map.getTile(tile) == -1:
                        break
                    else:
                        count += 1
                results.append(count)
                
            return results
        
        
        #if not explored, use sensors   
        all = self.getAll()
        return all[:3]
        
    
    def getLeft(self):
        """
        Returns left terrain in the form of a list, containing [front, back].
        front,back are integers.
        
        Similar to getFront(). Refer to getFront() above
        """
        #check if map explored, return obstacles
        if self.isLeftExplored():
            results = []
            tiles_array = self.robot.getBaseLineVertRange(length = self.left_sensors_range)
            
            for row in tiles_array:
                count = 0
                for tile in row:
                    if self.robot.map.getTile(tile) == 1 or self.robot.map.getTile(tile) == -1:
                        break
                    else:
                        count += 1
                results.append(count)
                
            return results
            
        
        #if not explored, use sensors  
        all = self.getAll()
        return all[:3]
    
    def getRight(self):
        """
        Returns right terrain in the form of a list, containing [right].
        Our robot uses long range sensors for right
        
        Similar to getFront(). Refer to getFront() above
        """
        #check if map explored, return obstacles
        if self.isRightExplored():
            results = []
            tiles_array = self.robot.getBaseLineVertRange(
                    length = self.right_sensors_range,
                    exclude_mid=False,
                    toRight=True
                )
            row = tiles_array.pop(self.right_sensors_position)
            
            count = 0
            for tile in row:
                if self.robot.map.getTile(tile) == 1 or self.robot.map.getTile(tile) == -1:
                    break
                else:
                    count += 1
            results.append(count)
                
            return results
            
        
        #if not explored, use sensors  
        instr = self.instructions["getRight"]
        
        self.arduino.write(instr)
        
        while True:
            msg = self.arduino.read()
            if msg == None:
                print("[#] nothing to read [read_from_serial]")
                
            else:
                right = msg
                break
                
            time.sleep(self.check_rate)
        
        return [int(right)]
    
    def isFrontExplored(self):
        tiles_array = self.robot.getBaseLineRange(length = self.front_sensors_range)

        for row in tiles_array:
            for tile in row:
                if self.robot.map.getTile(tile) == None:
                    return False
        return True
    
    
    def isLeftExplored(self):
        tiles_array = self.robot.getBaseLineVertRange(length = self.left_sensors_range)
    
        for row in tiles_array:
            for tile in row:
                if self.robot.map.getTile(tile) == None:
                    return False
        return True
        
    def isRightExplored(self):
        tiles_array = self.robot.getBaseLineVertRange(
                length = self.right_sensors_range,
                exclude_mid=False,
                toRight=True
            )
        row = tiles_array.pop(self.right_sensors_position)
        
        for tile in row:
            if self.robot.map.getTile(tile) == None:
                return False
        return True
    
    
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
        
    def getLeastSensors(self):
        results = self.getAll()
        results += self.getRight()

        return results