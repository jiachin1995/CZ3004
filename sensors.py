import time
        

class Sensors:
    """
    Sensors class. Reads sensors input.
    
    """
    arduino = None
    robot=None
    instructions = {
        "getFront": "get front sensors",
        "getLeft": "get left sensors",
        "getAll": "z"
    }
    check_rate = 0.01
    
    front_sensors_range = 3     #biggest integer that sensors will return us
    left_sensors_range = 3
    
    
    
    def __init__(self, robot, arduino):
        self.robot = robot
        self.arduino = arduino
    
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
        instr = self.instructions["getAll"]
        
        self.arduino.write(instr)
        print("[@] Sent to Serial: {}".format(instr))
        
        while True:
            msg = self.arduino.read()
            if msg == None:
                print("[#] nothing to read [read_from_serial]")
                
            else:
                front_mid,front_left, front_right,left_front, left_back = msg.split(',')
                break
                
            time.sleep(self.check_rate)
        
        return [int(front_left), int(front_mid), int(front_right)]
    
    def getLeft(self):
        """
        Returns left terrain in the form of a list, containing [front, back].
        front,back are integers.
        
        Similar to getFront(). Refer to getFront() above
        """
        #check if map explored, return obstacles
        if self.isLeftExplored():
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
        instr = self.instructions["getAll"]
        
        self.arduino.write(instr)
        
        while True:
            msg = self.arduino.read()
            if msg == None:
                print("[#] nothing to read [read_from_serial]")
                
            else:
                front_mid,front_left, front_right,left_front, left_back = msg.split(',')
                break
                
            time.sleep(self.check_rate)
        
        return [int(left_front), int(left_back)]
    
    def isFrontExplored(self):
        tiles_array = self.robot.getBaseLineRange(length = self.front_sensors_range)

        for row in tiles_array:
            for tile in row:
                if self.robot.map.getTile([x,y]) == None:
                    return False
        return True
    
    
    def isLeftExplored(self):
        tiles_array = self.robot.getBaseLineVertRange(length = self.left_sensors_range)
    
        for row in tiles_array:
            for tile in row:
                if self.robot.map.getTile([x,y]) == None:
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
        
 