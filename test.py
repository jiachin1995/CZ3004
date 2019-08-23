from map import Map
    
    
map = Map()
#map.printmap()

map.save("test.txt")
map.load("school_example.txt")
#map.load([0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 0x0])

# arr = [["a"]*15] *20
# map.load(arr)

#map.convert()