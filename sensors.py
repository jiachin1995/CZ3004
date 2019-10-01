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
        if isFrontExplored:
            baseline = self.getBaseLine()
            tileRange = self.getTileRange()
            
            results = []
            for tile in baseline:
                x,y = tile
                count = 0
                for i in range(self.front_sensors_range):  
                    if self.robot.map.getTile([x,y]) == 1 or self.robot.map.getTile([x,y]) == -1:
                        break
                    count += 1
                    x,y = eval(tileRange)
                    
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
        if isLeftExplored:
            baseline_vert = self.getBaseLineVert()
            baseline_vert.pop(1)
            tileRange_vert = self.getTileRangeVert()
            
            results = []
            for tile in baseline_vert:
                x,y = tile
                count = 0
                for i in range(self.left_sensors_range):  
                    if self.robot.map.getTile([x,y]) == 1 or self.robot.map.getTile([x,y]) == -1:
                        break
                    count += 1
                    x,y = eval(tileRange_vert)
                    
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
        baseline = self.getBaseLine()
        tileRange = self.getTileRange()
        
        for tile in baseline:
            x,y = tile
            for i in range(self.front_sensors_range):  
                if self.robot.map.getTile([x,y]) == None:
                    return False
                x,y = eval(tileRange)
    
        return True
    
    def isLeftExplored(self):
        baseline_vert = self.getBaseLineVert()
        baseline_vert.pop(1)
        tileRange_vert = self.getTileRangeVert()
        
        for tile in baseline_vert:
            x,y = tile
            for i in range(self.left_sensors_range):  
                if self.robot.map.getTile([x,y]) == None:
                    return False
                x,y = eval(tileRange_vert)
    
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
        
 