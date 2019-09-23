from threading import Thread

from map import Map
from pathfinder import Pathfinder
from robot import Robot

import time

class Interface:
    def __init__(self):
        self.instructions = {
            'forward': self.forward,
            'turnLeft': self.turnLeft,
            'turnRight': self.turnRight,
            'readmap': self.getmap,
            'explore': self.explore,
            'fastestpath': self.fastestpath,
            'new': self.new,
        }

        

    def mapGUI(self, termCondition):
        while not eval(termCondition):
            time.sleep(0.5)
            self.robot.map.printmap(self.robot)
           
      

    def stepsPerSec_test(self):
        userinput = input("Enter steps per second:")  
        
        try:
           val = int(userinput)
        except ValueError:
           print("That's not an int!")
           return

        self.robot.coordinator.stepsPerSec =  val

        termCondition = "self.robot.map.is_explored() and self.robot.pos == [1,1]"

        t1 = Thread(target=self.robot.explore, args=(None,))
        t2 = Thread(target=self.mapGUI, args=(termCondition,))

        #start thread
        t1.start()
        t2.start()

        # Waiting for threads to finish execution...
        t1.join()
        t2.join()

    def explore(self):
        pass

    def explorelimit_test(self):
        userinput = input("Enter explore limit in floats format. E.g. 0.0 : \n")  
        
        try:
           val = float(userinput)
        except ValueError:
           print("That's not a float!")
           return

        termCondition = "self.robot.explorer.state == 'Exploration done' and self.robot.pos == [1,1]"

        t1 = Thread(target=self.robot.explore, kwargs={'exploreLimit': val })
        t2 = Thread(target=self.mapGUI, args=(termCondition,))

        #start thread
        t1.start()
        t2.start()

        # Waiting for threads to finish execution...
        t1.join()
        t2.join()
     
    def fastestpath(self):
        pass

    def fastestpath_test(self):
        userinput = input("Enter waypoint in the format x,y:  \n")  
        
        try:
            x,y = userinput.split(",", 1)
       
            x = int(x)
            y = int(y)
        except ValueError:
           print("That's not an int!")
        
        self.robot.coordinator.stepsPerSec =  2

        termCondition = "self.robot.pos == [13,18]"

        t1 = Thread(target=self.robot.findpath, kwargs={'waypoint':[x,y]})
        t2 = Thread(target=self.mapGUI, args=(termCondition,))

        #start thread
        t1.start()
        t2.start()

        # Waiting for threads to finish execution...
        t1.join()
        t2.join()

    def forward(self):
        pass

    def getmap(self):
        pass

    def loadmap(self):
        userinput = input("Enter file name:")  
        
        try:
            global map 
            map = Map(userinput)
            
            self.robot = Robot(fakeRun=True, fakeMap = map)
        except FileNotFoundError:
            print("File does not exist!")
            return

        map.printmap()

    def new(self, fakeRun=False, fakeMap=None):
        self.robot = Robot(fakeRun=fakeRun, fakeMap = self.fakeMap)

    def printmap(self):
        map.printmap()


    def printMDF(self):
        print("Explored map string is:")
        for item in self.robot.map.convert():
            print(item)

    def read(self, instruction):
        pass
        
    def runSimulator(self):
        pass



    def timer_test(self):
        userinput = input("Enter timer in seconds (Integer):  \n")  
        
        try:
           val = int(userinput)
        except ValueError:
           print("That's not an int!")
           return
        
        termCondition = "self.robot.explorer.state == 'Out of time' and self.robot.pos == [1,1]"

        t1 = Thread(target=self.robot.explore, kwargs={'timer': val })
        t2 = Thread(target=self.mapGUI, args=(self.robot,termCondition,))

        #start thread
        t1.start()
        t2.start()

        # Waiting for threads to finish execution...
        t1.join()
        t2.join()
        
    def turnLeft(self):
        pass
        
    def turnRight(self):
        pass
        
    

if __name__ == "__main__":
    interface = Interface()

    interface.robot.map.printmap()
    print("The Map above is the virtual arena.")
    print(interface.robot.pos)
    print(interface.robot.orientation)

    prompt = "Choose an option:   \n  \
               0: break             \n  \
               1: simulate explore with steps per second  \n  \
               2: simulate explore with coverage limit    \n  \
               3: simulate explore with timer \n  \
               4: after running explore (option 1), show fastest path   \n  \
               5: show virtual arena    \n  \
               6: show explored map     \n  \
               7: load map from file    \n  \
               8: print MDF           \n    "

    switch= {
        0: "break",
        1: interface.stepsPerSec_test,
        2: interface.explorelimit_test,
        3: interface.timer_test,
        4: interface.fastestpath_test,
        5: interface.printmap,
        6: interface.robot.map.printmap,
        7: interface.loadmap,
        8: interface.printMDF,
    }
    while True:
        userinput = input(prompt)      
        
        try:
            val = int(userinput)
        except ValueError:
            print("That's not an int!")
            continue
        
        if val == 0:
            break
        
        switch[val]()