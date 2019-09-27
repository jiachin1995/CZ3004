from map import Map
from pathfinder import Pathfinder
from robot import Robot
from interface import Interface
import time

interface = Interface(fakeRun=True)
interface.robot.coordinator.stepsPerSec =20

print(interface.readinstructions("explore"))
print(interface.readinstructions("turnLeft"))
time.sleep(40)
print(interface.readinstructions("fastestpath"))

#interface.readinstructions("fastestpath")