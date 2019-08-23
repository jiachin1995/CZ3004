import settings

class Map:
    map = []
    start = [1, 1]
    goal = [13, 18]

    def __init__(self, load=None, ):
        self.x = 'Hello'
        
        if load:
            pass
            
        #if nothing to load, create empty 15x20 map
        else:
            self.map = [[0] * 15] * 20
            
    def printmap(self):
        print("======== VirtualMap ========")
        
        for row in reversed(self.map):
            for val in row:
                print(" "+str(val), end ='')
            print("\n")
        
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
            print(expl)
            print(expl_contents)

        return [expl, expl_contents]
        

    
    def save(self, filepath):
        exploration, exploration_contents  = self.convert()
        
        with open(filepath, 'w') as file:
            #write exploration bit strings
            file.write('explored/unexplored bit strings \n')
            file.write(exploration + "\n")
            #write exploration contents bit strings
            file.write(exploration_contents + '\n')
            file.write('map contents bit strings \n')
