# Title:  Isometric tile game
# Author: Igor Kucharski
# Class:  Projekt w języku skryptowym
# Date:   Spring 2017

# Author of player's graphics - Clint Bellanger - https://opengameart.org/users/clint-bellanger

import pygame
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


class Game:
	"""Main class."""
	
	def __init__(self):
		"""Initialization."""
		
		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(500, 100)
		self.running = True
		self.load_data()

	def load_data(self):
		"""Loading gamedata from files."""

		self.game_folder = path.dirname(__file__)
		img_folder = path.join(self.game_folder, 'img')
		self.map = Map(path.join(self.game_folder, 'map2.txt'))		
		self.playersheet = Spritesheet(path.join(img_folder, PLAYER_IMG))
		self.terrainsheet = Spritesheet(path.join(img_folder, TERRAIN_IMG))
		
	def new(self):
		"""Start a new game."""
		
		self.all_sprites = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.backgrounds = pygame.sprite.Group()
		
		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)
				if tile == 'P':
					self.player = Player(self, col, row)
		for x in range(16):
			for y  in range (16):			
				Background(self, x+2, y+2, x, y)

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

	def draw(self):
		"""Game loop - draw."""
		
		pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		self.screen.fill(WHITE)
		# self.draw_grid()
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		# pygame.draw.rect(self.screen, BLUE, self.player.hit_rect, 2)
		# pygame.draw.rect(self.screen, BLUE, self.player.bounding_rect, 2)
		# pygame.draw.rect(self.screen, BLUE, self.camera.apply(self.player), 2)
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
	
