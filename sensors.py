import time
        

class Sensors:
    """
    Sensors class. Reads sensors input.
    
    """
    arduino = None
    instructions = {
        "getFront": "get front sensors",
        "getLeft": "get left sensors",
        "getAll": "z"
    }
    check_rate = 0.5
    
    def __init__(self, arduino):
        self.arduino = arduino
    
    def getFront():
        """
        Returns front terrain in the form of a list, containing [left,middle,right].
        Left,middle,right are integers.
        if left == 0, it means there is a wall directly in front of robot, on the left side
        if middle == 2, it means there is a wall 2 steps in front of robot, at the middle
        
        For example, if front obstacle is T-shaped, getFront() might return 1, 0, 1.
        """
        instr = self.instructions["getAll"]
        
        self.arduino.write(instr)
        print("[@] Sent to Serial: {}".format(instr))
        
        while True:
            msg = self.arduino.read()
            if msg == None:
                print("[#] nothing to read [read_from_serial]")
                
            else:
                front_mid,front_left, front_right,left_front, left_back = msg.split(separator=',')
                break
                
            time.sleep(check_rate)
        
        return [int(front_left), int(front_mid), int(front_right)]
    
    def getLeft(self):
        """
        Returns left terrain in the form of a list, containing [front, back].
        front,back are integers.
        
        Similar to getFront(). Refer to getFront() above
        """
        instr = self.instructions["getAll"]
        
        self.arduino.write(instr)
        
        while True:
            msg = self.arduino.read()
            if msg == None:
                print("[#] nothing to read [read_from_serial]")
                
            else:
                front_mid,front_left, front_right,left_front, left_back = msg.split(separator=',')
                break
                
            time.sleep(check_rate)
        
        return [int(left_front), int(left_back)]
    
    
    def isFrontBlocked():
        """
        Returns True if any tiles immediately in front of robot is occupied.
        
        If any terrain in getFront() is 0, return False.
        """
        for val in self.getFront():
            if val == 0:
                return True
        return False
        
    def isLeftBlocked():
        """
        Returns True if any tiles immediately left of robot is occupied.
        
        If any terrain in getLeft() is 0, return False.
        """
        for val in self.getLeft():
            if val == 0:
                return True
        return False
        
 