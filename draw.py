#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit

from random import *
from math import pi

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
points = []
screen.fill((0, 0, 0))

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            # 按任意键可以清屏并把点回复到原始状态
            points = []
            screen.fill((255, 255, 255))
        if event.type == MOUSEBUTTONDOWN:

            # 获得当前鼠标点击位置
            x, y = pygame.mouse.get_pos()
            points.append((x, y))
            # 画点击轨迹图
            if len(points) > 1:
                pygame.draw.line(screen, (255, 255, 255), (0, 0), (x, y),5)
                # pygame.draw.lines(screen, (0, 255, 0), (0,0), (x,y), 2)
            # 和轨迹图基本一样，只不过是闭合的，因为会覆盖，所以这里注释了
            # if len(points) >= 3:
            #    pygame.draw.polygon(screen, (0, 155, 155), points, 2)
            # 把每个点画明显一点
            for p in points:
                pygame.draw.circle(screen, (155, 155, 155), p, 3)

    pygame.display.update()