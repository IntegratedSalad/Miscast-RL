from math import sqrt
from map_utils import is_blocked
import constants

class Object(object):

	def __init__(self, x, y, img, name, blocks=False, being=None, ai=None, usable=None):
		self.x = x
		self.y = y
		self.img = img
		self.name = name
		self.blocks = blocks
		self.being = being
		self.ai = ai
		self.usable = usable

		if self.being:
			self.owner.being = self

		if self.ai:
			self.owner.ai = self

		if self.usable:
			self.owner.usable = self

	def move(self, dx, dy, _map, fov_map):
		if not is_blocked(self.x + dx, self.y + dy, _map):
			self.x += dx
			self.y += dy
			# recalculate fovmap

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

class Being(object):

	# every being makes noise and can attack
	def __init__(self, hp, attack, special_attack_fn=None):
		self.hp = hp
		self.attack = attack
		self.speed = speed

	def attack(self, dx, dy, target):
		pass


class SimpleAI(object):
	def __init__(self):
		pass

	def take_turn(self):
		pass

