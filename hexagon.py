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
                self.img = frames[23] #snow castle
            else:
                self.img = frames[22] #snow town
        elif self.temperature<temperate_cutoff:
            if self.city_level > 2:
                self.img = frames[10] #stone walled town
            elif self.city_level > 1:
                self.img = frames[9] #wood walled town
            else:
                self.img = frames[8] #town
        else:
            if self.city_level > 2:
                self.img = frames[31] #desert walled town
            elif self.city_level > 1:
                self.img = frames[30] #desert town
            else:
                self.img = frames[29] #desert hut

    def setOceanImage(self,frames):
        if self.elevation<ocean_cutoff:
            self.img = frames[7] #deep ocean
        elif self.elevation<shallows_cutoff:
            if self.temperature<snow_cutoff:
                self.img = frames[21] #icy shallow ocean
            else:
                self.img = frames[6] #shallow ocean

    def setPlainsImage(self,frames):
        if self.temperature<snow_cutoff:
            if self.foliage >= max_foliage-1:
                self.img = frames[18] #snow forest
            elif self.foliage == max_foliage-2:
                self.img = frames[17] #snow sparse forest
            else:
                self.img = frames[16] #snow plains
        elif self.temperature<temperate_cutoff:
            if self.foliage == max_foliage:
                self.img = frames[32] #deep green forest
            elif self.foliage == max_foliage-1:
                self.img = frames[2] #forest
            elif self.foliage == max_foliage-2:
                self.img = frames[1] #sparse forest
            else:
                self.img = frames[0] #plains
        elif self.temperature<deep_desert_cutoff:
            if self.foliage > max_foliage-2:
                self.img = frames[11] #greening desert
            else:
                self.img = frames[24] #desert plains
        else:
            if self.foliage > max_foliage-1:
                self.img = frames[11] #greening desert
            else:
                self.img = frames[26] #desert dunes

    def setElevatedImage(self,frames):
        if self.temperature<snow_cutoff:
            if self.foliage > max_foliage-2:
                self.img = frames[20] #snow elevated forest
            else:
                self.img = frames[19] #snow elevated
        elif self.temperature<temperate_cutoff:
            if self.foliage > max_foliage-2:
                self.img = frames[4] #elevated forest
            else:
                self.img = frames[3] #elevated
        else:
            self.img = frames[25] #desert elevated

    def setMountainImage(self,frames):
        if self.temperature<temperate_cutoff:
            self.img = frames[5] #mountain
        else:
            self.img = frames[27] #desert mountain
