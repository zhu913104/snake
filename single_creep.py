background_image_filename = 'img/bluecreep.png'

import pygame,math
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1920, 1080), 0, 32)
background = pygame.image.load(background_image_filename).convert_alpha()

x, y = 0, 0
move_x, move_y = 0, 0
Fullscreen = False
pos=0
rotate=0

def wrap_angle(angle):
    return angle%360

class CREEP(object):
    def __init__(self,surface,position,direction=0,speed=1.0):
        self.direction=direction
        self.speed=speed
        self.surface=surface
        self.w, self.h = self.surface.get_size()
        self.surface_rotate=surface
        self.position_rotate = position[0]-self.w/2,position[1]-self.h/2
        self.position=position

    def move(self,x=0,y=0):
        self.position[0] += x*self.speed
        self.position[1] += y*self.speed
        self.position_rotate = self.position[0]-self.w/2,self.position[1]-self.h/2
    def rotate(self,angle):
        self.direction+=angle
        self.surface_rotate = pygame.transform.rotate(self.surface, self.direction)
        self.w, self.h = self.surface_rotate.get_size()
        self.position_rotate=self.surface_rotate.get_rect().move(self.position[0]-self.w/2,self.position[1]-self.h/2)


clock = pygame.time.Clock()
creep=CREEP(background,[screen.get_width()/2,screen.get_height()/2],speed=2)

while True:
    clock.tick(60)
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


            # if event.key == K_d:
            #     y=0
            #     x=1
            # elif event.key == K_s:
            #     y=1
            #     x=0
            # elif event.key == K_a:
            #     y=0
            #     x=-1
            # elif event.key == K_w:
            #     y=-1
            #     x=0

            elif event.key == K_LEFT:
                #按下的是左方向键的话，把x坐标减一
                rotate = 5
            elif event.key == K_RIGHT:
                #右方向键则加一
                rotate = -5

        elif event.type == KEYUP:
            #如果用户放开了键盘，图就不要动了
            x=0
            y=0
            rotate = 0
    #计算出新的坐标
    y=math.sin(creep.direction*math.pi/-180)
    x=math.cos(creep.direction*math.pi/-180)

    if creep.position[0]>screen.get_width()-background.get_width()+creep.w/2-1:
        creep.position[0]=screen.get_width()-background.get_width()+creep.w/2-1
    if creep.position[0]<=creep.w/2:
        creep.position[0] = creep.w/2
    if creep.position[1]>screen.get_height()-background.get_height()+creep.h/2-1:
        creep.position[1]=screen.get_height()-background.get_height()+creep.h/2-1
    if creep.position[1] <= creep.h/2:
        creep.position[1] = creep.h/2

    creep.rotate(rotate)
    creep.move(x,y)
    screen.fill((255,255,255))

    screen.blit(creep.surface_rotate, creep.position_rotate)
    #在新的位置上画图
    pygame.display.update()

