import pygame
from time import sleep
from pygame.locals import *
from random import randint

width = 40
height = 40
dead = (255,255,255)
alive = (0,0,0)
rand_gen = True
grid_size = 16
running = True

screen = pygame.display.set_mode((width*grid_size,height*grid_size))
pygame.init()


def init(rand_gen):
    if rand_gen:
        grid = [[randint(0,1) for x in range(width+1)] for y in range(height+1)]
    else:
        grid = [[0 for x in range(width)] for y in range(height)]
        grid[51][52] = 1
        grid[51][53] = 1
        grid[52][52] = 1
        grid[53][52] = 1
        grid[52][51] = 1

    return grid
grid = init(rand_gen)

def check_logic(location):
    value = 0
    current_state = grid[location[0]][location[1]]
    try:
        above = grid[location[0]+1][location[1]]
    except:
        above = 0
    try:
        below = grid[location[0]-1][location[1]]
    except:
        below = 0
    try:
        left = grid[location[0]][location[1]-1]
    except:
        left = 0
    try:
        right = grid[location[0]][location[1]+1]
    except:
        right = 0
    try:
        topleft = grid[location[0]+1][location[1]-1]
    except:
        topleft = 0
    try:
        topright = grid[location[0]+1][location[1]+1]
    except:
        topright = 0
    try:
        bottomleft = grid[location[0]-1][location[1]-1]
    except:
        bottomleft = 0
    try:
        bottomright = grid[location[0]-1][location[1]+1]
    except:
        bottomright = 0
    value = above + below + left + right + topleft + topright + bottomleft + bottomright
    if current_state == 1:
        if value > 3:
            return False
        elif value > 1:
            return True
        return False
    elif current_state == 0:
        if value == 3:
            return True
        return False

def update_board(location,state):
    if state:
        pygame.draw.rect(screen, alive, (location[1]*grid_size, location[0]*grid_size, grid_size, grid_size))
        new_grid[location[0]][location[1]] = 1
    else:
        new_grid[location[0]][location[1]] = 0

def reset():
    grid = [[randint(0,1) for x in range(width+1)] for y in range(height+1)]
    return grid

def update_game(grid,new_grid):
    grid = new_grid
    new_grid = None
    draw_screen()
    return grid

def draw_screen():
    pygame.display.flip()
    
pause = True
c = 0

while running:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            if event.button == 1: #pause/play on left click
                if pause == True:
                    pause = False
                else:
                    pause = True
            elif event.button == 3: #new randgen on right click
                grid = reset()
                c = 0
        if event.type == QUIT:
                running = False
    if (not pause) or (c == 0):
        screen.fill(dead)
        new_grid = [[0 for x in range(width)] for y in range(height)] 
        for y in range(0,height):
            for x in range(0,width):
                location = [y,x]
                new_state = check_logic(location)
                update_board(location,new_state)
        grid = update_game(grid,new_grid)
        c += 1
pygame.quit()
