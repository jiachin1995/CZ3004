from map import Map
from pathfinder import Pathfinder
from robot import Robot

robo = Robot()


map = Map(load='school_example.txt')
pf = Pathfinder(map)

pf.findpath()