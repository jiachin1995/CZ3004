import settings

class Map:
    """
        Map class. Creates a 15x20 map. 
        
        Length(top-bottom) of map is 20, represented by y-coordinates. Width(left-right) is 15, represented by x-coordinates.
        Bottom left corner tile of map is 0,0. Top right is 14,19.
        Start coordinates is [1,1]. End is [13,18]
        
        Each tile has values:
            1. None - unexplored
            2. 0 - explored, no obstacle
            3. 1 - explored, has obstacle
            4. -1 - Error. Out of range
            
            
        Attributes:
            map: a 15x20 array. Contains None, 0 or 1 as values.
            start: Centre of 3x3 start area. Default = [1,1]
            goal: Centre of 3x3 goal area. Default = [13,18]
    """
    map = []
    start = [1, 1]
    goal = [13, 18]

    islands = None

    def __init__(self, load=None, ):
        """
        Constructor. Creates a 15x20 map. 
        
        Args:
            load: Expects a load object. If left empty, create a 100% unexplored map. Otherwise, calls self.load() on load object. Refer to map.load()
        """
        self.x = 'Hello'
        
        if load:
            self.load(load)
            
        #if nothing to load, create empty 15x20 map
        else:
            self.map = [[None for _ in range(15)] for _ in range(20)]
        
        
    def convert(self):
        """
        Converts map object to bytes. Follows the MDF as specified by NTU MDP.
        """
    
        expl = ''
        expl_contents = ''
    
        for row in self.map:
            for val in row:
                if val is None:
                    expl += '0'
                else:
                    expl += '1'
                    expl_contents += str(val)
             
        #padding for exploration bits
        expl = "11" + expl + "11"
        
        #padding for exploration contents, pad to multiples of 8
        if len(expl_contents) % 8 != 0:
            leftover_bits = len(expl_contents) % 8
            expl_contents += "0" * (8 - leftover_bits)
              
        if settings.logging:
            print("=======Convert() in bits=======")
            print(expl)
            print(expl_contents)
            
        #if true, return map format in hex
        if settings.mapformat_returntype_isHex:
            #padding for expl_contents, to keep leading zeroes
            expl_contents = "1111" + expl_contents      
        
            #convert to hex
            expl_hex = hex(int(expl, 2))
            expl_contents_hex = hex(int(expl_contents, 2))
            
            #remove padding for exploration contents
            expl_contents_hex = "0x" + str(expl_contents_hex)[3:]
            
            if settings.logging:
                print("=======Convert() in hex=======")
                print(expl_hex)
                print(expl_contents_hex)
                
            return [str(expl_hex), expl_contents_hex]

        return [expl, expl_contents]

    def explored_percent(self):
        """
        Returns the percentage of explored map. Returns float from 0.0 to 1.0
        """
        totalTiles = 300.0
        expl_count = 0.0
        
        for row in self.map:
            for val in row:
                if val is not None: expl_count += 1.0

        return expl_count/totalTiles
        
    def getUnexploredTile(self):
        """
        Iterates through the map to find the first unexplored tile. Starts from [0,0],[1,0],[2,0]... to [13,19],[14,19]
        """
        for y in range(0, 20):
            for x in range(0,15):
                if self.getTile([x,y]) is None: 
                    return [x,y]
        
    def findAdjacentFreeSpace(self, tile):
        x,y = tile
        dict = {
            0: [x,y+2],
            1: [x+2,y],
            2: [x,y-2],
            3: [x-2,y],
        }
        
        #check right
        centre = dict[1]
        if self.is_freespace(centre):
            return [centre, 3]
            
        #check left
        centre = dict[3]
        if self.is_freespace(centre):
            return [centre, 1]
            
        #check bottom
        centre = dict[2]
        if self.is_freespace(centre):
            return [centre, 0]
            
        #check top
        centre = dict[0]
        if self.is_freespace(centre):
            return [centre, 2]
            
        
        
    def findSpaceInRow(self, y, toRight=True):
        """
        Given horizontal row, find a space that robot can occupy in said row. 
        Looks for a 3x3 unobstructed area from left to right.
        
        Args:
            toRight: Default is True. If false, searches for 3x3 unobstructed area from right to left.
        """
        
        if toRight:
            searchlist = range(0,15)
        else:
            searchlist = reversed(range(0,15))
        
        #find 3 consecutive columns that are free
        count = 0
        for x in searchlist:
            #if obstacle/unexplored is found, skip this col
            if self.getTile([x, y+1]) != 0 or self.getTile([x, y]) != 0 or self.getTile([x, y-1]) != 0: 
                count = 0
                continue
            
            else: 
                count += 1
                if count == 3:          #free 3x3 space found. return centre of 3x3
                    if toRight:
                        x = x-1
                    else:
                        x = x+1
                        
                    return [x, y]
       
    def getObstacles(self):
        """Return all obstacles in a list"""
        obs_list = []
        for y in range(0, 20):
            for x in range(0,15):
                if self.getTile([x,y]) == 1: 
                    obs_list.append([x,y])
       
        return obs_list
        
    def getIslands(self):
        """Return all obstacles as islands(groups of adjacent obstacles)"""
        if self.islands:
            return self.islands
        
        isle_list = []

        obs_list = self.getObstacles()
        for obs in obs_list:
            self.addIsland(obs, obs_list, isle_list)
        
        return isle_list
        
    def addIsland(self, obs, obs_list, isle_list, isle=[]):
        isle = [obs]
        obs_list.remove(obs)
        
        bool = True
        while bool:
            bool = False
            x,y = obs
            
            neighbours = [
                [x,y+1],
                [x,y-1],
                [x+1,y],
                [x-1,y],
            ]
            
            for n in neighbours:
                if n in obs_list:
                    obs = n
                    obs_list.remove(obs)
                    isle.append(obs)
                    
                    bool=True

        isle_list.append(isle)
        
    def getTile(self, pos):             
        """
        Given x,y coordinates, return value at that tile
        
        Args:
            pos: Expects [x,y] as arguments
        """
        x,y = pos
        if x<0 or x>14:
            return -1
        if y<0 or y>19:
            return -1
            
        return self.map[pos[1]][pos[0]]
      
    def is_explored(self):
        """
        Returns True if map is entirely explored
        """
        for row in self.map:
            for val in row:
                if val is None: return False
        return True
        
    def is_freespace(self, centretile):
        x, y = centretile
        
        for i in range(-1,2):
            for j in range(-1,2):
                if self.getTile([x+i,y+j]) != 0:
                    return False

        return True

        
    def is_rowexplored(self, y):
        """
        Given y axis, return True if entire row is explored.
        
        Args:
            y: y-axis. Expects an integer 
        """
        for val in self.map[y]:
            if val is None: return False
        
        return True
      
      
    def load(self, loadobject):
        """ Loads map. Accepts 3 types of inputs.
            
        Args:
            loadobject: Accepts 3 types of inputs. String, List of length 2, 15x20 List. <see below>
            loadobject-String: Name of txt file to load. Example: "maze.txt".
            loadobject-List_of_length_2: Assumes list contains 2 bit/byte strings. [exploration_bits, exploration_contents]. Accepts both bits & bytes.
            loadobject-15x20_List: Assumes list to contain map. Sets map=loadobject. List should be of size [20][15].


        Raises:
            Exception: invalid loadobject argument
        """
        
        """matched Code === loadingFromDisk()"""
    
        #if loadobject is string, assume it is filepath
        if isinstance(loadobject, str):
            import os
            filepath = os.path.join("mazes", loadobject)
            
            with open(filepath, 'r') as file:
                lines = file.readlines()
                
                #input text file are expected to have required bits on line 2 and 4
                expl = lines[1]
                expl_contents = lines[3]
                
            #padding for expl_contents, to keep leading zeroes
            if expl_contents[:2] == '0x':
                expl_contents = "0xf" + expl_contents[2:]
                #create bit string from exploration_contents, excluding leading '0b1111'
                expl_contents = bin(eval(expl_contents))[6:]
            elif expl_contents[:2] == '0b':
                expl_contents = "0b1" + expl_contents[2:]
                #create bit string from exploration_contents, excluding leading '0b1'
                expl_contents = bin(eval(expl_contents))[3:]
            else:
                raise Exception('exploration content string is not in bits or bytes')
                
            bits_list = [
                        bin(eval(expl))[4:-2],  #return exploration as bit string, excluding leading '0b11' and tail '11'
                        expl_contents
                    ]
            
            self._loadmap(bits_list)
                
            return
            
        elif isinstance(loadobject, list):
            #if loadobject is list with length 2, assume it is exploration & content bits, in string dtype
            if len(loadobject) == 2:
                self._loadmap(loadobject)
                
                return
                
            #if loadobject is list with length 20, assume it is a map
            if len(loadobject) == 20:
                if len(loadobject[0]) == 15:
                    self.map = loadobject
                    
                    if settings.logging:
                        self.printmap()
                    
                    return
                
        raise Exception('invalid loadobject argument')
    
    def _loadmap(self, loadbits_list):
        #convert string to list
        exploration = list(loadbits_list[0])
        exploration_contents = list(loadbits_list[1])
        
        #create map filled with None/unexplored
        self.map = [[None for _ in range(15)] for _ in range(20)]
        
        for y in range(20):
            for x in range(15):
                if exploration.pop(0) == '1':
                    #check if list is empty. if empty, continue filling explored areas
                    if exploration_contents:
                        self.map[y][x] = int(exploration_contents.pop(0))
                    else:
                        self.map[y][x] = 0
                    
        if settings.logging:
                self.printmap()
        
        return
    
    def printmap(self, robot = None):
        """
        Prints map. Bottom left corner is [0,0] & contains start corner. Top right is [14,19] & contains goal
        
        Args:
            robot: Defaults to None. If robot is given, prints map with robot position and orientation
        """
        print("======== VirtualMap ========")
        
        if robot:
            self.printmapwithRobot(robot)
        else:
        
            for row in reversed(self.map):
                for val in row:
                    if val is None:
                        print(" ?", end ='')
                    else:
                        print(" "+str(val), end ='')
                print("\n")
    
    def printmapwithRobot(self, robot):
        """
        Prints map with robot. Bottom left corner is [0,0] & contains start corner. Top right is [14,19] & contains goal.
        Called from printmap if robot argument is supplied.
        
        Args:
            robot: Robot object. Prints map with robot position and orientation
        """
        orient_dict = {
            0: '^',
            1: '>',
            2: 'V',
            3: '<'
        }
        orient = orient_dict[robot.orientation]
        
        x,y = robot.pos
        pos_list = [
            [x-1,y-1],
            [x-1,y],
            [x-1,y+1],
            [x,y-1],
            [x,y],
            [x,y+1],
            [x+1,y-1],
            [x+1,y],
            [x+1,y+1],
        ]
    
        for y in reversed(range(20)):
            for x in range(15):
                if [x,y] in pos_list:
                    print(" "+orient, end ='')
                elif self.getTile([x,y]) is None:
                    print(" ?", end ='')
                else:
                    print(" "+str(self.getTile([x,y])), end ='')
            print("\n")

    
    
    def save(self, filepath):
        """
        Saves map to file. 
        
        Args:
            filepath: String. Expects name of file to be written to.
        """
        import os
        filepath = os.path.join("mazes", filepath)
    
        exploration, exploration_contents  = self.convert()
        
        with open(filepath, 'w') as file:
            #write exploration bit strings
            file.write('explored/unexplored bit strings \n')
            file.write(exploration + "\n")
            
            #write exploration contents bit strings
            file.write('map contents bit strings \n')
            file.write(exploration_contents + '\n')

    def setTile(self, pos, value):
        """
        Sets selected Tile to given value. 
        
        Args:
            pos: Expects [x,y] list object. Coordinates of tile to change.
            value: New value of tile.
        """
        x,y = pos
        if x<0 or x>14:
            return
        if y<0 or y>19:
            return
        
        self.map[y][x] = value
        
    def setTiles(self, poslist, valuelist):
        """
        Sets selected list of Tiles to given values. 
        
        Args:
            poslist: Expects list of [x,y] coordinates. List of tile coordinates to change.
            valuelist: List of values of tiles
        """
            
        for pos, val in zip(poslist,valuelist):
            x,y = pos
            if x<0 or x>14:
                continue
            if y<0 or y>19:
                continue
            self.map[pos[1]][pos[0]] = val
	
