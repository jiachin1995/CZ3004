class Sensors:
    """
    Sensors class. Reads sensors input.
    
    """
    
    def getFront():
        """
        Returns front terrain in the form of a list, containing [left,middle,right].
        Left,middle,right are integers.
        if left == 0, it means there is a wall directly in front of robot, on the left side
        if middle == 2, it means there is a wall 2 steps in front of robot, at the middle
        
        For example, if front obstacle is T-shaped, getFront() might return 1, 0, 1.
        """
    
        pass
    
    def getLeft(self):
        """
        Returns left terrain in the form of a list, containing [front, back].
        front,back are integers.
        
        Similar to getFront(). Refer to getFront() above
        """
        pass
    
    
    def isFrontBlocked():
        """
        Returns True if any tiles immediately in front of robot is occupied.
        
        If any terrain in getFront() is 0, return False.
        """
        pass
        
    def isLeftBlocked():
        """
        Returns True if any tiles immediately left of robot is occupied.
        
        If any terrain in getLeft() is 0, return False.
        """
        pass
        
 