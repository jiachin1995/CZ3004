#purpose of this module is to ensure robot alignment, position & movement

class Coordinator:
    fakeRun = False
    stepsPerSec = 2

    def forward(self,steps):
        if self.fakeRun:
            self.fakeRunWait()
            return
        pass
    
    def turnLeft(self):
        if self.fakeRun:
            self.fakeRunWait()
            return
        pass
    
    def turnRight(self):
        if self.fakeRun:
            self.fakeRunWait()
            return
        pass
        
    def fakeRunWait(self):
        import time
        
        wait = 1.0/ float(self.stepsPerSec)
        time.sleep(wait)

        return