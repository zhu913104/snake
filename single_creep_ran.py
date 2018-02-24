

import pygame,math
from pygame.locals import *
from sys import exit
import numpy as np
from pygame.color import THECOLORS



creep_image_filename = 'img/bluecreep.png'
background_image_filename = 'img/map2.png'
pygame.init()
screen = pygame.display.set_mode((1280 , 720), 0, 32)
creep_image = pygame.image.load(creep_image_filename).convert_alpha()
background = pygame.image.load(background_image_filename).convert()
show_sensors = False
draw_screen = True

num=3
x=[]
ck=[]
act=0
dist=[]


class CREEP(object):
    def __init__(self,surface,background,position,direction=0,speed=1.0):
        self.direction=direction
        self.speed=speed
        self.surface=surface
        self.w, self.h = self.surface.get_size()
        self.surface_rotate=surface
        self.position_rotate = position[0]-self.w/2,position[1]-self.h/2
        self.position=position
        self.distance=0
        self.crashed=False
        self.reading=[]
        self.reading_nl=[]
        self.background=background
    def frame_step(self,action):
        screen.blit(self.background, (0,0))

        screen.blit(self.surface_rotate, self.position_rotate)
        rotate = 0
        if action == 0:  # Turn left.
            rotate= 5
        elif action == 1:  # Turn right.
            rotate= -5

        clock.tick()
        y = math.sin(self.direction * math.pi / -180)
        x = math.cos(self.direction * math.pi / -180)
        self.reading=self.get_sonar_readings(self.position[0], 720-self.position[1], self.direction* math.pi / 180)
        # print(reading,self.distance)
        self.reading_nl=np.array( self.reading)/39

        self.move(x, y)
        self.rotate(rotate)
        if draw_screen:
            pygame.display.flip()
        if self.car_is_crashed(self.reading):
            self.crashed = True

        else:
            self.distance+=1



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
        spread = 10  # Default spread.
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
        readings.append(self.get_arm_distance(arm_left_f, x, y, angle, 0.4799655442984406))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right_f, x, y, angle, -0.4799655442984406))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.9599310885968813))



        if show_sensors:
            pygame.display.update()
        readings=np.array(readings)
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
        if reading == THECOLORS['green']:
            return 1
        else:
            return 0
    def car_is_crashed(self,reading):
        if (reading==1).any():
            return True
        else:
            return False
    def recover_from_crash(self):
        """
        We hit something, so recover.
        """
        while self.crashed:
            # Go backwards.
            self.crashed = False
            for i in range(10):
                self.direction += 2  # Turn a little.
                self.position=[np.random.randint(1280),np.random.randint(720)]
                clock.tick()


clock = pygame.time.Clock()


