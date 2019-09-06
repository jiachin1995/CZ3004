def setup():
  size (600,700)
  
def draw(): 
  background(255)
  x,y = 0,0
  for row in robot.rMap:
    for col in row:
      if col == -1:    """-1 refers to the start of the map"""
        fill (255, 0 , 0)
      elif col == None:  """
        fill (150, 150, 150)
      elif col == 1:
        fill (0,0,0)
      else:
        fill (255)
      rect(x,y,w,w)
      x = x + w
   y = y+w
   x = 0

myrobot.display()
myrobot.explore()
delay(100)

   
  
           
