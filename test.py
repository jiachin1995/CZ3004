from map import Map
from pathfinder import Pathfinder
from robot import Robot


map = Map('sample_maze.txt')


# robot = Robot(fakeRun=True, fakeMap = map)
# print(robot.getBaseLineRange(length=0))


""" code to create mazes"""
# map = [[0 for _ in range(15)] for _ in range(20)]
# map = Map(map)
# poslist = [
        # [5,0],
        # [13,1],
        # [9,3],
        # [3,4],[4,4],[5,4],
        # [11,5], [11,6], [11,7],[11,8],[11,9],[11,10],
        # [3,9], [3,10], [3,11], [3,12], [3,13], [3,14],
        # [9,15], [10,15], [11,15], 
        # [5,16],
        # [1,18], 
        # [9,19], 
    # ]
# valuelist = [1]*len(poslist)
# map.setTiles(poslist,valuelist)
# map.printmap()
# map.save("testmaze5.txt")

# map.save("sample_maze.txt")
"""code to test pathfinder"""
# pf = Pathfinder(map)
# pf.findpath()


"""code to test simulator"""

# robot = Robot(fakeRun=True, fakeMap = map)
# robot.forward(5)
# robot.turnRight()
# robot.forward(3)
# robot.turnLeft()
# robot.map.printmap()

"""code to check explorer.py"""
robot = Robot(fakeRun=True, fakeMap = map)
robot.explore()

robot.map.printmap()
print(robot.pos)
print(robot.orientation)


"""code to check explorer + timer"""
# robot = Robot(fakeRun=True, fakeMap = map)
# robot.explore(timer = 200)

# robot.map.printmap()
# print(robot.pos)
# print(robot.orientation)


"""code to check explorer + exploration limit"""
# robot = Robot(fakeRun=True, fakeMap = map)
# robot.explore(exploreLimit = 0.2)

# robot.map.printmap()
# print(robot.pos)
# print(robot.orientation)

"""code to check explorer + steps per sec limit"""
# robot = Robot(fakeRun=True, fakeMap = map, stepsPerSec = 1)
# robot.explore()

# robot.map.printmap()
# print(robot.pos)
# print(robot.orientation)

"""code to check map exploration"""
#map.printmap()
# print(robot.map.explored_percent())
# print(robot.map.is_explored())
