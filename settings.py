# Title:  Isometric tile game
# Author: Igor Kucharski
# Class:  Projekt w języku skryptowym
# Date:   Spring 2017

# Author of player's graphics - Clint Bellanger - https://opengameart.org/users/clint-bellanger

import pygame

# Display parameteres
TITLE = "Gra v0.01"
WIDTH = 1024
HEIGHT = 768
FPS = 60

# Colors definition
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game parameters
TILESIZE = 32
GRINDWIDTH = WIDTH / TILESIZE
GRINDHEIGHT = HEIGHT / TILESIZE

# Map settings
TERRAIN_IMG = 'mountain_landscape.png'
TERRAIN_IMG_SIZE = 32

# Player settings
PLAYER_SPEED = 250
PLAYER_IMG = 'warrior_sprite.png'
IMG_SIZE = 128
PLAYER_HIT_RECT = pygame.Rect(0, 0, 32, 48)
