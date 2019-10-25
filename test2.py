from map import Map
# from pathfinder import Pathfinder
# from robot import Robot
# from interface import Interface
# import time

# from boundingbox import Imagefinder
# imf = Imagefinder()
# imf.find()

from islandsfinder import Islandsfinder


map = Map("zz2.txt")
finder = Islandsfinder(map)
print(finder.printislandsmap())

iterator = finder.nextIsland()
results = next(iterator, None)
print(results)


# interface.robot.coordinator.stepsPerSec =20

# print(interface.readinstructions("explore"))
# print(interface.readinstructions("turnLeft"))
# time.sleep(40)
# print(interface.readinstructions("fastestpath"))

# #interface.readinstructions("fastestpath")
