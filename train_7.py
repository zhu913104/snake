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
start=(1153,616)
font = pygame.font.SysFont("arial", 32)
font_2 = pygame.font.SysFont("arial", 16)
creep_ga=[]
generation=0
distance_limit=100000
# pop=np.array(False)
train_historys = np.zeros(2)
np.save("data/train_historys_map7_GA_5(9, 15,8, 3).npy", train_historys)
pop = np.load("data/parameter_map2(9, 15,8, 3).npy")
# pop=np.array(False)
TUNR_OFF=True


ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE,pop=pop)
world = World()
for creep_no in range(POP_SIZE):
    creep = CREEP(world, creep_image, [start[0], start[1]], speed=2, direction=90+np.random.rand())
    world.add_entity(creep)
    creep_ga.append([])

while generation<301:
    clock.tick()

    for idx, individual in enumerate(ga.pop):
        creep_ga[idx] = MLP(individual, Layers)
    while world.all_not_crashed :
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        for idx, reading in enumerate(world.get_reading()):
            creep_ga[idx].forward(reading)
        action=np.vstack([np.argmax(creep_ga_one.p) for creep_ga_one in creep_ga])
        # action = np.random.randint(0, 3, (POP_SIZE))
        # print(world.get_distance().max())
        text="max distance:"+str(world.get_distance().max())
        text_2="Number of survivors:"+str(POP_SIZE-world.crash_num)
        world.process(action)
        world.render(screen)
        screen.blit(font.render(text, True, (255, 0, 0)), (0, 0))
        screen.blit(font_2.render(text_2, True, (255, 0, 0)), (0, 32))
        # if world.get_distance().max()>distance_limit:
        #     distance_limit=world.get_distance().max*1.5
        #     break
        pygame.display.update()
    if world.all_not_crashed!=True:
        generation += 1
        print("generation",generation,text,"mean distance:",world.get_distance().mean())
        distances=world.get_distance()
        ga.evolve(distances)
        world = World()
        train_historys = np.load("data/train_historys_map7_GA_5(9, 15,8, 3).npy")
        train_history = np.hstack((distances.mean(),distances.max()))
        train_historys = np.vstack((train_historys, train_history))
        np.save("data/train_historys_map7_GA_5(9, 15,8, 3).npy", train_historys)
        np.save("data/parameter_map7_GA_5(9, 15,8, 3).npy", ga.pop)
        for creep_no in range(POP_SIZE):
            creep = CREEP(world, creep_image, [start[0], start[1]], speed=2, direction=90+np.random.rand())
            world.add_entity(creep)
