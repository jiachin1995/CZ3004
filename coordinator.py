import time
        

class Coordinator:
    """
    Coordinator class. Controls the movement of the robot.
    

        
    Attributes:
        fakeRun: Defaults to False. Set to True if running in simulation
        stepsPerSec: Number of steps to take per second, if running in simulation
    """
    instructions = {
        "forward": "w",
        "backward": "s1",
        "left": "a2",
        "right": "d2",
        "movement done" : "done"
    }
    fakeRun = False
    stepsPerSec = 2
    check_rate = 0.5


    arduino = None
    
    def backward(self):
        """ 
        Moves the robot backward
        """   
        if self.fakeRun:
            for i in range(0,steps):
                self.fakeRunWait()
            return
        else:
            instr = self.instructions["backward"]
        
            self.arduino.write(bytes(instr, 'utf-8'))
            print("[@] Sent to Serial: {}".format(instr))
            
            while True:
                msg = self.arduino.read()
                if msg == None:
                    print("[#] nothing to read [read_from_serial]")
                    
                elif str(msg) == self.instructions["movement done"]:
                    return
                    
                time.sleep(check_rate)
    
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
            instr += str(steps)
        
            self.arduino.write(bytes(instr, 'utf-8'))
            print("[@] Sent to Serial: {}".format(instr))
            
            while True:
                msg = self.arduino.read()
                if msg == None:
                    print("[#] nothing to read [read_from_serial]")
                    
                elif str(msg) == self.instructions["movement done"]:
                    return
                    
                time.sleep(check_rate)
    
    def turnLeft(self):
        """ 
        Turns the robot left
        """   
        if self.fakeRun:
            self.fakeRunWait()
            return
        else:
            instr = self.instructions["forward"]
        
            self.arduino.write(bytes(instr, 'utf-8'))
            print("[@] Sent to Serial: {}".format(instr))
            
            while True:
                msg = self.arduino.read()
                if msg == None:
                    print("[#] nothing to read [read_from_serial]")
                
                elif str(msg) == self.instructions["movement done"]:
                    return
                    
                time.sleep(check_rate)
    
    def turnRight(self):
        """ 
        Turns the robot right
        """ 
        if self.fakeRun:
            self.fakeRunWait()
            return
        else:
            instr = self.instructions["forward"]
        
            self.arduino.write(bytes(instr, 'utf-8'))
            print("[@] Sent to Serial: {}".format(instr))  
            
            while True:
                msg = self.arduino.read()
                if msg == None:
                    print("[#] nothing to read [read_from_serial]")
                
                elif str(msg) == self.instructions["movement done"]:
                    return
                    
                time.sleep(check_rate)
            
    def fakeRunWait(self):
        """ 
        If running in simulation, pause the algorithm for (1/stepsPerSec) seconds.
        """ 

        wait = 1.0/ float(self.stepsPerSec)
        time.sleep(wait)

        return