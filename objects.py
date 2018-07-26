from math import sqrt
from map_utils import is_blocked
import field_of_view
import constants
import random


class Object(object):

	def __init__(self, x, y, img, name, blocks=False, block_sight=None, fighter=None, ai=None, item=None, light_source=None):
		self.x = x
		self.y = y
		self.img = img
		self.name = name
		self.blocks = blocks
		self.fighter = fighter
		self.ai = ai
		self.item = item
		self.block_sight = block_sight
		self.sended_messages = []
		self.light_source = light_source # player is a light source
		self.description =  ""

		if self.fighter:
			self.fighter.owner = self

		if self.ai:
			self.ai.owner = self

		if self.item:
			self.item.owner = self

	def move(self, dx, dy, _map, fov_map, objects, pushing=False):
		if not is_blocked(self.x + dx, self.y + dy, _map, objects) and (self.fighter is not None ):#or pushing):
			self.clear(self.x, self.y, _map)
			self.x += dx
			self.y += dy
		else:
			for obj in objects:
				if self.name != constants.PLAYER_NAME:
					if (self.x + dx == obj.x and self.y + dy == obj.y) and obj.fighter is not None and self.fighter is not None and obj.name == constants.PLAYER_NAME:
						self.fighter.attack(obj)
				else:
					if (self.x + dx == obj.x and self.y + dy == obj.y) and obj.fighter is not None and self.fighter is not None:
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

	def clear_messages(self):
		self.sended_messages = []

	def send_message(self):
		# add the possibility to change the color (it would need to be a list of message and the RGB value)
		pass

	def destroy(self):
		self.item = None
		self.img = None


class Fighter(object):

	# every being makes noise and can attack, have inventory
	def __init__(self, max_hp, attack_stat, special_attack_fn=None, area_of_hearing=5):
		self.max_hp = max_hp
		self.hp = max_hp
		self.attack_stat = attack_stat
		self.area_of_hearing = area_of_hearing
		self.inventory = []
		self.equipment = []

	def attack(self, target):

		attack_value = random.randint(0, self.attack_stat)

		target.fighter.hp -= attack_value

		if attack_value != 0:
			mess = "{0} attacks {1} and deals {2} dmg!".format(self.owner.name.capitalize(), target.name.capitalize(), attack_value)
		else:
			mess = "{0} attacks {1} and misses!".format(self.owner.name.capitalize(), target.name.capitalize())

		self.owner.sended_messages.append(mess)

	def kill(self, fov_map, player_x, player_y, _map, images):
		self.owner.ai = None
		self.owner.fighter = None
		self.owner.block_sight = False
		self.owner.blocks = False
		self.owner.img = images[6] # instead, use specific image for every character and corpse stats overall
		self.owner.clear(self.owner.x, self.owner.y, _map)
		field_of_view.fov_recalculate(fov_map, player_x, player_y, _map)
		self.owner.sended_messages.append(self.owner.name.capitalize() + " is dead.")

	def get(self, objects):
		for obj in objects:
			if obj.item is not None:
				if self.owner.x == obj.x and self.owner.y == obj.y:
					self.inventory.append(obj)
					self.owner.sended_messages.append("{0} picks up {1}.".format(self.owner.name.capitalize(), obj.name))
					objects.remove(obj)
					return obj

	def drop(self, objects, obj):
		obj.x = self.owner.x
		obj.y = self.owner.y
		self.inventory.remove(obj)
		self.owner.sended_messages.append("{0} drops {1}.".format(self.owner.name.capitalize(), obj.name))
		objects.append(obj)


class SimpleAI(object):

	# simple ai does not make any noise nor listens for it

	def take_turn(self, _map, fov_map, objects, player):

		if fov_map[self.owner.x][self.owner.y] != 1 and self.owner.distance_to(player) >= self.owner.fighter.area_of_hearing: 
			# walk randomly
			rand_dir_x = random.randint(-1, 1)
			rand_dir_y = random.randint(-1, 1)

			if rand_dir_x and rand_dir_y != 0:
				self.owner.move(rand_dir_x, rand_dir_y, _map, fov_map, objects)
		else:
			# get to the player

			distance = self.owner.distance_to(player)

			if distance != 0:
			
				dx = player.x - self.owner.x
				dy = player.y - self.owner.y

				dx = int(round(dx / distance))
				dy = int(round(dy / distance))

				self.owner.move(dx, dy, _map, fov_map, objects)


	def target_enemy():
		# instead of always choosing player, it will have a better usability
		pass


class NoiseAI(object):

	def __init__(self, hearing):
		pass


class Item(object):
	def __init__(self, use_func=None, equipment=None, can_break=False, targetable=False, **kwargs):
		self.use_func = use_func
		self.can_break = can_break
		self.targetable = targetable
		self.equipment = equipment
		self.kwargs = kwargs

		if self.equipment:
			self.equipment.owner = self

	def use(self, **kwargs):
		# it must be generic

		user = kwargs.get('user')

		kwargs.update(self.kwargs)

		if self.use_func is not None:

			if self.use_func(**kwargs) == 'used':
				# remove from obj inventory
				user.fighter.inventory.remove(self.owner)
		else:
			user.sended_messages.append("You cannot use that.")


class Equipment(object):

	def __init__(self, slot, power_bonus=0, defence_bonus=0):
		self.slot = slot
		self.power_bonus = power_bonus
		self.defence_bonus = defence_bonus


