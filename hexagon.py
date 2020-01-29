from pygame import draw, Rect, quit
from functions import *
from constants import scale

class Hexagon:
    def __init__(self, row, col, elevation, temperature):
        self.img = None
        self.row = row
        self.col = col
        self.elevation = elevation
        self.temperature = temperature
        self.foliage = 0
        self.city_level = 0
        self.selected = False
        self.is_port = False
        #Image of a road to overlay, if any
        self.road_image = None
        #The directions by road out of this cell
        self.road_directions = []
        #marked is set to a color or None. marked is used for
        #debugging road drawing and neighbor calculation
        self.marked = None

    def getX(self,scale=100):
        image_width = self.img.get_rect().width
        #I don't know why these fudge factors are needed
        #probably something to do with the image widths
        #being slightly different from the drawn boundary
        #of the tiles. In any case, this works.
        if self.row%2==0:
            fudge_factor = self.col*2+2
            return int((x_offset+self.col*(image_width+gap)-fudge_factor)*scale/100)
        else:
            fudge_factor = self.col*2
            return int((self.col*(image_width+gap)-fudge_factor)*scale/100)

    def getY(self,scale=100):
        return int((self.row*height_adjust)*scale/100)

    def isWater(self):
        return self.elevation<shallows_cutoff

    def addDirection(self, direction):
        if direction not in self.road_directions:
            self.road_directions.append(direction)

    def getRowCol(self,direction):
        '''Returns row col in the indicated direction.'''
        return getRowCol(self.row,self.col,direction)

    def getMovementCost(self):
        cost = 0
        #Temperature costs
        if self.temperature<snow_cutoff:
            cost += cold_cost
        elif self.temperature>deep_desert_cutoff:
            cost += deep_desert_cost
        elif self.temperature>temperate_cutoff:
            cost += desert_cost
        #Elevation costs
        if self.isWater():
            cost += port_cost
        elif self.elevation>elevated_cutoff:
            cost += mountain_cost
        elif self.elevation>flat_cutoff:
            cost += elevated_cost
        else:
            cost += plains_cost
        return cost

    def draw(self, surface):
        surface.blit(self.img, (self.getX(),self.getY()))

    def drawExtras(self, surface):
        '''This separates the drawing of roads
        so that tall tiles like mountains don't end up getting
        drawn above the roads in the tiles to the north of them.
        '''
        if self.road_image != None:
            surface.blit(self.road_image, (self.getX(),self.getY()))

    def getRect(self, scale):
        w = self.img.get_rect().width
        #Make adjustments so the hitbox is actually what
        #it seems to be
        x = int(self.getX(scale)+hex_box_adjust*scale/100)
        y =int(self.getY(scale)+(height_adjust+hex_box_adjust+box_height_adjust)*scale/100)
        width = int((w-2*hex_box_adjust)*scale/100)
        height = int((w-hex_box_adjust)*scale/100)
        return Rect(x,y,width,height)

    def drawMarkings(self,surface,scale):
        if self.selected:
            #Draw a rectangle that matches the hitbox
            r = self.getRect(scale)
            draw.rect(surface, (255,0,0), r, 3)
        if self.marked != None:
            #Draw a circle on this hexagon
            radius = int((x_offset/2)*scale/100)
            center = int(hex_box_adjust*scale/100+self.getX(scale)+radius), \
                    int(hex_box_adjust*scale/100+self.getY(scale)+radius+height_adjust*scale/100)
            draw.circle(surface, self.marked, center, radius, 3)


    def collidePoint(self, pos, scale):
        r = self.getRect(scale)
        return r.collidepoint(pos)

    def setImage(self, frames):
        #City overrides everything else
        if self.city_level > 0:
            self.setCityImage(frames)
        elif self.elevation<shallows_cutoff:
            self.setOceanImage(frames)
        elif self.elevation<flat_cutoff:
            self.setPlainsImage(frames)
        elif self.elevation<elevated_cutoff:
            self.setElevatedImage(frames)
        else:
            self.setMountainImage(frames)

    def setCityImage(self,frames):
        if self.temperature<snow_cutoff or self.elevation>elevated_cutoff:
            if self.city_level > 2:
                self.img = frames[snow_castle]
            else:
                self.img = frames[snow_town]
        elif self.temperature<temperate_cutoff:
            if self.city_level > 2:
                self.img = frames[town_stone_wall]
            elif self.city_level > 1:
                self.img = frames[town_wood_wall]
            else:
                self.img = frames[town]
        else:
            if self.city_level > 2:
                self.img = frames[desert_town_stone_wall]
            elif self.city_level > 1:
                self.img = frames[desert_town_wood_wall]
            else:
                self.img = frames[desert_town]

    def setOceanImage(self,frames):
        if self.elevation<ocean_cutoff:
            self.img = frames[ocean]
        elif self.elevation<shallows_cutoff:
            if self.temperature<snow_cutoff:
                self.img = frames[shallows_icey]
            else:
                self.img = frames[shallows]

    def setPlainsImage(self,frames):
        if self.temperature<snow_cutoff:
            if self.foliage >= max_foliage-1:
                self.img = frames[plains_snow_forest]
            elif self.foliage == max_foliage-2:
                self.img = frames[plains_snow_sparse_forest]
            else:
                self.img = frames[plains_snow]
        elif self.temperature<temperate_cutoff:
            if self.foliage == max_foliage:
                self.img = frames[plains_deep_forest]
            elif self.foliage == max_foliage-1:
                self.img = frames[plains_forest1]
            elif self.foliage == max_foliage-2:
                self.img = frames[plains_sparse_forest]
            else:
                self.img = frames[plains_smooth]
        elif self.temperature<deep_desert_cutoff:
            if self.foliage > max_foliage-2:
                self.img = frames[desert_greenish]
            else:
                self.img = frames[desert1]
        else:
            if self.foliage > max_foliage-1:
                self.img = frames[desert_trees]
            else:
                self.img = frames[desert_rolling]

    def setElevatedImage(self,frames):
        if self.temperature<snow_cutoff:
            if self.foliage > max_foliage-2:
                self.img = frames[elevated_snow_forest]
            else:
                self.img = frames[elevated_snow]
        elif self.temperature<temperate_cutoff:
            if self.foliage > max_foliage-2:
                self.img = frames[elevated_forest1]
            else:
                self.img = frames[elevated_rocky1]
        else:
            self.img = frames[elevated_desert1]

    def setMountainImage(self,frames):
        if self.temperature<temperate_cutoff:
            self.img = frames[mountain_snow]
        else:
            self.img = frames[mountain_desert]
