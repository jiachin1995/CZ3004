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
        
     public void sendAndroid(Grid grid, Robot robot, boolean realRun) {
		if (realRun) {
			SocketMgr.getInstance().sendMessage(CALL_ANDROID,
                    MessageMgr.generateMapDescriptorMsg(grid.generateMapDescriptor1(), grid.generateMapDescriptor2(), robot.getCenterPositionX(), robot.getCenterPositionY(), robot.getDirection()));
		}
	}
    
    public int checkFrontExplored(Grid grid, Robot robot) {
		int direction = robot.getDirection();
        int robotCurrentX = robot.getPositionX();
        int robotCurrentY = robot.getPositionY();
        
        int moveCount = 1;
        
        if(direction == NORTH) {
    		// Update the new robot Y position after move forward by 1
    		if(robotCurrentY == 1) {
    			return moveCount;
    		} else {
    			robotCurrentY--;
//    			if(isInEndingZone(robotCurrentX, robotCurrentY)) {
//            		moveCount = moveCount +2;
//            		return moveCount;
//            	}
    		}
    	} else if(direction == SOUTH) {
    		// Update the new robot Y position after move forward by 1
    		if(robotCurrentY == 18) {
    			return moveCount;
    		} else {
    			robotCurrentY++;
//    			if(isInEndingZone(robotCurrentX, robotCurrentY+2)) {
//            		moveCount = moveCount +2;
//            		return moveCount;
//            	}
    		}
    	} else if(direction == EAST) {
    		// Update the new robot X position after move forward by 1
    		if(robotCurrentX == 13) {
    			return moveCount;
    		} else {
    			robotCurrentX++;
//    			if(isInEndingZone(robotCurrentX+2, robotCurrentY)) {
//            		moveCount = moveCount +2;
//            		return moveCount;
//            	}
    		}
    	} else if(direction == WEST) {
    		// Update the new robot X position after move forward by 1
    		if(robotCurrentX == 1) {
    			return moveCount;
    		} else {
    			robotCurrentX--;
//    			if(isInEndingZone(robotCurrentX, robotCurrentY)) {
//            		moveCount = moveCount +2;
//            		return moveCount;
//            	}
    		}
    	}
        
        while(!checkObstacleInfront(grid, robotCurrentX, robotCurrentY, direction) && (!checkAbleToTurn(grid, robotCurrentX, robotCurrentY, direction)) && checkLeftRangeExplored(grid, robotCurrentX, robotCurrentY, direction) && checkRightRangeExplored(grid, robotCurrentX, robotCurrentY, direction)) {
        	
        	moveCount++;
        	if(direction == NORTH) {
        		// Update the new robot Y position after move forward by 1
        		if(robotCurrentY == 1) {
        			break;
        		} else {
        			robotCurrentY--;
        			if(isInEndingZone(robotCurrentX, robotCurrentY)) {
                		moveCount = moveCount +2;
                		break;
                	}
        		}
        	} else if(direction == SOUTH) {
        		// Update the new robot Y position after move forward by 1
        		if(robotCurrentY == 18) {
        			break;
        		} else {
        			robotCurrentY++;
        			if(isInEndingZone(robotCurrentX, robotCurrentY+2)) {
                		moveCount = moveCount +2;
                		break;
                	}
        		}
        	} else if(direction == EAST) {
        		// Update the new robot X position after move forward by 1
        		if(robotCurrentX == 13) {
        			break;
        		} else {
        			robotCurrentX++;
        			if(isInEndingZone(robotCurrentX+2, robotCurrentY)) {
                		moveCount = moveCount +2;
                		break;
                	}
        		}
        	} else if(direction == WEST) {
        		// Update the new robot X position after move forward by 1
        		if(robotCurrentX == 1) {
        			break;
        		} else {
        			robotCurrentX--;
        			if(isInEndingZone(robotCurrentX, robotCurrentY)) {
                		moveCount = moveCount +2;
                		break;
                	}
        		}
        	}
        }
        
//        if(uTurn) {
//        	uTurn = false;
//        	moveCount--;
//        }
        
		return moveCount;
	}


private boolean checkLeftRangeExplored(Grid grid, int robotXPos, int robotYPos, int direction) {
		if(direction == NORTH) {
			for(int x=-1; x>-3; x--) {
				if(!grid.isOutOfArena(robotXPos+x, robotYPos)) {
					if(!grid.getIsExplored(robotXPos+x, robotYPos)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos+x, robotYPos)) {
						return true;
					}
				} else {
					return true;
				}
			}
		} else if(direction == SOUTH) {
			for(int x=3; x<5; x++) {
				if(!grid.isOutOfArena(robotXPos+x, robotYPos+2)) {
					if(!grid.getIsExplored(robotXPos+x, robotYPos+2)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos+x, robotYPos+2)) {
						return true;
					}
				} else {
					return true;
				}
			}
		} else if(direction == EAST) {
			for(int y=-1; y>-3; y--) {
				if(!grid.isOutOfArena(robotXPos+2, robotYPos+y)) {
					if(!grid.getIsExplored(robotXPos+2, robotYPos+y)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos+2, robotYPos+y)) {
						return true;
					}
				} else {
					return true;
				}
			}
		} else if(direction == WEST) {
			for(int y=3; y<5; y++) {
				if(!grid.isOutOfArena(robotXPos, robotYPos+y)) {
					if(!grid.getIsExplored(robotXPos, robotYPos+y)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos, robotYPos+y)) {
						return true;
					}
				} else {
					return true;
				}
			}
		}
		
		return true;
	}
	
	private boolean checkRightRangeExplored(Grid grid, int robotXPos, int robotYPos, int direction) {
		if(direction == NORTH) {
			for(int x=3; x<8; x++) {
				if(!grid.isOutOfArena(robotXPos+x, robotYPos)) {
					if(!grid.getIsExplored(robotXPos+x, robotYPos)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos+x, robotYPos)) {
						return true;
					}
				} else {
					return true;
				}
			}
		} else if(direction == SOUTH) {
			for(int x=-1; x>-6; x--) {
				if(!grid.isOutOfArena(robotXPos+x, robotYPos+2)) {
					if(!grid.getIsExplored(robotXPos+x, robotYPos+2)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos+x, robotYPos+2)) {
						return true;
					}
				} else {
					return true;
				}
			}
		} else if(direction == EAST) {
			for(int y=3; y<8; y++) {
				if(!grid.isOutOfArena(robotXPos+2, robotYPos+y)) {
					if(!grid.getIsExplored(robotXPos+2, robotYPos+y)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos+2, robotYPos+y)) {
						return true;
					}
				} else {
					return true;
				}
			}
		} else if(direction == WEST) {
			for(int y=-1; y>-6; y--) {
				if(!grid.isOutOfArena(robotXPos, robotYPos+y)) {
					if(!grid.getIsExplored(robotXPos, robotYPos+y)) {
						return false;
					} else if(grid.getIsObstacle(robotXPos, robotYPos+y)) {
						return true;
					}
				} else {
					return true;
				}
			}
		}
		
		return true;
	}

public boolean isOutOfArena(int x, int y) {
        return x < 0 || y < 0 || x >= 13 || y >= 18;
    }
	
	private boolean rightSideNotFullyExplored(Grid grid, Robot robot) {
		
		int count = 0;
		
		for (int i = 0; i < SIZE_OF_ROBOT; i++) {
            if (robot.getDirection() == NORTH) {
                if (grid.isOutOfArena(robot.getPositionX() + 3, robot.getPositionY() + i) || grid.getIsExplored(robot.getPositionX() + 3, robot.getPositionY() + i)) {
                	count++;
                }
            }
            else if (robot.getDirection() == SOUTH) {
                if (grid.isOutOfArena(robot.getPositionX() - 1, robot.getPositionY() + i) || grid.getIsExplored(robot.getPositionX() - 1, robot.getPositionY() + i)) {
                	count++;
                }
            }
            else if (robot.getDirection() == EAST) {
                if (grid.isOutOfArena(robot.getPositionX() + i, robot.getPositionY() + 3) || grid.getIsExplored(robot.getPositionX() + i, robot.getPositionY() + 3)) {
                	count++;
                }
            }
            else if (robot.getDirection() == WEST) {
                if (grid.isOutOfArena(robot.getPositionX() + i, robot.getPositionY() - 1) || grid.getIsExplored(robot.getPositionX() + i, robot.getPositionY() - 1)) {
                	count++;
                }
            }
        }
		
		if(count == 3) {
			return false;
		}
		
		return true;
	}

private boolean leftSideNotFullyExplored(Grid grid, Robot robot) {
		int count = 0;
		
		for (int i = 0; i < SIZE_OF_ROBOT; i++) {
            if (robot.getDirection() == NORTH) {
                if (grid.isOutOfArena(robot.getPositionX() -1, robot.getPositionY() + i) || grid.getIsExplored(robot.getPositionX() -1, robot.getPositionY() + i)) {
                	count++;
                }
            }
            else if (robot.getDirection() == SOUTH) {
                if (grid.isOutOfArena(robot.getPositionX() +3, robot.getPositionY() + i) || grid.getIsExplored(robot.getPositionX() +3, robot.getPositionY() + i)) {
                	count++;
                }
            }
            else if (robot.getDirection() == EAST) {
                if (grid.isOutOfArena(robot.getPositionX() + i, robot.getPositionY() -1) || grid.getIsExplored(robot.getPositionX() + i, robot.getPositionY() -1)) {
                	count++;
                }
            }
            else if (robot.getDirection() == WEST) {
                if (grid.isOutOfArena(robot.getPositionX() + i, robot.getPositionY() +3) || grid.getIsExplored(robot.getPositionX() + i, robot.getPositionY() +3)) {
                	count++;
                }
            }
        }
		
		if(count == 3) {
			return false;
		}
		
		return true;
	}
	
	public boolean isInEndingZone(int x, int y){
		return (y < ZONE_SIZE) && (y >= 0) && (x < MAP_COLUMNS) && (x >= MAP_COLUMNS - ZONE_SIZE);
                
	}
	
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
            
            
            
        #check left wall, return true
        #check no left wall & have front wall. turn right & return true
