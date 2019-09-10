from threading import Thread

from map import Map
from pathfinder import Pathfinder
from robot import Robot

import time

map = Map('sample_maze.txt')


"""code to check explorer + steps per sec limit"""
robot = Robot(fakeRun=True, fakeMap = map)


def mapGUI(robot, termCondition):
    while not eval(termCondition):
        time.sleep(0.5)
        robot.map.printmap(robot)
        

def stepsPerSec_test():
    userinput = input("Enter steps per second:")  
    
    try:
       val = int(userinput)
    except ValueError:
       print("That's not an int!")
       return

    robot.coordinator.stepsPerSec =  val

    termCondition = "robot.map.is_explored() and robot.pos == [1,1]"

    t1 = Thread(target=robot.explore, args=(None,))
    t2 = Thread(target=mapGUI, args=(robot,termCondition,))

    #start thread
    t1.start()
    t2.start()

    # Waiting for threads to finish execution...
    t1.join()
    t2.join()

def explorelimit_test():
    userinput = input("Enter explore limit in floats format. E.g. 0.0 : \n")  
    
    try:
       val = float(userinput)
    except ValueError:
       print("That's not a float!")
       return

    termCondition = "robot.explorer.state == 'Exploration done' and robot.pos == [1,1]"

    t1 = Thread(target=robot.explore, kwargs={'exploreLimit': val })
    t2 = Thread(target=mapGUI, args=(robot,termCondition,))

    #start thread
    t1.start()
    t2.start()

    # Waiting for threads to finish execution...
    t1.join()
    t2.join()
 

def fastestpath_test():
    userinput = input("Enter waypoint in the format x,y:  \n")  
    
    try:
        x,y = userinput.split(",", 1)
   
        x = int(x)
        y = int(y)
    except ValueError:
       print("That's not an int!")
    
    robot.coordinator.stepsPerSec =  2

    termCondition = "robot.pos == [13,18]"

    t1 = Thread(target=robot.findpath, kwargs={'waypoint':[x,y]})
    t2 = Thread(target=mapGUI, args=(robot,termCondition,))

    #start thread
    t1.start()
    t2.start()

    # Waiting for threads to finish execution...
    t1.join()
    t2.join()

def loadmap():
    userinput = input("Enter file name:")  
    
    try:
        global map 
        map = Map(userinput)
        
        global robot
        robot = Robot(fakeRun=True, fakeMap = map)
    except FileNotFoundError:
        print("File does not exist!")
        return

    map.printmap()

def printmap():
    map.printmap()

def timer_test():
    userinput = input("Enter timer in seconds (Integer):  \n")  
    
    try:
       val = int(userinput)
    except ValueError:
       print("That's not an int!")
       return
    
    termCondition = "robot.explorer.state == 'Out of time' and robot.pos == [1,1]"

    t1 = Thread(target=robot.explore, kwargs={'timer': val })
    t2 = Thread(target=mapGUI, args=(robot,termCondition,))

    #start thread
    t1.start()
    t2.start()

    # Waiting for threads to finish execution...
    t1.join()
    t2.join()


robot.map.printmap()
print("The Map above is the virtual arena.")
print(robot.pos)
print(robot.orientation)



prompt = "Choose an option:   \n  \
           0: break             \n  \
           1: simulate explore with steps per second  \n  \
           2: simulate explore with coverage limit    \n  \
           3: simulate explore with timer \n  \
           4: after running explore (option 1), show fastest path   \n  \
           5: show virtual arena    \n  \
           6: show explored map     \n  \
           7: load map from file    \n  \
"


switch= {
    0: "break",
    1: stepsPerSec_test,
    2: explorelimit_test,
    3: timer_test,
    4: fastestpath_test,
    5: printmap,
    6: robot.map.printmap,
    7: loadmap,
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