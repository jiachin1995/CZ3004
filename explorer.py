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
            
