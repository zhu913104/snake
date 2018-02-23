from single_creep_ran import CREEP
from genetic_algorithm import GA
from neural_network import MLP
import pygame
import numpy as np
from sys import exit
from pygame.locals import *

creep_image_filename = 'img/bluecreep.png'
background_image_filename = 'img/map1.png'
pygame.init()
screen = pygame.display.set_mode((1280 , 720), 0, 32)
creep_image = pygame.image.load(creep_image_filename).convert_alpha()
background = pygame.image.load(background_image_filename).convert()
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
    creep.append(CREEP(creep_image,[153,631],speed=5))
    distance.append([])
    creep_ga.append([])

ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE,Sub_pop_size=Sub_pop_size)

while True:
    clock.tick(600)



    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
    for generation in range(N_GENERATIONS):
        for idx,pop in enumerate(ga.pop):
            for index,individual in enumerate(pop):
                creep_ga[idx].append([])
                distance[idx].append([])
                creep_ga[idx][index]=MLP(individual)

            for _ in range(Sub_pop_size):
                for i in range(POP_SIZE):
                    if creep[i]:
                        if creep[i].crashed:
                            distance[_][i]=creep[i].distance

                            creep[i]=None
                        else:

                            creep_ga[_][i].forward(creep[i].reading_nl)
                            act=np.argmax(creep_ga[_][i].p)

                            creep[i].frame_step(act)


            d=np.array(creep)

            # print(distance,distance.sum())
            if (d==None).all():
                distance_np=np.array(distance)
                np.save("d.npy",distance_np)
                p=distance_np/distance_np.sum()

                ga.evolve(distance_np,p)


                distance=[]
                creep=[]
                for _ in range(Sub_pop_size):
                    creep_ga.append([])
                    distance.append([])
                    for i in range(POP_SIZE):
                        creep.append(CREEP(creep_image, [153, 631], speed=5))
                        distance[_].append([])
                        creep_ga[_].append([])


        print("OK")