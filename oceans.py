from functions import outOfBounds,resetMarked
from constants import DIRECTIONS,NORTH,SOUTH

def getPotentialDocks(row,col,grid,visited):
    """return list of water tile row,cols that border land to
    the east or west and are reachable from this tile. Don't
    revisit cells in visited."""
    docks = []
    visited.append((row,col))
    for direction in DIRECTIONS:
        r,c = grid[row][col].getRowCol(direction)
        #Skip out of bounds, visited, and water cells.
        if not outOfBounds(r,c) and not((r,c) in visited):
            if grid[r][c].isWater():
                temp,_ = getPotentialDocks(r,c,grid,visited)
                docks += temp
            elif direction not in [NORTH,SOUTH]:
                docks.append((row,col))
    return docks,visited

class OceanManager:
    def __init__(self,grid):
        self.grid = grid #keep reference to the grid
        oceans = self.chartOceans()
        #coastal and water are both lists of lists of row,column
        #pairs. The length of the outer list matches the
        #number of separate bodies of water. The length of the
        #inner lists matches the number of coastal tiles or
        #total water tiles respectively.
        self.coastal = []
        self.water = []
        for coast,water in oceans:
            self.coastal.append(coast)
            self.water.append(water)
        print('Total number of bodies of water is ',len(self.water))

    def chartOceans(self):
        """Save time by pre-charting all the oceans and their
        coasts."""
        visited = []
        oceans = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (row,col) not in visited and self.grid[row][col].isWater():
                    docks,water = getPotentialDocks(row,col,self.grid,[])
                    oceans.append((docks,water))
                    for w in water:
                        if w not in visited:
                            visited.append(w)
        return oceans

    def testChartOceans(self):
        """Mark all ocean tiles and all coastal tiles"""
        resetMarked(self.grid)
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                for i in range(len(self.water)):
                    if (row,col) in self.coastal[i]:
                        self.grid[row][col].marked = (0,0,0)
                        break
                    elif (row,col) in self.water[i]:
                        self.grid[row][col].marked = (255,255,255)
                        break

    def getDocks(self,row,col):
        """Returns all dock tiles reachable by row,col."""
        for i in range(len(self.water)):
            if (row,col) in self.water[i]:
                return self.coastal[i]
        return None
