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
        if self.state == "Initial": 
            self.hugleftwall()
        
        # while not self.robot.map.is_explored(): 
            # self.spelunk()
            
        #TODO-return to start
        
    def hugleftwall(self, turns = 0, startpos = None):
        print("debug")
        print(self.robot.pos)
        print(turns)
    
        #run once when first called
        if startpos == None:
            if self.hugleftprep():
                startpos = self.robot.pos
            else: return             #prep failed. Cancel left wall hugging
        
        #if left is free, turn left, move forward once
        if not self.robot.sensors.isLeftBlocked():
            self.robot.turnLeft()                #no need to update map cause next step will update instead.
            self.robot.forward()   #in theory, there should be at least one row of free space. 
            turns = (turns + 3) % 4
            
        #elif if front is free, move forward (up to 3)
        elif not self.robot.sensors.isFrontBlocked():
            front,back = self.robot.sensors.getLeft()
            if front != 0: 
                steps = 1        #we go 1 step at a time to find where left wall ends
            else:
                front_terrain = self.robot.sensors.getFront()
                steps = min(front_terrain)      #go as far as possible
                if steps>3: steps = 3           #we do this as we have to check & hug left wall
            
            self.robot.forward(steps)

        #if both failed, turn right
        else:
            self.robot.turnRight()
            turns = (turns + 3) % 4
         
        #check terminate or continue
        #if turns == 0, it means robot is facing starting orientation.
        if turns == 0 and self.robot.pos == startpos: 
            return
        else: 
            self.hugleftwall(turns = turns, startpos = startpos)
        
    def hugleftprep(self):
        """ Prepares robot for left wall hugging algorithm. 
            Expects an adjacent wall before starting.
            
        Args:
            none: no arguments

        Raises:
            Warning: Left Wall Hugging Cancelled. No adjacent walls found.
        """
    
        self.state = "LeftWallHugging"
        if settings.logging:  
              print("New State: " + self.state)   
            
        #if left wall exists, return true
        if self.robot.sensors.isLeftBlocked():
            return True
        #elif front wall exists, turn right and return true
        elif self.robot.sensors.isFrontBlocked():
            self.robot.turnRight()
            
            #Check for T-blocks
            left, middle, right = sensors.getFront()
            if middle==0 and left != 0 and right !=0:
                self.robot.forward()
            
            return True
        else:
            if settings.logging:  
                print("Warning: Left Wall Hugging Cancelled. No adjacent walls found.")
            return False
           
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
 
    
    ***handleMoveForward() should match explorer.hugleftwall(). 
    
    private void handleMoveForward(Grid grid, Robot robot, boolean realRun) {
		if(trustExplored) {
			/*// Checks if need to do U-Turn in front
			if(checkUTurnAhead(grid, robot)) {
				SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "U");
				robot.turn(RIGHT);
				robot.turn(RIGHT);
				
				int numberOfSteps = checkFrontExplored(grid, robot);
				// numberOfSteps: 0
				if(numberOfSteps == 0) {
					justTurned = false;
					System.out.println("Cannot move forward. Obstacles in front");
				} 
				// numberOfSteps: 1-9
				else if(numberOfSteps < 10) {
					SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "ZM0" + String.valueOf(numberOfSteps));
					justTurned = false;
				}
				// numberOfSteps: 10-17
				else {
					SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "ZM" + String.valueOf(numberOfSteps));
					justTurned = false;
				}
				
				// Update the simulator
				if(numberOfSteps != 0) {
					for(int i=0; i<numberOfSteps; i++) {
						robotMovementString+="M";
						robot.move();
					}
				}
				
				// Sense the surrounding
				robot.sense(realRun, true);
				
				// Update Android when there is a move forward
				sendAndroid(grid, robot, realRun);
//				handleMoveForward(grid, robot, realRun);
				
//				if(robot.isObstacleOnRightSide()) {
//					SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
//					robot.turn(LEFT);
//					robot.sense(realRun, true);
//				} else if(robot.isObstacleOnLeftSide()) {
//					SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
//					robot.turn(RIGHT);
//					robot.sense(realRun, true);
//				}
			}*/ 
			// No need to do U-Turn in front, go ahead and move forward
			//else {
//				if(justTurned) {
					int numberOfSteps = checkFrontExplored(grid, robot);
					// numberOfSteps: 0
					if(numberOfSteps == 0) {
						System.out.println("Cannot move forward. Obstacles in front");
					} 
					// numberOfSteps: 1-9
					else if(numberOfSteps < 10) {
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "ZM0" + String.valueOf(numberOfSteps));
					}
					// numberOfSteps: 10-17
					else {
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "ZM" + String.valueOf(numberOfSteps));
					}
					
					// Update the simulator
					if(numberOfSteps != 0) {
						for(int i=0; i<numberOfSteps; i++) {
							robotMovementString+="M";
							robot.move();
						}
					}
					
					// Sense the surrounding
					robot.sense(realRun, true);
					
					// Update Android when there is a move forward
					sendAndroid(grid, robot, realRun);
					
					// Checks if need to do U-Turn in front
					/*if(checkUTurnAhead(grid, robot)) {
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "U");
						robot.turn(RIGHT);
						robot.turn(RIGHT);
						robot.sense(realRun, true);
						
						numberOfSteps = 0;
						numberOfSteps = checkFrontExplored(grid, robot);
						// numberOfSteps: 0
						if(numberOfSteps == 0) {
							System.out.println("Cannot move forward. Obstacles in front");
						} 
						// numberOfSteps: 1-9
						else if(numberOfSteps < 10) {
							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "ZM0" + String.valueOf(numberOfSteps));
						}
						// numberOfSteps: 10-17
						else {
							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "ZM" + String.valueOf(numberOfSteps));
						}
						
						// Update the simulator
						if(numberOfSteps != 0) {
							for(int i=0; i<numberOfSteps; i++) {
								robotMovementString+="M";
								robot.move();
							}
						}
						
						// Sense the surrounding
						robot.sense(realRun, true);
						
						// Update Android when there is a move forward
						sendAndroid(grid, robot, realRun);
//						handleMoveForward(grid, robot, realRun);
						
//						if(robot.isObstacleOnRightSide()) {
//							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
//							robot.turn(LEFT);
//							robot.sense(realRun, true);
//						} else if(robot.isObstacleOnLeftSide()) {
//							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
//							robot.turn(RIGHT);
//							robot.sense(realRun, true);
//						}
					}*/

					
//					if(numberOfSteps > 1) {
//						if(!isInEndingZone(robot.getPositionX(), robot.getPositionY())) {
//							int zoneNumber = getExploringZone(robot.getPositionX(), robot.getPositionY());
//							if(zoneNumber == 2 || zoneNumber == 3) {
//								if(robot.getDirection() != EAST) {
//									if(rightSideNotFullyExplored(grid, robot)) {
//										SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
//										robot.turn(RIGHT);
//										robot.sense(realRun);
//										
//										SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
//										robot.turn(LEFT);
//										robot.sense(realRun, true);
//										
//									}
//								}
//							} else {
//								if(rightSideNotFullyExplored(grid, robot)) {
//									SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
//									robot.turn(RIGHT);
//									robot.sense(realRun);
//									
//									SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
//									robot.turn(LEFT);
//									robot.sense(realRun, true);
//									
//								}
//							}
//						}
//					}
				/*} else {
					// Sensor readings show there is obstacles in front of robot; DO NOT MOVE FORWARD
					if(robot.getFrontCenter() < 2 || robot.getFrontLeft() < 2 || robot.getFrontRight() < 2) {
						// Simulator shows there is no obstacle in front
						if(!robot.isObstacleInfront()) {
							System.out.println("Sensor readings conflict with simulator. Robot is prevented from moving forward.");
							System.out.println("Sensor readings: FL: " + robot.getFrontLeft() + ", FC: " + robot.getFrontCenter() + ", FR: " + robot.getFrontRight());
							// Sense again
							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
							robot.turn(RIGHT);
							robot.sense(realRun);
							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
							robot.turn(LEFT);
							robot.sense(realRun, true);
						}
					}
					// Sensor readings show there is NO obstacles in front of robot
					else {
						// Simulator shows there is obstacle(s) in front
						if(robot.isObstacleInfront()) {
							System.out.println("Sensor readings conflict with simulator. Robot is prevented from moving forward.");
							System.out.println("Sensor readings: FL: " + robot.getFrontLeft() + ", FC: " + robot.getFrontCenter() + ", FR: " + robot.getFrontRight());
							
							// Sense again to correct the front using the left sensors
							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
							robot.turn(RIGHT);
							robot.sense(realRun);
							// Sense again to correct the front using the front sensors
							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
							robot.turn(LEFT);
							robot.sense(realRun, true);
						}
						// No conflict move forward
						else {
							SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "M1");
							//robot.setDetectNextMove(false);
							robotMovementString+="M";
							System.out.println("----------------------Moving Forward----------------------");
							System.out.println(robotMovementString);
							
							// show the robot move forward on the simulator
							robot.move();
							
							

							// Sense the surrounding
							robot.sense(realRun, true);
							
							
							// Update Android when there is a move forward
							sendAndroid(grid, robot, realRun);
							
						}
					}
				}*/
			//}
		} 
		// I do not trust the area I have already explored. Only move 1 step at a time
		else {
			if(uTurnFlagForNoTrustExplored) {
				uTurnFlagForNoTrustExplored = false;
			} else {
				// Sensor readings show there is obstacles in front of robot; DO NOT MOVE FORWARD
				if(robot.getFrontCenter() < 2 || robot.getFrontLeft() < 2 || robot.getFrontRight() < 2) {
					// Simulator shows there is no obstacle in front
					if(!robot.isObstacleInfront()) {
						/*System.out.println("Sensor readings conflict with simulator. Robot is prevented from moving forward.");
						System.out.println("Sensor readings: FL: " + robot.getFrontLeft() + ", FC: " + robot.getFrontCenter() + ", FR: " + robot.getFrontRight());*/
						// Sense again
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
						robot.turn(RIGHT);
						robot.sense(realRun);
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
						robot.turn(LEFT);
						robot.sense(realRun, true);
					}
				}
				// Sensor readings show there is NO obstacles in front of robot
				else {
					// Simulator shows there is obstacle(s) in front
					if(robot.isObstacleInfront()) {
						/*System.out.println("Sensor readings conflict with simulator. Robot is prevented from moving forward.");
						System.out.println("Sensor readings: FL: " + robot.getFrontLeft() + ", FC: " + robot.getFrontCenter() + ", FR: " + robot.getFrontRight());*/
						
						// Sense again to correct the front using the left sensors
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "R");
						robot.turn(RIGHT);
						robot.sense(realRun);
						// Sense again to correct the front using the front sensors
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "L");
						robot.turn(LEFT);
						robot.sense(realRun, true);
					}
					// No conflict move forward
					else {
						SocketMgr.getInstance().sendMessage(CALL_ARDUINO, "M1");
						//robot.setDetectNextMove(false);
						robotMovementString+="M";
						/*System.out.println("----------------------Moving Forward----------------------");
						System.out.println(robotMovementString);*/
						
						// show the robot move forward on the simulator
						robot.move();
						
						// Sense the surrounding
						robot.sense(realRun, true);
						
						// Update Android when there is a move forward
						sendAndroid(grid, robot, realRun);
						
						
					}
				}
			}
		}		
	}
        """
            
