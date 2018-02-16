import pygame,math
from pygame.locals import *
from pygame.color import THECOLORS

screen = pygame.display.set_mode((1280 , 720), 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
    if screen.get_at((111,111))==THECOLORS['white']:
        print(THECOLORS['white'])
    screen.fill((255,255,255))
    pygame.display.update()