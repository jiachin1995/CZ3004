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
        #update weightmap, the goal will have weight 0
        self.bfs(self.goal, self.start, 0)
        
        if settings.logging:
            self.printweightmap()
            
        #find fastest pat with least turns. path contains route in coordinates form. directions contains route with {top,left,bottom,right}
        path, directions = self.findLeastTurns()
      
        if settings.logging:  
            print("===========Path & Directions============")
            print(path)
            print(directions)
        
        
    """
        Follow weights to find shortest path. minimises turning.
        
        Orientation refers to where the robot is facing:
            0. Top
            1. Right
            2. Bottom
            3. Left
        
    """
    def findLeastTurns(self, pos=start, orientation=0, path=[], directions = []):
        path.append(pos)
        directions.append(orientation)
                
        x = pos[0]
        y = pos[1]
        currentweight = self.weightmap[y][x]
        
        #return if goal is reached
        if currentweight == 0:
            #remove extra direction. The first direction is extraneous
            directions.pop(0)
            return
        
        #order of tiles to search. For example, if facing right, search right, top then bottom.
        if orientation == 0: turns = [0,1,3] 
        if orientation == 1: turns = [1,0,2] 
        if orientation == 2: turns = [2,1,3] 
        if orientation == 3: turns = [3,0,2] 
        
        while turns:
            orient = turns.pop(0)
            nextpos = self.getnextTile(pos, orient)
            if self.weightmap[nextpos[1]][nextpos[0]] == currentweight -1:
                break
                
        self.findLeastTurns(nextpos, orient, path=path, directions=directions)
        
        return [
            path,
            directions
        ]
            
            
        
        
 
    def getnextTile(self, pos, orientation):
        x = pos[0]
        y = pos[1]
    
        if orientation == 0: nextTile = [x, y+1] 
        if orientation == 1: nextTile = [x+1, y]
        if orientation == 2: nextTile = [x, y-1] 
        if orientation == 3: nextTile = [x-1, y] 
        
        return nextTile

        
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
    