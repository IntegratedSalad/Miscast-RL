from math import sqrt
from map_utils import is_blocked
import constants

class Object(object):

	def __init__(self, x, y, img, name, blocks=False):
		self.x = x
		self.y = y
		self.img = img
		self.name = name
		self.blocks = blocks

	def move(self, dx, dy, _map):
		if not is_blocked(self.x + dx, self.y + dy, _map):
			self.x += dx
			self.y += dy

	def draw(self, screen):
		_x = self.x * constants.TILE_SIZE
		_y = self.y * constants.TILE_SIZE
		screen.blit(self.img, (_x, _y))

	def clear(self, floor_img, screen):
		screen.blit(floor_img, (self.x, self.y))

	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return sqrt(dx ** 2 + dy ** 2)

class Fighter(object):
	pass

