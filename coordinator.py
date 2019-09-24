#purpose of this module is to ensure robot alignment, position & movement

class Coordinator:
    """
    Coordinator class. Controls the movement of the robot.
    

        
    Attributes:
        fakeRun: Defaults to False. Set to True if running in simulation
        stepsPerSec: Number of steps to take per second, if running in simulation
    """
    instructions = {
        "forward": "forward",
        "left": "left"",
        "right": "right",
        "movement done" : "done"
    }
    fakeRun = False
    stepsPerSec = 2

    arduino = None
    
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
        else:
            instr = self.instructions["forward"]
        
            self.arduino.write(instr)
            print("[@] Sent to Serial: {}".format(instr))
            
            while True:
                msg = self.arduino.read()
                if msg == None:
                    return print("[#] nothing to read [read_from_serial]")
                
                elif msg == self.instructions["movement done"]:
                    return
    
    def turnLeft(self):
        """ 
        Turns the robot left
        """   
        if self.fakeRun:
            self.fakeRunWait()
            return
        else:
            instr = self.instructions["forward"]
        
            self.arduino.write(instr)
            print("[@] Sent to Serial: {}".format(instr))
            
            while True:
                msg = self.arduino.read()
                if msg == None:
                    return print("[#] nothing to read [read_from_serial]")
                
                elif msg == self.instructions["movement done"]:
                    return
    
    def turnRight(self):
        """ 
        Turns the robot right
        """ 
        if self.fakeRun:
            self.fakeRunWait()
            return
        else:
            instr = self.instructions["forward"]
        
            self.arduino.write(instr)
            print("[@] Sent to Serial: {}".format(instr))  
            
            while True:
                msg = self.arduino.read()
                if msg == None:
                    return print("[#] nothing to read [read_from_serial]")
                
                elif msg == self.instructions["movement done"]:
                    return
            
    def fakeRunWait(self):
        """ 
        If running in simulation, pause the algorithm for (1/stepsPerSec) seconds.
        """ 
        import time
        
        wait = 1.0/ float(self.stepsPerSec)
        time.sleep(wait)

        return