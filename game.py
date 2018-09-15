import pygame
from time import sleep
from pygame.locals import *
from random import randint
from math import floor

width = 200
height = 200
dead = (255,255,255)
alive = (0,0,0)
rand_gen = False
grid_size = 4
running = True

screen = pygame.display.set_mode((width*grid_size,height*grid_size))
pygame.init()


def init(rand_gen):
    grid = reset(rand_gen)
    return grid

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

def update_board(location,state,new_grid):
    if state:
        pygame.draw.rect(screen, alive, (location[1]*grid_size, location[0]*grid_size, grid_size, grid_size))
        new_grid[location[0]][location[1]] = 1
    else:
        new_grid[location[0]][location[1]] = 0

def change_life(x,y):
    if grid[y][x] == 1:
        grid[y][x] = 0
    else:
        grid[y][x] = 1
    special_screen_draw()

def next_gen(grid,c):
    screen.fill(dead)
    new_grid = [[0 for x in range(width)] for y in range(height)] 
    for y in range(0,height):
        for x in range(0,width):
            location = [y,x]
            new_state = check_logic(location)
            update_board(location,new_state,new_grid)
    grid = update_game(grid,new_grid)
    c += 1
    return grid,c

def reset(rand_gen,saved_grid=False):
    if (saved_grid != False):
        grid = saved_grid
    elif rand_gen:
        grid = [[randint(0,1) for x in range(width+1)] for y in range(height+1)]
    else:
        grid = [[0 for x in range(width)] for y in range(height)]
        x = round(width/2)
        y = round(height/2)
        grid[y + 1][x + 2] = 1
        grid[y + 1][x + 3] = 1
        grid[y + 2][x + 2] = 1
        grid[y + 3][x + 2] = 1
        grid[y + 2][x + 1] = 1
    return grid

def save(grid):
    saved_grid = grid
    return saved_grid

def update_game(grid,new_grid):
    grid = new_grid
    new_grid = None
    draw_screen()
    return grid

def draw_screen():
    pygame.display.flip()

def special_screen_draw():
    screen.fill(dead)
    for y in range(0,height):
        for x in range(0,width):
            location = [y,x]
            state = grid[location[0]][location[1]]
            if state == 1:
                pygame.draw.rect(screen, alive, (location[1]*grid_size, location[0]*grid_size, grid_size, grid_size))
    draw_screen()

pause = True
buildmode = False
c = -1

grid = init(rand_gen)
saved_grid = False

while running:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            if event.button == 1: #pause/play on left click
                if buildmode == False:
                    if pause == True:
                        pause = False
                        print("resumed")
                    else:
                        print("paused")
                        pause = True
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print(mouse_x,mouse_y)
                    grid_x = floor(mouse_x/grid_size)
                    grid_y = floor(mouse_y/grid_size)
                    print(grid_x,grid_y)
                    change_life(grid_x,grid_y)
            elif event.button == 3: #new randgen on right click
                grid = reset(rand_gen)
                c = -1
                print("reset")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pause == True:
                    pause = False
                    print("resumed")
                else:
                    print("paused")
                    pause = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                grid = reset(rand_gen)
                c = -1
                print("reset")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                if buildmode == True:
                    buildmode = False
                    print("build mode off")
                else:
                    buildmode = True
                    print("build mode on")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                print("step generation")
                grid,c = next_gen(grid,c)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print("save game")
                saved_grid = save(grid)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                if saved_grid != False:
                    print("load game")
                    grid = reset(rand_gen,saved_grid)
                    c = -1
                else:
                    print("no save to load")
        if event.type == QUIT:
                running = False
    if (c == -1) and (pause == True):
        special_screen_draw()
        c = 0
    
    if (not pause):
        grid,c = next_gen(grid,c)
pygame.quit()

