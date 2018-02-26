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
screen = pygame.display.set_mode((1280, 720), 0, 32)
creep_image = pygame.image.load(creep_image_filename).convert_alpha()
background = pygame.image.load(background_image_filename).convert()
show_sensors = True

Layers = (5, 10,8, 3)
Parameter = 175
CROSS_RATE = 0.1
MUTATE_RATE = 0.09
POP_SIZE = 500
N_GENERATIONS = 300
Sub_pop_size = 1
creep = []
creep_ga = []
distance = []
generation = 0
clock = pygame.time.Clock()

train_historys = np.zeros(2)
np.save("data/train_historys_0226(5, 10,10, 3).npy", train_historys)
pop = np.load("data/parameter_0226(5, 10,8, 3).npy")
# pop=np.array(False)
for i in range(POP_SIZE):
    creep.append(CREEP(creep_image, background, [104, 575], speed= 5, direction=90))
    distance.append([])
    creep_ga.append([])

ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE, pop=pop)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    # while generation<N_GENERATIONS:
    while True:
        for idx, individual in enumerate(ga.pop):
            creep_ga[idx] = MLP(individual, Layers)

        d = 0
        while d <POP_SIZE:
            if creep[d]:
                if creep[d].crashed  :
                    distance[d]=creep[d].distance
                    creep[d]=None
                    print("NO.",d,"distance:",distance[d])
                    d+=1
                elif creep[d].distance>100000:
                    distance[d]=creep[d].distance
                    creep[d]=None
                    # usefulparameter=np.load("data/UsefulParameter.npy")
                    # usefulparameter=np.vstack((usefulparameter,ga.pop[d]))
                    print("NO.",d,"distance:",distance[d])
                    # np.save("data/UsefulParameter.npy",usefulparameter)
                    # print("over 10000",d)
                    d+=1
                else:
                    distance[d]=creep[d].distance
                    creep_ga[d].forward(creep[d].reading_nl)
                    act=np.argmax(creep_ga[d].p)
                    creep[d].frame_step(act)
        d = np.array(creep)

        # print(distance,distance.sum())
        if (d == None).all():
            generation += 1
            distance_np = np.array(distance)
            print("generation", generation, distance_np.max())
            distance = []
            creep = []
            creep_ga = []
            train_historys = np.load("data/train_historys_0226(5, 10,10, 3).npy")
            train_history = np.hstack((generation, distance_np.mean()))
            train_historys = np.vstack((train_historys, train_history))
            np.save("data/train_historys_0226(5, 10,10, 3).npy", train_historys)
            np.save("data/parameter_0226(5, 10,8, 3).npy", ga.pop)
            ga.evolve(distance_np)
            for i in range(POP_SIZE):
                creep.append(CREEP(creep_image, background, [104, 575], speed=5, direction=90))
                distance.append([])
                creep_ga.append([])