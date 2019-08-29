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
            if self.hugleftprep():
                startpos = self.robot.pos
            else: return             #prep failed. Cancel left wall hugging

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
        if not (sensors.isFrontBlocked()) and not (sensors.isLeftBlocked()):
            if settings.logging:  
                print("Warning: Left Wall Hugging Cancelled. No adjacent walls found.")
            return False
                    
        #check left wall, return true
        #check no left wall & have front wall. turn right & return true

    """
    To Kevin: 
        explorer.py should still call the below methods. 
            Example: sensors.isFrontBlocked() is similar to checkFrontExplored().
        
        
    public void sendAndroid(Grid grid, Robot robot, boolean realRun) {
		if (realRun) {
			SocketMgr.getInstance().sendMessage(CALL_ANDROID,
                    MessageMgr.generateMapDescriptorMsg(grid.generateMapDescriptor1(), grid.generateMapDescriptor2(), robot.getCenterPositionX(), robot.getCenterPositionY(), robot.getDirection()));
		}
	}
    ^Currently considering creating an Interface class to handle robot-android communications. Subject to change
    
    
    checkFrontExplored() moved to sensors.py
    checkLeftRangeExplored() moved to sensors.py
    checkRightRangeExplored() moved to sensors.py
    leftSideNotFullyExplored() moved to sensors.py
    rightSideNotFullyExplored() moved to sensors.py

    isOutOfArena() removed. deemed unnecessary
    isInEndingZone() removed. deemed unnecessary
    
    handleMoveForward() moved to coordinator.py
        """
            
