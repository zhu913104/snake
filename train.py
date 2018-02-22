from single_creep_ran import CREEP
from genetic_algorithm import GA
from neural_network import MLP
import pygame
import numpy as np
from sys import exit
from pygame.locals import *

background_image_filename = 'img/bluecreep.png'
pygame.init()
screen = pygame.display.set_mode((1280 , 720), 0, 32)
background = pygame.image.load(background_image_filename).convert_alpha()
show_sensors = True

Layers=(5,10,3)
Parameter = 93
CROSS_RATE = 0.05
MUTATE_RATE = 0.05
POP_SIZE = 5
N_GENERATIONS = 1000
Sub_pop_size = 1
creep=[]
creep_ga=[]
distance=[]

clock = pygame.time.Clock()


for i in range(POP_SIZE):
    creep.append(CREEP(background,[600,500],speed=5))
    distance.append([])
    creep_ga.append([])

ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE,Sub_pop_size=Sub_pop_size)

while True:
    clock.tick(600)



    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
    for generation in range(N_GENERATIONS):
        for pop in ga.pop:
            for index,individual in enumerate(pop):
                creep_ga[index]=MLP(individual)
        # print(len(creep_ga),len(creep))
            for i in range(POP_SIZE):
                if creep[i]:
                    if creep[i].crashed:
                        distance[i]=creep[i].distance

                        creep[i]=None
                    else:

                        creep_ga[i].forward(creep[i].reading_nl)
                        act=np.argmax(creep_ga[i].p)

                        creep[i].frame_step(act)


                d=np.array(creep)
                # print(distance,distance.sum())
                if (d==None).all():
                    distance_np=np.array(distance)
                    print(distance_np)
                    creep=[]

                    for i in range(POP_SIZE):
                        creep.append(CREEP(background, [np.random.randint(1280), np.random.randint(720)], speed=5))


