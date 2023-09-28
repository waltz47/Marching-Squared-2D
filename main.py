import pygame
from pygame.locals import *
from sys import exit
import time
from marching_squares import *

ROWS = 60
COLS = 60
SCREENSIZE = (800, 800)
CELL_WIDTH = SCREENSIZE[0] / COLS
CELL_HEIGHT = SCREENSIZE[1] / ROWS
POLYGON_COLOR = (75, 99, 110)

pygame.init()
display = pygame.display.set_mode(SCREENSIZE, 0 , 32)
clock = pygame.time.Clock()

square_march_obj = SquareMarch(ROWS, COLS, CELL_WIDTH, CELL_HEIGHT)
# print(square_march_obj.grid)
while True:
    dt = clock.tick(10)
    display.fill((255, 255, 255))
    square_march_obj.build_grid()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        square_march_obj.iso -= 0.05
    if keys[pygame.K_s]:
        square_march_obj.iso += 0.05
    if keys[pygame.K_SPACE]:
        square_march_obj.reseed()
        square_march_obj.build_grid()
    
    lines = square_march_obj.get_polygons()
    for points in lines:
        if(len(points) >= 3):
            pygame.draw.polygon(display, POLYGON_COLOR ,points, width = 0)
    
    pygame.display.update()
