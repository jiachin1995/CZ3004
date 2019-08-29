class Sensors:
    
    
    
    
    def isFrontBlocked():
        pass
        
    def isLeftBlocked():
        pass
        
        """
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


        """
        
