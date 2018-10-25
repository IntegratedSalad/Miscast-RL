from math import sqrt
from map_utils import is_blocked
import libtcodpy as libtcod
import field_of_view
import constants
import random
import utils


class Object(object):

	def __init__(self, x, y, img, name, blocks=False, block_sight=None, fighter=None, ai=None, item=None, initial_light_radius=0):
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
		self.noise_map = {}
		self.noises = {'move': (9, 10, 3)} # LVL | RADIUS | FADE VALUE
		self.initial_light_radius = initial_light_radius # player is a light source
		self.description =  '' # add multiple entries in dict

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
			noise = utils.make_noise_map(self.x, self.y, _map, self.noises['move'][1], self.noises['move'][2], self.noises['move'][0])
			self.noise_map['noise_map'] = noise
			self.noise_map['source'] = (self.x, self.y)
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

	def destroy(self): # make it that it removes obj from objects
		self.item = None
		self.img = None


class Fighter(object):

	# every being makes noise and can attack, have inventory
	def __init__(self, hp, initial_attack_stat, initial_defense_stat, special_attack_fn=None): # make it not that straightforward, add chances to stun, chances to miss etc.
		self.starting_max_hp = hp
		self.hp = hp
		self.initial_attack_stat = initial_attack_stat
		self.initial_defense_stat = initial_defense_stat
		self.inventory = []
		self.equipment = []

	@property
	def max_light_radius(self):

		bonus_light = 0

		for eq in self.equipment:
			if eq.item.equipment.light_radius_bonus is not None:
				if eq.item.equipment.activated:
					# It activates here, the Equipment object has the values already "on"
					bonus_light += eq.item.equipment.light_radius_bonus

		return self.owner.initial_light_radius + bonus_light

	@property
	def attack_stat(self):
		final_val = 0
		for piece in self.equipment:
			final_val += piece.item.equipment.power_bonus
		return final_val

	@property
	def max_hp(self):
		bonus = 0
		for piece in self.equipment:
			bonus += piece.item.equipment.max_health_bonus
		return self.starting_max_hp + bonus


	@property
	def defense_stat(self):
		bonus = 0
		for piece in self.equipment:
			bonus += piece.item.equipment.defence_bonus
		return self.initial_attack_stat + bonus


	def attack(self, target):

		attack_value = random.randint(0, self.attack_stat) + random.randint(0, self.initial_attack_stat) # miss cannot be included in damage, if damage == 0 -> "but does no damage"

		attack_value = attack_value - (target.fighter.defense_stat / 2)

		if attack_value > 0:
			target.fighter.hp -= attack_value
			mess = "{0} attacks {1} and deals {2} dmg!".format(self.owner.name.title(), target.name.title(), attack_value)
		else:
			mess = "{0} attacks {1} and misses!".format(self.owner.name.title(), target.name.title())

		self.owner.sended_messages.append(mess)

	def kill(self, fov_map, player_x, player_y, _map, images, player_light_radius):
		self.owner.ai = None
		self.owner.fighter = None
		self.owner.block_sight = False
		self.owner.blocks = False
		self.owner.img = images[6] # instead, use specific image for every character and corpse stats overall
		self.owner.clear(self.owner.x, self.owner.y, _map)
		field_of_view.fov_recalculate(fov_map, player_x, player_y, _map, radius=player_light_radius)
		self.owner.sended_messages.append(self.owner.name.title() + " is dead.")

	def get(self, objects):
		for obj in objects:
			if obj.item is not None:
				if self.owner.x == obj.x and self.owner.y == obj.y:
					self.inventory.append(obj)
					self.owner.sended_messages.append("{0} picks up {1}.".format(self.owner.name.title(), obj.name.title()))
					objects.remove(obj)
					return obj

	def drop(self, objects, obj):

		for ob in objects:
			if (ob.x, ob.y) == (self.owner.x, self.owner.y) and ob.name != constants.PLAYER_NAME:
				self.owner.sended_messages.append("There is something already there.")
				return

		obj.x = self.owner.x
		obj.y = self.owner.y
		self.inventory.remove(obj)
		self.owner.sended_messages.append("{0} drops {1}.".format(self.owner.name.title(), obj.name.title()))
		objects.append(obj)

	def manage_equipment(self):
		for eq in self.equipment:
			if eq.item.equipment.activation_func is not None:
				eq.item.equipment.wear_off(self.owner, eq.name)


class SimpleAI(object):

	# simple ai does not make any noise nor listens for it
	def take_turn(self, _map, fov_map, objects, player):

		if fov_map[self.owner.x][self.owner.y] != 1: 
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


	def __init__(self, hearing=6, noise_map=None):
		self.hearing = hearing
		self.noise_map = noise_map
		self.destination = None
		self.chasing = False
		self.attacking = False
		# it will only listen for player
		# it gives chase to the place that he heard the sound coming from

	def take_turn(self, _map, fov_map, objects, player):


		if self.noise_map is not None and not self.chasing:

			noise_map = self.noise_map.get('noise_map')
			source = self.noise_map.get('source')

			if noise_map is not None:

				if (self.owner.x, self.owner.y) in noise_map.keys():
					if self.hearing <= noise_map[(self.owner.x, self.owner.y)]:
						self.destination = source
						self.chasing = True
						print self.owner.name, "gives chase!"

		if self.chasing:
			# A* kicks in
			self.move_astar(_map, fov_map, objects, player)

		if self.attacking:
			# it has to attack only if it sees the player
			self.move_to(_map, fov_map, objects, player)

	def move_astar(self, _map, fov_map, objects, player):

		fov = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

		for y1 in range(constants.MAP_WIDTH):
			for x1 in range(constants.MAP_HEIGHT):
				libtcod.map_set_properties(fov, x1, y1, not _map[x1][y1].block_sight, not _map[x1][y1].block_movement)

		for obj in objects:
			if obj.blocks and obj != self.owner and obj != player: # obj.x, obj.y != source
				libtcod.map_set_properties(fov, obj.x, obj.y, True, False)

		monster_path = libtcod.path_new_using_map(fov, 1.41)
		libtcod.path_compute(monster_path, self.owner.x, self.owner.y, player.x, player.y)

		if not libtcod.path_is_empty(monster_path) and libtcod.path_size(monster_path) < 25:
			x, y = libtcod.path_walk(monster_path, True)


			if self.owner.distance_to(player) > 2:
				if x or y:
					self.owner.x = x
					self.owner.y = y
			else:
				self.chasing = False
				self.attacking = True
				self.move_to(_map, fov_map, objects, player)
	
	def move_to(self, _map, fov_map, objects, player):
		distance = self.owner.distance_to(player)

		if distance != 0:
			
			dx = player.x - self.owner.x
			dy = player.y - self.owner.y

			dx = int(round(dx / distance))
			dy = int(round(dy / distance))

			self.owner.move(dx, dy, _map, fov_map, objects)				


class Item(object):
	def __init__(self, use_func=None, equipment=None, can_break=False, targetable=False, **kwargs):
		self.use_func = use_func
		self.can_break = can_break
		self.targetable = targetable
		self.equipment = equipment
		self.kwargs = kwargs

		if self.equipment:
			self.equipment.owner = self

	def use(self, **kwargs): # throwing makes noise within throw function
		# it must be generic

		user = kwargs.get('user')
		ui = kwargs.get('UI')

		kwargs.update(self.kwargs)

		if self.use_func is not None:

			if self.use_func(**kwargs) == 'used':
				# remove from obj inventory
				if user.fighter.hp > 0:
					ui.remove_item_from_UI(self.owner.x, self.owner.y)
					user.fighter.inventory.remove(self.owner)
					# add noise value to the effect if item
			else:
				return 'cancelled'
		else:
			user.sended_messages.append("You cannot use that.")


class Equipment(object):

	def __init__(self, slot, power_bonus=0, defence_bonus=0, equipment_effect=None, max_health_bonus=0, light_radius_bonus=0, charges=0, activated=False, activation_func=None, deactivation_string="", wear_off_string="", **kwargs):
		self.slot = slot
		self.power_bonus = power_bonus
		self.defence_bonus = defence_bonus
		self.equipment_effect = equipment_effect
		self.max_health_bonus = max_health_bonus
		self.light_radius_bonus = light_radius_bonus
		self.charges = charges
		self.max_charges = charges
		self.activated = activated
		self.activation_func = activation_func
		self.deactivation_string = deactivation_string # Must be a verb
		self.wear_off_string = wear_off_string # Must be a verb too
		self.kwargs = kwargs

	def activate(self, **kwargs):
		# this function only adds to the instance's attributes and manages activation func

		just_activated = False

		kwargs.update(self.kwargs)

		user = kwargs.get('user')
		eq_name = kwargs.get('eq_name')

		if self.activation_func is not None and not self.activated and self.charges > 0:
			if self.activation_func(**kwargs) == 'activated':
				self.activated = True
				just_activated = True

		if self.activation_func is not None and self.activated and not just_activated:
			self.activated = False
			user.sended_messages.append("{0} {1} {2}".format(user.name.title(), self.deactivation_string, eq_name.title()))

	def wear_off(self, user, eq_name):
		if self.activated and self.charges > 0: self.charges -= 1

		if self.charges <= 0: self.deactivate_from_wear(user, eq_name)


	def deactivate_from_wear(self, user, eq_name):
		self.activated = False
		user.sended_messages.append("{0}'s {1} {2}.".format(user.name.title(), eq_name.title(), self.wear_off_string))



