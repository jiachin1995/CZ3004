import settings

class Pathfinder:
    start = [1, 1]
    goal = [13, 18]
    
    map = []
    weightmap = []
    
    def __init__(self, map):
        self.map = map
    
        #Initialise weight map to store tile distances. Untraversible tiles are marked with -1/X.
        self.weightmap = [[None for _ in range(15)] for _ in range(20)]
        #mark edges are untraversible
        self.weightmap[0] = [-1 for _ in range(15)]
        self.weightmap[19] = [-1 for _ in range(15)]
        for row in self.weightmap:
            row[0] = -1
            row[14] = -1
            
            
        self.mark_untraversible()
    
    
    def bfs(self,pos, end, weight, checklist=[]):
        x = pos[0]
        y = pos[1]
    
        self.weightmap[y][x] = weight
    
        #check if end is reached
        if pos == end:
            return
        
        
        #else, check 4 cardinal directions for weights. If absent, search those tiles
        neighbours = [
                [x,y+1],
                [x+1,y],
                [x,y-1],
                [x-1,y]
            ]
        for coords in neighbours:
            if self.weightmap[coords[1]][coords[0]] is None:
                self.weightmap[coords[1]][coords[0]] = weight+1
            
                #add tiles to list to be checked
                checklist.append(
                        {
                        'pos': coords,
                        'end': end,
                        'weight':weight+1,
                    }
                )
        
        if checklist:
            self.bfs(**checklist.pop(0), checklist=checklist)
        
    """
        findpath() has 2 steps:
        1. Using breadth-first-search, find weights of all tiles until goal is reached, searching from goal to start (reversed)
        2. Afterwards, from start to goal, find shortest path, taking into account turning
    """
    def findpath(self, start=start, goal=goal):
        self.bfs(self.goal, self.start, 0)
        
    
        if settings.logging:
            self.printweightmap()
        
    def mark_untraversible(self):
        for y in range(1,19):
            for x in range(1,14):
                if self.map.getTile([x,y]) == '1': 
                    #if obstacle is found, mark as untraversible in a 3x3 area around it
                    for i in range(-1,2):
                        self.weightmap[y-1][x+i] = -1
                        self.weightmap[y][x+i] = -1
                        self.weightmap[y+1][x+i] = -1
                    

        
    def printweightmap(self):
        print("======== WeightMap ========")
        
        for row in reversed(self.weightmap):
            for val in row:
                if val is None:
                    print("  ?", end ='')
                elif val is -1:
                    print("  X", end ='')
                else:
                    print(" %2s" % str(val), end ='')
            print("\n")
    