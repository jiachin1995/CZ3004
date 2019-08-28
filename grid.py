import settings

class grid:
  
  def __init__(self, obstaclesNumber, col_amount, row_amount):
    self.obstaclesNumber = 0
    self.cell_list = [] #empty list to hold all cells
    
    for col in range (col_amount):
      for row in range (row_amount):
        
	private Cell[][] cells;
	
	public Grid(){
		cells = new Cell[MAP_COLUMNS][MAP_ROWS];
		for (int x = 0 : x < MAP_COLUMNS){
			for ( int y = 0 : y < MAP_ROWS){
				cells[x][y] = new Cell();
			}
		}
		reset();
		
	}  


