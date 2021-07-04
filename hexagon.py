from pygame import draw, Rect, quit
from functions import *

class Hexagon:
    def __init__(self, row, col, elevation, temperature):
        self.img = None
        self.img_type = -1
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
        self.breadcrumb = None #Cal
        self.running_total = 0 #Cal

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
            self.setCityImage()
        elif self.elevation<shallows_cutoff:
            self.setOceanImage()
        elif self.elevation<flat_cutoff:
            self.setPlainsImage()
        elif self.elevation<elevated_cutoff:
            self.setElevatedImage()
        else:
            self.setMountainImage()
        self.img = frames[self.img_type]

    def setCityImage(self):
        if self.temperature<snow_cutoff or self.elevation>elevated_cutoff:
            if self.city_level > 2:
                self.img_type=snow_castle
            else:
                self.img_type=snow_town
        elif self.temperature<temperate_cutoff:
            if self.city_level > 2:
                self.img_type=town_stone_wall
            elif self.city_level > 1:
                self.img_type=town_wood_wall
            else:
                self.img_type=town
        else:
            if self.city_level > 2:
                self.img_type=desert_town_stone_wall
            elif self.city_level > 1:
                self.img_type=desert_town_wood_wall
            else:
                self.img_type=desert_town

    def setOceanImage(self):
        if self.elevation<ocean_cutoff:
            self.img_type=ocean
        elif self.elevation<shallows_cutoff:
            if self.temperature<snow_cutoff:
                self.img_type=shallows_icey
            else:
                self.img_type=shallows

    def setPlainsImage(self):
        if self.temperature<snow_cutoff:
            if self.foliage >= max_foliage-1:
                self.img_type=plains_snow_forest
            elif self.foliage == max_foliage-2:
                self.img_type=plains_snow_sparse_forest
            else:
                self.img_type=plains_snow
        elif self.temperature<temperate_cutoff:
            if self.foliage == max_foliage:
                self.img_type=plains_deep_forest
            elif self.foliage == max_foliage-1:
                self.img_type=plains_forest1
            elif self.foliage == max_foliage-2:
                self.img_type=plains_sparse_forest
            else:
                self.img_type=plains_smooth
        elif self.temperature<deep_desert_cutoff:
            if self.foliage > max_foliage-2:
                self.img_type=desert_greenish
            else:
                self.img_type=desert1
        else:
            if self.foliage > max_foliage-1:
                self.img_type=desert_trees
            else:
                self.img_type=desert_rolling

    def setElevatedImage(self):
        if self.temperature<snow_cutoff:
            if self.foliage > max_foliage-2:
                self.img_type=elevated_snow_forest
            else:
                self.img_type=elevated_snow
        elif self.temperature<temperate_cutoff:
            if self.foliage > max_foliage-2:
                self.img_type=elevated_forest1
            else:
                self.img_type=elevated_rocky1
        else:
            self.img_type=elevated_desert1

    def setMountainImage(self):
        if self.temperature<temperate_cutoff:
            self.img_type=mountain_snow
        else:
            self.img_type=mountain_desert

    def getInfo(self):
        to_return = "\nImage type: "+str(self.img_type)
        to_return += "\nRow:"+str(self.row)+". Col:"+str(self.col)
        to_return += "\nElevation:"+str(self.elevation)
        to_return += "\nTemperature:"+str(self.temperature)
        to_return += "\nFoliage:"+str(self.foliage)
        to_return += "\nCity:"+str(self.city_level)
        to_return += "\nPort:"+str(self.is_port)
        to_return += "\nDirections:"
        for d in self.road_directions:
            to_return += "\n\t"+directionToEnglish(d)
        return to_return
