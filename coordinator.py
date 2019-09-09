#purpose of this module is to ensure robot alignment, position & movement

class Coordinator:
    """
    Coordinator class. Controls the movement of the robot.
    

        
    Attributes:
        fakeRun: Defaults to False. Set to True if running in simulation
        stepsPerSec: Number of steps to take per second, if running in simulation
    """

    fakeRun = False
    stepsPerSec = 2

    def forward(self,steps):
        """ 
        Moves the robot forward
            
        Args:
            steps: Integer. Number of steps to take.
        """   
        if self.fakeRun:
            for i in range(0,steps):
                self.fakeRunWait()
            return
        pass
    
    def turnLeft(self):
        """ 
        Turns the robot left
        """   
        if self.fakeRun:
            self.fakeRunWait()
            return
        pass
    
    def turnRight(self):
        """ 
        Turns the robot right
        """ 
        if self.fakeRun:
            self.fakeRunWait()
            return
        pass
        
    def fakeRunWait(self):
        """ 
        If running in simulation, pause the algorithm for (1/stepsPerSec) seconds.
        """ 
        import time
        
        wait = 1.0/ float(self.stepsPerSec)
        time.sleep(wait)

        return