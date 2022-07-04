# -*- coding: utf-8 -*-
"""

@author: z.czaplinski
"""


import pygame
import sys
from pygame.locals import *
import numpy as np
from scipy.spatial import cKDTree


# load images
bacground = pygame.image.load("background.jpeg")
shark = pygame.image.load("shark.png")
fish = pygame.image.load("fish.png")
x,y = bacground.get_size()

# parametrs
n = 100                     # number of fishes
level_of_fear = 120         
level_of_friendship =10
level_of_coping = 1
speed = 1

#
pos = 0
vel = 0
x_s = 0
y_s = 0


def generate_fish(n, x, y):
    
    global pos

    np.random.seed(17)
    pos = np.random.rand(n, 2) * np.array([x, y])


def generate_velocity(n, speed):
    
    global vel
    
    vel = np.zeros((n, 2))
    theta = 2*np.pi*np.random.randn(n)

    vel[:, 0] += speed*np.cos(theta)
    vel[:, 1] += speed*np.sin(theta)


def fish_friends(pos, speed, level_of_friendship, level_of_coping):

    # Boids try to fly towards the centre of mass of neighbouring boids
    d = (np.average(pos, axis=0))*(n/(n-1))
    vec = ((d - pos)/100)

    # Boids try to keep a small distance away from other boids
    tree = cKDTree(pos)
    pairs = tree.query_pairs(level_of_friendship, p=2)

    for (i, j) in pairs:
        c = -(pos[i, :] - pos[j, :])
        vec[i, :] += c
        vec[j, :] += c

    # Boids try to match velocity with near boids
    b = (np.average(vel, axis=0))*(n/(n-1))
    vec += ((b-vel)/8)*level_of_coping

    # raning away from shark
    tree_f = cKDTree(pos)
    points = tree_f.query_ball_point((x_s, y_s), level_of_fear)
    for k in points:
        d = (pos[k, :] - np.array([x_s, y_s]))/8
        vec[k, :] += d

    return vec


def sharky(shark):
    global x_s, y_s
    pic_wid = shark.get_width()
    pic_heig = shark.get_width()
    mx, my = pygame.mouse.get_pos()
    vec1 = pygame.math.Vector2(x_s-mx, y_s-my)
    vec2 = pygame.math.Vector2(0, 1)

    angle = vec1.angle_to(vec2)
    if angle != 90.0:
        shark = pygame.transform.rotate(shark, angle)

    window.blit(shark, (mx-0.5*pic_wid, my-0.5*pic_heig))

    x_s = mx
    y_s = my


# main game loop:

def main():
    global pos
    generate_fish(n, x, y)
    generate_velocity(n, speed)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        window.blit(bacground, (0, 0))

        for i in range(n):
            window.blit(fish, (pos[i, 0], pos[i, 1]))

        sharky(shark)
        v = fish_friends(pos, speed, level_of_friendship, level_of_coping)
        pos += (vel+v)
        
        #boundry conditions 
        pos[:, 0] = pos[:, 0] % x
        pos[:, 1] = pos[:, 1] % y

        pygame.display.flip()
        clock.tick(30)


# creating a simulation window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((x, y))
pygame.display.set_caption('Symulacja ')


main()
