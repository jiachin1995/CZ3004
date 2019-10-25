import settings

class Islandsfinder:
    """
    Goal of this class is to find groups of obstacles(islands).
    
    """
    islands = None
    
    map = None
    islands_map = None
    
    def __init__(self, map):
        """ 
        Constructor. 
            
        Args:
            map: Map object.
        """  
        self.map = map
        self.createIslandsMap()
        
        self.getIslands()
        self.removeEdgeIslands()
        
        self.updateIslandsMap()
        

      
    def addIsland(self, obs_list, isle_list, isle=[]):
        obs = obs_list.pop(0)
        check_isles = [obs]
        isle = [obs]
        
        while check_isles:
            x,y = check_isles.pop(0)
            
            neighbours = [
                [x-3,y+3],[x-2,y+3],[x-1,y+3],[x,y+3],[x+1,y+3],[x+2,y+3],[x+3,y+3],
                [x-3,y+2],[x-2,y+2],[x-1,y+2],[x,y+2],[x+1,y+2],[x+2,y+2],[x+3,y+2],
                [x-3,y+1],[x-2,y+1],[x-1,y+1],[x,y+1],[x+1,y+1],[x+2,y+1],[x+3,y+1],
                [x-3, y ],[x-2, y ],[x-1, y ],[x, y ],[x+1, y ],[x+2, y ],[x+3, y ],
                [x-3,y-1],[x-2,y-1],[x-1,y-1],[x,y-1],[x+1,y-1],[x+2,y-1],[x+3,y-1],
                [x-3,y-2],[x-2,y-2],[x-1,y-2],[x,y-2],[x+1,y-2],[x+2,y-2],[x+3,y-2],
                [x-3,y-3],[x-2,y-3],[x-1,y-3],[x,y-3],[x+1,y-3],[x+2,y-3],[x+3,y-3],
            ]
            
            for n in neighbours:
                x,y = n
                if x<0 or x>14 or y<0 or y>19:
                    continue
            
                if n in obs_list: 
                    check_isles.append(n)
                    obs_list.remove(n)
                    isle.append(n)
                    

        isle_list.append(isle)
      
        if obs_list:
            self.addIsland(obs_list,isle_list)
      

      
    def createIslandsMap(self):
        self.islands_map = [[set() for _ in range(15)] for _ in range(20)]
    
    def findroute(self,id):
        isle = self.islands[id]
        pos = self.getposbyId(id)
        
        orientation = self.getOrient(isle,pos)
                    
        return [pos, orientation]
    
    def getposbyId(self, id):
        for y in range(0, 20):              #search adjacent free space from bottom to top.
            for x in range(0,15):           #search ^^ from left to right
                if type(self.islands_map[y][x]) is set and id in self.islands_map[y][x]:
                    pos = [x,y]
                    return pos
    
    def getIslands(self):
        """
        Return all obstacles as islands(groups of adjacent obstacles).
        Each island is stored as a list of obstacles
        self.islands contain a list of islands
        """
        if self.islands:
            return self.islands
        
        isle_list = []
        obs_list = self.getObstacles()
        self.addIsland(obs_list, isle_list)
        
        self.islands = isle_list
        
        return isle_list

    def getObstacles(self):
        """Return all obstacles in a list"""
        obs_list = []
        for y in reversed(range(0, 20)):        #we reverse this as we want the islands to be ordered from top to bottom
            for x in reversed(range(0,15)):     #we reverse this as we want the islands to be ordered from right to left
                if self.map.getTile([x,y]) == 1: 
                    obs_list.append([x,y])
       
        return obs_list
      
    def getOrient(self, isle, pos):
        x,y = pos
        
        search_dict = {
            0:[x,y+2],
            1:[x+2,y],
            2:[x,y-2],
            3:[x-2,y],
        }
        
        for key, val in search_dict.items():
            if val in isle:
                return key 
      
    def nextIsland(self):
        for id in range(len(self.islands)):
            pos, orientation = self.findroute(id)
            
            yield [pos,orientation]
        
    def printislandsmap(self):
        """
        Prints islands map.
        
        Values are:
            None - No content
            -1 - tile is an island
            list - contains the perimeter of the island. contains island id
        """
        print("======== Island Map ========")
        
        for row in reversed(self.islands_map):
            for val in row:
                if val == set():
                    print("     ?", end ='')
                elif val is -1:
                    print("     X", end ='')
                else:
                    print(" %5s" % str(val), end ='')
            print("\n")
        
    def removeEdgeIslands(self):
        edge_list = []
        for isle in self.islands:
            for obst in isle:
                x,y = obst
                if x<3 or x>11 or y<3 or y>16:
                    if settings.logging:
                        print("isle removed {}".format(isle))
                    edge_list.append(isle)
                    break
        
        for item in edge_list:
            self.islands.remove(item)
        
    def updateIslandsMap(self):
        #update map. 
        id = 0
        
        for island in self.islands:
            for obst in island:
                x,y = obst
                self.islands_map[y][x] = -1
                
                adjacent_spaces = [
                    [x,y+2],
                    [x+2,y],
                    [x,y-2],
                    [x-2,y],
                ]
                
                for pos in adjacent_spaces:
                    if self.map.is_freespace(pos):
                        self.islands_map[pos[1]][pos[0]].add(id)
                        
            id += 1
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                
        
                