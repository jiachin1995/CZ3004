import settings

class Map:
    map = []
    start = [1, 1]
    goal = [13, 18]

    def __init__(self, load=None, ):
        self.x = 'Hello'
        
        if load:
            self.load(load)
            
        #if nothing to load, create empty 15x20 map
        else:
            self.map = [[0 for _ in range(15)] for _ in range(20)]
        
        
    def convert(self):
        expl = ''
        expl_contents = ''
    
        for row in reversed(self.map):
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
            expl_contents = "11" + expl_contents      
        
            #convert to hex
            expl_hex = hex(int(expl, 2))
            expl_contents_hex = hex(int(expl_contents, 2))
            
            #remove padding for exploration contents
            expl_contents_hex = "0x" + str(expl_contents_hex)[4:]
            
            if settings.logging:
                print("=======Convert() in hex=======")
                print(expl_hex)
                print(expl_contents_hex)
                
            return [str(expl_hex), expl_contents_hex]

        return [expl, expl_contents]
        
            
    def load(self, loadobject):
        #if loadobject is string, assume it is filepath
        if isinstance(loadobject, str):
            with open(loadobject, 'r') as file:
                lines = file.readlines()
                
                expl = lines[1][4:-2]
                expl_contents = lines[3][2:]
                
                bits_list = [
                            expl,
                            expl_contents
                        ]
            
            self.loadmap(bits_list)
                
            return
            
        elif isinstance(loadobject, list):
            #if loadobject is list with length 2, assume it is exploration & content bits, in string dtype
            if len(loadobject) == 2:
                self.loadmap(loadobject)
                
                return
                
            #if loadobject is list with length 20, assume it is map
            if len(loadobject) == 20:
                if len(loadobject[0]) == 15:
                    self.map = loadobject
                    
                    if settings.logging:
                        self.printmap()
                    
                    return
                
        raise Exception('invalid loadobject argument')
    
    def loadmap(self, loadbits_list):
        #convert string to list
        exploration = list(loadbits_list[0])
        exploration_contents = list(loadbits_list[1])
        
        print(exploration)
        print(exploration_contents)
        
        #create map filled with None
        self.map = [[None for _ in range(15)] for _ in range(20)]
        
        for y in range(20):
            for x in range(15):
                if exploration.pop(0) == '1':
                    #check if list is empty. if empty, continue filling explored areas
                    if exploration_contents:
                        print([y,x,exploration_contents])
                        self.map[y][x] = exploration_contents.pop(0)
                    else:
                        print([y,x,exploration_contents])
                    
                        self.map[y][x] = '0'
                    
        if settings.logging:
                self.printmap()
        
        return
    
    def printmap(self):
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