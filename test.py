import pygame,math
from pygame.locals import *
from pygame.color import THECOLORS
pygame.init()
screen = pygame.display.set_mode((1280 , 720), 0, 32)
font = pygame.font.SysFont("arial", 16)
pygame.display.update()
def show_text(text, x, y):#專門顯示文字的方法，除了顯示文字還能指定顯示的位置
    x = x
    y = y
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x, y))
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
           exit()

    show_text("aaa",0,100)
    pygame.display.update()