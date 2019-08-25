from map import Map
from pathfinder import Pathfinder
    
map = Map()
map.load("school_example.txt")


pf = Pathfinder(map)
#pf.findpath()
pf.findpath(waypoint = [1,17])