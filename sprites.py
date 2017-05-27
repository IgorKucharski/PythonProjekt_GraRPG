# Title:  Isometric tile game
# Author: Igor Kucharski
# Class:  Projekt w języku skryptowym
# Date:   Spring 2017

# Author of player's graphics - Clint Bellanger - https://opengameart.org/users/clint-bellanger

import pygame
from settings import *

# Loading vector from pygame library
vec = pygame.math.Vector2

def collide_hit_rect(one, two):
	return one.hit_rect.colliderect(two.rect)

class Spritesheet:
	"""Class using to load specific image from spritesheet."""

	def __init__(self, filename):
		"""Setting used spritesheet."""		
		self.spritesheet = pygame.image.load(filename).convert_alpha()

	def get_image(self, x, y, width, height):
		"""Clipping spritesheet to target sprite image."""

		self.spritesheet.set_clip(pygame.Rect(x, y, width, height))
		self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
		# self.image.set_clip(self.image.get_bounding_rect())
		# self.image = self.image.subsurface(self.image.get_clip())

		return self.image


class Player(pygame.sprite.DirtySprite):
	"""Player class"""

	def __init__(self, game, x, y):
		"""Initialization."""

		self.groups = game.all_sprites
		pygame.sprite.DirtySprite.__init__(self, self.groups)
		self.game = game

		self.behaviours = {}
		self.behaviour_init()
		
		self.direction = 6
		# self.directions = ["l", "ul", "u", "ur", "r", "dr", "d", "dl" ] 
		# l - left, ul - upper-left, u - up, ur - upper-right, r - right, dr - down-right, d - down, dl - down-left

		self.current_frame = 0
		self.last_update = 0
		self.behaviour_img = {}
		self.load_images()

		self.image = self.behaviour_img["stand"][self.direction][0]
		self.rect = self.image.get_rect()
		self.hit_rect = PLAYER_HIT_RECT


		self.vel = vec(0, 0)
		self.pos = vec(x, y) * TILESIZE


	def load_images(self):

		self.behaviour_img["stand"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(0, 4)] for row in range(8)]
		self.behaviour_img["walk"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(4, 12)] for row in range(8)]
		self.behaviour_img["fight"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(12, 16)] for row in range(8)]
		self.behaviour_img["block"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(16, 18)] for row in range(8)]
		self.behaviour_img["death"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(18, 24)] for row in range(8)]
		self.behaviour_img["cast"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(24, 28)] for row in range(8)]
		self.behaviour_img["shoot"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(28, 32)] for row in range(8)]


	def behaviour_init(self):

		self.behaviours["stand"] = True 
		self.behaviours["walk"] = False
		self.behaviours["fight"] = False
		self.behaviours["block"] = False
		self.behaviours["death"] = False
		self.behaviours["cast"] = False
		self.behaviours["shoot"] = False


	def get_keys(self):
		"""Player's sprite reaction in case of keyboard event."""

		self.vel.x, self.vel.y = 0, 0
		self.behaviour_init()
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.vel.y = -PLAYER_SPEED
			self.behaviours["walk"] = True
			self.direction = 2

		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.vel.y = PLAYER_SPEED
			self.behaviours["walk"] = True
			self.direction = 6

		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.vel.x = -PLAYER_SPEED 
			self.behaviours["walk"] = True
			self.direction = 0

			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.direction = 1
			if keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.direction = 7

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.vel.x = PLAYER_SPEED
			self.behaviours["walk"] = True
			self.direction = 4

			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.direction = 3
			if keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.direction = 5


		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071

		if keys[pygame.K_SPACE]:
			self.vel.x, self.vel.y = 0, 0
			self.behaviours["walk"] = False
			self.behaviours["fight"] = True

		if keys[pygame.K_b]:
			self.vel.x, self.vel.y = 0, 0
			self.behaviours["walk"] = False
			self.behaviours["block"] = True
#temp
		if keys[pygame.K_x]:
			self.vel.x, self.vel.y = 0, 0
			self.behaviours["walk"] = False
			self.behaviours["death"] = True

		if keys[pygame.K_c]:
			self.vel.x, self.vel.y = 0, 0
			self.behaviours["walk"] = False
			self.behaviours["cast"] = True

		if keys[pygame.K_v]:
			self.vel.x, self.vel.y = 0, 0
			self.behaviours["walk"] = False
			self.behaviours["shoot"] = True

		if 	(self.behaviours["walk"] != False or
			self.behaviours["fight"] != False or
			self.behaviours["block"] != False or
			self.behaviours["death"] != False or
			self.behaviours["cast"] != False or
			self.behaviours["shoot"] != False):
				self.behaviours["stand"] = False


	def collide_with_walls(self, dir):
		"""Player's sprite reaction to collide, depending on player's sprite move direction."""

		if dir == 'x':
			hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
			if hits:
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
				self.vel.x = 0
				self.hit_rect.centerx = self.pos.x
		if dir == 'y':
			hits = pygame.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
			if hits:
				if self.vel.y > 0:
					self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
				if self.vel.y < 0:
					self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
				self.vel.y = 0
				self.hit_rect.centery = self.pos.y


	def update(self):
		"""Override function using to update player's spirit"""
		
		self.get_keys()
		self.animate()
		self.pos += self.vel * self.game.dt
		self.hit_rect.centerx = self.pos.x
		self.collide_with_walls('x')
		self.hit_rect.centery = self.pos.y
		self.collide_with_walls('y')
		self.rect.center = self.hit_rect.center - vec(0, 10)


	def behaviour_animation(self, now, refresh_rate, behaviour):
		if self.behaviours[behaviour]:
			if now - self.last_update > refresh_rate:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.behaviour_img[behaviour][self.direction])
				self.image = self.behaviour_img[behaviour][self.direction][self.current_frame]
				self.rect = self.image.get_rect()
				self.rect.center = self.hit_rect.center - vec(0, 10)


	def animate(self):
		now = pygame.time.get_ticks()
		self.behaviour_animation(now, 150, "stand")
		self.behaviour_animation(now, 80, "walk")
		self.behaviour_animation(now, 100, "fight")
		self.behaviour_animation(now, 200, "block")
		self.behaviour_animation(now, 100, "death")
		self.behaviour_animation(now, 200, "cast")
		self.behaviour_animation(now, 200, "shoot")


class Wall(pygame.sprite.Sprite):
	"""Class using to create walls."""

	def __init__(self, game, x, y):
		"""Setting up walls."""

		self.groups = game.all_sprites, game.walls
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE


class Background(pygame.sprite.Sprite):

	def __init__(self, game, x, y, bg_col, bg_row):

		self.groups = game.all_sprites, game.backgrounds
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.background = [[self.game.terrainsheet.get_image(row* TERRAIN_IMG_SIZE, col * TERRAIN_IMG_SIZE, TERRAIN_IMG_SIZE, TERRAIN_IMG_SIZE) for col in range(16)] for row in range(16)]
		self.image = self.background[bg_col][bg_row]
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

		print(len(self.background))
		print(len(self.background[0]))


