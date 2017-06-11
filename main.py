# Title:  Isometric tile game
# Author: Igor Kucharski
# Class:  Projekt w języku skryptowym
# Date:   Spring 2017

# Author of player's graphics - Clint Bellanger - https://opengameart.org/users/clint-bellanger
# Background: Credit goes to Jetrel, Daniel Cook, Bertram and Zabin - https://opengameart.org/users/zabin

import pygame
import sys
import pytmx
from os import path
from settings import *
from sprites import *
from tilemap import *


#HUD Functions
def draw_player_health(surface, x, y, pct):
	"""HUD Function: draw player's health bar."""

	if pct < 0:
		pct = 0
	HP_BAR_LENGTH = 100
	HP_BAR_HEIGTH = 20
	fill = pct * HP_BAR_LENGTH
	background_rect = pygame.Rect(x, y, HP_BAR_LENGTH, HP_BAR_HEIGTH)
	outline_rect = pygame.Rect(x, y, HP_BAR_LENGTH, HP_BAR_HEIGTH)
	fill_rect = pygame.Rect(x, y, fill, HP_BAR_HEIGTH)
	if pct > 0.6:
		col = GREEN
	elif pct > 0.3:
		col = YELLOW
	else:
		col = RED
	pygame.draw.rect(surface, WHITE, background_rect)
	pygame.draw.rect(surface, col, fill_rect)
	pygame.draw.rect(surface, BLACK, outline_rect, 2)


class Game:
	"""Main class."""
	
	def __init__(self):
		"""Initialization."""
		
		pygame.init()
		# pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		# pygame.key.set_repeat(0, ATTACK_RATE)
		self.running = True
		self.load_data()

	def load_data(self):
		"""Loading gamedata from files."""

		self.game_folder = path.dirname(__file__)
		img_folder = path.join(self.game_folder, 'img')
		map_folder = path.join(self.game_folder, 'maps')
		self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
		self.map_img = self.map.make_map()
		self.map_rect = self.map_img.get_rect()
		self.playersheet = Spritesheet(path.join(img_folder, PLAYER_IMG))
		self.terrainsheet = Spritesheet(path.join(img_folder, TERRAIN_IMG))
		self.skeletonsheet = Spritesheet(path.join(img_folder, SKELETON_IMG))
		
	def new(self):
		"""Start a new game."""
		
		self.all_sprites = pygame.sprite.Group()
		self.player_group = pygame.sprite.GroupSingle()
		self.walls = pygame.sprite.Group()
		self.backgrounds = pygame.sprite.Group()
		self.mobs = pygame.sprite.Group()
		self.corpses = pygame.sprite.Group()
		self.players_attacks = pygame.sprite.Group()
		self.mobs_attacks = pygame.sprite.Group()

		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == 'Player':
				self.player = Player(self, tile_object.x, tile_object.y)

			if tile_object.name == 'river':
				Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

			if tile_object.name == 'Skel_sentry':
				Skeleton(self, tile_object.x, tile_object.y, "sentry")

			if tile_object.name == 'Skel_random':
				Skeleton(self, tile_object.x, tile_object.y, "random")

			if tile_object.name == 'Skel_patrol_x':
				Skeleton(self, tile_object.x, tile_object.y, "patrol_x", patrol_range_x = 200)

			if tile_object.name == 'Skel_patrol_y':
				Skeleton(self, tile_object.x, tile_object.y, "patrol_y", patrol_range_y = 200)

		self.camera = Camera(self.map.width, self.map.height)
		self.run()
		
	def run(self):
		"""Game loop."""
		
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()

	def quit(self):
		"""Quit game."""

		pygame.quit()
		sys.exit()
		
	def update(self):
		"""Game loop - update."""
	
		hits = pygame.sprite.groupcollide(self.player_group, self.mobs_attacks, False, True, collide_hit_rect)
		for hit in hits:
			if hit.behaviours["block"] == True:
				hit.health -= SKELETON_DAMAGE * PLAYER_BLOCK_MOD
			else:	
				hit.health -= SKELETON_DAMAGE
			if hit.health <= 0:
				self.playing = False

		hits = pygame.sprite.groupcollide(self.mobs, self.players_attacks, False, True, collide_hit_rect)
		for hit in hits:
			hit.health -= PLAYER_DAMAGE
				
		self.all_sprites.update()
		self.camera.update(self.player)


	def draw_grid(self):
		"""Drawing grid in background."""

		for x in range(0, WIDTH, TILESIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


	def events(self):
		"""Game loop - events."""
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.quit()
				if event.key == pygame.K_u:  
					print(1)

	def draw(self):
		"""Game loop - draw."""
		
		pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		# self.screen.fill(WHITE)
		# self.draw_grid()
		self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))

			if isinstance(sprite, Skeleton):
				sprite.draw_health()                 

		draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HP)
		pygame.display.flip()
		
	def show_start_screen(self):
		"""Game start screen."""
		
		pass
		
	def show_go_screen(self):
		""" Game over screen."""
		
		pass
		

new_game = Game()
new_game.show_start_screen()

while True:
	new_game.new()
	new_game.run()
	new_game.show_go_screen()
	
