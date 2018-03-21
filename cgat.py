from muti_creep import *
from genetic_algorithm import GA
from neural_network import MLP
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
import time



pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width ,height), 0, 32)
Layers = (9, 15,8, 3)
Parameter = 305
clock = pygame.time.Clock()
show_sensors = True
draw_screen = True
start=(370,676)
targetlist=np.array([(750,540),(750,440),(750,340),(750,240),(750,140),(550,140),(550,240),(550,340),(550,440),(550,540),(150,650),(150,550),(150,450),(150,350),(150,250),(150,150),(200,100),(300,100),(400,100),(500,100),(600,100),(700,100),(800,100),(900,100),(1000,100),(1100,100),(1170,150),(1170,250),(1170,350),(1170,450),(1170,550),(1170,650)])
x=np.random.randint(len(targetlist))
target=targetlist[x]
targetlist=np.delete(targetlist,x,0)
font = pygame.font.SysFont("arial", 32)
font_2 = pygame.font.SysFont("arial", 16)
creep_ga=[]
generation=0
distance_limit=100000




pop = np.load("data/parameter_EXB_train_1.npy")

prameter=pop[1]


world = World()

creep = CREEP(world, creep_image, [start[0], start[1]], speed=1, direction=90+np.random.rand())
world.add_entity(creep)
creep_ga.append([])
mask=np.array([0.57357643635104605,0.75183980747897738,0.88701083317822171,0.97134206981326154,1,0.97134206981326154,0.88701083317822171,0.75183980747897738,0.57357643635104605])
while True:
    clock.tick(6)
    id = MLP(prameter,Layers)
    min=0
    reading_mask=0
    while world.all_not_crashed :
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        reading=world.get_reading()[0]

        id.forward(reading)

        if reading.shape!=(0,):
            reading_mask=mask*reading
            min = reading_mask.min()
        action = [np.argmax(id.p)]

        if min > 0.1:
            action = [2]
            selfposition_direction = world.get_direction()[0][0] % 360
            position2taget = world.get_position()[0] - target
            taget_direction = (np.arccos(position2taget[0] / (position2taget[1] ** 2 + position2taget[0] ** 2) ** 0.5) / np.pi * 180) + 180
            taget_direction %= 360
            if position2taget[1] > 0:
                taget_direction -= 360
                taget_direction *= -1
            if ((taget_direction-selfposition_direction)>0 and abs(taget_direction-selfposition_direction)<180) or((taget_direction-selfposition_direction)<0 and abs(taget_direction-selfposition_direction)>180) :
                action=[0]
            elif ((taget_direction-selfposition_direction)<0 and abs(taget_direction-selfposition_direction)<180) or((taget_direction-selfposition_direction)>0 and abs(taget_direction-selfposition_direction)>180) :
                action=[1]
            else:
                action=[2]
        else:
            action=[np.argmax(id.p)]


        position2taget = world.get_position()[0] - target
        if ((position2taget[1] ** 2 + position2taget[0] ** 2) ** 0.5)<20:
            x = np.random.randint(len(targetlist))
            target = targetlist[x]
            targetlist = np.delete(targetlist, x, 0)

        text="Distance to target :"+str(int((position2taget[1] ** 2 + position2taget[0] ** 2) ** 0.5))

        world.render(screen)
        world.process(action)

        screen.blit(font.render(text, True, (255, 0, 0)), (0, 0))

        # if world.get_distance().max()>distance_limit:
        #     distance_limit=world.get_distance().max*1.5
        #     break

        pygame.draw.circle(screen, (255, 255, 255), (target), 10)
        for x in targetlist:
            pygame.draw.circle(screen, (255, 255, 255), (x), 2)

        pygame.display.update()
    if world.all_not_crashed!=True:
        break
