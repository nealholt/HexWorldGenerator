import pygame
from constants import scale,scale_change

def scaleImage(image, scale_factor):
    #Resize the image
    rectangle = image.get_rect()
    dimensions = (int(rectangle.width*scale_factor), int(rectangle.height*scale_factor))
    return pygame.transform.scale(image, dimensions)


def zoom(screen, og_background, zoom_in):
    global scale
    if zoom_in:
        scale += scale_change
    else:
        scale -= scale_change
    print('Scale',scale)
    w = int(og_background.get_width()*scale/100)
    h = int(og_background.get_height()*scale/100)
    screen.fill((0,0,0)) #Erase previous background
    #smoothscale (as opposed to scale) gives a smoother (aka
    #blurrier) feel when zoomed in, but I like it. It looks
    #soft
    return pygame.transform.smoothscale(og_background,(w,h)),scale


def load_image(name, colorkey=None):
    #Load the image from file
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print('ERROR: Failed to load image named "'+name+'". Probably a typo.')
        pygame.quit()
        exit()
    #This next line creates a copy that will draw more quickly on the screen.
    image = image.convert()
    #If colorkey is None, then don't worry about transparency
    if colorkey is not None:
        #colorkey of -1 means that the color of upper left most pixel should
        #be used as transparency color.
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        '''The optional flags argument can be set to pygame.RLEACCEL to provide better performance on non accelerated 
        displays. An RLEACCEL Surface will be slower to modify, but quicker to blit as a source. '''
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    #Return the image and its rectangle
    return image, image.get_rect()


def strip_from_sheet():
    """Strips individual frames from specific sprite sheet.
    This function has been modified oddly to work with this
    particular quirky sprite sheet."""
    sheet,_ = load_image('images/UECvRdS_copy.png', -1)
    r = sheet.get_rect()
    rows = 10
    columns = 15
    img_width = r.w/columns
    img_height = r.h/rows
    frames = []
    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(col*img_width, 1+row*img_height, img_width, img_height-1)
            frames.append(sheet.subsurface(rect))
    return frames


def strip_roads_from_sheet():
    """Strips individual frames from specific sprite sheet.
    This function has been modified oddly to work with this
    particular quirky sprite sheet."""
    sheet,_ = load_image('images/roads_and_rivers.png', -1)

    r = sheet.get_rect()
    rows = 10
    columns = 22
    img_width = r.w/columns
    img_height = r.h/rows

    frames = []
    for row in range(rows):
        for col in range(columns):
            #rect = pygame.Rect(col*img_width, row*img_height, img_width, img_height) #OLD
            rect = pygame.Rect(col*img_width, 1+row*img_height, img_width, img_height-1)
            frames.append(sheet.subsurface(rect))

    #Many images are blank so delete them.
    for i in reversed(range(180,220)): #Ninth and tenth rows
        del frames[i]
    for i in reversed(range(161,176)): #Eighth
        del frames[i]
    for i in reversed(range(136,154)): #Seventh
        del frames[i]
    for i in reversed(range(117,132)): #Sixth
        del frames[i]
    for i in reversed(range(92,110)): #Fifth
        del frames[i]
    for i in reversed(range(73,88)): #Fourth row
        del frames[i]
    for i in reversed(range(13,22)): #First row
        del frames[i]
    return frames

def drawGrid(grid,surface):
    #Draw land tiles
    for row in grid:
        for col in row:
            col.draw(surface)
    #Draw roads second to guarantee
    #that they are drawn above land features.
    for row in grid:
        for col in row:
            col.drawExtras(surface)


def drawMarkings(grid,surface,scale_val, x_adjust=0, y_adjust=0):
    for row in grid:
        for col in row:
            col.drawMarkings(surface,scale_val, x_adjust, y_adjust)
