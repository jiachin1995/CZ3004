from map import Map
from pathfinder import Pathfinder
#from robot import Robot

#robo = Robot()


map = Map('sample_maze.txt')

# poslist = [
        # [3,9],
        # [9,14],
    # ]
# valuelist = [1]*len(poslist)
# map.setTiles(poslist,valuelist)

# map.save("sample_maze.txt")

pf = Pathfinder(map)
pf.findpath()