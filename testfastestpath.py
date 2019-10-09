from arduino import Arduino
from coordinator import Coordinator

c = Coordinator()

self.arduino = Arduino()
self.arduino.connect()

time.sleep(1)

coordinator.arduino = arduino


text = input("Press enter to start fastest path")


#tests- run only one of them per test. start from 1,1. goal is 13,18
#test 1
c.forward(5)            #1,6
c.turnRight()
c.forward(12)           #13,6
c.turnLeft()            
c.forward(12)           #13,18

#test 2
# c.forward(3)            #1,4
# c.turnRight()
# c.forward(3)            #4,4
# c.turnLeft()
# c.forward(5)            #4,9
# c.turnRight()
# c.forward(9)            #13,9
# c.turnLeft()            
# c.forward(9)             #13,18

self.arduino.close()