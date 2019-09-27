from map import Map
from pathfinder import Pathfinder
from robot import Robot


map = Map('zz.txt')



robot = Robot(fakeRun=True, fakeMap = map)

robot.coordinator.stepsPerSec = 15
robot.explorer.start()



