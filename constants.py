
row_count = 38
col_count = 20

scale = 100
scale_change = 2

#image names for the bigger image set
plains_smooth=0 #used
plains_rolling=1
plains_grass=2
plains_sparse_forest=3 #used
plains_sparse_forest_rocky=4
plains_forest1=5 #used
plains_forest2=6
elevated_green=7
elevated_rocky1=8 #used
elevated_rocky2=9
elevated_forest1=10 #used
elevated_forest2=11
marsh1=12
pond=13
plains_scrub=15
plains_scrub_greenish=16
plains_scrub_greener=17
marsh2=18
plains_scrub_sparse_forest=19
plains_scrub_forest=20
plains_deep_forest=21 #used
plains_deep_dark_forest=22
plains_scrub_greenest=23
pasture_dark=24
scrub_palm_trees=25
desert1=30 #used
desert_greenish=31 #used
desert_rolling=32 #used
desert_tree=33
desert_trees=34 #used
desert_brush=35
desert_brush_tree=36
desert_brush_trees=37
elevated_desert1=38 #used
elevated_desert_trees=39
desert_african_trees=40
plains_african_trees=41
plains_snow_warming=45
plains_snow_sparse_forest_warming=46
plains_snow_sparse_forest_warming=47
elevated_snow_warming=48
elevated_snow_forest_warming=49
plains_snow=51 #used
plains_snow_sparse_forest=52 #used
plains_snow_forest=53 #used
elevated_snow=54 #used
elevated_snow_forest=55 #used
desert2=60
desert_palm_trees=61
desert_rolling_dark=62
elevated_desert2=63
mountain_desert=64 #used
mountain_desert_narrow=65
shallows=75 #used
shallows_icey=76 #used
shallows_icier1=77
shallows_icier2=78
ocean=79 #used
ocean_icey=80
ocean_icier1=81
ocean_icier2=82
ocean_iciest=83
port_east=84 #used
port_west=85 #used
port_east_icey=86
port_west_icey=87
#lava1?=88
#lava2?=89
mountain_snow=90 #used
mountain_lava=91
mountain_lava_bowl=92
mountain_lava_bowl_taller=93
mountain_lava_flow=94
mountain_lava_bowl_leak_more=95
mountain_lava_bowl_leak=96
mountain_lava_flow_more=97
mountain_lava_bowl_flow_more=98
mountain_lava_bowl_flow=99
mountain=100
caldera_short=101
caldera_tall=102
forest_town=105
forest_town_wood_wall=106
forest_town_stone_wall=107
snow_town=108 #used
snow_town_wood_wall=109
snow_town_stone_wall=110
desert_town=111 #used
desert_town_wood_wall=112 #used
desert_town_stone_wall=113 #used
#???
#???
town=116 #used
town_wood_wall=117 #used
town_stone_wall=118 #used
overlay_cave=120
overlay_cave_snow=121
overlay_cave_desert=122
overlay_cemetery1=123
overlay_cemetery2=124
overlay_huts_gray=125
overlay_huts_brown=126
overlay_oasis=127
overlay_caldera_lava=128
overlay_caldera=129
overlay_castle=130
overlay_lighthouse1=131
overlay_lighthouse2=132
overlay_lighthouse3=133
snow_castle=135 #used
snow_ruins=136
ruins=137
concrete=138

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
smoothing_passes_min = 2
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

def directionToEnglish(direction):
    if direction==NORTH:
        return 'north'
    elif direction==SOUTH:
        return 'south'
    elif direction==NORTHWEST:
        return 'northwest'
    elif direction==NORTHEAST:
        return 'northeast'
    elif direction==SOUTHWEST:
        return 'southwest'
    elif direction==SOUTHEAST:
        return 'southeast'
    else:
        print('ERROR in constants.directionToEnglish direction '+str(direction)+' not recognized.')

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


