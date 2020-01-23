from map_generation import *
clock = pygame.time.Clock()
surface = pygame.display.set_mode((1000,600))

#Get all the hex tile images
frames = strip_from_sheet()
#Get the grid world of hexes
grid,water = resetGrid(frames)
background = pygame.Surface((1000,600))
drawGrid(grid,background)
original_background = background.copy()
#Most recently clicked cell
selected = None


done=False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            #print(event.key)
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == 32: #Space bar
                #Reset the world
                grid,water=resetGrid(frames)
                background = pygame.Surface((1000,600))
                drawGrid(grid,background)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #Mouse wheel rolled away from body
                background=zoom(surface,original_background,False)
            elif event.button == 5: #Mouse wheel rolled towards body
                background=zoom(surface,original_background,True)
            else: #Left or right mouse click
                pos = pygame.mouse.get_pos()
                selected = markClicked(pos,grid,water,selected)

    surface.blit(background, (0, 0))
    drawMarkings(grid,surface)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()