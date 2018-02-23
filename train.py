from single_creep_ran import CREEP
from genetic_algorithm import GA
from neural_network import MLP
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
import time

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
MUTATE_RATE = 0.5
POP_SIZE = 50
N_GENERATIONS = 300
Sub_pop_size = 1
creep=[]
creep_ga=[]
distance=[]

clock = pygame.time.Clock()


for i in range(POP_SIZE):
    creep.append(CREEP(creep_image,[153,631],speed=5))
    distance.append([])
    creep_ga.append([])

ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
    for generation in range(100):
        for idx,individual in enumerate(ga.pop):
            creep_ga[idx]=MLP(individual)

        for i in range(POP_SIZE):

            if creep[i]:
                if creep[i].crashed  :
                    distance[i]=creep[i].distance
                    creep[i]=None
                    np.save("over1000.npy",creep_ga[i])
                elif creep[i].distance>10000:
                    distance[i]=creep[i].distance
                    creep[i]=None
                    np.save("over1000.npy",creep_ga[i])
                else:
                    distance[i]=creep[i].distance
                    creep_ga[i].forward(creep[i].reading_nl)
                    act=np.argmax(creep_ga[i].p)
                    creep[i].frame_step(act)
        d=np.array(creep)

        # print(distance,distance.sum())
        if (d==None).all() :
            print("generation",generation,distance)
            distance_np=np.array(distance)
            distance=[]
            creep=[]
            creep_ga=[]
            np.save("distance_np.npy",distance_np)
            np.save("parameter.npy",ga.pop)
            ga.evolve(distance_np)
            for i in range(POP_SIZE):
                creep.append(CREEP(creep_image, [153, 631], speed=5))
                distance.append([])
                creep_ga.append([])