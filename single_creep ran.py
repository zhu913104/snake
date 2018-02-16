background_image_filename = 'img/bluecreep.png'

import pygame,math
from pygame.locals import *
from sys import exit
import numpy as np
from pygame.color import THECOLORS

pygame.init()
screen = pygame.display.set_mode((1280 , 720), 0, 32)
background = pygame.image.load(background_image_filename).convert_alpha()
show_sensors = True

x, y = 0, 0
move_x, move_y = 0, 0
Fullscreen = False
draw_screen=True
pos=0
rotate=0
act=0

def wrap_angle(angle):
    return angle%360

class CREEP(object):
    def __init__(self,surface,position,direction=0,speed=1.0):
        self.direction=direction
        self.speed=speed
        self.surface=surface
        self.w, self.h = self.surface.get_size()
        self.surface_rotate=surface
        self.position_rotate = position[0]-self.w/2,position[1]-self.h/2
        self.position=position
    def frame_step(self,action):
        screen.fill(THECOLORS["black"])
        pygame.draw.circle(screen, THECOLORS["red"], ((250, 250)), 100)
        pygame.draw.circle(screen, THECOLORS["red"], ((1000, 300)), 200)
        screen.blit(creep.surface_rotate, creep.position_rotate)
        rotate = 0
        if action == 0:  # Turn left.
            rotate= 5
        elif action == 1:  # Turn right.
            rotate= -5
        if draw_screen:
            pygame.display.flip()
        clock.tick()
        y = math.sin(creep.direction * math.pi / -180)
        x = math.cos(creep.direction * math.pi / -180)
        print(self.get_sonar_readings(self.position[0], 720-self.position[1], self.direction* math.pi / 180))
        self.move(x, y)
        self.rotate(rotate)



    def move(self,x=0,y=0):
        self.position[0] += x*self.speed
        self.position[1] += y*self.speed
        self.position_rotate = self.position[0]-self.w/2,self.position[1]-self.h/2
    def rotate(self,angle):
        self.direction+=angle
        self.surface_rotate = pygame.transform.rotate(self.surface, self.direction)
        self.w, self.h = self.surface_rotate.get_size()
        self.position_rotate=self.surface_rotate.get_rect().move(self.position[0]-self.w/2,self.position[1]-self.h/2)

    def make_sonar_arm(self, x, y):
        spread = 5  # Default spread.
        distance = 10  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))
        return arm_points
    def get_sonar_readings(self, x, y, angle):
        readings = []
        """
        Instead of using a grid of boolean(ish) sensors, sonar readings
        simply return N "distance" readings, one for each sonar
        we're simulating. The distance is a count of the first non-zero
        reading starting at the object. For instance, if the fifth sensor
        in a sonar "arm" is non-zero, then that arm returns a distance of 5.
        """
        # Make our arms.
        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left
        arm_left_f=arm_left
        arm_right_f=arm_left

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.9599310885968813))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.9599310885968813))
        readings.append(self.get_arm_distance(arm_left_f, x, y, angle, 0.4799655442984406))
        readings.append(self.get_arm_distance(arm_right_f, x, y, angle, -0.4799655442984406))

        if show_sensors:
            pygame.display.update()

        return readings
    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= 1280 or rotated_p[1] >= 720:
                return i  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                if self.get_track_or_not(obs) != 0:
                    return i

            if show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)

        # Return the distance for the arm.
        return i
    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = 720 - (y_change + y_1)
        return int(new_x), int(new_y)
    def get_track_or_not(self, reading):
        if reading == THECOLORS['black']:
            return 0
        else:
            return 1

clock = pygame.time.Clock()
creep=CREEP(background,[screen.get_width()/2,screen.get_height()/2],speed=5)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
           exit()
        # if event.type == KEYDOWN:
        #     #键盘有按下？
        #
        #
        #
        #     # if event.key == K_d:
        #     #     y=0
        #     #     x=1
        #     # elif event.key == K_s:
        #     #     y=1
        #     #     x=0
        #     # elif event.key == K_a:
        #     #     y=0
        #     #     x=-1
        #     # elif event.key == K_w:
        #     #     y=-1
        #     #     x=0
        #
        #     if event.key == K_LEFT:
        #         #按下的是左方向键的话，把x坐标减一
        #         act=0
        #     elif event.key == K_RIGHT:
        #         #右方向键则加一
        #         act=1
        #
        # elif event.type == KEYUP:
        #     #如果用户放开了键盘，图就不要动了
        #
        #     act=None
    act=np.random.randint(0,2)
    creep.frame_step(act)
    #计算出新的坐标


    if creep.position[0]>screen.get_width()-background.get_width()+creep.w/2-1:
        creep.position[0]=screen.get_width()-background.get_width()+creep.w/2-1
    if creep.position[0]<=creep.w/2:
        creep.position[0] = creep.w/2
    if creep.position[1]>screen.get_height()-background.get_height()+creep.h/2-1:
        creep.position[1]=screen.get_height()-background.get_height()+creep.h/2-1
    if creep.position[1] <= creep.h/2:
        creep.position[1] = creep.h/2






    drawx,drawy=int(creep.position[0]),int(creep.position[1])

    # for _ in range(-55,56,22):
    #
    #     px,py= int(np.cos(-(creep.direction+_)*np.pi/180)*100+creep.position[0]),int(np.sin(-(creep.direction+_)*np.pi/180)*100+creep.position[1])
    #     pygame.draw.line(screen, (0, 0, 0), (drawx,drawy),  (px,py), 3)






    #在新的位置上画图
    pygame.display.update()

