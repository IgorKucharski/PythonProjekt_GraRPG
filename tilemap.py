# Title:  Isometric tile game
# Author: Igor Kucharski
# Class:  Projekt w języku skryptowym
# Date:   Spring 2017

# Author of player's graphics - Clint Bellanger - https://opengameart.org/users/clint-bellanger
# Background: Credit goes to Jetrel, Daniel Cook, Bertram and Zabin - https://opengameart.org/users/zabin

import pygame
import pytmx
from settings import *

class Map:
	"""Class using for crate map from txt files."""

	def __init__(self, filename):
		"""Initialization."""

		self.data = []
		with open(filename, 'rt') as f:
			for line in f:
				self.data.append(line.strip())

		self.tilewidth = len(self.data[0])
		self.tileheight = len(self.data)
		self.width = self.tilewidth * TILESIZE
		self.height = self.tileheight * TILESIZE


#===================================================================================================================================================#


class TiledMap:
	"""Class using for crate map from tmx files."""

	def __init__(self, filename):
		"""Initialization."""

		tm = pytmx.load_pygame(filename, pixelalpha = True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm


	def render(self, surface):
		"""Rendering map."""

		ti = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_layers:
			if isinstance(layer, pytmx.TiledTileLayer):
				for x, y, gid, in layer:
					tile = ti(gid)
					if tile:
						surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))


	def make_map(self):
		"""Return map's surface."""

		temp_surface = pygame.Surface((self.width, self.height))
		self.render(temp_surface)
		return temp_surface


#===================================================================================================================================================#


class Camera:
	"""Class using for moving view across the map, depending on player's position."""

	def __init__(self, width, height):
		"""Initialization."""

		self.camera = pygame.Rect(0,0, width, height)
		self.width = width
		self.height = height


	def apply(self, entity):
		"""Function using for display sprites in proper place after move the screen."""

		return entity.rect.move(self.camera.topleft)


	def apply_rect(self, rect):
		"""Function using for display rectangles in proper place after move the screen."""

		return rect.move(self.camera.topleft)


	def update(self, target):
		"""Override function using to update view."""

		x = -target.rect.centerx + int(WIDTH / 2)
		y = -target.rect.centery + int(HEIGHT / 2)

		# Limit scrolling to map size
		x = min(0, x) # left
		y = min(0, y) # top
		x = max(-(self.width - WIDTH), x) # right
		y = max(-(self.height - HEIGHT), y) # bottom
		
		self.camera = pygame.Rect(x, y, self.width, self.height)