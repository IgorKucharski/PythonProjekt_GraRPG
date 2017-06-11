# Title:  Isometric tile game
# Author: Igor Kucharski
# Class:  Projekt w języku skryptowym
# Date:   Spring 2017

# Author of player's graphics - Clint Bellanger - https://opengameart.org/users/clint-bellanger
# Background: Credit goes to Jetrel, Daniel Cook, Bertram and Zabin - https://opengameart.org/users/zabin

import pygame

# Display parameteres
TITLE = "Gra v0.01"
WIDTH = 1024
HEIGHT = 768
FPS = 60

# Colors definition
ALPHA = (0, 0, 0, 0)
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
PLAYER_ATTACK_RATE = 400
PLAYER_HP = 100
PLAYER_DAMAGE = 10
PLAYER_BLOCK_MOD = 0.5

# Sword attack settings
SWORD_ATTACK_SPEED = 1000
SWORD_ATTACK_RANGE = 50
# SWORD_DAMAGE = 10
SWORD_ATTACK_SURFACE = pygame.Surface((5, 5), pygame.SRCALPHA)

# Skeleton settings
SKELETON_IMG = 'skeleton_sprite.png'
SKELETON_SPEED = 200
SKELETON_HIT_RECT = pygame.Rect(0, 0, 50, 50)
SKELETON_WALL_HIT_RECT = pygame.Rect(0, 0, 42, 58)
SKELETON_ATTACK_RATE = 400
SKELETON_TRACKING_RADIUS = 200
SKELETON_DAMAGE = 10
SKELETON_HP = 100
SKELETON_HP_BAR = pygame.Rect(0, 0, 50, 7)

