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
creep_image_filename = 'img/bluecreep.png'
background_image_filename = 'img/map4.png'
Layers=(5,10,3)
Parameter = 93
CROSS_RATE = 0.1
MUTATE_RATE = 0.09
POP_SIZE = 50
N_GENERATIONS = 300
creep_num=20
clock = pygame.time.Clock()
show_sensors = True
draw_screen = True
creep_image = pygame.image.load(creep_image_filename).convert_alpha()
background = pygame.image.load(background_image_filename).convert()
creep_ga=[]
pop=np.array(False)


ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE,pop=pop)
world = World()
for creep_no in range(POP_SIZE):
    creep = CREEP(world, creep_image, [104, 575], speed=1, direction=90)
    world.add_entity(creep)
    creep_ga.append([])

while True:
    clock.tick()
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    for idx, individual in enumerate(ga.pop):
        creep_ga[idx] = MLP(individual, Layers)
    while world.all_not_crashed:


        for idx, reading in enumerate(world.get_reading()):
            creep_ga[idx].forward(reading)
        action=np.vstack([np.argmax(creep_ga_one.p) for creep_ga_one in creep_ga])
        # action = np.random.randint(0, 3, (POP_SIZE))
        world.process(action)
        world.render(screen)
        pygame.display.update()
    print("OK")
    world = World()
    for creep_no in range(POP_SIZE):
        creep = CREEP(world, creep_image, [104, 575], speed=1, direction=90)
        world.add_entity(creep)
