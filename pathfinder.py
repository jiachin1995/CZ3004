import settings

class Pathfinder:
    """
    Pathfinder class. Used to find shortest path.
         
    Attributes:
        start: Start coordinates of arena. [1,1]
        goal: Goal coordinates of arena. [13,18]
        map: Map object
        weightmap: Weights of paths from goal. The further the tile from goal, the heavier the weights
    """
    start = [1, 1]
    goal = [13, 18]
    
    map = None
    weightmap = []
    
    def __init__(self, map):
        """ 
        Constructor. 
            
        Args:
            map: Map object.
        """  
        self.map = map
    
    
    def bfs(self,pos, end, weight=0, checklist=[]):
        """ 
        Gives weight of tiles from goal. Starts from goal and performs breadth first search on adjacent tiles.
        The further the tile from goal, the heavier the weight of the tiles.
            
        Args:
            pos: [x,y] coordinates. Starting coordinates. bfs() ends when this tile is searched.
            end: [x,y] coordinates. Goal of shortest path search. Weight = 0
            weight: Weight of current tile
            checklist: Do not provide an argument. List of tiles to check
        """ 
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
           
    def findpath(self, start=start, goal=goal, waypoint=None, orientation=0):
        """
        Call this method to begin shortest path exploration.
        
        findpath() has 2 steps:
        1. Using breadth-first-search, find weights of all tiles until goal is reached, searching from goal to start (reversed)
        2. Afterwards, from start to goal, find shortest path, taking into account turning
        
        Args:
            start: [x,y] coordinates. Defaults to [1,1]. Start position of shortest path search.
            goal: [x,y] coordinates. Defaults to [13,18]. Goal of shortest path search.
            waypoint: [x,y] coordinates. Waypoint for shortest path search to bypass.
            orientation: Integer. Defaults to 0. Direction where the robot is currently facing.
        
        """
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
        path, directions = self.findLeastTurns(pos=start, orientation=orientation)
        
        
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
        Reads weights map to find straightest & shortest path. Minimises turning.
        
        Recursive function. Ends when goal is reached.
          
        Args:
            pos: [x,y] coordinates. Initial argument should be initial position of robot.
            orientation: Integer. Initial argument should be initial direction where robot is facing.
            path: List. Do not provide an argument. Shortest path, in coordinates form.
            directions: List. Do not provide an argument. Shortest path, in movement form.  
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
        """
        Returns the coordinates of next Tile by reading current position and orientation.
        
        Args:
            pos: [x,y] coordinates. 
            orientation: Integer. 
        """
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
        """
        Updates weight map by marking all obstacles and a 3x3 area around obstacle as untraversible.

        """
    
        for y in range(1,19):
            for x in range(1,14):
                if self.map.getTile([x,y]) != 0: 
                    #if obstacle/unexplored is found, mark as untraversible in a 3x3 area around it
                    for i in range(-1,2):
                        self.weightmap[y-1][x+i] = -1
                        self.weightmap[y][x+i] = -1
                        self.weightmap[y+1][x+i] = -1
                    

    def optimise_diagonals(self, directions):
        """unimplemented. Method to optimse movement by adding in diagonal movement"""
        #consider that square diagonals are 1.4x the width
        pass
        
        return directions
        
    def printweightmap(self):
        """
        Prints weight map.
        
        Values are:
            ? - Tile is has unknown weight
            X - Tile is untraversible
            Integer - Weight of Tile. Goal has 0 weight. The further the tile from goal, the heavier the weight.
        """
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
        """
        Resets weight map. Removes all weight so that new shortest path can be found.
        """
        #Initialise weight map to store tile distances. Untraversible tiles are marked with -1/X.
        self.weightmap = [[None for _ in range(15)] for _ in range(20)]
        
        #mark edges as untraversible
        self.weightmap[0] = [-1 for _ in range(15)]
        self.weightmap[19] = [-1 for _ in range(15)]
        for row in self.weightmap:
            row[0] = -1
            row[14] = -1
            
        self.mark_untraversible()
    
            
            