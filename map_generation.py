from hexagon import *
from image_processing import *
from oceans import OceanManager
pygame.init()
import time


def getDirection(r1, c1, r2, c2):
    if r1 - 2 == r2 and c1 == c2:
        return NORTH
    elif r1 + 2 == r2 and c1 == c2:
        return SOUTH
    elif r1%2 == 0:
        if r1 - 1 == r2 and c1 == c2:
            return NORTHWEST
        elif r1 - 1 == r2 and c1 + 1 == c2:
            return NORTHEAST
        elif r1 + 1 == r2 and c1 == c2:
            return SOUTHWEST
        elif r1 + 1 == r2 and c1 + 1 == c2:
            return SOUTHEAST
        else:
            #Throw custom error
            print(r1, c1, r2, c2)
            raise Exception("ERROR: getDirection between two non-adjacent cells")
    else:
        if r1 - 1 == r2 and c1 - 1 == c2:
            return NORTHWEST
        elif r1 - 1 == r2 and c1 == c2:
            return NORTHEAST
        elif r1 + 1 == r2 and c1 - 1 == c2:
            return SOUTHWEST
        elif r1 + 1 == r2 and c1 == c2:
            return SOUTHEAST
        else:
            #Throw custom error
            print(r1, c1, r2, c2)
            raise Exception("ERROR: getDirection between two non-adjacent cells")


def createGrid():
    grid = []
    for row in range(row_count):
        temp_row = []
        for col in range(col_count):
            #Randomize grid cell starting conditions
            elevation = cell_variation_min+random.random()*(cell_variation_max-cell_variation_min)
            temperature = cell_variation_min+random.random()*(cell_variation_max-cell_variation_min)
            h = Hexagon(row,col,elevation,temperature)
            temp_row.append(h)
        grid.append(temp_row)
    print('Elevation min-max: ',cell_variation_min,' to ',cell_variation_max)
    print('Temperature min-max: ',cell_variation_min,' to ',cell_variation_max)
    return grid


def plantCountTrees(grid, count, level):
    #Keep and return a list of all planted forest locations
    forest_locations = []
    for _ in range(count):
        row,col = getRandomNoExtremes(grid)
        grid[row][col].foliage = level
        forest_locations.append((row,col))
    return forest_locations

def forestSpread(grid,row,col,countdown):
    '''Recursively spread foliage.
    countdown is a limit on the amount of recursion.'''
    countdown -= 1
    if countdown < 0:
        return
    #Foliage value where the forest is spreading from
    spreadee_level = grid[row][col].foliage
    #Get neighbors
    ns = getHexNeighbors(row,col)
    #Spread foliage this number of times
    for _ in range(foliage_spread):
        #Get the cell to spread to
        row,col = random.choice(ns)
        cell = grid[row][col]
        #Only spread to neighbors with foliage levels lower than
        #current cell's value and lower than max
        if cell.foliage<spreadee_level and cell.foliage<max_foliage:
            cell.foliage += 1
            forestSpread(grid,row,col,countdown)

def plantTrees(grid):
    '''This function changes random grid cells to forest and
    randomly spreads those forest values. Oceans and mountains
    and extreme deserts are skipped.
    This should be called AFTER smoothing has occurred.'''
    #Plant deep forests
    count = random.randint(min_deep_foliage,max_deep_foliage)
    forest_locations = plantCountTrees(grid, count, max_foliage)
    print('Deep forest count: ',count)
    #Plant medium forests
    count = random.randint(min_med_foliage,max_med_foliage)
    forest_locations += plantCountTrees(grid, count, max_foliage-1)
    print('Medium forest count: ',count)
    #Spread forests
    for row,col in forest_locations:
        forestSpread(grid,row,col,foliage_max_depth)
    print('Forest spread max depth: ',foliage_max_depth)


def placeCities(grid, count, level):
    #Return coordinates of all cities placed
    cities = []
    for _ in range(count):
        row,col = getRandomRowCol()
        cell = grid[row][col]
        #No ocean cities or cities in same location as other cities
        limit = 100 #Avoid possible infinite looping on small maps
        count = 0
        while (cell.elevation<shallows_cutoff or cell.city_level!=0) and count<limit:
            row,col = getRandomRowCol()
            cell = grid[row][col]
            count+=1
        if count<limit:
            cell.city_level = level
            cities.append((row,col))
    return cities

def randomizeTerrain(grid):
    '''This function sprinkles in a random number of randomly
    located extreme temperature and elevation values.'''
    #Sprinkle in random high elevations
    count = random.randint(0,elevation_high_count)
    print('High elevation count: ',count)
    for _ in range(count):
        cell = getRandomCell(grid)
        amount = random.randint(elevation_high_min,elevation_high_max)
        print('    ',amount)
        cell.elevation = amount
    #Sprinkle in random low elevations
    count = random.randint(0,elevation_low_count)
    print('Low elevation count: ',count)
    for _ in range(count):
        cell = getRandomCell(grid)
        amount = random.randint(elevation_low_min,elevation_low_max)
        print('    ',amount)
        cell.elevation = amount
    #Sprinkle in random high temperature
    count = random.randint(0,temperature_high_count)
    print('High temperature count: ',count)
    for _ in range(count):
        cell = getRandomCell(grid)
        amount = random.randint(temperature_high_min,temperature_high_max)
        print('    ',amount)
        cell.temperature = amount
    #Sprinkle in random low temperature
    count = random.randint(0,temperature_low_count)
    print('Low temperature count: ',count)
    for _ in range(count):
        cell = getRandomCell(grid)
        amount = random.randint(temperature_low_min,temperature_low_max)
        print('    ',amount)
        cell.temperature = amount


def smoothGrid(grid):
    smoothing_passes = random.randint(smoothing_passes_min,smoothing_passes_max)
    print('Smoothing passes: ',smoothing_passes)
    weight = random.randint(weight_min,weight_max)
    print('Central cell weight: ',weight)
    for _ in range(smoothing_passes):
        temperatures = []
        elevations = []
        for row in range(row_count):
            temp_temps = []
            temp_elevs = []
            for col in range(col_count):
                ns = getHexNeighbors(row,col)
                avg_temp = grid[row][col].temperature*weight
                avg_elev = grid[row][col].elevation*weight
                for r,c in ns:
                    avg_temp += grid[r][c].temperature
                    avg_elev += grid[r][c].elevation
                temp_temps.append(avg_temp/(len(ns)+weight))
                temp_elevs.append(avg_elev/(len(ns)+weight))
            temperatures.append(temp_temps)
            elevations.append(temp_elevs)
        #Update grid
        for row in range(row_count):
            for col in range(col_count):
                grid[row][col].temperature = temperatures[row][col]
                grid[row][col].elevation = elevations[row][col]


def setImages(grid, frames):
    for row in range(row_count):
        for col in range(col_count):
            grid[row][col].setImage(frames)


def markClicked(pos,grid,oceans,selected,scale):
    #Erase previous mark and selection
    if selected != None:
        selected.selected = False
        #neighbors = getHexNeighbors(selected.row,selected.col)
        #for r,c in neighbors:
        #    grid[r][c].marked = None
        resetMarked(grid)
    #Store previous selected to mark shortest path between points
    old_selected = selected
    #Get new selected
    selected = getClicked(pos, grid, scale)
    if selected != None:
        #Print information about this hex
        print(selected.getInfo())
        selected.selected = True
        #mark all the neighbors and print their travel costs
        neighbors = getPathableNeighbors(selected,grid,oceans)
        for n,_ in neighbors:
            grid[n.row][n.col].marked = (0,255,0)
            #Print cost to each neighbor
            english_direction=directionToEnglish(getDirection(selected.row,selected.col,n.row,n.col))
            print("Cost to "+english_direction+":"+str(getTravelCost(selected,n)))
    #If both old selected and new selected are not None
    #mark and print the travel cost between them
    if selected!=None and old_selected!=None:
        path = calcShortestPath((selected.row,selected.col),(old_selected.row,old_selected.col),grid,oceans)
        finalized_path = greedySearchPostProcessing(path, selected, grid)
        for cell in finalized_path:
            cell.marked = (100,255,200)
            #TODO LEFT OFF HERE - calculate the total cost of
            #this path and print it.
    return selected

def shortPathHelper(grid,upcoming,r_end,c_end):
    #Get index of next cell to check. It should be cell with
    #cheapest cost
    cheapest = 2**28
    index = 0
    for i in range(len(upcoming)):
        r,c,cost,direction,distance_cost = upcoming[i]
        #Factor in the distance from this cell to the
        #destination. We make the calculation and save it in
        #upcoming because recalculating it is time-expensive.
        #We add in the distance cost here so it does not
        #accumulate. The distance cost should not accumulate
        #because then our costs go up the longer we've traveled
        #and the closer we are to our goal.
        cost += distance_cost
        #In the event of a tie, flip a coin
        if cost < cheapest or (cost==cheapest and random.randint(0,1)):
            cheapest = cost
            index = i
    return index

def getPathableNeighbors(cell,grid,oceans):
    '''This is a helper function for calcShortestPath that
    retrieves neighboring cells of the given cell. This
    operation is complicated by the special way we want to
    treat water such that any water cell is reachable
    instantly as long as there is a path through other water
    cells and water can not be entered from land by the north
    or south because there are no north or south facing port
    images.

    The neighbor_list returned will either be full of
    cell,None tuples in the case of water, or be full of
    cell,direction tuples in the case of land.'''
    neighbor_list = []
    if cell.isWater():
        #get all land-bordering tiles reachable from this
        #water with east or west opening docks.
        temp = oceans.getDocks(cell.row,cell.col)
        for r,c in temp:
            neighbor_list.append((grid[r][c],None))
        #Also get all land cells immediately adjacent to
        #this water to the east or west
        for direction in DIRECTIONS:
            rn,cn = cell.getRowCol(direction)
            #Skip out of bounds cells, water cells, and cells to
            #the north or south
            if direction not in [NORTH,SOUTH] and not(outOfBounds(rn,cn)) and not(grid[rn][cn].isWater()):
                neighbor_list.append((grid[rn][cn],direction))
    else:
        for direction in DIRECTIONS:
            rn,cn = cell.getRowCol(direction)
            #Skip out of bounds cells
            if not(outOfBounds(rn,cn)):
                #If it's not water or it's water reachable to the east or west
                if not grid[rn][cn].isWater() or direction not in [NORTH,SOUTH]:
                    neighbor_list.append((grid[rn][cn],direction))
    return neighbor_list

def getTravelCost(start,end):
    '''start and end are both cells. Return the cost to
    travel from start to end. Order matters. The cost of
    start,end is not necessarilly the same as the cost
    of end,start.'''
    #This initial penalty is needed so that the cost reduction
    #from traveling over roads doesn't make the cost negative
    #thereby causing the pathing to take extra journeys over
    #roads that it doesn't need to take.
    cost = path_penalty
    #If moving from water to water then add a minimal cost
    if areBothWater(start,end):
        #If moving from water to water and both are ports, add an even
        #smaller cost. I have verified that this reduces the number of
        #redundant ports.
        if start.is_port and end.is_port:
            cost += 1
        else:
            cost += 2
    #If moving from water to land then movement cost
    #is just the destination.
    elif start.isWater() and not end.isWater():
        #Cost factors in terrain
        cost += int(end.getMovementCost()/2)
        #Reduce the cost for every road already connecting through this cell
        cost -= len(end.road_directions)*multi_road_reduction
    #If moving from land to water then movement cost
    #is the port_cost and half the current terrain cost.
    elif not start.isWater() and end.isWater():
        #Cost factors in terrain
        cost += int(end.getMovementCost()/2) + port_cost
    else: #Moving from land to land
        #Cost factors in terrain
        cost += int((end.getMovementCost() + start.getMovementCost())/2)
        #Reduce the cost for every road already connecting through this cell
        cost -= len(end.road_directions)*multi_road_reduction
    return cost


def calcShortestPath(coords1,coords2,grid,oceans):
    '''Do a greedy search to find shortest path.
    Don't path through water for now.
    This function does not return a list of hexagons.
    Instead it returns a list of hexagon,direction
    pairs, but not all of these pairs are actually
    on the path. The list has to be processed by
    walking from the end back to the start to find
    the actual path and remove extraneous hexes.
    In other words, this function returns all the
    hex,direction pairs that were used in the greedy
    search.'''
    r,c = coords1 #Starting location
    r_end,c_end = coords2 #ending_location
    path = [] #Store best path
    visited = [(r,c)] #Visited cells
    #upcoming contains quintuples of row,col,
    #cost-to-visit, direction, and hex distance.
    upcoming = [(r,c,0,-1,0)]
    while len(upcoming) > 0:
        #Get next cell to check. It should be cell with
        #cheapest cost
        index = shortPathHelper(grid, upcoming, r_end, c_end)
        r,c,cost,direction,_ = upcoming.pop(index)
        cell = grid[r][c]
        #Add cell to path
        path.append((cell,direction))
        #Check for win condition. Did we find destination?
        if (r,c) == (r_end,c_end):
            return path
        neighbor_list = getPathableNeighbors(cell,grid,oceans)
        #Remove cells previously added to upcoming
        for i in reversed(range(len(neighbor_list))):
            r = neighbor_list[i][0].row
            c = neighbor_list[i][0].col
            #If cell has already been visited, remove it
            #from the neighbor list, otherwise add it to
            #visited.
            if (r,c) in visited:
                del neighbor_list[i]
            else:
                visited.append((r,c))
        #Add each neighbor of next cell to upcoming.
        for neighbor in neighbor_list:
            #make cost cumulative by initializing total cost
            #to the cost of the most recently popped cell.
            total_cost = cost
            destination,direction = neighbor
            #Calculate distance cost once then keep it in upcoming
            #so you don't have to keep recalculating it.
            distance_cost = getHexDistance(destination.row,destination.col,r_end,c_end)*dist_cost
            #Factor terrain and water into the total cost
            total_cost += getTravelCost(cell,destination)
            #If moving from water to water then use the source cell
            #instead of a direction since direction is irrelevant.
            if cell.isWater() and destination.isWater():
                direction = cell
            upcoming.append((destination.row,destination.col,total_cost,direction,distance_cost))
    print('Warning: Failed to find path in calcShortestPath(',coords1,',',coords2,')')
    return []

def invertDirection(direction):
    '''Return the opposite of the given direction.'''
    if direction == NORTH:
        return SOUTH
    elif direction == SOUTH:
        return NORTH
    elif direction == NORTHWEST:
        return SOUTHEAST
    elif direction == NORTHEAST:
        return SOUTHWEST
    elif direction == SOUTHWEST:
        return NORTHEAST
    elif direction == SOUTHEAST:
        return NORTHWEST
    else:
        #Throw custom error
        raise Exception('ERROR: Unrecognized direction ',direction,' in map_generation.invertDirection')

def setPortImage(grid, cell, port_east, port_west):
    '''Determine if cell's port should open to the east or west.
    If port borders a city, there won't necessarilly be a road
    headed into the port so also check if there's a city.'''
    r,c=cell.getRowCol(NORTHWEST)
    r2,c2=cell.getRowCol(SOUTHWEST)
    if not(outOfBounds(r,c)) and (grid[r][c].city_level > 0 or (not grid[r][c].isWater() and SOUTHEAST in grid[r][c].road_directions)):
        cell.img = port_east
    elif not(outOfBounds(r2,c2)) and (grid[r2][c2].city_level > 0 or (not grid[r2][c2].isWater() and NORTHEAST in grid[r2][c2].road_directions)):
        cell.img = port_east
    else:
        cell.img = port_west

def setRoadImages(grid, port_east, port_west):
    road_images = strip_roads_from_sheet()
    for row in grid:
        for cell in row:
            #If this cell is a port, set image of a port
            #facing the right direction
            if cell.is_port:
                setPortImage(grid, cell, port_east, port_west)
            #else if this cell has a road and is not a city
            elif len(cell.road_directions)>1 and cell.city_level==0:
                #Find the image index of the road.
                for i in range(len(road_map)):
                    #ignore images that clearly don't match
                    if len(road_map[i]) == len(cell.road_directions):
                        #Make sure all the directions are found
                        found = True
                        for d in cell.road_directions:
                            if not(d in road_map[i]):
                                found = False
                                break
                        if found:
                            cell.road_image = road_images[i]
                            break
                if cell.road_image == None:
                    raise Exception('ERROR: no road image found for road with directions:',cell.road_directions)

def handleWaterInPath(cell1,cell2,path):
    '''Pre: cell1 and cell2 are both water. Make both cells
    ports and find the next cell matching cell2 in the path
    and pop and return it.'''
    for k in range(len(path)):
        if path[k][0] == cell2:
            return path.pop(k)
    raise Exception('cell not found')


def areBothWater(a,b):
    try:
        return a.isWater() and b.isWater()
    except:
        return False

def greedySearchPostProcessing(path, destination, grid):
    '''Pre: path is a list of hex,direction pairs.
    destination is a hex.
    grid is the 2d list of all hexes.
    Post: This function pares down the path list from
    calcShortestPath into a list of hexes, in order,
    on the path from one place to another. The list of
    hexes is returned.'''

    '''path is a list of cell,direction pairs. start
    with last item in path, but don't use it. follow
    inverse directions back through cells in the path.
    path contains more than we need because it's
    constructed with a greedy search.
    The goal below is to walk through path backwards
    painting roads only where they are needed.'''
    #The last cell in path should be the destination
    cell,direction = path.pop(len(path)-1)
    finalized_path = [cell]
    #This if is needed so you can select paths that start
    #on water.
    if areBothWater(cell,direction):
        cell,direction = handleWaterInPath(cell,direction,path)
        r = cell.row
        c = cell.col
        finalized_path.append(cell)
    #Invert direction to find the next cell to travel to
    direction = invertDirection(direction)
    #r,c are the row,col of the next cell to travel to
    r,c = cell.getRowCol(direction)
    #Repeat until we reach destination
    while grid[r][c] != destination:
        #Pop the next cell out of path.
        for k in range(len(path)):
            if path[k][0] == grid[r][c]:
                cell,direction = path.pop(k)
                finalized_path.append(cell)
                break
        #While they are both water, keep popping.
        if areBothWater(cell,direction):
            cell,direction = handleWaterInPath(cell,direction,path)
            r = cell.row
            c = cell.col
            finalized_path.append(cell)
        #check if reached destination
        if direction == -1:
            break
        #Use inverted direction to find next.
        direction = invertDirection(direction)
        r,c = cell.getRowCol(direction)
    return finalized_path

def connectByRoad(path):
    for k in range(len(path)-1):
        #If they are both water, add ports
        if areBothWater(path[k], path[k+1]):
            path[k].is_port = True
            path[k+1].is_port = True
        else:
            r1 = path[k].row
            c1 = path[k].col
            r2 = path[k+1].row
            c2 = path[k+1].col
            direction = getDirection(r1,c1,r2,c2)
            path[k].addDirection(direction)
            path[k+1].addDirection(invertDirection(direction))

def calculateCityPaths(grid,city_locations,oceans):
    '''city_locations is a list of row,column pairs of
    city locations on the grid.
    Calculate all pairs shortest paths.'''
    #Loop through each city and recurse
    for i in range(len(city_locations)-1):
        for j in range(i+1,len(city_locations)):
            #Do a greedy shortest path search
            path = calcShortestPath(city_locations[i],city_locations[j],grid,oceans)
            #Gracefully handle pathing failure
            if len(path) == 0:
                print('WARNING: Pathing failed in map_generation.calculateCityPaths')
                break
            finalized_path = greedySearchPostProcessing(path, city_locations[i], grid)

            #TODO TESTING LEFT
            #for cell in finalized_path:
            #    cell.marked = (100,255,200)

            #lay down roads along the path
            connectByRoad(finalized_path)

def resetGrid(frames):
    print()
    seed = random.randint(-2**16,2**16)
    print('Seed:',seed)
    random.seed(seed)
    print('Creating grid')
    start_time = time.time()
    grid = createGrid()
    elapsed = time.time()-start_time
    print("Grid creation complete in ",elapsed,"seconds\nRandomizing terrain")
    #Add random extremes of temperature and elevation
    start_time = time.time()
    randomizeTerrain(grid)
    elapsed = time.time()-start_time
    print("Terrain randomization complete in ",elapsed,"seconds\nSmoothing")
    #Use something like heat flow to run a smoothing pass then
    #determine images based on elevation and temperature.
    start_time = time.time()
    smoothGrid(grid)
    elapsed = time.time()-start_time
    print("Smoothing complete in ",elapsed,"seconds\nPlanting trees")
    #Plant trees and spread them to neighboring cells
    start_time = time.time()
    plantTrees(grid)
    elapsed = time.time()-start_time
    print("Tree planting complete in ",elapsed,"seconds\nPlancing cities")
    #Place cities
    start_time = time.time()
    city_locations = []
    city_locations += placeCities(grid, level1_city_count, 1)
    city_locations += placeCities(grid, level2_city_count, 2)
    city_locations += placeCities(grid, level3_city_count, 3)
    elapsed = time.time()-start_time
    print("City placement complete in ",elapsed,"seconds\nCharting oceans")
    #Calculate cheapest paths between cities
    start_time = time.time()
    water = OceanManager(grid)
    #water.testChartOceans()
    elapsed = time.time()-start_time
    print("Ocean charting complete in ",elapsed,"seconds\nPathing")
    start_time = time.time()
    calculateCityPaths(grid,city_locations,water)
    elapsed = time.time()-start_time
    print("Pathing complete in ",elapsed,"seconds\nDetermining images")
    #Finally set the images based on the elevation and temperature
    start_time = time.time()
    setImages(grid, frames)
    elapsed = time.time()-start_time
    print("Image determination complete in ",elapsed,"seconds\nSetting road images")
    #Set road images
    start_time = time.time()
    setRoadImages(grid, frames[port_east], frames[port_west])
    elapsed = time.time()-start_time
    print("Road images complete in ",elapsed,"seconds")
    return grid,water

