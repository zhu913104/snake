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
CROSS_RATE = 0.3
MUTATE_RATE = 0.15
POP_SIZE = 500
N_GENERATIONS = 300
clock = pygame.time.Clock()
show_sensors = True
draw_screen = True
start=(500,500)
font = pygame.font.SysFont("arial", 32)
font_2 = pygame.font.SysFont("arial", 16)
creep_ga=[]
generation=0
distance_limit=100000



pop = np.load("data/parameter_map7_CGA_2(9, 15,8, 3).npy")

prameter=pop[0]

ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE,pop=pop)
world = World()

creep = CREEP(world, creep_image, [start[0], start[1]], speed=.2, direction=-90+np.random.rand())
world.add_entity(creep)
creep_ga.append([])
mask=np.array([0.57357643635104605,0.75183980747897738,0.88701083317822171,0.97134206981326154,1,0.97134206981326154,0.88701083317822171,0.75183980747897738,0.57357643635104605])
while True:
    clock.tick(6)
    id = MLP(prameter,Layers)
    Safety_rate=0
    while world.all_not_crashed :
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        reading=world.get_reading()[0]

        id.forward(reading)
        print(reading.shape,mask.shape)
        if reading.shape!=(0,):
            Safety_rate=mask.dot(reading)
        action = [np.argmax(id.p)]
        if Safety_rate>4.5:
            action=[2]
        else:
            action=[np.argmax(id.p)]
        print(action)
        # action = np.random.randint(0, 3, (POP_SIZE))
        # print(world.get_distance().max())
        text="max distance:"+str(world.get_distance().max())
        text_2="Number of survivors:"+str(POP_SIZE-world.crash_num)
        text_3="Safety_rate"+str(Safety_rate)
        world.process(action)
        world.render(screen)
        screen.blit(font.render(text, True, (255, 0, 0)), (0, 0))
        screen.blit(font_2.render(text_2, True, (255, 0, 0)), (0, 32))
        screen.blit(font_2.render(text_3, True, (255, 0, 0)), (0, 48))
        # if world.get_distance().max()>distance_limit:
        #     distance_limit=world.get_distance().max*1.5
        #     break
        pygame.display.update()
    if world.all_not_crashed!=True:
        break
