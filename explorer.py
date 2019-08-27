import settings

class Explorer:
    robot = None
    state = "Initial"

    def __init__(self, robot):
        self.robot = robot
        if settings.logging:  
            print("====== Starting Explorer =======")
            print("New State: " + self.state)
    
    def start(self):

        self.hugleftwall()
        
    def hugleftwall(self, turns_count = 0, startpos = None):
        #run once when first called
        if startpos == None:
            self.hugleftprep()
            startpos = self.robot.pos

        left, middle, right = sensors.getFront()
        front, back = sensors.getLeft()
        
        x, y = self.robot.pos
        #baseline refers to the left,middle & right (from the robot's perspective) tiles the robot is occupying. 
        #baseline_dict contains the tiles to search. For example, if facing right, search top, middle & bottom tiles
        baseline_dict = {
            0: [[x-1,y],[x,y],[x+1,y]],
            1: [[x,y+1],[x,y],[x,y-1]],
            2: [[x+1,y],[x,y],[x-1,y]],
            3: [[x,y-1],[x,y],[x,y+1]]
        }
        baseline = baseline_dict[robot.orientation]
        
    def hugleftprep(self):
        self.state = "LeftWallHugging"
        if settings.logging:  
              print("New State: " + self.state)   
        if !(sensors.isFrontBlocked()) and !(sensors.isLeftBlocked()):
            if settings.logging:  
                print("Warning: Left Wall Hugging Cancelled. No adjacent walls found.")
            return