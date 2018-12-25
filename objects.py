from math import sqrt
from map_utils import is_blocked
import libtcodpy as libtcod
import field_of_view
import constants
import random
import utils


class Object(object):

	def __init__(self, x, y, img, name, blocks=False, block_sight=None, fighter=None, ai=None, item=None, initial_light_radius=0, initial_fov=0):
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
		self.noise_map = {'noise_map': '', 'source': '', 'sound': ''} # dictionary of noises
		self.noises = {'move': (10, 10, 10), 'crouch': (2, 2, 1)} # LVL | RADIUS | FADE VALUE
		self.sounds = {'sound_walk': '', 'sound_sneak': ''} # names of sounds
		self.initial_light_radius = initial_light_radius # player is a light source variable for objects
		self.initial_fov = initial_fov # for monsters
		self.description =  '' # add multiple entries in dict

		if self.fighter:
			self.fov_map = []
			self.fov_map = field_of_view.set_fov(self.fov_map)
			self.fighter.owner = self

		if self.ai:
			self.ai.owner = self

		if self.item:
			self.item.owner = self

	def move(self, dx, dy, _map, fov_map, objects, pushing=False):
		if not is_blocked(self.x + dx, self.y + dy, _map, objects) and (self.fighter is not None):#or pushing):
			self.clear(self.x, self.y, _map)
			self.x += dx
			self.y += dy
			if not self.fighter.sneaking:
				self.make_noise(_map, self.noises['move'][0], self.noises['move'][1], self.noises['move'][2], self.sounds['sound_walk'])
			else:
				self.make_noise(_map, self.noises['crouch'][0], self.noises['crouch'][1], self.noises['crouch'][2], self.sounds['sound_sneak'])
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

	def make_noise(self, _map, lvl, radius, fade_value, name):
		noise = utils.make_noise_map(self.x, self.y, _map, radius, fade_value, lvl)

		self.noise_map['noise_map'] = noise
		self.noise_map['source'] = (self.x, self.y)
		self.noise_map['sound'] = name

	def player_hear_sound(self, sound):
		final_text = "You hear: "

		key = str(sound['key'])
		data = sound['sound'][2]
		text_sound = ""

		for x in data:
			if x.has_key(key):
				text_sound = x[key]
				break

		final_text += text_sound

		self.sended_messages.append(final_text)


class Fighter(object):

	# every being makes noise and can attack, have inventory
	def __init__(self, hp, initial_attack_stat, initial_defense_stat, special_attack_fn=None): # make it not that straightforward, add chances to stun, chances to miss etc.
		self.starting_max_hp = hp
		self.hp = hp
		self.initial_attack_stat = initial_attack_stat
		self.initial_defense_stat = initial_defense_stat
		self.inventory = []
		self.equipment = []
		self.sneaking = False
		self.knees = 10 # knee health

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

	def manage_equipment(self): # change to manage fighter, so that it deals with sneaking too
		for eq in self.equipment:
			if eq.item.equipment.activation_func is not None:
				eq.item.equipment.wear_off(self.owner, eq.name)

	def sneak(self):
		if not self.sneaking:
			self.sneaking = True
			self.owner.sended_messages.append("You crouch.")
		else:
			self.sneaking = False
			self.owner.sended_messages.append("You stand up.")


class SimpleAI(object):

	# simple ai does not make any noise nor listens for it
	def take_turn(self, _map, fov_map, objects, player):

		field_of_view.cast_rays(self.owner.x, self.owner.y, fov_map, _map, self.owner.initial_fov)

		if fov_map[player.x][player.y] != 1: 
			# walk randomly
			rand_dir_x = random.randint(-1, 1)
			rand_dir_y = random.randint(-1, 1)

			self.owner.move(rand_dir_x, rand_dir_y, _map, fov_map, objects)

			field_of_view.fov_recalculate(fov_map, self.owner.x, self.owner.y, _map, self.owner.initial_fov)

		else:
			# get to the player

			distance = self.owner.distance_to(player)

			if distance != 0:
			
				dx = player.x - self.owner.x
				dy = player.y - self.owner.y

				dx = int(round(dx / distance))
				dy = int(round(dy / distance))

				self.owner.move(dx, dy, _map, fov_map, objects)
				field_of_view.fov_recalculate(fov_map, self.owner.x, self.owner.y, _map, self.owner.initial_fov)


	def target_enemy():
		# instead of always choosing player, it will have a better usability
		pass


class NoiseAI(object):

	# make so that it for some turns remembers where is the player
	def __init__(self, hearing, noise_map=None):
		self.hearing = hearing
		self.noise_map = noise_map
		self.destination = None
		self.investigating = False
		# it will only listen for player
		# it gives chase to the place that he heard the sound coming from


	def listen(self):
		try:
			got_noise_map = self.noise_map.get('noise_map')
			if got_noise_map is not None: 
				if (self.owner.x, self.owner.y) in got_noise_map.keys():
					if self.hearing <= got_noise_map[(self.owner.x, self.owner.y)]:
						return self.noise_map.get('source')
					else:
						return None
		except AttributeError:
			pass


	def take_turn(self, _map, fov_map, objects, player):

		# Listen
		# Investigate
		# If you are here and there's no player - wander
		# Stop investigating only when you're at your target

		field_of_view.cast_rays(self.owner.x, self.owner.y, fov_map, _map, self.owner.initial_fov)
		noise = self.listen()
		vision = self.use_eyes(fov_map, player.x, player.y)

		if noise is not None:
			print 'A NEW NOISE!' # hear will be the growl
			self.destination = noise
			self.investigating = True

		if self.investigating and not vision:
			result = self.investigate(fov_map, _map, objects, self.destination, player)
			if (result == 'reached'):
				self.investigating = False

		if not self.investigating and not vision:
			# walk randomly
			rand_dir_x = random.randint(-1, 1)
			rand_dir_y = random.randint(-1, 1)

			self.owner.move(rand_dir_x, rand_dir_y, _map, fov_map, objects)

			field_of_view.fov_recalculate(fov_map, self.owner.x, self.owner.y, _map, self.owner.initial_fov)

		if vision:
			self.move_astar(_map, objects, (player.x, player.y), player)

		field_of_view.fov_recalculate(fov_map, self.owner.x, self.owner.y, _map, self.owner.initial_fov)

		#print "INVESTIGATING: {0} SEEING: {1}".format(self.investigating, vision)


	def investigate(self, fov_map, _map, objects, goal, player):
		process = self.move_astar(_map, objects, goal, player)
		field_of_view.fov_recalculate(fov_map, self.owner.x, self.owner.y, _map, self.owner.initial_fov)
		return process

	def move_astar(self, _map, objects, goal, player):

		fov = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

		for y1 in range(constants.MAP_WIDTH):
			for x1 in range(constants.MAP_HEIGHT):
				libtcod.map_set_properties(fov, x1, y1, not _map[x1][y1].block_sight, not _map[x1][y1].block_movement)

		for obj in objects:
			if obj.blocks and obj != self.owner and obj != player:
				libtcod.map_set_properties(fov, obj.x, obj.y, True, False)

		monster_path = libtcod.path_new_using_map(fov, 1.41)
		libtcod.path_compute(monster_path, self.owner.x, self.owner.y, goal[0], goal[1])

		if not libtcod.path_is_empty(monster_path) and libtcod.path_size(monster_path) < 100:
			x, y = libtcod.path_walk(monster_path, True)

			if x or y:
				# here will be time to move or attack, and it will return found and fighting

				self.move_to_not_player(_map, fov, objects, x, y)

				if utils.non_obj_distance_to((goal[0], goal[1]), self.owner.x, self.owner.y) < 1:
					return 'reached'


	def move_to_not_player(self, _map, fov_map, objects, target_x, target_y):
		distance = utils.non_obj_distance_to((target_x, target_y), self.owner.x, self.owner.y)

		if distance != 0:
			
			dx = target_x - self.owner.x
			dy = target_y - self.owner.y

			dx = int(round(dx / distance))
			dy = int(round(dy / distance))

			self.owner.move(dx, dy, _map, fov_map, objects)	

	def use_eyes(self, fov_map, target_x, target_y):
		if fov_map[target_x][target_y] != 1: 
			return False
		return True

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

		print str(user) + ": USER"

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

def player_listen_to_noise(player): 
	
	try:

		noise_maps = player.hearing_map.get('noise_maps')
		sources = player.hearing_map.get('sources')
		sounds = player.hearing_map.get('sounds')
		# add the "sound effect" | name of the noise
		list_of_sources = []
		list_of_sources_with_sounds = []

		len_of_noises = len(noise_maps)

		for x in range(len_of_noises):
			noise_map = noise_maps[x]
			source = sources[x]
			sound = sounds[x]
			# We have our noises and sources grouped
			
			if (player.x, player.y) in noise_maps[x].keys():
				if player.hearing <= noise_map[(player.x, player.y)]:
					list_of_sources.append(source)

			list_of_sources_with_sounds.append({str(source): sound})
					
		return list_of_sources, sounds, list_of_sources_with_sounds

	except IndexError:
		pass


def player_hurt_or_heal_knees(player, _map):

	max_knees = 10

	#print max_knees, player.fighter.knees


	if player.fighter.sneaking:
		player.fighter.knees -= 0.5

	if not player.fighter.sneaking and player.fighter.knees < max_knees:
		#print 'dd'
		player.fighter.knees += 0.1

	if player.fighter.knees <= 0 and player.fighter.sneaking:
		player_scream(player, _map)

def player_scream(player, _map):

	player.make_noise(_map, 10, 500, 50, 'AW FUCK')
	player.sended_messages.append("You scream: 'AW FUCK MY KNEES!'")
