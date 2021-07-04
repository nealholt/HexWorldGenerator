from map_generation import *
clock = pygame.time.Clock()
surface = pygame.display.set_mode((1000,600))

#Get all the hex tile images
frames = strip_from_sheet()
#Get the grid world of hexes
grid,water = resetGrid(frames)
background = pygame.Surface((1000,600))
print('Drawing')
drawGrid(grid,background)
print('Drawing complete')
original_background = background.copy()
#Most recently clicked cell
selected = None

vertical_adjust = 0
horizontal_adjust = 0
scroll_up = False
scroll_down = False
scroll_left = False
scroll_right = False

done=False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == 32: #Space bar
                #Reset the world
                grid,water=resetGrid(frames)
                background = pygame.Surface((1000,600))
                print('Drawing')
                drawGrid(grid,background)
                print('Drawing complete')

            scroll_up = event.key == 273 or event.key == 119
            scroll_down = event.key == 274 or event.key == 115
            scroll_left = event.key == 276 or event.key == 97
            scroll_right = event.key == 275 or event.key == 100

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #Mouse wheel rolled away from body
                background,scale=zoom(surface,original_background,False)
            elif event.button == 5: #Mouse wheel rolled towards body
                background,scale=zoom(surface,original_background,True)
            else: #Left or right mouse click
                pos = pygame.mouse.get_pos()
                selected = markClicked(pos,grid,water,selected,scale)

    if scroll_up:
        vertical_adjust += 1
    elif scroll_down:
        vertical_adjust -= 1
    if scroll_right:
        horizontal_adjust -= 1
    elif scroll_left:
        horizontal_adjust += 1

    surface.blit(background, (horizontal_adjust, vertical_adjust))
    drawMarkings(grid,surface,scale)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()