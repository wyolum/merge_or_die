#! /usr/bin/env python

import os
import random
import pygame
import time

# Class for the orange dude
class Player(object):
    
    def __init__(self, pos, speed=0):
        self.speed = speed
        self.rect = pygame.Rect(pos[0], pos[1], 22, 32)
        self.fx = float(pos[0])
        self.fy = float(pos[1])

    def set_x(self, x):
        self.fx = x
        self.rect.x = x
    def get_x(self):
        return self.fx
    x = property(get_x, set_x)
    def set_y(self, y):
        self.fy = y
        self.rect.y = y
    def get_y(self):
        return self.fy
    y = property(get_y, set_y)
    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
        if self.rect.y < 0:
            self.fy = HEIGHT
            self.rect.y = HEIGHT
    def move_single_axis(self, dx, dy):
        self.fy += float(dy)
        # Move the rect
        self.rect.x += dx
        self.rect.y = self.fy
        # self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

# Nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")
WIDTH = 520
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
start_x = 420
start_y = HEIGHT - 50
player = Player((start_x, start_y)) # Create the player
drones = []
spacing = 250
for j in range(8):
    speed = 1.5 + j / 4. +  random.uniform(.5, 1)
    for i in range(HEIGHT // spacing):
        drones.append(Player((378 - 40 * j,16 + spacing * i + spacing/2  * j), speed)) # Create the other drivers
# Holds the level layout in a list of strings.
level = [
"               W         W    ",
"               W         W    ",
"               W          W   ",
"W              W           W  ",
" W             W            W  ",
"  W            W             W",
"   W           W              W",
" E  W          W               W",
"    W          W               W",
"    W          W               W",
"    W          W               W",
"    W          W               W",
"    W          W               W",
"    W          W               W",
"    W          W         W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W                    W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
"    W          W         W     W  ",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 16)
        x += 16
    y += 16
    x = 0

running = True
while running:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-3, 0)
    if key[pygame.K_RIGHT]:
        player.move(3, 0)
    if key[pygame.K_UP]:
        player.speed += .01
    elif key[pygame.K_DOWN]:
        if player.speed > 0.05:
            player.speed -= .05
        else:
            player.speed = 0
            
    else:
        if player.speed > 0:
            player.speed -= .005
    if player.fy < 0:
        player.y = HEIGHT

    player.move(0, -player.speed)
    for drone in drones:
        drone.move(0, -drone.speed)
        if drone.rect.y < 0:
            drone.y = HEIGHT
            pygame.draw.rect(screen, (0, 200, 0), player.rect)
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        pygame.draw.rect(screen, (0, 255, 0), player.rect)
        pygame.display.flip()
        time.sleep(2)
        player.x = start_x
        player.y = start_y
        player.speed = 0
    
    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (0, 200, 0), player.rect)
    for drone in drones:
        pygame.draw.rect(screen, (255, 200, 0), drone.rect)
        if player.rect.colliderect(drone.rect):
            pygame.display.flip()
            screen.fill((0, 0, 0))
            for wall in walls:
                pygame.draw.rect(screen, (255, 255, 255), wall.rect)
            pygame.draw.rect(screen, (255, 200, 0), drone.rect)
            pygame.draw.rect(screen, (255, 0, 0), player.rect)
            pygame.display.flip()
            time.sleep(2)
            player.x = start_x
            player.y = start_y
            player.speed = 0
            # raise SystemExit, "You crashed!"
    pygame.display.flip()
