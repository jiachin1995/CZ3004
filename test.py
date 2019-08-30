from map import Map
from pathfinder import Pathfinder
from robot import Robot


map = Map('sample_maze.txt')

""" code to create mazes"""
# poslist = [
        # [3,9],
        # [9,14],
    # ]
# valuelist = [1]*len(poslist)
# map.setTiles(poslist,valuelist)

# map.save("sample_maze.txt")
"""code to test pathfinder"""
# pf = Pathfinder(map)
# pf.findpath()


"""code to test simulator"""

robot = Robot(fakeRun=True, fakeMap = map)
robot.forward()
robot.map.printmap()
