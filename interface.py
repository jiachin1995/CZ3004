#from multiprocessing import Process, Lock
from threading import Thread

from map import Map
from pathfinder import Pathfinder
from robot import Robot

import json
import time

class Interface:
    robot = None
    android=None
    
    thread = Thread()
    
    check_rate = 0.4
    
    def __init__(self, arduino=None, fakeRun=False, fakeMap=None, android=None):
        self.instructions = {
            'w1': self.forward,
            'a2': self.turnLeft,
            'd2': self.turnRight,
            's1': self.backward,
            'getreport': self.getreport,
            "getimages": self.getimages,
            'explore': self.explore,
            'stopexplore': self.stopexplore,
            'fastestpath': self.fastestpath,
            'waypoint': self.setwaypoint,
            'reset': self.reset,
            'setrobotpos': self.setpos,
            'loadfakeMap': self.loadmap,
        }
        
        self.reset(arduino=arduino, fakeRun=fakeRun, fakeMap=fakeMap)
        
        if android:
            self.android = android
    
    def stopexplore(self):
        raise Exception("stop command issued")

    def backward(self):
        return self.startprocess(target = self.robot.backward)

    def mapGUI(self, termCondition):
        while not eval(termCondition):
            time.sleep(self.check_rate)
            self.robot.map.printmap(self.robot)

    def explore(self, **kwargs):
        return self.startprocess(target = self.robot.explore)
        

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
     
    def fastestpath(self, **kwargs):
        return self.startprocess(target = self.robot.findpath)
    

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

    def forward(self, steps = 1):
        return self.startprocess(target = self.robot.forward, **{'steps':steps})


    def getreport(self):
        results = "" 
        for item in self.robot.map.convert():
            results += item[2:].upper() + ','
            
        for coords in self.robot.pos:
            results += str(coords) + ','
        
        orientation = 90 * self.robot.orientation
        results += str(orientation)
        
        dict = {
            "robot" : results
        }
        output = json.dumps(dict)
        
        return output

    def getimages(self):
        results = [] 

        #{"numberDisplay": [x,y, "some_letter"]}

        dict = {
            "numberDisplay" : results
        }
        output = json.dumps(dict)
        
        return output


    def loadmap_test(self):
        userinput = input("Enter file name:")  
        
        try:
            global map 
            map = Map(userinput)
            
            self.robot = Robot(fakeRun=True, fakeMap = map)
        except FileNotFoundError:
            print("File does not exist!")
            return

        map.printmap()
        
    def loadmap(self, load):
        try:
            map = Map(load)
            self.robot = Robot(fakeRun=True, fakeMap = map)
            
            return "Done"
   
        except Exception as e:
            print("Unable to load map")
            print(e)
            
            return "Unable to load map"

    def printmap(self):
        map.printmap()

    def printMDF(self):
        # print("Explored map string is:")
        # for item in self.robot.map.convert():
            # print(item)
        print(self.getreport())

    
    def readinstructions(self, instr):
        try:
            kwargs = {}
        
            if "waypointCoord" in instr:
                instr, waypoint = instr.split(separator=" ", maxsplit = 1)
                func = self.instructions["waypoint"]
                kwargs = {'waypoint' : eval(waypoint)}
                
                #return setwaypoint(waypoint = eval(waypoint))
            elif "robotCoord" in instr:
                instr, pos = instr.split(separator=" ", maxsplit = 1)
                func = self.instructions["setrobotpos"]
                kwargs = {'pos' : eval(pos)}
                
                #return setpos(pos = eval(pos))  
            else: 
                func = self.instructions[instr]
            
            return func(**kwargs)
            
        except KeyError as e:
            print("Key Error. Forwarding instruction to arduino")
            
            instr = e.args[0]
            self.robot.sensors.arduino.write(instr)
    
            while True:
                msg = self.robot.sensors.arduino.read()
                if msg == None:
                    print("[#] nothing to read [read_from_serial]")
                    
                else:
                    return msg
                    
                time.sleep(self.check_rate)
        

    def reset(self, arduino = None, fakeRun=False, fakeMap=None):
        self.robot = Robot(arduino=arduino, fakeRun=fakeRun, fakeMap = fakeMap)
    
           
    def startprocess(self, target, **kwargs):
        if not self.thread.isAlive():
            self.thread = Thread(target=target, kwargs=kwargs)
            self.thread.start()
    
            self.writeReport()
    
            return "done"
        else:
            return "Cancelled Instruction. Other processes already running."
        
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

    
    
    def setpos(self, pos):
        self.robot.pos = list(pos)
    
    def setwaypoint(self, waypoint):
        self.robot.pathfinder.waypoint = list(waypoint)
    
    def timer_test(self):
        userinput = input("Enter timer in seconds (Integer):  \n")  
        
        try:
           val = int(userinput)
        except ValueError:
           print("That's not an int!")
           return
        
        termCondition = "self.robot.explorer.state == 'Out of time' and self.robot.pos == [1,1]"

        t1 = Thread(target=self.robot.explore, kwargs={'timer': val })
        t2 = Thread(target=self.mapGUI, args=(termCondition,))

        #start thread
        t1.start()
        t2.start()

        # Waiting for threads to finish execution...
        t1.join()
        t2.join()
        
    def turnLeft(self):
        return self.startprocess(target = self.robot.turnLeft)
        
    def turnRight(self):
        return self.startprocess(target = self.robot.turnRight)
       
    def writeImages(self):
        img_list = []
    
        for img in self.robot.images:
            x,y = img[1]
            id = img[0]
            
            img_list.append([x,y,id])
            
        output = {"imageDisplay":img_list}
        
        output = json.dumps(output)
        self.android.write(output)
       
    def writeReport(self):
        report_thread = Thread(target=self._writeReport, args=())
        report_thread.start()

        
    def _writeReport(self):
        movement_thread = self.thread
    
        while movement_thread.isAlive:
            report = self.getreport()
            self.android.write(report)
            
            if self.robot.sendimages:
                self.robot.sendimages = False
                self.writeImages()
                
            
            time.sleep(self.check_rate)

        report = self.getreport()
        self.android.write(report)
        
        
if __name__ == "__main__":
    map = Map("sample_maze.txt")
    interface = Interface(fakeRun= True, fakeMap = map)

    interface.robot.map.printmap(robot = interface.robot)
    print("The Map above is the virtual arena.")


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
        7: interface.loadmap_test,
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