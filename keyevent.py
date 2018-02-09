background_image_filename = 'img/bluecreep.png'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.image.load(background_image_filename).convert_alpha()

x, y = 0, 0
move_x, move_y = 0, 0
Fullscreen = False
pos=0

class CREEP(object):
    def __init__(self,surface,position,direction=0,speed=1.0):
        self.position=position
        self.direction=direction
        self.speed=speed
        self.surface=surface
    def move(self,x=0,y=0):
        self.position[0] += x*self.speed
        self.position[1] += y*self.speed
    def rotate(self,angle):
        if self.direction==angle:
            pass
        elif abs(self.direction-angle)==2:
            self.surface = pygame.transform.rotate(self.surface, 180)
        elif self.direction-angle==1 or self.direction-angle==-3:
            self.surface = pygame.transform.rotate(self.surface, 90)
        elif self.direction-angle==-1 or self.direction-angle==3:
            self.surface = pygame.transform.rotate(self.surface, 270)
        self.direction=angle


creep=CREEP(background,[0,0],speed=0.05)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
        if event.type == KEYDOWN:
            #键盘有按下？
            if event.key==K_f:
                Fullscreen=not Fullscreen
                if Fullscreen:
                    screen = pygame.display.set_mode((640, 480), FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode((640, 480), 0, 32)

            if event.key == K_LEFT:
                #按下的是左方向键的话，把x坐标减一
                x=-1
                y=0
                creep.rotate(2)
            elif event.key == K_RIGHT:
                #右方向键则加一
                x=1
                y=0
                creep.rotate(0)

            elif event.key == K_UP:
                y=-1
                x=0
                creep.rotate(3)

            elif event.key == K_DOWN:
                y=1
                x=0
                creep.rotate(1)
        elif event.type == KEYUP:
            #如果用户放开了键盘，图就不要动了
            x=0
            y=0
    #计算出新的坐标
    if creep.position[0]>=625:
        creep.position[0]=625
    if creep.position[0]<=0:
        creep.position[0] = 0
    if creep.position[1]>=465:
        creep.position[1]=465
    if creep.position[1] <= 0:
        creep.position[1] = 0

    creep.move(x,y)
    screen.fill((255,255,255))
    screen.blit(creep.surface, creep.position)
    #在新的位置上画图
    pygame.display.update()