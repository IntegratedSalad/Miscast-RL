from math import sqrt
from map_utils import is_blocked
import constants
import random


class Object(object):

	def __init__(self, x, y, img, name, blocks=False, block_sight=None, fighter=None, ai=None, usable=None):
		self.x = x
		self.y = y
		self.img = img
		self.name = name
		self.blocks = blocks
		self.fighter = fighter
		self.ai = ai
		self.usable = usable
		self.block_sight = block_sight

		if self.fighter:
			self.fighter.owner = self

		if self.ai:
			self.ai.owner = self

		if self.usable:
			self.usable.owner = self

	def move(self, dx, dy, _map, fov_map, objects):
		if not is_blocked(self.x + dx, self.y + dy, _map, objects):
			self.clear(self.x, self.y, _map)
			self.x += dx
			self.y += dy
			# recalculate fovmap, but in the main loop
		else:
			for obj in objects:
				if (self.x + dx == obj.x and self.y + dy == obj.y) and obj.fighter is not None:
					self.fighter.attack(obj)

	def draw(self, screen):
		_x = self.x * constants.TILE_SIZE
		_y = self.y * constants.TILE_SIZE

		screen.blit(self.img, (_x, _y))

	def clear(self, x, y, _map):
		_map[x][y].block_sight = False

	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return sqrt(dx ** 2 + dy ** 2)

class Fighter(object):

	# every being makes noise and can attack
	def __init__(self, hp, attack_value, special_attack_fn=None, area_of_hearing=5):
		self.hp = hp
		self.attack_value = attack_value
		self.area_of_hearing = area_of_hearing

	def attack(self, target):
		print "{0} attacks {1} and they seem to not do anything".format(self.owner.name, target.name)


class SimpleAI(object):

	def take_turn(self, _map, fov_map, objects, player):

		if fov_map[self.owner.x][self.owner.y] != 1 and self.owner.distance_to(player) >= self.owner.fighter.area_of_hearing:
			# walk randomly
			rand_dir_x = random.randint(-1, 1)
			rand_dir_y = random.randint(-1, 1)

			if rand_dir_x or rand_dir_y != 0:
				self.owner.move(rand_dir_x, rand_dir_y, _map, fov_map, objects)
		else:
			# get to the player

			distance = self.owner.distance_to(player)
			
			dx = player.x - self.owner.x
			dy = player.y - self.owner.y

			dx = int(round(dx / distance))
			dy = int(round(dy / distance))

			self.owner.move(dx, dy, _map, fov_map, objects)

			print "{0} hears you!".format(self.owner.name)

	def target_enemy():
		# instead of always choosing player, it will have a better usability
		pass


class NoiseAI(object):
	pass
