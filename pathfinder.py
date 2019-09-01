import settings

class Pathfinder:
    start = [1, 1]
    goal = [13, 18]
    
    map = []
    weightmap = []
    
    def __init__(self, map):
        self.map = map
    
    
    def bfs(self,pos, end, weight=0, checklist=[]):
        x,y = pos
    
        self.weightmap[y][x] = weight
    
        #check if end is reached
        if pos == end:
            checklist.clear()       #need to be cleared. apparently bfs() will keep checklist if not cleared
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
    def findpath(self, start=start, goal=goal, waypoint=None):
        #ensure that weightmap is clean
        self.resetweights()
    
        #update weightmap, the goal will have weight 0
        if waypoint:
            self.bfs(waypoint, start)    #search from start to waypoint
        else:
            self.bfs(goal, start)        #search from start to goal

        if settings.logging:
            self.printweightmap()
    
            
        #find fastest pat with least turns. path contains route in coordinates form. directions contains route with {top,left,bottom,right}
        path, directions = self.findLeastTurns(pos=start)
        
        
        #If there is waypoint, we must now search from waypoint to goal
        if waypoint:
            #reset weights before doing bfs again
            self.resetweights()
            
            self.bfs(goal, waypoint)
            if settings.logging:
                print("====== Waypoint Weights ======= \n")
                self.printweightmap()     
            path2, directions2 = self.findLeastTurns(pos=path[-1], orientation=directions[-1])
            path += path2
            directions += directions2
      
      
        """unimplemented. Method to optimse movement by adding in diagonal movement"""
        if settings.optimise_diagonals:
            directions = self.optimise_diagonals(directions)
      
        if settings.logging:  
            print("=========== Path & Directions ============")
            print(path)
            print(directions)
            
        return [path,directions]
        
        

    def findLeastTurns(self, pos, orientation=0, path=[], directions = []):
        """
            Follow weights to find shortest path. Minimises turning.
          
        """
        path.append(pos)
        directions.append(orientation)
                
        x,y = pos
        currentweight = self.weightmap[y][x]
        
        #return if goal is reached
        if currentweight == 0:
            #remove extra direction. The first direction is extraneous
            directions.pop(0)
            
            
            import copy
            results =  [
                copy.deepcopy(path),
                copy.deepcopy(directions)
            ]
                  
            #need to be cleared. apparently method will keep lists if not cleared                  
            path.clear()
            directions.clear()
            
            return results
        
        #order of tiles to search. For example, if facing right, search right, top then bottom.
        turns_dict = {
                0: [0,1,3,2], 
                1: [1,0,2,3],
                2: [2,1,3,0],
                3: [3,0,2,1] 
            }
        turns = turns_dict[orientation]
        
        while turns:
            orient = turns.pop(0)
            nextpos = self.getnextTile(pos, orient)

            if self.weightmap[nextpos[1]][nextpos[0]] == currentweight -1:
                break
                
        return self.findLeastTurns(nextpos, orient, path=path, directions=directions)
        

    def getnextTile(self, pos, orientation):
        x = pos[0]
        y = pos[1]
        
        #dictionary of nextTile. For example, if facing right, return tile on right.
        nextTile_dict = {
            0: [x, y+1],
            1: [x+1, y],
            2: [x, y-1],
            3: [x-1, y]         
        }
        nextTile = nextTile_dict[orientation]
        
        return nextTile

        
    def mark_untraversible(self):
        for y in range(1,19):
            for x in range(1,14):
                if self.map.getTile([x,y]) != 0: 
                    #if obstacle/unexplored is found, mark as untraversible in a 3x3 area around it
                    for i in range(-1,2):
                        self.weightmap[y-1][x+i] = -1
                        self.weightmap[y][x+i] = -1
                        self.weightmap[y+1][x+i] = -1
                    

    def optimise_diagonals(self, directions):
        #consider that square diagonals are 1.4x the width
        pass
        
        return directions
        
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
    
    def resetweights(self):
            
        #Initialise weight map to store tile distances. Untraversible tiles are marked with -1/X.
        self.weightmap = [[None for _ in range(15)] for _ in range(20)]
        
        #mark edges as untraversible
        self.weightmap[0] = [-1 for _ in range(15)]
        self.weightmap[19] = [-1 for _ in range(15)]
        for row in self.weightmap:
            row[0] = -1
            row[14] = -1
            
        self.mark_untraversible()
    
            
            