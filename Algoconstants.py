
"""Predefined constant values to be used in the algorithms """


"""Possible constant values to be considered, i will just put here first, jia chin!!"""


import numpy as np

# DIRECTIONS
NORTH = 1               #0   -- im using 0,1,2,3
EAST = 2                #1
SOUTH = 3               #2
WEST = 4                #3

# MOVEMENTS
LEFT = "A"
RIGHT = "D"
FORWARD = "W"

# MAP CONSTANTS
MAX_ROWS = 20               #15
MAX_COLS = 15               #20
START = np.asarray([18, 1])             # (1,1)
GOAL = np.asarray([1, 13])              # (13,18)
BOTTOM_LEFT_CORNER = START
BOTTOM_RIGHT_CORNER = np.asarray([18,13])
TOP_RIGHT_CORNER = GOAL
TOP_LEFT_CORNER = np.asarray([1,1]
