# Title:  Isometric tile game
# Author: Igor Kucharski
# Class:  Projekt w języku skryptowym
# Date:   Spring 2017

# Author of player's graphics - Clint Bellanger - https://opengameart.org/users/clint-bellanger
# Background: Credit goes to Jetrel, Daniel Cook, Bertram and Zabin - https://opengameart.org/users/zabin

import pygame
import random
from settings import *

# Loading vector from pygame library
vec = pygame.math.Vector2

def collide_hit_rect(one, two):
	"""Function using for change rectangles paricipating in collide."""

	return one.hit_rect.colliderect(two.hit_rect)


def behaviour_animation(sprite, now, refresh_rate, behaviour):
	"""Function which animating player and skeletons, depending on theirs behaviour or direction."""

	if sprite.behaviours[behaviour]:
		if now - sprite.last_update > refresh_rate:
			sprite.last_update = now
			sprite.current_frame = (sprite.current_frame + 1) % len(sprite.behaviour_img[behaviour][sprite.direction])
			sprite.image = sprite.behaviour_img[behaviour][sprite.direction][sprite.current_frame]
			sprite.rect = sprite.image.get_rect()


def behaviour_init(sprite):
	"""Behaviour initialization."""

	sprite.behaviours["stand"] = True 
	sprite.behaviours["walk"] = False
	sprite.behaviours["fight"] = False
	sprite.behaviours["block"] = False
	sprite.behaviours["death"] = False
	sprite.behaviours["cast"] = False
	sprite.behaviours["shoot"] = False

def sword_attack(sprite, trigger, now, attack_rate, group):
	"""Function using for coordinate attack and it's animation."""

	temp02 = trigger and not sprite.temp01
	sprite.temp01 = trigger
	
	if temp02:
		sprite.attack_permission = True
		Sword_attack(sprite.game, sprite.pos, attack_direction(sprite), group)
		sprite.last_attack = now
	
	if now - sprite.last_attack >= attack_rate and trigger:
		sprite.attack_permission = True
		Sword_attack(sprite.game, sprite.pos, attack_direction(sprite), group)
		sprite.last_attack = now

	if now - sprite.last_attack >= attack_rate and not trigger:		
		sprite.attack_permission = False
	
	if sprite.attack_permission:		
		sprite.vel.x, sprite.vel.y = 0, 0
		sprite.behaviours["walk"] = False
		sprite.behaviours["fight"] = True
		behaviour_animation(sprite, now, 100, "fight")

def attack_direction(sprite):
	"""Function using for choosing attack direction depending on sprite direction.""" 

	if sprite.direction == 0:
		return vec(-1,0)
	elif sprite.direction == 1:
		return vec(-1,-1)
	elif sprite.direction == 2:
		return vec(0,-1)
	elif sprite.direction == 3:
		return vec(1,-1)
	elif sprite.direction == 4:
		return vec(1,0)
	elif sprite.direction == 5:
		return vec(1,1)
	elif sprite.direction == 6:
		return vec(0,1)
	elif sprite.direction == 7:
		return vec(-1,1)


def collide_with_walls(sprite, dir, group, vel_x, vel_y):
	"""Sprite's reaction to collide, depending on moving direction."""

	if dir == 'x':
		hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if sprite.vel.x > 0:
				sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
			if sprite.vel.x < 0:
				sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
			sprite.vel.x = vel_x
			sprite.hit_rect.centerx = sprite.pos.x

	if dir == 'y':
		hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if sprite.vel.y > 0:
				sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
			if sprite.vel.y < 0:
				sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
			sprite.vel.y = vel_y
			sprite.hit_rect.centery = sprite.pos.y

#===================================================================================================================================================#

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

#===================================================================================================================================================#

class Player(pygame.sprite.Sprite):
	"""Player class"""

	def __init__(self, game, x, y):
		"""Initialization."""

		self.groups = game.all_sprites, game.player_group
		# self.layers = game.layer_01
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.behaviours = {}
		behaviour_init(self)
		self.temp01 = False
		self.temp02 = False
		
		self.direction = 6
		self.attack_permission = False
		self.current_frame = 0
		self.last_update = 0
		self.last_attack = 0
		self.behaviour_img = {}
		self.load_images()

		self.image = self.behaviour_img["stand"][self.direction][0]
		self.rect = self.image.get_rect()
		self.hit_rect = PLAYER_HIT_RECT
		
		self.health = PLAYER_HP

		self.vel = vec(0, 0)
		self.pos = vec(x, y)


	def load_images(self):
		"""Loading player's sprite images."""

		self.behaviour_img["stand"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(0, 4)] for row in range(8)]
		self.behaviour_img["walk"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(4, 12)] for row in range(8)]
		self.behaviour_img["fight"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(12, 16)] for row in range(8)]
		self.behaviour_img["block"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(16, 18)] for row in range(8)]
		self.behaviour_img["death"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(18, 24)] for row in range(8)]
		self.behaviour_img["cast"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(24, 28)] for row in range(8)]
		self.behaviour_img["shoot"] = [[self.game.playersheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(28, 32)] for row in range(8)]


	def get_keys(self):
		"""Player's sprite reaction in case of keyboard event."""

		self.vel.x, self.vel.y = 0, 0
		behaviour_init(self)
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

		now = pygame.time.get_ticks()
		sword_attack(self, keys[pygame.K_SPACE], now, PLAYER_ATTACK_RATE, self.game.players_attacks)

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


	def update(self):
		"""Override function using to update player's spirit."""
			
		self.animate()
		self.get_keys()
		# print(self.direction)
		self.pos += self.vel * self.game.dt
		self.hit_rect.centerx = self.pos.x
		collide_with_walls(self, 'x', self.game.walls, 0, 0)
		self.hit_rect.centery = self.pos.y
		collide_with_walls(self, 'y', self.game.walls, 0, 0)
		self.rect.center = self.hit_rect.center - vec(0, 10)	


	def animate(self):
		"""Animation player's sprite actions."""

		now = pygame.time.get_ticks()
		behaviour_animation(self, now, 150, "stand")
		behaviour_animation(self, now, 80, "walk")
		# behaviour_animation(self, now, 100, "fight")
		behaviour_animation(self, now, 200, "block")
		behaviour_animation(self, now, 100, "death")
		behaviour_animation(self, now, 200, "cast")
		behaviour_animation(self, now, 200, "shoot")


#===================================================================================================================================================#

class Sword_attack(pygame.sprite.Sprite):
	"""Class which create invisible short-range bullets using for imitate sword attack."""

	def __init__(self, game, pos, dir, group):
		"""Initialization."""

		self.groups = game.all_sprites, group
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = SWORD_ATTACK_SURFACE
		self.image.fill(ALPHA)
		self.rect = self.image.get_rect()
		self.hit_rect = self.rect
		self.pos = vec(pos)
		self.rect.center = pos
		self.vel = vec(dir) * SWORD_ATTACK_SPEED


	def update(self):
		"""Override function using to update spirit."""

		self.pos += self.vel * self.game.dt
		self.rect.center = self.pos			
		if pygame.sprite.spritecollideany(self, self.game.walls):
			self.kill()
		if (self.pos - self.game.player.pos).length() > SWORD_ATTACK_RANGE:
			self.kill()


#===================================================================================================================================================#

class Skeleton(pygame.sprite.Sprite):
	"""Skeleton class"""

	def __init__(self, game, x, y, stance, patrol_range_x = 0, patrol_range_y = 0):
		"""Initialization."""

		self.groups = game.all_sprites, game.mobs
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		# self.nr = nr

		self.temp01 = False
		self.temp02 = False
		self.attack_permission = False
		self.last_attack = 0
		self.fight = False
		self.behaviours = {}
		self.stance = stance
		self.patrol_range = vec(patrol_range_x, patrol_range_y)
		behaviour_init(self)
		
		self.direction = 6

		self.current_frame = 0
		self.last_update = 0
		self.last_move_update = 0
		self.behaviour_img = {}
		self.load_images()

		self.image = self.behaviour_img["stand"][self.direction][0]
		self.rect = self.image.get_rect()
		self.hit_rect = SKELETON_HIT_RECT.copy()
		self.health_bar = SKELETON_HP_BAR.copy()

		self.vel = vec(0, 0)
		self.init_pos = vec(x, y)
		self.pos = vec(x, y)

		self.health = SKELETON_HP


	def load_images(self):
		"""Loading skeletons' sprite images."""

		self.behaviour_img["stand"] = [[self.game.skeletonsheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(0, 4)] for row in range(8)]
		self.behaviour_img["walk"] = [[self.game.skeletonsheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(4, 12)] for row in range(8)]
		self.behaviour_img["fight"] = [[self.game.skeletonsheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(12, 16)] for row in range(8)]
		self.behaviour_img["cast"] = [[self.game.skeletonsheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(16, 20)] for row in range(8)]
		self.behaviour_img["block"] = [[self.game.skeletonsheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(20, 22)] for row in range(8)]
		self.behaviour_img["death"] = [[self.game.skeletonsheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(22, 28)] for row in range(8)]
		self.behaviour_img["shoot"] = [[self.game.skeletonsheet.get_image(x * IMG_SIZE, row * IMG_SIZE, IMG_SIZE, IMG_SIZE) for x in range(28, 32)] for row in range(8)]


	def move(self):
		"""Skeleton's movement."""

		if self.vel.x < 0 and self.vel.y == 0:
			self.direction = 0
		elif self.vel.x < 0 and self.vel.y < 0:
			self.direction = 1
		elif self.vel.x == 0 and self.vel.y < 0:
			self.direction = 2
		elif self.vel.x > 0 and self.vel.y < 0:
			self.direction = 3
		elif self.vel.x > 0 and self.vel.y == 0:
			self.direction = 4
		elif self.vel.x > 0 and self.vel.y > 0:
			self.direction = 5
		elif self.vel.x == 0 and self.vel.y > 0:
			self.direction = 6
		elif self.vel.x < 0 and self.vel.y > 0:
			self.direction = 7

		if self.vel.x != 0 or self.vel.y != 0:
			self.behaviours["walk"] = True
		else:
			self.behaviours["walk"] = False

		if (self.game.player.pos - self.pos).length() < SKELETON_TRACKING_RADIUS:
			self.tracking()
		elif self.stance == "random":
			self.random_walk()
		elif self.stance == "sentry":
			self.sentry()
		elif self.stance == "patrol_x":
			self.patrol()
		elif self.stance == "patrol_y":
			self.patrol()		

		now = pygame.time.get_ticks()
		sword_attack(self, self.fight, now, SKELETON_ATTACK_RATE, self.game.mobs_attacks)


	def random_walk(self):
		"""Skeleton - random walk mode."""

		now = pygame.time.get_ticks()
			
		if now - self.last_move_update > 1000:
			
			self.last_move_update = now
			behaviour_init(self)
			# self.vel.x, self.vel.y = 0, 0
			self.direction = random.randint(0, 7)
			self.walk()


	def sentry(self):
		"""Skeleton - sentry mode."""

		now = pygame.time.get_ticks()

		if (self.init_pos - self.pos).length() > 5:
			self.vel = (self.init_pos - self.pos).normalize() * SKELETON_SPEED	
		else:
			self.vel = vec(0,0)

		if now - self.last_move_update > 1000:
			
			self.last_move_update = now
			behaviour_init(self)
			self.direction = random.randint(0, 7)


	def patrol(self):
		"""Skeleton - patrol mode."""

		dest_pos = self.init_pos + self.patrol_range
		if (self.init_pos - self.pos).length() >= self.patrol_range.length():
			self.vel = (self.init_pos - self.pos).normalize() * SKELETON_SPEED
		elif (self.init_pos - self.pos).length() < 5:
			self.vel = (dest_pos - self.pos).normalize() * SKELETON_SPEED


	def tracking(self):
		"""Skeleton - following after player mode."""

		now = pygame.time.get_ticks()
			
		if now - self.last_move_update > 250:
			
			self.last_move_update = now
			behaviour_init(self)
			if (self.game.player.pos - self.pos).length() != 0:
				dir_vec = (self.game.player.pos - self.pos).normalize()
				self.vel = dir_vec * SKELETON_SPEED
			

	def walk(self):
		"""Skeleton's move in specific direction."""

		if self.direction == 0:
			self.vel.x = -SKELETON_SPEED 
			self.behaviours["walk"] = True

		if self.direction == 1:
			self.vel.x = -SKELETON_SPEED
			self.vel.y = -SKELETON_SPEED 
			self.behaviours["walk"] = True

		if self.direction == 2:
			self.vel.y = -SKELETON_SPEED
			self.behaviours["walk"] = True

		if self.direction == 3:
			self.vel.x = SKELETON_SPEED
			self.vel.y = -SKELETON_SPEED 
			self.behaviours["walk"] = True	

		if self.direction == 4:
			self.vel.x = SKELETON_SPEED
			self.behaviours["walk"] = True

		if self.direction == 5:
			self.vel.x = SKELETON_SPEED
			self.vel.y = SKELETON_SPEED 
			self.behaviours["walk"] = True	

		if self.direction == 6:
			self.vel.y = SKELETON_SPEED
			self.behaviours["walk"] = True

		if self.direction == 7:
			self.vel.x = -SKELETON_SPEED
			self.vel.y = SKELETON_SPEED 
			self.behaviours["walk"] = True			

		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071

		if 	(self.behaviours["walk"] != False or
			self.behaviours["fight"] != False or
			self.behaviours["block"] != False or
			self.behaviours["death"] != False or
			self.behaviours["cast"] != False or
			self.behaviours["shoot"] != False):
				self.behaviours["stand"] = False


	def attack(self):
		"""Attack function - smooth choosing direction to attack.""" 

		self.fight = self.hit_rect.colliderect(self.game.player.hit_rect)		
		if self.fight:
		
			self.last_move_update = pygame.time.get_ticks()

			if (self.game.player.hit_rect.centerx < self.hit_rect.left and 
				self.game.player.hit_rect.top < self.hit_rect.centery and
				self.game.player.hit_rect.bottom > self.hit_rect.centery):
				self.direction = 0

			elif ((self.game.player.hit_rect.centerx < self.hit_rect.left and 
				self.game.player.hit_rect.bottom < self.hit_rect.centery) or
				(self.game.player.hit_rect.centery < self.hit_rect.top and 
				self.game.player.hit_rect.right < self.hit_rect.centerx)): 
				self.direction = 1

			elif (self.game.player.hit_rect.centery < self.hit_rect.top and 
				self.game.player.hit_rect.left < self.hit_rect.centerx and
				self.game.player.hit_rect.right > self.hit_rect.centerx):
				self.direction = 2

			elif ((self.game.player.hit_rect.centerx > self.hit_rect.right and 
				self.game.player.hit_rect.bottom < self.hit_rect.centery)or
				(self.game.player.hit_rect.centery < self.hit_rect.top and 
				self.game.player.hit_rect.left > self.hit_rect.centerx)):  
				self.direction = 3

			elif (self.game.player.hit_rect.centerx > self.hit_rect.right and 
				self.game.player.hit_rect.top < self.hit_rect.centery and
				self.game.player.hit_rect.bottom > self.hit_rect.centery):
				self.direction = 4

			elif ((self.game.player.hit_rect.centerx > self.hit_rect.right and 
				self.game.player.hit_rect.top > self.hit_rect.centery)or
				(self.game.player.hit_rect.centery > self.hit_rect.bottom and 
				self.game.player.hit_rect.left > self.hit_rect.centerx)):  
				self.direction = 5

			elif (self.game.player.hit_rect.centery > self.hit_rect.bottom and 
				self.game.player.hit_rect.left < self.hit_rect.centerx and
				self.game.player.hit_rect.right > self.hit_rect.centerx):
				self.direction = 6

			elif ((self.game.player.hit_rect.centerx < self.hit_rect.left and 
				self.game.player.hit_rect.top > self.hit_rect.centery)or
				(self.game.player.hit_rect.centery > self.hit_rect.bottom and 
				self.game.player.hit_rect.right < self.hit_rect.centerx)): 
				self.direction = 7


	def update(self):
		"""Override function using to update skeletons's spirit"""

		self.move()
		self.animate()
		self.pos += self.vel * self.game.dt
		self.hit_rect.centerx = self.pos.x
		collide_with_walls(self, 'x', self.game.walls, -self.vel.x, -self.vel.y)
		self.hit_rect.centery = self.pos.y
		collide_with_walls(self, 'y', self.game.walls, -self.vel.x, -self.vel.y)
		self.rect.center = self.hit_rect.center - vec(0, 5)
		self.attack()
		if self.health <= 0:
			self.kill()
			SkeletonCorpse(self.game, self, self.direction, self.pos)		


	def draw_health(self):
		"""Drawing skeleton's health bar if it's health isn't full."""

		if self.health > 0.6 * SKELETON_HP:
			color = GREEN
		elif self.health > 0.3 * SKELETON_HP:
			color = YELLOW
		else:
			color = RED
		width = int(self.hit_rect.width * self.health / SKELETON_HP)
		self.health_bar = pygame.Rect(0, 0, width, 7)
		self.health_bar.bottomleft = self.hit_rect.topleft + vec(0,-5)
		if self.health < SKELETON_HP and (self.game.player.pos - self.pos).length() < SKELETON_TRACKING_RADIUS:
			pygame.draw.rect(self.game.screen, color, self.game.camera.apply_rect(self.health_bar))
			# print(self.health)


	def animate(self):
		"""Animation skeleton's sprite actions."""

		now = pygame.time.get_ticks()
		behaviour_animation(self, now, 150, "stand")
		behaviour_animation(self, now, 80, "walk")
		# behaviour_animation(self, now, 100, "fight")
		behaviour_animation(self, now, 200, "cast")
		behaviour_animation(self, now, 200, "block")
		behaviour_animation(self, now, 100, "death")
		behaviour_animation(self, now, 200, "shoot")

#===================================================================================================================================================#

class SkeletonCorpse(pygame.sprite.Sprite):
	"""Class using for creating skeleton's corpse after it's death.""" 

	def __init__(self, game, sprite, direction, pos):

		self.groups = game.all_sprites, game.corpses
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = sprite.behaviour_img["death"][sprite.direction][5]
		self.rect = self.image.get_rect()
		self.rect.center = pos - vec(0,5)

#===================================================================================================================================================#

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
		self.hit_rect = self.rect
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

#===================================================================================================================================================#

class Obstacle(pygame.sprite.Sprite):
	"""Class using to create obstacles."""

	def __init__(self, game, x, y, w, h):
		"""Setting up obstacles."""

		self.groups = game.walls
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pygame.Rect(x, y, w, h)
		self.hit_rect = self.rect
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

#===================================================================================================================================================#