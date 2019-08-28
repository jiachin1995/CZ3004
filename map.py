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
            
            
        Attributes:
            map: a 15x20 array. Contains None, 0 or 1 as values.
            start: Centre of 3x3 start area. Default = [1,1]
            goal: Centre of 3x3 goal area. Default = [13,18]
    """
    map = []
    start = [1, 1]
    goal = [13, 18]

    def __init__(self, load=None, ):
        self.x = 'Hello'
        
        if load:
            self.load(load)
            
        #if nothing to load, create empty 15x20 map
        else:
            self.map = [[None for _ in range(15)] for _ in range(20)]
        
        
    def convert(self):
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
        
    def getTile(self, pos):             #expects [x,y] as arguments
        return self.map[pos[1]][pos[0]]
            
    def load(self, loadobject):
        """ Loads map. Accepts 3 types of inputs.
            
        Args:
            loadobject: Accepts 3 types of inputs. String, List of length 2, 15x20 List
            loadobject-String: Name of txt file to load. Example: "maze.txt".
            loadobject-List_of_length_2: Assumes list contains 2 bit/byte strings. [exploration_bits, exploration_contents]. Accepts both bits & bytes.
            loadobject-15x20_List: Assumes list to contain map. Sets map=loadobject. List should be of size [20][15].


        Raises:
            Exception: invalid loadobject argument
        """
    
        #if loadobject is string, assume it is filepath
        if isinstance(loadobject, str):
            with open(loadobject, 'r') as file:
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
                        self.map[y][x] = exploration_contents.pop(0)
                    else:
                        self.map[y][x] = '0'
                    
        if settings.logging:
                self.printmap()
        
        return
    
    def printmap(self):
        """Prints map. Bottom left corner is [0,0] & contains start corner. Top right is [14,19] & contains goal"""
        print("======== VirtualMap ========")
        
        for row in reversed(self.map):
            for val in row:
                if val is None:
                    print(" ?", end ='')
                else:
                    print(" "+str(val), end ='')
            print("\n")
    
    
    def save(self, filepath):
        exploration, exploration_contents  = self.convert()
        
        with open(filepath, 'w') as file:
            #write exploration bit strings
            file.write('explored/unexplored bit strings \n')
            file.write(exploration + "\n")
            
            #write exploration contents bit strings
            file.write('map contents bit strings \n')
            file.write(exploration_contents + '\n')

    def setTile(self, pos, value):
        self.map[pos[1]][pos[0]] = value
        
    def setTiles(self, poslist, valuelist):
        for pos, val in zip(poslist,valuelist):
            self.map[pos[1]][pos[0]] = val