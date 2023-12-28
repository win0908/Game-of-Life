import pygame
import time
import numpy as np

COLOR_GRID       = ( 50, 50, 50)
COLOR_DIE        = ( 10, 10, 10)
COLOR_ALIVE      = (225,225,225)
COLOR_ALIVE_NEXT = (250, 50, 50)

WIDTH  = 1000
HEIGHT = 1000
SIZE = 10

running = False
progress = False
cells         = np.full((WIDTH // SIZE, HEIGHT // SIZE), 0)
# len(cells)     -> Width  
# len(cells[0])  -> Height  

def updated( cells, SIZE, progress):
    '''
    A live cell dies if it has fewer than two live neighbors.
    A live cell with two or three live neighbors lives on to the next generation.
    A live cell with more than three live neighbors dies.
    A dead cell will be brought back to live if it has exactly three live neighbors.
    '''
    
    updated_cells = np.full((WIDTH // SIZE, HEIGHT // SIZE), 0)
    
    for x in range(len(cells)):
        for y in range(len(cells[x])):
            
            if not progress:
                neighbors = np.sum(cells[x-1:x+2, y-1:y+2]) - round(cells[x,y])
                if cells[x,y] == 1:
                    if neighbors < 2 or neighbors > 3:      updated_cells[x,y]  = 0 
                    elif 2 <= neighbors <= 3:               updated_cells[x,y]  = 1
                else:
                    if neighbors == 3:                      updated_cells[x,y]  = 2
            
            else: 
                if cells[x,y] == 2:                         updated_cells[x,y]  = 1
                else:                                       updated_cells[x,y] = cells[x,y]
    
    return updated_cells


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(COLOR_GRID)
while True:
    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:                
                running = not running                
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pos_x = pos[0] // SIZE
            pos_y = pos[1] // SIZE
            if cells[pos_x, pos_y] == 0:  cells[pos_x, pos_y] = 1
            else: cells[pos_x, pos_y] = 0

    # Draw rect
    #cells = updated_cells
    for x in range(len(cells)):
        for y in range(len(cells[x])):
            if cells[x][y] == 0:
                pygame.draw.rect(screen, COLOR_DIE, (x*SIZE, y*SIZE, SIZE-1, SIZE-1))
            if cells[x][y] == 1:
                pygame.draw.rect(screen, COLOR_ALIVE, (x*SIZE, y*SIZE, SIZE-1, SIZE-1))

            if cells[x][y] == 2:
                pygame.draw.rect(screen, COLOR_ALIVE_NEXT, (x*SIZE, y*SIZE, SIZE-1, SIZE-1))
    
    if running:
        cells = updated( cells, SIZE, progress)
        progress = not progress
    
    # end
    time.sleep(0.01)
    pygame.display.flip()
    pygame.display.update()
    

    


    
            
