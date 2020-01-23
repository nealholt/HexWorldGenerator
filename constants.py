
row_count = 38
col_count = 20

scale = 100
scale_change = 2

#Adjustment to the size of hex hitboxes to make them
#more what they actually seem to be.
hex_box_adjust = 3
box_height_adjust = 2

#gap is the width of the top and bottom size of a hex
#This was fudged by hand because I didn't know how else to get it
#positioned correctly. Measuring the number of pixels didn't work.
gap = 18
x_offset = 26
#height_adjust is half the height of a hex.
#This was fudged by hand because I didn't know how else to get it
#positioned correctly. Measuring the number of pixels didn't work.
height_adjust = 14

#Upper range of randomized highs and lows.
#The lower range is zero which is set in
#map_generation.randomizeTerrain
elevation_high_count = 3
elevation_low_count = 3
temperature_high_count = 2
temperature_low_count = 2
#Values of randomized highs and lows
elevation_high_max = 6**3
elevation_high_min = 6
elevation_low_min = -6**3
elevation_low_max = -6
temperature_high_max = 6**3
temperature_high_min = 6
temperature_low_min = -6**3
temperature_low_max = -6

#This is the range of values individual cells will have their
#temperature and elevation initialized to
cell_variation_min = -0.2
cell_variation_max = 1.2

#Used for the heat-flow-like smoothing of terrain.
#Upper and lower bound on the random number of smoothing passes
#to run.
smoothing_passes_min = 1
smoothing_passes_max = 7
#Upper and lower bound on the random amount to emphasize central
#cell value when smoothing
weight_min = 1
weight_max = 4

#Temperature cut offs:
#Below this value make it snowy
snow_cutoff = 0.2
#Above snow cutoff and below this make it temperate
temperate_cutoff = 0.7
#Otherwise make it desert
deep_desert_cutoff = 0.85

#Elevation cut offs:
#Below this value make it deep ocean
ocean_cutoff = 0.2
shallows_cutoff = 0.4
flat_cutoff = 0.6
elevated_cutoff = 0.8
#Above elevated is mountain

#Maximum foliage level
max_foliage = 3
#Range of number of deep forests (level 3) to plant
min_deep_foliage = 1
max_deep_foliage = 3
#Range of number of medium forests (level 2) to plant
min_med_foliage = 1
max_med_foliage = 5
#Number of times to randomly spread forests to neighbors
foliage_spread = 3
#Limit the tree spreading recursion
foliage_max_depth = 7

#number of cities of varying levels
level1_city_count = 3
level2_city_count = 2
level3_city_count = 2

#Costs to travel over various elevations and temperatures
mountain_cost = 30
elevated_cost = 5
plains_cost = 1
cold_cost = 4
desert_cost = 4
deep_desert_cost = 10
port_cost = 5 #cost to move into water
#multiplier on the cost of a longer distance path. Used for
#road construction.
dist_cost = 2

#cost reduction per existing road connection in a tile.
#Making this zero makes a bunch of redundant roads, but
#in some ways I like that. An alternative is to occassionally
#randomly choose from among the best cells to make a road
#through in map_generation.calcShortestPath rather than always
#choosing the lowest cost road.
multi_road_reduction = 1

#Neighbors are gotten in this order: N, S, NW, NE, SW, SE
#The inverse is needed for pathing.
NORTH = 0
SOUTH = 1
NORTHWEST = 2
NORTHEAST = 3
SOUTHWEST = 4
SOUTHEAST = 5
inverse_neighbor_order = [SOUTH, NORTH, SOUTHEAST, SOUTHWEST, NORTHEAST, NORTHWEST]
DIRECTIONS = inverse_neighbor_order

#Incomplete mapping between directions and road image indices.
#Example: the index 0 image is the road connecting north and south.
#Indicies in the list below match indicies in the road images
road_map = [[NORTH,SOUTH],
            [NORTH,NORTHWEST],
            [NORTH,SOUTHWEST],
            [NORTH,SOUTHEAST],
            [NORTH,NORTHEAST],
            [NORTHWEST,SOUTH],
            [SOUTHWEST,SOUTH],
            [SOUTH,SOUTHEAST],
            [SOUTH,NORTHEAST],
            [NORTHEAST,NORTH,SOUTH],
            [SOUTHWEST,NORTH,SOUTH],
            [NORTHWEST,NORTH,SOUTH],
            [SOUTHEAST,NORTH,SOUTH],
            [NORTHWEST,NORTHEAST,SOUTHWEST,SOUTHEAST],
            [SOUTHWEST,NORTHEAST],
            [NORTHWEST,SOUTHEAST],
            [NORTHWEST,SOUTHWEST],
            [NORTHEAST,SOUTHEAST],
            [SOUTHWEST,SOUTHEAST],
            [NORTHWEST,NORTHEAST],
            [NORTH,SOUTH,SOUTHEAST,NORTHWEST],
            [NORTHWEST,SOUTH,SOUTHEAST],
            [NORTHWEST,NORTH,SOUTHEAST],
            [NORTH,NORTHWEST,SOUTH,SOUTHWEST],
            [NORTHWEST,SOUTH,SOUTHWEST],
            [NORTHWEST,NORTH,SOUTHWEST],
            [NORTHEAST,NORTH,SOUTHEAST,SOUTH],
            [SOUTH,NORTHEAST,SOUTHEAST],
            [NORTH,NORTHEAST,SOUTHEAST],
            [NORTH,NORTHWEST,SOUTHEAST,SOUTHWEST,SOUTH],
            [NORTHWEST,SOUTHEAST,SOUTHWEST,SOUTH],
            [NORTHWEST,NORTH,SOUTHEAST,SOUTHWEST],
            [NORTH,NORTHWEST,NORTHEAST,SOUTH,SOUTHWEST],
            [NORTHWEST,NORTHEAST,SOUTHWEST,SOUTH],
            [NORTH,NORTHWEST,NORTHEAST,SOUTHWEST],
            [NORTHWEST,SOUTHWEST,SOUTHEAST],
            [NORTHEAST,SOUTHWEST,SOUTHEAST],
            [NORTHEAST,SOUTHWEST,NORTHWEST],
            [NORTHEAST,SOUTHEAST,NORTHWEST],
            [NORTH,NORTHWEST,NORTHEAST,SOUTH,SOUTHWEST,SOUTHEAST],
            [NORTHWEST,NORTHEAST,SOUTH,SOUTHWEST,SOUTHEAST],
            [NORTH,NORTHWEST,NORTHEAST,SOUTHWEST,SOUTHEAST],
            [NORTH,NORTHEAST,SOUTH,SOUTHWEST],
            [NORTHEAST,SOUTH,SOUTHWEST],
            [NORTHEAST,NORTH,SOUTHWEST],
            [NORTH,SOUTH,SOUTHWEST,SOUTHEAST],
            [NORTH,SOUTHWEST,SOUTHEAST],
            [SOUTH,SOUTHWEST,SOUTHEAST],
            [NORTH,SOUTH,NORTHWEST,NORTHEAST],
            [SOUTH,NORTHWEST,NORTHEAST],
            [NORTH,NORTHWEST,NORTHEAST],
            [NORTH,NORTHEAST,SOUTHEAST,SOUTH,SOUTHWEST],
            [NORTHEAST,SOUTHEAST,SOUTH,SOUTHWEST],
            [NORTH,NORTHEAST,SOUTHEAST,SOUTHWEST],
            [NORTHWEST,NORTH,NORTHEAST,SOUTHEAST,SOUTH],
            [NORTHWEST,NORTHEAST,SOUTHEAST,SOUTH],
            [NORTHWEST,NORTH,NORTHEAST,SOUTHEAST]
        ]

#Sanity check. are there duplicates in road_map?
for i in range(len(road_map)-1):
    for j in range(i+1,len(road_map)):
        if len(road_map[i])==len(road_map[j]):
            match = True
            for direction in road_map[i]:
                if direction not in road_map[j]:
                    match = False
                    break
            if match:
                print('duplicates found:',i,' ',j)
                print(road_map[i])
                print(road_map[j])
                exit()


