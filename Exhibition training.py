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
start=(1042,676)
targetlist=np.array([(750,540),(750,440),(750,340),(750,240),(750,140),(550,140),(550,240),(550,340),(550,440),(550,540),(150,650),(150,550),(150,450),(150,350),(150,250),(150,150),(200,100),(300,100),(400,100),(500,100),(600,100),(700,100),(800,100),(900,100),(1000,100),(1100,100),(1170,150),(1170,250),(1170,350),(1170,450),(1170,550),(1170,650)])
x = np.random.randint(len(targetlist))
target=targetlist[x]
font = pygame.font.SysFont("arial", 32)
font_2 = pygame.font.SysFont("arial", 16)
creep_ga=[]
generation=0
distance_limit=100000




pop = np.load("data/parameter_EXB_train_1.npy")


ga = GA(DNA_size=Parameter, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE,pop=pop)
world = World()

for creep_no in range(POP_SIZE):
    creep = CREEP(world, creep_image, [start[0], start[1]], speed=2, direction=90+np.random.rand())
    world.add_entity(creep)
    creep_ga.append([])
mask=np.array([0.57357643635104605,0.75183980747897738,0.88701083317822171,0.97134206981326154,1,0.97134206981326154,0.88701083317822171,0.75183980747897738,0.57357643635104605])

while True:
    clock.tick()
    position2taget_distance=[]
    action=[]
    position2taget_exp=[]
    arrived=True
    for idx, individual in enumerate(ga.pop):
        creep_ga[idx] = MLP(individual, Layers)
    while world.all_not_crashed and arrived :
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        for idx, data in enumerate(zip(world.get_reading(),world.get_direction(),world.get_position())):
            min = 0.0
            reading_mask = 0
            creep_ga[idx].forward(data[0])
            action.append([])
            position2taget_distance.append([])
            if data[0].shape!=(0,):
                reading_mask = mask * data[0]
                min = reading_mask.min()
            if min >0.1:
                selfposition_direction = data[1] % 360
                position2taget = data[2] - target
                taget_direction = (np.arccos(
                    position2taget[0] / (position2taget[1] ** 2 + position2taget[0] ** 2) ** 0.5) / np.pi * 180) + 180
                taget_direction %= 360
                if position2taget[1] > 0:
                    taget_direction -= 360
                    taget_direction *= -1
                if ((taget_direction - selfposition_direction) > 0 and abs(
                            taget_direction - selfposition_direction) < 180) or (
                        (taget_direction - selfposition_direction) < 0 and abs(
                            taget_direction - selfposition_direction) > 180):
                    action[idx] = 0
                elif ((taget_direction - selfposition_direction) < 0 and abs(
                            taget_direction - selfposition_direction) < 180) or (
                        (taget_direction - selfposition_direction) > 0 and abs(
                            taget_direction - selfposition_direction) > 180):
                    action[idx] = 1
                else:
                    action[idx] = 2
            else:

                action[idx] = np.argmax(creep_ga[idx].p)
            position2taget = data[2] - target
            position2taget_distance[idx]=np.sqrt(np.square(position2taget[0])+np.square(position2taget[1]))

        position2taget_distance=np.array(position2taget_distance)
        position2taget_exp=np.exp(100/position2taget_distance)

        if position2taget_distance.min()<10.0  or  world.all_not_crashed!=True or world.get_distance().max()>10000:
            generation += 1
            target_new=(0,0)
            p=position2taget_distance.argmin()
            x = np.random.randint(len(targetlist))
            world.set_postion(world.get_position()[p])
            target_new = targetlist[x]
            print(target_new,target)
            print(((target_new[0]-target[0])**2+(target_new[1]+target[1])**2)**0.5)
            while ((target_new[0]-target[0])**2+(target_new[1]+target[1])**2)**0.5 ==0:
                x = np.random.randint(len(targetlist))
                target_new = targetlist[x]
            else:
                target = target_new
            arrived = False
            ga.evolve(position2taget_exp)
            print("eve")


        world.process(action)
        world.render(screen)
        action=[]
        position2taget_distance = []
        # if world.get_distance().max()>distance_limit:
        #     distance_limit=world.get_distance().max*1.5
        #     break

        pygame.draw.circle(screen, (255, 255, 255), (target), 10)
        for x in targetlist:
            pygame.draw.circle(screen, (255, 255, 255), (x), 2)
        text_2="generation:"+str(generation)
        screen.blit(font.render(text_2, True, (255, 0, 0)), (0, 0))
        pygame.display.update()
    np.save("data/parameter_EXB_train_1.npy", ga.pop)