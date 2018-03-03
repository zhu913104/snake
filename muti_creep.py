import pygame,math
from pygame.locals import *
from sys import exit
import numpy as np
from pygame.color import THECOLORS


pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width ,height), 0, 32)
creep_image_filename = 'img/bluecreep.png'
background_image_filename = 'img/map7.png'


clock = pygame.time.Clock()
show_sensors = False
draw_screen = True
creep_image = pygame.image.load(creep_image_filename).convert_alpha()
background = pygame.image.load(background_image_filename).convert()





class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.background = pygame.display.set_mode((width , height), 0, 32)
        self.background.blit(background, (0,0))
        self.all_not_crashed =True
        self.crash_num=0

    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1


    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, action):
        for entity,act in zip(self.entities.values(),action):
            entity.process(act)
        crash_num=np.vstack([entity.crashed for entity in self.entities.values()])
        crash_num=crash_num.astype(int).sum()
        self.crash_num=crash_num
        if np.vstack([entity.crashed for entity in self.entities.values()]).all()==True:
            self.all_not_crashed=False

    def render(self, surface):
        self.background.blit(background, (0,0))
        for entity in self.entities.values():
            entity.render(surface)
    def get_distance(self):
        return np.hstack([entity.distance for entity in self.entities.values()])
    def get_reading(self):
        return np.vstack([entity.reading_nl for entity in self.entities.values()])





class GameEntity(object):
    def __init__(self, world, name, image,position,speed):
        self.world = world
        self.name = name
        self.image = image
        self.image_rotate = image

        self.location = position
        self.speed = 0.
        self.id = 0

    def render(self, surface):
        surface.blit(self.image_rotate, self.position_rotate)
    # def process(self, time_passed,action):
    #     if self.speed > 0. and self.location != self.destination:
    #         vec_to_destination = self.destination - self.location
    #         distance_to_destination = vec_to_destination.get_length()
    #         heading = vec_to_destination.get_normalized()
    #         travel_distance = min(distance_to_destination, time_passed * self.speed)
    #         self.location += travel_distance * heading



class CREEP(GameEntity):
    def __init__(self,world,image,position,direction=0,speed=1.0):
        GameEntity.__init__(self, world, "creep", image,position,speed)
        self.direction=direction
        self.speed=speed
        self.w, self.h = width ,height
        self.position_rotate = position[0]-self.w/2,position[1]-self.h/2
        self.position=position
        self.distance=0
        self.crashed=False
        self.reading=[]
        self.reading_nl=[]
    def process(self,action):
        if self.crashed !=True:
            rotate = 0
            if action == 0:  # Turn left.
                rotate= 5
            elif action == 1:  # Turn right.
                rotate= -5
            y = math.sin(self.direction * math.pi / -180)
            x = math.cos(self.direction * math.pi / -180)
            self.reading=self.get_sonar_readings(self.position[0], 720-self.position[1], self.direction* math.pi / 180)
            # print(reading,self.distance)
            self.reading_nl=np.array( self.reading)/79
            self.move(x, y)
            self.rotate(rotate)
            if self.car_is_crashed(self.reading):
                self.crashed = True
            else:
                self.distance+=1*self.speed



    def move(self,x=0,y=0):
        self.position[0] += x*self.speed
        self.position[1] += y*self.speed
        self.position_rotate = self.position[0]-self.w/2,self.position[1]-self.h/2
    def rotate(self,angle):
        self.direction+=angle
        self.image_rotate = pygame.transform.rotate(self.image, self.direction)
        self.w, self.h = self.image_rotate.get_size()
        self.position_rotate=self.image_rotate.get_rect().move(self.position[0]-self.w/2,self.position[1]-self.h/2)

    def make_sonar_arm(self, x, y):
        spread = 5  # Default spread.
        distance = 5  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 80):
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
        arm_left_f0=arm_left
        arm_right_f0=arm_left
        arm_right_f1=arm_left
        arm_left_f1=arm_left
        arm_right_f2=arm_left
        arm_left_f2=arm_left


        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.9599310885968813))
        readings.append(self.get_arm_distance(arm_left_f2, x, y, angle, 0.719948316447661))
        readings.append(self.get_arm_distance(arm_left_f1, x, y, angle, 0.4799655442984406))
        readings.append(self.get_arm_distance(arm_left_f0, x, y, angle, 0.2399827721492203))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right_f0, x, y, angle, -0.2399827721492203))
        readings.append(self.get_arm_distance(arm_right_f1, x, y, angle, -0.4799655442984406))
        readings.append(self.get_arm_distance(arm_right_f2, x, y, angle, -0.719948316447661))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.9599310885968813))




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
    def render(self, surface):
        GameEntity.render(self, surface)


# world = World()
# for creep_no in range(creep_num):
#     creep=CREEP(world,creep_image, [np.random.randint(500,1000), np.random.randint(200,300)], speed=1, direction=90)
#     world.add_entity(creep)
#
# while True:
#     clock.tick()
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     while world.all_not_crashed:
#
#         action=np.random.randint(0,3,(creep_num))
#
#         world.process(action)
#         world.render(screen)
#         pygame.display.update()
#     print("OK")
#     world = World()
#     for creep_no in range(creep_num):
#         creep = CREEP(world, creep_image, [np.random.randint(500, 1000), np.random.randint(200, 300)], speed=1,
#                       direction=90)
#         world.add_entity(creep)

