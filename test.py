from single_creep_ran import CREEP
from genetic_algorithm import GA
from neural_network import MLP
import pygame
import numpy as np
from sys import exit
from pygame.locals import *
import time

creep_image_filename = 'img/bluecreep.png'
background_image_filename = 'img/map3.png'
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


distance=[]

clock = pygame.time.Clock()

pop=np.load("data/parameter_0223.npy")

creep=CREEP(creep_image,background,[104,575],speed=5,direction=90)




while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
    for  idx,i in enumerate(pop):
        creep_ga = MLP(i)
        if creep:
            if creep.crashed  :
                creep=None
                creep = CREEP(creep_image, background, [104, 575], speed=5, direction=90)
            else:
                creep_ga.forward(creep.reading_nl)
                act=np.argmax(creep_ga.p)
                creep.frame_step(act)

        # print(distance,distance.sum())
