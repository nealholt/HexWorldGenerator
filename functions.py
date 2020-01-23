import math,random
from constants import *


def getRowCol(row,col,direction):
    '''Returns row col in the indicated direction.'''
    if direction == NORTH:
        return row-2,col
    elif direction == SOUTH:
        return row+2,col
    elif direction == NORTHWEST:
        if row%2==0:
            return row-1,col
        else:
            return row-1,col-1
    elif direction == NORTHEAST:
        if row%2==0:
            return row-1,col+1
        else:
            return row-1,col
    elif direction == SOUTHWEST:
        if row%2==0:
            return row+1,col
        else:
            return row+1,col-1
    elif direction == SOUTHEAST:
        if row%2==0:
            return row+1,col+1
        else:
            return row+1,col
    else:
        print('ERROR in functions.getRowCol unrecognized direction "',direction,'"')
        exit()

def resetSelected(grid):
    for row in grid:
        for cell in row:
            cell.selected = False

def resetMarked(grid):
    for row in grid:
        for cell in row:
            cell.marked = None

def getRandomRowCol():
    row = random.randint(0,row_count-1)
    col = random.randint(0,col_count-1)
    return row,col

def getRandomNoExtremes(grid):
    row,col = getRandomRowCol()
    retry_limit = 100 #Don't try more than this
    count = 0
    #Skip oceans and mountains. Retry
    while (grid[row][col].elevation<shallows_cutoff or \
    grid[row][col].elevation>elevated_cutoff) and count<retry_limit:
        count+=1
        row,col = getRandomRowCol()
    return row, col

def getRandomCell(grid):
    row = random.choice(grid)
    return random.choice(row)

def distanceEuclidean(grid, r1, c1, r2, c2):
    '''This returns the distance between upper left corners
    of cells, but since it is consistent, I think that's ok.'''
    cell1 = grid[r1][c1]
    x1 = cell1.x
    y1 = cell1.y
    cell2 = grid[r2][c2]
    x2 = cell2.x
    y2 = cell2.y
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def getDirectPath(grid, r1, c1, r2, c2):
    '''Returns direct path between cells. Does not include
    starting location on path. Does include destination.
    Ignores terrain.'''
    path = []
    while (r1,c1) != (r2,c2):
        neighbors = getHexNeighbors(r1,c1)
        #Get only the closest neighbor
        closest_distance = 2**20
        index = 0
        for i in range(len(neighbors)):
            r3,c3 = neighbors[i]
            distance = distanceEuclidean(grid,r2,c2,r3,c3)
            if distance < closest_distance:
                closest_distance = distance
                index = i
        r1,c1 = neighbors[index]
        path.append((r1,c1))
    return path


def distanceHex(grid, r1, c1, r2, c2):
    '''Returns the distance in units of cells between
    the given cells. Ignores terrain.'''
    path = getDirectPath(grid, r1, c1, r2, c2)
    return len(path)

def getHexDistance(r1, c1, r2, c2):
    '''Returns the distance in units of cells
    between the given cells. Ignores terrain.

    TODO: This SHOULD be identical to distanceHex
    above, but should run considerably faster.
    I think this will occassionally be off by one
    since I'm not distinguishing even versus odd
    rows, but I'm ok with that for now.'''
    row_diff = abs(r1-r2)
    col_diff = abs(c1-c2)
    if row_diff>col_diff:
        #In a hex map you can cross a row and a
        #column simultaneously, so by subtracting
        #here I'm simply assuming movement along
        #the diagonal.
        row_diff -= col_diff
        #North and south movement actually skips
        #a row so divide row_diff by two
        return col_diff + int(row_diff/2)
    else:
        col_diff -= row_diff
        return row_diff + int(col_diff/2)


def getClicked(pos, grid):
    for i in range(row_count):
        for j in range(col_count):
            if grid[i][j].collidePoint(pos):
                return grid[i][j]
    return None

def resetMarked(grid):
    for row in grid:
        for cell in row:
            cell.marked = None

def outOfBounds(row,col):
    return row<0 or col<0 or row>=row_count or col>=col_count

def getNeighbors(row,col):
    '''Returns list of exactly 6 row,col pairs that are neighbors
    of the given row,col. Out of bounds neighbors are returned
    as None.
    Order matters too. These are returned in the order:
        N, S, NW, NE, SW, SE
    This is used for determining directional neighbors for a
    hex.'''
    neighbors = []
    for direction in DIRECTIONS:
        r,c = getRowCol(row,col,direction)
        neighbors.append((r,c))
    #Replace out of bounds pairs with None
    for i in reversed(range(len(neighbors))):
        r,c = neighbors[i]
        if outOfBounds(r,c):
            neighbors[i] = None
    return neighbors


def getHexNeighbors(row,col):
    '''Returns list of up to 6 row,col pairs that are neighbors
    of the given row,col. Out of bounds neighbors are removed.'''
    neighbors = getNeighbors(row,col)
    #Remove out of bounds pairs
    for i in reversed(range(len(neighbors))):
        if neighbors[i] is None:
            del neighbors[i]
    return neighbors

