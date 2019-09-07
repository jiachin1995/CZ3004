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

    

prompt = " Choose an option:   \n  \
           0: break             \n  \
           1: simulate explore with steps per second  \n  \
           2: after running explore (option 1), show fastest path   \n  \
           3: show virtual arena    \n  \
           4: show explored map     \n  \
"

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


robot.map.printmap()
print("The Map above is the virtual arena.")
print(robot.pos)
print(robot.orientation)

switch= {
    0: "break",
    1: stepsPerSec_test,
    2: fastestpath_test,
    3: map.printmap,
    4: robot.map.printmap,
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