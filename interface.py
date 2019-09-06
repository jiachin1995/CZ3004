from threading import Thread

from map import Map
from pathfinder import Pathfinder
from robot import Robot

import time

map = Map('sample_maze.txt')


"""code to check explorer + steps per sec limit"""
robot = Robot(fakeRun=True, fakeMap = map)


def mapGUI(robot):
    while not robot.map.is_explored():
        time.sleep(1)
        robot.map.printmap()

def stepsPerSec_test():
    userinput = input("Enter steps per second:")  
    
    try:
       val = int(userinput)
    except ValueError:
       print("That's not an int!")
       return

    robot.stepsPerSec =  val


    t1 = Thread(target=robot.explore, args=(None,))
    t2 = Thread(target=mapGUI, args=(robot,))

    #start thread
    t1.start()
    t2.start()

    # Waiting for threads to finish execution...
    t1.join()
    t2.join()

    

prompt = " Choose an option:   \n  \
           0: break             \n  \
           1: simulate explore with steps per second  \n  \
           2: show virtual arena    \n  \
           3: show explored map     \n  \
"



robot.map.printmap()
print("The Map above is the virtual arena.")
print(robot.pos)
print(robot.orientation)

switch= {
    0: "break",
    1: stepsPerSec_test,
    2: map.printmap,
    3: robot.map.printmap,
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