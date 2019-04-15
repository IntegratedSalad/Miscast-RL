#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random
import constants
import field_of_view
import objects
import utils
import use_functions
import textwrap
from spritesheet import Spritesheet
from map_utils import Tile
from map_utils import CA_CaveFactory as CA_map

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
LIGHT_RED = (255, 0, 0)
GREEN = (3, 172, 37)
PALE = (172, 112, 100)
GOLD = (255, 215, 0)

class Game(object): # move this to objects

	def __init__(self, state=None):
		self.state = state
		self.current_raw_map = self.take_raw_map()
		self.map = self.set_map()
		self.images = []
		self.objects = []
		self.fov_map = []
		self.messages_history = []
		self.messages = []
		self.ui = None
		self.world = "Dungeon" # to keep the track of worlds
		self.level = 1

	def take_raw_map(self):
		map_list = []
		line = ""
		with open("map.txt", "r") as game_map:
			for n in range(0, constants.MAP_WIDTH):
				line = game_map.readline()
				map_list.append(line)
		return map_list


	def gen_map(self):
		pass


	def get_images(self):

		characters_SPRITES = Spritesheet("tiles/Player0.png")
		walls_SPRITES = Spritesheet("tiles/Tile.png")
		enemies_pests_SPRITES = Spritesheet("tiles/Pest0.png")
		misc_enemies_SPRITES = Spritesheet("tiles/Misc0.png")
		corpses_SPRITES = Spritesheet("tiles/Flesh.png")
		ui_SPRITES = Spritesheet("tiles/Wall.png")
		potions_SPRITES = Spritesheet("tiles/Potion.png")
		scrolls_SPRITES = Spritesheet("tiles/Scroll.png")
		ui_two_SPRITES = Spritesheet("tiles/GUI0.png")
		armor_SPRITES = Spritesheet("tiles/Armor.png")
		medium_weapons_SPRITES = Spritesheet("tiles/MedWep.png")
		helmets_SPRITES = Spritesheet("tiles/Hat.png")
		long_weapons = Spritesheet("tiles/LongWep.png")
		light_SPRITES = Spritesheet("tiles/Light.png")
		music_SPRITES = Spritesheet("tiles/Music.png")
		chests_SPRITES = Spritesheet("tiles/Chest0.png")

		player_IMG = characters_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		wall_IMG = walls_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE))
		floor_IMG = pygame.image.load("tiles/floor.png")
		empty_spaceIMG = walls_SPRITES.image_at((0, constants.TILE_SIZE * 2, constants.TILE_SIZE, constants.TILE_SIZE))
		worm_IMG = enemies_pests_SPRITES.image_at((7 * constants.TILE_SIZE, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 22 12
		abhorrent_creature_IMG = misc_enemies_SPRITES.image_at((0, 5 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 28 27
		corpse_IMG = corpses_SPRITES.image_at((4 * constants.TILE_SIZE, 2 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		inventory_slot_IMG = ui_two_SPRITES.image_at((8 * constants.TILE_SIZE, 10 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE))
		great_steel_long_sword_IMG = long_weapons.image_at((0, constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		lantern_IMG = light_SPRITES.image_at((3 * constants.TILE_SIZE, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		goblin_IMG = characters_SPRITES.image_at((0 * constants.TILE_SIZE, 12 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		magic_bell_IMG = music_SPRITES.image_at((constants.TILE_SIZE, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		noise_indicator_IMG = ui_two_SPRITES.image_at((12 * constants.TILE_SIZE, 3 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		chest_IMG = chests_SPRITES.image_at((constants.TILE_SIZE, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		hp_potion_IMG = potions_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		ultimate_hp_potion_IMG = potions_SPRITES.image_at((1 * constants.TILE_SIZE, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		scroll_of_death_IMG = scrolls_SPRITES.image_at((5 * constants.TILE_SIZE, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		scroll_of_uncontrolled_teleportation_IMG = scrolls_SPRITES.image_at((4 * constants.TILE_SIZE, 2 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		oil_IMG = potions_SPRITES.image_at((2 * constants.TILE_SIZE, 2 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		potion_of_death_IMG = potions_SPRITES.image_at((0, constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		potion_of_confusion_IMG = potions_SPRITES.image_at((constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		iron_sword_IMG = medium_weapons_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		bronze_armor_IMG = armor_SPRITES.image_at((0, 6 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		crystal_armor_IMG = armor_SPRITES.image_at((7 * constants.TILE_SIZE, 6 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		crown_IMG = helmets_SPRITES.image_at((2 * constants.TILE_SIZE, 3 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		cloak_of_invisibility_IMG = armor_SPRITES.image_at((constants.TILE_SIZE, 5 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		ui_MESSAGE_HORIZONTAL = ui_SPRITES.image_at((constants.TILE_SIZE, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_LEFT = ui_SPRITES.image_at((0, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_LEFT = ui_SPRITES.image_at((0, constants.TILE_SIZE * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_RIGHT = ui_SPRITES.image_at((2 * constants.TILE_SIZE, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_RIGHT = ui_SPRITES.image_at((2 * constants.TILE_SIZE, constants.TILE_SIZE * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_VERTICAL = ui_SPRITES.image_at((0, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE))

		return [player_IMG, wall_IMG, floor_IMG, empty_spaceIMG, worm_IMG, abhorrent_creature_IMG, corpse_IMG,
				ui_MESSAGE_HORIZONTAL, ui_MESSAGE_TOP_LEFT, ui_MESSAGE_BOTTOM_LEFT, ui_MESSAGE_TOP_RIGHT, ui_MESSAGE_BOTTOM_RIGHT, ui_MESSAGE_VERTICAL, hp_potion_IMG, scroll_of_death_IMG, inventory_slot_IMG, bronze_armor_IMG,
				scroll_of_uncontrolled_teleportation_IMG, crystal_armor_IMG, iron_sword_IMG, crown_IMG,
				ultimate_hp_potion_IMG, great_steel_long_sword_IMG, lantern_IMG, oil_IMG, goblin_IMG, magic_bell_IMG, noise_indicator_IMG, potion_of_death_IMG, cloak_of_invisibility_IMG, potion_of_confusion_IMG, chest_IMG]
																														#  27				28					29							30						31

	def set_map(self):

		final_map = [[Tile(True, block_sight=True, is_map_structure=True) for x in range(constants.MAP_WIDTH)] for y in range(constants.MAP_HEIGHT)]

		for x in range(0, 30):
			for y in range(0, 30):
				if self.current_raw_map[x][y] == '.':
					final_map[x][y] = Tile(block_movement=False, block_sight=False)

		return final_map


	def init_pygame(self):
		global scr, player, font

		pygame.init()
		pygame.font.init()
		pygame.mouse.set_visible(True)
		font = pygame.font.Font("Px437_IBM_VGA8.ttf", constants.FONT_SIZE)
		subscript_font = pygame.font.Font("Px437_IBM_VGA8.ttf", 8) # font will be used to tell how many of exact items are in the inventory | NOT USED

		scr = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))#, pygame.FULLSCREEN)

		pygame.display.set_caption("{0} {1}".format(constants.title, constants.version))

		self.images = self.get_images()

		player_fighter_component = objects.Fighter(500, 3, 5)
		# sprites in dict too
		player = objects.Object(1, 6, self.images[0], constants.PLAYER_NAME, blocks=True, fighter=player_fighter_component, initial_light_radius=3)
		player.description = constants.player_DESCRIPTION
		player.fighter.modificators.update(constants.mods)
		#player.fighter.modificators['mod_to_be_heard'] = -100
		player.fighter.modificators["mod_to_be_seen"] = 100
		#player.hearing = 1 change to modificator
		player.knee_health = 10

		worm_AI = objects.SimpleAI()
		worm_fighter_component = objects.Fighter(2, 2, 1)
		worm = objects.Object(1, 7, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component)

		# for variety only, demo implementation
		#for n in range(constants.MAX_ENEMIES + 30):
		#	mon_x = random.randint(1, constants.MAP_WIDTH - 1)
		#	mon_y = random.randint(1, constants.MAP_HEIGHT - 1)
		#	if self.map[mon_x][mon_y].block_sight or (mon_x, mon_y) == (player.x, player.y):
		#		continue
		#	else:
		#		gobleen_ai = objects.NoiseAI(hearing_chance=60)
		#		gobleen_fighter_component = objects.Fighter(25, 10, 10)
		#		gobleen = objects.Object(mon_x, mon_y, self.images[25], 'goblin', blocks=True, block_sight=True, ai=gobleen_ai, fighter=gobleen_fighter_component, initial_seeing_chance=90) # 2 7
		#		gobleen.sounds['sound_walk'] = "mumbling and shuffling."
		#		gobleen.fighter.modificators.update(constants.mods)
		#		self.objects.append(gobleen)
 

 		abhorrent_creature_BRAIN = objects.FSM()
		abhorrent_creature_AI = objects.NoiseAI(hearing_chance=100, brain=abhorrent_creature_BRAIN)
		abhorrent_creature_fighter_component = objects.Fighter(constants.ABHORRENT_CREATURE_MAX_HP, 40, 50)
		abhorrent_creature = objects.Object(27, 28, self.images[5], 'Abhorrent Creature', blocks=True, block_sight=True, fighter=abhorrent_creature_fighter_component, ai=abhorrent_creature_AI, initial_seeing_chance=20)
		abhorrent_creature.sounds['sound_walk'] = "deep low humming."
		abhorrent_creature.description = constants.abhorrent_creature_DESCRIPTION
		abhorrent_creature.fighter.modificators.update(constants.mods)

		gobleen_BRAIN = objects.FSM()
		gobleen_ai = objects.NoiseAI(hearing_chance=60, brain=gobleen_BRAIN)
		gobleen_fighter_component = objects.Fighter(25, 10, 10)
		gobleen = objects.Object(24, 11, self.images[25], 'goblin', blocks=True, block_sight=True, ai=gobleen_ai, fighter=gobleen_fighter_component, initial_seeing_chance=90) # 2 7
		gobleen.sounds['sound_walk'] = "mumbling and shuffling."
		gobleen.fighter.modificators.update(constants.mods)
		#gobleen.fighter.modificators["mod_to_seeing"] += 70
		#magic_bell = objects.Object(24, 11, self.images[26], 'Magic Bell', blocks=True, block_sight=True)
		#second_magic_bell = objects.Object(24, 17, self.images[26], 'Magic Bell', blocks=True, block_sight=True)

		for n in range(200):
			rand_x = random.randrange(constants.MAP_WIDTH)
			rand_y = random.randrange(constants.MAP_HEIGHT)

			if not self.map[rand_x][rand_y].block_sight:
				hp_potion_item_component = objects.Item(use_func=use_functions.heal, can_break=True, heal_value=5)
				hp_potion = objects.Object(player.x + 1, player.y, self.images[constants.IMAGES_POTION_HP], 'healing potion', item=hp_potion_item_component)
				self.objects.append(hp_potion)

		scroll_of_death_item_component = objects.Item(targetable=True, use_func=use_functions.instant_death)
		scroll_of_death = objects.Object(player.x + 2, player.y, self.images[constants.IMAGES_SCROLL_OF_DEATH], 'scroll of death', item=scroll_of_death_item_component)

		ultimate_hp_potion_item_component = objects.Item(use_func=use_functions.heal, can_break=True, heal_value=50)
		ultimate_hp_potion = objects.Object(player.x + 3, player.y, self.images[21], 'ultimate healing potion', item=ultimate_hp_potion_item_component)

		potion_of_death_item_component = objects.Item(use_func=use_functions.instant_death, can_break=True)
		potion_of_death = objects.Object(player.x + 4, player.y + 1, self.images[28], 'potion of death', item=potion_of_death_item_component)
		potion_of_confusion_item_component = objects.Item(use_func=use_functions.confuse, can_break=True)
		potion_of_confusion = objects.Object(player.x + 1, player.y + 3, self.images[30], 'potion of confusion', item=potion_of_confusion_item_component)

		oil_item_component = objects.Item(use_func=use_functions.refill_lantern, can_break=True, oil_value=500)
		oil = objects.Object(player.x + 3, player.y + 2, self.images[24], 'oil', item=oil_item_component)


		for n in range(5):
			scroll_of_uncontrolled_teleportation_item_component = objects.Item(use_func=use_functions.uncontrolled_teleportation, map=self.map)
			scroll_of_uncontrolled_teleportation = objects.Object(player.x + 2, player.y+1, self.images[17], 'scroll of uncontrolled teleportation', item=scroll_of_uncontrolled_teleportation_item_component)
			self.objects.append(scroll_of_uncontrolled_teleportation)


		self.ui = UI(player.fighter, self.images, 'game_screen')
		bronze_armor_equipment_component = objects.Equipment(slot='breastplate', defence_bonus=4)
		bronze_armor_item_component = objects.Item(use_func=use_functions.equip, name='bronze breastplate', equipment=bronze_armor_equipment_component, UI=self.ui, weight=41)
		bronze_armor = objects.Object(player.x + 1, player.y + 1, self.images[16], 'bronze breastplate', item=bronze_armor_item_component)

		crystal_armor_equipment_component = objects.Equipment(slot='breastplate', defence_bonus=50)
		crystal_armor_item_component = objects.Item(use_func=use_functions.equip, name='crystal breastplate', equipment=crystal_armor_equipment_component, UI=self.ui, weight=51)
		crystal_armor = objects.Object(player.x, player.y + 1, self.images[18], 'crystal breastplate', item=crystal_armor_item_component)

		crown_equipment_component = objects.Equipment(slot='helmet', defence_bonus=2, max_health_bonus=100)
		crown_item_component = objects.Item(use_func=use_functions.equip, name='golden crown of great health', equipment=crown_equipment_component, UI=self.ui)
		crown = objects.Object(player.x + 3, player.y + 1, self.images[20], 'golden crown of great health', item=crown_item_component)

		cloak_of_invisibility_equipment_component = objects.Equipment(slot='cloak', defence_bonus=3, chance_to_be_seen_modificator=-200)
		cloak_of_invisibility_item_component = objects.Item(use_func=use_functions.equip, name='cloak of invisibility', equipment=cloak_of_invisibility_equipment_component, UI=self.ui)
		cloak_of_invibility = objects.Object(player.x + 4, player.y + 2, self.images[29], 'cloak of invisibility', item=cloak_of_invisibility_item_component)


		iron_sword_equipment_component = objects.Equipment(slot='right_hand', power_bonus=10) # for now fixed hand
		iron_sword_item_component = objects.Item(use_func=use_functions.equip, name='iron sword', equipment=iron_sword_equipment_component, UI=self.ui)
		iron_sword = objects.Object(player.x + 1, player.y - 1, self.images[19], 'iron sword', item=iron_sword_item_component)
		great_steel_long_sword_equipment_component = objects.Equipment(slot='left_hand', power_bonus=30)
		great_steel_long_sword_item_component = objects.Item(use_func=use_functions.equip, name='great steel long sword', equipment=great_steel_long_sword_equipment_component, UI=self.ui)
		great_steel_long_sword = objects.Object(player.x + 1, player.y + 2, self.images[22], 'great steel long sword', item=great_steel_long_sword_item_component)

		lantern_equipment_component = objects.Equipment(slot='accessory', charges=700 ,light_radius_bonus=10, activation_func=use_functions.light_lantern, deactivation_string="turns off", wear_off_string="run out of oil")
		lantern_item_component = objects.Item(use_func=use_functions.equip, name='lantern', equipment=lantern_equipment_component, UI=self.ui)
		lantern = objects.Object(player.x + 2, player.y+2, self.images[23], 'lantern', item=lantern_item_component)

		chest_loot = []

		for n in range(10):
			potion_of_death_item_component = objects.Item(use_func=use_functions.instant_death, can_break=True)
			potion_of_death = objects.Object(player.x + 4, player.y + 1, self.images[28], 'potion of death', item=potion_of_death_item_component)
			chest_loot.append(potion_of_death)

		chest_container_component = objects.Container(loot=chest_loot)
		chest = objects.Object(player.x + 2, player.y + 4, self.images[31], 'chest', container=chest_container_component)

		self.objects.append(player)
		self.objects.append(abhorrent_creature)
		self.objects.append(scroll_of_death)
		self.objects.append(bronze_armor)
		self.objects.append(crystal_armor)
		self.objects.append(iron_sword)
		self.objects.append(crown)
		self.objects.append(ultimate_hp_potion)
		self.objects.append(great_steel_long_sword)
		self.objects.append(lantern)
		self.objects.append(oil)
		self.objects.append(gobleen)
		self.objects.append(potion_of_death)
		self.objects.append(cloak_of_invibility)
		self.objects.append(potion_of_confusion)
		self.objects.append(chest)
		#self.objects.append(goblin)
		#self.objects.append(magic_bell)
		#self.objects.append(second_magic_bell)

		self.fov_map = field_of_view.set_fov(self.fov_map)
		field_of_view.cast_rays(player.x, player.y, self.fov_map, self.map, radius=player.fighter.max_light_radius)

	def handle_keys(self):

		# change this to an action, for instance "up" can progress player along y axis and can scroll menus or move line of sight upwards

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					exit(0)
				if event.key == pygame.K_l:
					player.move(1, 0, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_h:
					player.move(-1, 0, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_k:
					player.move(0, -1, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_j:
					player.move(0, 1, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_y:
					player.move(-1, -1, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_u:
					player.move(1, -1, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_n:
					player.move(1, 1, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_b:
					player.move(-1, 1, self.map, self.fov_map, self.objects)
					return 'took_turn'
				if event.key == pygame.K_c:
					player.fighter.sneak()
					return 'took_turn'
				if event.key == pygame.K_g:
					item = player.fighter.get(self.objects, self.ui)
					if item is not None:
						if item.container is None:
							self.ui.add_item_to_UI(item)
						return 'took_turn'

				if event.key == pygame.K_t:
					return "throw"
				if event.key == pygame.K_SEMICOLON:
					return 'look'
				if event.key == pygame.K_PERIOD:
					player.noise_made = {'range': 0, 'chance_to_be_heard': 0, 'source': '', 'sound_name': ''} 
					return 'took_turn'

		return 'idle'

	def handle_mouse(self):
		""" Returns 'took_turn' or 'idle' or 'hovering over'
			Action can be use, drop or 'hovering over'
		"""

		m_x, m_y = pygame.mouse.get_pos()

		area_Inventory = pygame.Rect(constants.INVENTORY_BOX_X * constants.TILE_SIZE, constants.INVENTORY_BOX_Y * constants.TILE_SIZE, constants.INVENTORY_WIDTH * constants.TILE_SIZE ,constants.INVENTORY_HEIGHT * constants.TILE_SIZE)
		area_Equipment = pygame.Rect(constants.EQUIPMENT_AREA_START_X * constants.TILE_SIZE, constants.EQUIPMENT_AREA_START_Y * constants.TILE_SIZE, constants.EQUIPMENT_AREA_WIDTH * constants.TILE_SIZE,
			constants.EQUIPMENT_AREA_HEIGHT * constants.TILE_SIZE)

		if area_Inventory.collidepoint(m_x, m_y):

			action = self.handle_clicks(player.fighter.inventory)

			if action.has_key('item_to_use'):
				self.pause_menu()
				result = self.use_item_by_mouse(action['item_to_use'])
				return result  # player can resign, it then returns idle

			else:
				if action.has_key('item_to_drop'):
					self.pause_menu()
					self.drop_item_by_mouse(action['item_to_drop'])
					return 'took_turn'

		if area_Equipment.collidepoint(m_x, m_y):
			action = self.handle_clicks(player.fighter.equipment)

			if action.has_key('item_to_use'):

				item = action['item_to_use']

				# activate special effects, which I am not going to implement now
				# but the one that i WILL, will be light
				self.pause_menu()

				# here decide to use

				equipment_piece = item.item.equipment

				# use function of torch
				if equipment_piece.activation_func is not None:
					equipment_piece.activate(user=player, eq_name=item.name)

				else:
					player.sent_messages.append("You press your {0} but nothing happens.".format(item.name.title()))

				return 'took_turn'

			else:
				if action.has_key('item_to_drop'):

					item = action['item_to_drop']
					self.pause_menu()
					self.remove_equipment_by_mouse(item)
					player.sent_messages.append("You remove your {0}.".format(item.name.title()))
					return 'took_turn'

		return 'idle'

	def handle_clicks(self, area):

		m_x, m_y = pygame.mouse.get_pos()
		r_click = pygame.mouse.get_pressed()[2]
		l_click = pygame.mouse.get_pressed()[0]

		if l_click == 1:

			for item in area:

				to_check = pygame.Rect(item.x * constants.FONT_SIZE, item.y * constants.FONT_SIZE, constants.FONT_SIZE, constants.FONT_SIZE)
				# it creates rect that bounds item on the screen

				if to_check.collidepoint(m_x, m_y):
					return {'item_to_use': item}

		if r_click == 1:

			for item in area:

				to_check = pygame.Rect(item.x * constants.FONT_SIZE, item.y * constants.FONT_SIZE, constants.FONT_SIZE, constants.FONT_SIZE)
				# it creates rect that bounds item on the screen


				if to_check.collidepoint(m_x, m_y):
					# here decide

					action = self.ui.draw_info_window(item, scr, decide_to_drop=True)
					return action

		return {}

	def use_item_by_mouse(self, item):

		if item.item.targetable:
			target = self.enter_look_mode("Target what?")
			if target is not None:
				item.item.use(target=target, user=player, item=item, UI=self.ui)
				return 'took_turn'

			else:
				return 'idle'

		else:
			item.item.use(user=player, target=player, item=item, UI=self.ui)
			return 'took_turn'

		return 'idle'


	def drop_item_by_mouse(self, item):
		self.ui.remove_item_from_UI(item.x, item.y)
		player.fighter.drop(self.objects, item, self.ui)

	def remove_equipment_by_mouse(self, item):
		self.ui.remove_item_from_equipment_slot(item)
		item.item.equipment.activated = False
		player.fighter.equipment.remove(item)

	def run(self):
		self.state = 'playing'
		clock = pygame.time.Clock()
		player.sent_messages.append("To exit, press ESC.")
		player.sent_messages.append("For more help press '?'.")
		player.sent_messages.append("You descend into your own basement.")
		self.listen_for_messagess(player)
		noises = None

		turn = 'player_turn'

		while self.state == 'playing':
			clock.tick(60)
			scr.fill(BLACK)
			screen_to_draw = 'game_screen'

			if self.state == 'playing':

				if turn == 'player_turn' and player.ai is None:

					player_action = self.handle_keys()
					mouse_action = self.handle_mouse()

					#noises = objects.player_listen_to_noise(player)

					if player_action == 'look':
						noises = player.heard_noises
						target = self.enter_look_mode("Look at what?", got_noise=noises)
						if target is not None:
							self.ui.draw_info_window(target, scr)

					if player_action == 'throw':
						item_to_throw = self.ui.draw_inventory_list(choose_item_text="Throw what?")
						if item_to_throw is not None:
							self.ui.remove_item_from_UI(item_to_throw.x, item_to_throw.y)
							player.fighter.inventory.remove(item_to_throw)
							self.throw_mode(item_to_throw)
							player_action = 'took_turn'

					self.state = self.check_for_player_death()

					if player_action == 'took_turn' or mouse_action == 'took_turn':


						player.fighter.manage_fighter()
						objects.player_hurt_or_heal_knees(player, self.map)
						self.listen_for_messagess(player)
						turn = 'monster_turn'

						# add manage_player function, where there will be all this everything that is done with player, and recovering knee health.

				if player.ai is not None: # Confused
					player.ai.take_turn(_map=self.map, objects=self.objects, player=player, fov_map=self.fov_map)
					player.fighter.manage_fighter()
					objects.player_hurt_or_heal_knees(player, self.map)
					#self.listen_for_messagess(player)
					self.pause_menu()
					turn = 'monster_turn'

				if turn == 'monster_turn':

					player.heard_noises = dict()
					player.heard_noises['monster_sounds'] = []

					for obj in self.objects: # to not iterate over whole list - add monsters to a dedicated one


						self.check_for_death(obj)

						if obj.ai and obj.name != constants.PLAYER_NAME:
							obj.fighter.manage_fighter()

							obj.clear_messages() # clear messages - any previous messages are not up to date
							obj.ai.take_turn(_map=self.map, objects=self.objects, player=player, fov_map=self.fov_map)
							self.listen_for_messagess(obj)

							# Thrown rocks will be player's noise but with different source

							# Make a function out of this (one function - can_hear(obj_one, obj_two, chances...))

							player_noise_range = player.noise_made['range']
							player_noise_source = player.noise_made['source']
							player_noise_chance = player.noise_made['chance_to_be_heard']

							monster_noise_range = obj.noise_made['range']
							monster_noise_source = obj.noise_made['source']
							monster_noise_sound = obj.noise_made['sound_name']
							monster_noise_chance = obj.noise_made['chance_to_be_heard']

							#print player.noise_made

							# monster hearing player
							if utils.can_hear(obj, player, player_noise_range, player_noise_source, player_noise_chance):
								#.print 'A NEW NOISE!'
								obj.ai.destination = (player_noise_source.x, player_noise_source.y)

							# player hearing monster

							if utils.can_hear(player, obj, monster_noise_range, monster_noise_source, monster_noise_chance):
								player.heard_noises['monster_sounds'].append((obj, monster_noise_sound))

					turn = 'player_turn'

					player.noise_made = {'range': 0, 'chance_to_be_heard': 0, 'source': '', 'sound_name': ''} 
				self.draw_all()
				if player.heard_noises: # move that to draw_all
						# display "!";
					noise_to_draw = [x[0] for x in player.heard_noises['monster_sounds']]
					self.ui.draw_noise_indicators(noise_to_draw, self.fov_map)

			fps = font.render("FPS: {0}".format(int(clock.get_fps())), False, WHITE)
			scr.blit(fps, (0, 0))
			pygame.display.flip()

		while self.state == 'game_over':
			self.show_game_over_demo()

	def draw_all(self):

		self.print_messages()
		# self.ui.draw_current_view

		if self.ui.current_view == 'game_screen' or 'inventory_screen':

			field_of_view.fov_recalculate(self.fov_map, player.x, player.y, self.map, player.fighter.max_light_radius)

			for x in range(0, 30):
				for y in range(0, 30):
					_x = x * constants.TILE_SIZE
					_y = y * constants.TILE_SIZE

					if self.fov_map[x][y] == 1:
						if self.map[x][y].block_sight and self.map[x][y].is_map_structure:
							scr.blit(self.images[1], (_x, _y))
						else:
							scr.blit(self.images[2], (_x, _y))
					else:
						scr.blit(self.images[3], (_x, _y))

		self.ui.draw(scr, player.fighter.knees)
		self.draw_objects()
		player.draw(scr)
		player.clear_messages() # we clear his messages after we process them, that is we cannot do that in run method

	def draw_objects(self):

		for obj in self.objects:
			if obj.fighter is None:
				#if field_of_view.is_in_fov(self.fov_map, obj): # comment this out to see every object on map
				obj.draw(scr)

		for obj in self.objects:
			if obj.fighter is not None and obj.name != 'player':
				#if field_of_view.is_in_fov(self.fov_map, obj):
				obj.draw(scr)
			obj.clear_messages()


	def spawn_objects(self):

		number_of_enemies = constants.MAX_ENEMIES

		# first player
		# stairs
		# secondly objects
		# thirdly monsters

		while True:

			# get a random number
			# check if it's not wall
			# check if enemy has a chance to spawn
			# place
			pass

	def check_for_death(self, obj):
		if obj.fighter is not None and obj.name != player.name:
			if obj.fighter.hp <= 0:
				obj.fighter.kill(self.fov_map, player.x, player.y, self.map, self.images, player.fighter.max_light_radius)

	def check_for_player_death(self):
		if player.fighter.hp <= 0:
			player.img = self.images[6]
			return 'game_over'
		else:
			return 'playing'

	def show_game_over_demo(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					exit(0)

		scr.fill(BLACK)
		for x in range(0, 30):
			for y in range(0, 30):
				_x = x * constants.TILE_SIZE
				_y = y * constants.TILE_SIZE
				if self.map[x][y].block_sight and self.map[x][y].is_map_structure:
					scr.blit(self.images[1], (_x, _y))
				else:
					scr.blit(self.images[2], (_x, _y))
		#self.draw_all()

		self.draw_objects()
		self.listen_for_messagess(player)
		self.print_messages()
		pygame.display.flip()

	def listen_for_messagess(self, obj):

		# it has to remove that amount of messages, so the only 5 remains
		if len(self.messages) <= 5:
			self.messages.extend(obj.sent_messages)
			self.messages_history.extend(obj.sent_messages)
		else:
			to_delete = abs(len(self.messages) - 5)
			del self.messages[:to_delete]
			self.messages.extend(obj.sent_messages)

	def print_messages(self):
		y = constants.SCREEN_SIZE_HEIGHT - 2
		_y = y * constants.FONT_SIZE

		# add portrait of a monster here - if player can hear monster, he will receive his message | or that he hears something

		for message in reversed(self.messages): # last ones are the latest
			message_to_blit = font.render(message, False, WHITE) # color, add custom color
			scr.blit(message_to_blit, (16, _y))
			_y -= constants.FONT_SIZE

	def pause_menu(self):
		# to prevent player from activating bunch of items at once

		unpause = False

		more_text = font.render("More...", False, WHITE)

		while not unpause:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						unpause = True

			self.draw_all()
			scr.blit(more_text, (0, 0))
			pygame.display.flip()


	def enter_look_mode(self, title, throwing=False, **kwargs):

		action = None

		look_text = font.render(title, False, WHITE)

		noise = kwargs.get('got_noise')

		if noise is not None:
			noise_to_draw = [x[0] for x in noise['monster_sounds']]

		x = player.x
		y = player.y

		while action is None:

			for event in pygame.event.get():

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_l:
						x += 1
					if event.key == pygame.K_h:
						x -= 1
					if event.key == pygame.K_k:
						y -= 1
					if event.key == pygame.K_j:
						y += 1
					if event.key == pygame.K_y:
						y -= 1
						x -= 1
					if event.key == pygame.K_u:
						y -= 1
						x += 1
					if event.key == pygame.K_n:
						y += 1
						x += 1
					if event.key == pygame.K_b:
						y += 1
						x -= 1
					if event.key == pygame.K_RETURN:
						for obj in self.objects:
							if (obj.x, obj.y) == (x, y) and (obj.fighter or obj.item) and self.fov_map[obj.x][obj.y] == 1 and not throwing:
								return obj

							if (obj.x, obj.y) == (x, y) and obj.fighter and self.fov_map[obj.x][obj.y] != 1 and noise is not None: # sound

								monsters = noise['monster_sounds']

								for mon in monsters:

									if obj == mon[0]:
										player.sent_messages.append("You hear: {0}".format(mon[1]))
										self.listen_for_messagess(player)
										break
						if throwing:
							return (x,y)
						else:				
							return None

			self.draw_all()
			self.draw_bresenham_line(player.x, player.y, x, y)
			self.print_messages()
			scr.blit(look_text, (0, 0))
			if noise is not None:
				self.ui.draw_noise_indicators(noise_to_draw, self.fov_map)
			pygame.display.flip()

	def draw_bresenham_line(self, x0, y0, x1, y1):
		"Bresenham's line algorithm - taken from: https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python"

		line_img = font.render("*", False, WHITE)

		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		x, y = x0, y0
		sx = -1 if x0 > x1 else 1
		sy = -1 if y0 > y1 else 1

		count = 0

		if dx > dy:
			err = dx / 2.0
			while x != x1:
				err -= dy
				if err < 0:
					y += sy
					err += dx
				x += sx

				black_rect = pygame.Rect(x * constants.FONT_SIZE, y * constants.FONT_SIZE, 16, 16)
				scr.fill(BLACK, black_rect)
				scr.blit(line_img, (x * constants.FONT_SIZE, y * constants.FONT_SIZE))

		else:
			count = 0
			err = dy / 2.0
			while y != y1:
				err -= dx
				if err <0:
					x += sx
					err += dy
				y += sy

				black_rect = pygame.Rect(x * constants.FONT_SIZE, y * constants.FONT_SIZE, 16, 16)
				scr.fill(BLACK, black_rect)
				scr.blit(line_img, (x * constants.FONT_SIZE, y * constants.FONT_SIZE))

	def throw_mode(self, item): # add the functionality of casting spells - to show the spell effect traversing the path (or "item" will be spell, and string in self.enter_look_mode will be "cast where?") 

		destination = self.enter_look_mode("Throw where?", throwing=True)

		path_of_projectile = utils.bresenham_alg(player.x, player.y, destination[0], destination[1])

		# now: scroll through the map and check if it doesn't collide with an object or wall.


		#print "player x,y: {0} {1}".format(player.x, player.y)
		obj = self.return_obj_at_impact(path_of_projectile, item)
		player.sent_messages.append("{0} throws {1}!".format(player.name.title(), item.name.title()))
		player.noise_made['range'] = 10
		player.noise_made['chance_to_be_heard'] = 100 # + armor
		player.noise_made['source'] = item
		player.noise_made['sound_name'] = 'jeb'

		print obj


		if obj != 'didnt throw' and obj is not None:
		
			if obj.fighter is not None and not item.item.can_break:
				# apply the effect on the monster

				print "dupa"

				# lesser damage

				player.sent_messages.append("{0} hits {1}!".format(item.name.title(), obj.name.title()))
				#self.listen_for_messagess(player)
				return

			if obj.fighter is not None and item.item.can_break:
				player.sent_messages.append("{0} hits {1}!".format(item.name.title(), obj.name.title()))

				# damage

				#obj.fighter.hp

				if item.item.use_func is not None:
					print 'dodo'
					item.item.use(target=obj, user=player, item=item, UI=self.ui)
					self.check_for_death(obj)
				player.sent_messages.append("{0} shatters!".format(item.name.title()))
				#self.listen_for_messagess(obj)
				return

			#if obj.fighter is None and item.item.can_break:
			#	player.sent_messages.append("{0} shatters!".format(item.name.title()))
				#self.listen_for_messagess(player)
			#	return


		else:

			# there wasn't any object and item was breakable

			if obj == 'didnt throw':
				player.sent_messages.append("{0} apparently doesn't know how to throw things.".format(player.name.title()))
				return

			elif obj is None:
				if item.item.can_break:
					player.sent_messages.append("{0} shatters!".format(item.name.title()))
				return



	def return_obj_at_impact(self, path, item):

		SHOW_PROJECTILE_EVENT = pygame.USEREVENT
		SHOW_PROJECTILE_MS = 100

		pygame.time.set_timer(SHOW_PROJECTILE_EVENT, SHOW_PROJECTILE_MS)
		done = False
		index = 0

		if path != 'dont throw':

			while not done:
	
				try:
	
					for event in pygame.event.get():
	
						if event.type == SHOW_PROJECTILE_EVENT:
							x = path[index][0]
							y = path[index][1]
	
							if not self.map[x][y].block_sight:
	
								for obj in self.objects:
									if obj.x == x and obj.y == y and obj.fighter and obj.name != constants.PLAYER_NAME:
										print 'hit'
										item.x = path[index-1][0]
										item.y = path[index-1][1]
										if not item.item.can_break:
											self.objects.append(item)

										#if not item.item.can_break:
										#	print "dupsko"
										#	self.objects.append(item)
										return obj

								#print "{0} {1}ok".format(x, y)
								pygame.time.set_timer(SHOW_PROJECTILE_EVENT, SHOW_PROJECTILE_MS)
	
								self.draw_all()
								black_rect = pygame.Rect(x * constants.FONT_SIZE, y * constants.FONT_SIZE, 16, 16)
								scr.fill(BLACK, black_rect)
								scr.blit(item.img, (x * constants.TILE_SIZE, y * constants.TILE_SIZE))
								pygame.display.flip()
	
								index += 1
							else:
								if not len(path) == 1: # When player is close to the wall, do not throw it onto the wall (because starting position is not taken into an account)
									item.x = path[index-1][0]
									item.y = path[index-1][1]
								else:
									item.x = player.x
									item.y = player.y
								self.objects.append(item)
								done = True
	
				except IndexError:
					if not item.item.can_break:
						item.x = path[index-1][0]
						item.y = path[index-1][1]
						self.objects.append(item)
						return
					else:
						return None
		else:
			player.fighter.inventory.append(item)
			self.ui.add_item_to_UI(item)
			return 'didnt throw'


class UI(object): # move this to objects
	# this class is responsible for drawing the inventory, noise indicators and various windows
	def __init__(self, player, images, current_view):
		self.images = images
		self.current_view = current_view
		self.inv_start_pos_x = constants.INVENTORY_ITEMS_START_X * constants.FONT_SIZE
		self.inv_start_pos_y = constants.INVENTORY_ITEMS_START_Y * constants.FONT_SIZE

		self.inventory_places = [[y, x, None] for y in range(constants.INVENTORY_ITEMS_START_Y, constants.INVENTORY_PLACES_HEIGHT + constants.INVENTORY_ITEMS_START_Y)
											  for x in range(constants.INVENTORY_ITEMS_START_X, constants.INVENTORY_PLACES_WIDTH + constants.INVENTORY_ITEMS_START_X)]

		self.inventory_rect = pygame.Rect(constants.INVENTORY_ITEMS_START_X * constants.FONT_SIZE, constants.INVENTORY_ITEMS_START_Y * constants.FONT_SIZE,
										  constants.INVENTORY_WIDTH * constants.FONT_SIZE, constants.INVENTORY_HEIGHT * constants.FONT_SIZE)

		self.equipment_places = { 'helmet': [constants.UI_HELMET_SLOT, None],
								  'breastplate': [constants.UI_BREASTPLATE_SLOT, None],
								  'cloak': [constants.UI_CLOAK_SLOT, None],
								  'right_hand': [constants.UI_RIGHT_HAND_SLOT, None],
								  'left_hand': [constants.UI_LEFT_HAND_SLOT, None],
								  'left_foot': [constants.UI_LEFT_FOOT_SLOT, None],
								  'right_foot': [constants.UI_RIGHT_FOOT_SLOT, None],
								  'amulet': [constants.UI_AMULET_SLOT, None],
								  'accessory': [constants.UI_ACCESSORY_SLOT, None],
								  'left_ring': [constants.UI_LEFT_RING_SLOT, None],
								  'right_ring': [constants.UI_RIGHT_RING_SLOT, None]
								}

	def draw_rect(self, start_x, start_y, width, height, border_tiles, scr, title=None):
		# border tiles is a list with 5 tiles - horizontal, vertical and four corners

		TOP_LEFT, BOTTOM_LEFT, TOP_RIGHT, BOTTOM_RIGHT, HORIZONTAL, VERTICAL = border_tiles

		for x in range(start_x, width + start_x):
			for y in range(start_y, height + start_y):
				_x = x * constants.TILE_SIZE
				_y = y * constants.TILE_SIZE

				if x == start_x and y == start_y:
					scr.blit(TOP_LEFT, (_x, _y))

				elif x == start_x + width-1 and y == start_y:
					scr.blit(TOP_RIGHT, (_x, _y))

				elif x == start_x and y == start_y + height-1:
					scr.blit(BOTTOM_LEFT, (_x, _y))

				elif x == start_x + width-1 and y == start_y + height-1:
					scr.blit(BOTTOM_RIGHT, (_x, _y))

				elif x == start_x and y != start_y + height-1 or x == start_x + width-1 and y != start_y + height-1 and y != start_y:
					scr.blit(VERTICAL, (_x, _y))

				elif y == start_y and x != start_x and x != start_x + width-1 or y == start_y + height-1 and x != start_x and x != start_x + width-1:
					scr.blit(HORIZONTAL, (_x, _y))


		if title is not None:

			title_len = len(title)
			if (title_len % 2 == 0):
				title_even = True
			else:
				title_even = False

			text_to_blit = font.render(title, False, WHITE)

			x = (start_x + (width / 2)  - (title_len / 2)) * constants.FONT_SIZE
			y = start_y * constants.TILE_SIZE + 4

			if title_even:
				black_rect = pygame.Rect(x, y, title_len * constants.FONT_SIZE, constants.FONT_SIZE - 5)

			else:
				black_rect = pygame.Rect(x, y, (title_len - 1) * constants.FONT_SIZE, constants.FONT_SIZE - 5)

			scr.fill(BLACK, rect=black_rect)

			x = (black_rect.centerx - (title_len * constants.FONT_SIZE) / 4)

			scr.blit(text_to_blit, (x, y - 2))

		# add contents here
		# draw name of the rect in the middle of upper part of the rect

	def draw(self, scr, knee_health): #draw_main_screen
		messages_IMAGES = [self.images[8], self.images[9], self.images[10], self.images[11], self.images[7], self.images[12]]
		information_IMAGES  = messages_IMAGES

		self.draw_rect(constants.START_MESSAGE_BOX_X, constants.START_MESSAGE_BOX_Y, 30, 7, messages_IMAGES, scr, 'MESSAGES')
		self.draw_rect(constants.START_INFORMATION_BOX_X, constants.START_INFORMATION_BOX_Y, 12, 20, messages_IMAGES, scr, player.name.upper())
		self.draw_rect(constants.INVENTORY_BOX_X, constants.INVENTORY_BOX_Y, constants.INVENTORY_WIDTH, constants.INVENTORY_HEIGHT, messages_IMAGES, scr, 'INVENTORY')
		self.draw_inventory(scr)
		self.draw_equipment(scr, knee_health)

		hp_to_blit = font.render("HP: {0} / {1}".format(player.fighter.hp, player.fighter.max_hp), False, RED)

		scr.blit(hp_to_blit, (constants.HP_START_X * constants.TILE_SIZE, constants.HP_START_Y))

	def draw_inventory(self, scr): # change that
		for item in player.fighter.inventory:

			_x = item.x * constants.FONT_SIZE
			_y = item.y * constants.FONT_SIZE

			scr.blit(item.img, (_x, _y))

	def add_item_to_UI(self, item):
		# checks how many items there is, basically it changes the item x and y so that it goes to the inventory area

		x = 1
		y = 0
		slot = 2

		for place in self.inventory_places:
			if place[slot] is None:
				item.x = place[x]
				item.y = place[y]
				place[slot] = item
				break

	def remove_item_from_UI(self, item_x, item_y):

		# sort inventory - goes through all items and sets them again

		x = 1
		y = 0
		slot = 2

		for place in self.inventory_places:
			if place[x] == item_x and place[y] == item_y:
				place[slot] = None
				break

	def draw_info_window(self, obj, scr, decide_to_drop=False):
		messages_IMAGES = [self.images[8], self.images[9], self.images[10], self.images[11], self.images[7], self.images[12]]


		# General description about any object
		# If object.fighter - draw additional info
		# If object.item - draw additional info
		# If object.equipment - draw additional info

		first_paragraph = "It is {0}."
		wrapped_description = textwrap.wrap(obj.description, 80)
		#name_to_blit =  #center this below imaage

		object_image = pygame.transform.scale(obj.img, (100, 100))

		if obj.fighter:

			attack_to_blit = font.render("Attack: " + str(obj.fighter.attack_stat + obj.fighter.initial_attack_stat), False, WHITE)
			hp_to_blit = font.render("HP: " + str(obj.fighter.hp ), False, RED)


		escaped = False

		while not escaped:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
				if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_d and decide_to_drop:
						scr.fill(BLACK)

						return {'item_to_drop': obj}

					else:
						escaped = True
						return {}

						escaped = True
					break


			scr.fill(BLACK)


			self.draw_rect(0, 0, 42, 37, messages_IMAGES ,scr, title=obj.name.title())
			y = 1
			for line in wrapped_description:
				line = font.render(line, False, WHITE)
				scr.blit(line, (constants.FONT_SIZE, y * constants.FONT_SIZE))
				y += 1

			scr.blit(object_image, (25 * constants.TILE_SIZE, 12 * constants.TILE_SIZE))

			if obj.fighter:
				scr.blit(hp_to_blit, (10 *constants.TILE_SIZE, 15 * constants.TILE_SIZE))
				scr.blit(attack_to_blit, (10 *constants.TILE_SIZE, 16 * constants.TILE_SIZE))

			if decide_to_drop:
				drop = "(D) to drop or remove."
				drop_to_blit = font.render(drop, False, WHITE)
				scr.blit(drop_to_blit, ((constants.SCREEN_SIZE_WIDTH - 1 - len(drop) / 2) * constants.FONT_SIZE, (constants.SCREEN_SIZE_HEIGHT-2) * constants.FONT_SIZE))

			pygame.display.flip()


	def add_item_to_equipment_slot(self, piece_of_equipment):

		slot = piece_of_equipment.item.equipment.slot
		if self.equipment_places[slot][1] is None:
			self.equipment_places[slot][1] = piece_of_equipment
			self.remove_item_from_UI(piece_of_equipment.x, piece_of_equipment.y) # remove before moving (changing the coordinates) the item.
			x = self.equipment_places[slot][0][0]
			y = self.equipment_places[slot][0][1]
			piece_of_equipment.x = x
			piece_of_equipment.y = y
			return True
		else:
			return False

	def remove_item_from_equipment_slot(self, piece_of_equipment):
		slot = piece_of_equipment.item.equipment.slot

		if self.equipment_places[slot][1] is not None:
			self.equipment_places[slot][1] = None
			player.fighter.inventory.append(piece_of_equipment)
			self.add_item_to_UI(piece_of_equipment)

	def draw_equipment(self, scr, knee_health):

		helmet = self.equipment_places['helmet']
		breastplate = self.equipment_places['breastplate']
		cloak = self.equipment_places['cloak']
		l_hand = self.equipment_places['left_hand']
		r_hand = self.equipment_places['right_hand']
		l_foot = self.equipment_places['left_foot']
		r_foot = self.equipment_places['right_foot']
		l_ring = self.equipment_places['left_ring']
		r_ring = self.equipment_places['right_ring']
		amulet = self.equipment_places['amulet']
		accessory = self.equipment_places['accessory']

		items = [helmet, breastplate, cloak, l_hand, r_hand, l_foot, r_foot, l_ring, r_ring, amulet, accessory]

		for i in items:
			scr.blit(self.images[15], (i[0][0] * constants.FONT_SIZE, i[0][1] * constants.FONT_SIZE))

		for piece in items:
			if piece[1] is not None:
				image_to_blit = piece[1].img
				x = piece[1].x * constants.TILE_SIZE
				y = piece[1].y * constants.TILE_SIZE
				scr.blit(image_to_blit, (x, y))

		self.draw_infos(knee_health) # such as sneaking and sound

	def draw_infos(self, knee_health):

		# knees

		knee_health_to_display = knee_health
		if knee_health_to_display < 0:
			knee_health_to_display = 0

		knees_to_blit = font.render("Knees:", False, WHITE)
		open_sqr_bracket = font.render("[", False, WHITE)
		close_sqr_bracket = font.render("]", False, WHITE)
		knee_good = font.render("|", False, GREEN)
		knee_bad = font.render("|", False, RED)
		sneaking_TXT = font.render("Crouching", False, PALE)
		overburdened_TXT = font.render("Overburdened!", False, RED)
		burdened_TXT = font.render("Burdened", False, LIGHT_RED)

		health_BAD_rect = pygame.Rect((constants.START_INFORMATION_BOX_X + 4.3) * constants.TILE_SIZE, ((constants.START_INFORMATION_BOX_Y + 12.3) * constants.TILE_SIZE), 10 * 10, 8)
		health_GOOD_rect = pygame.Rect((constants.START_INFORMATION_BOX_X + 4.3) * constants.TILE_SIZE, ((constants.START_INFORMATION_BOX_Y + 12.3) * constants.TILE_SIZE), knee_health_to_display * 10, 8)
		scr.fill(RED, rect=health_BAD_rect)
		scr.fill(GREEN, rect=health_GOOD_rect)

		scr.blit(knees_to_blit, (((constants.START_INFORMATION_BOX_X + 1) * constants.TILE_SIZE, (constants.START_INFORMATION_BOX_Y + 12) * constants.TILE_SIZE)))

		if player.fighter.sneaking:
			scr.blit(sneaking_TXT, ((constants.START_INFORMATION_BOX_X + 1) * constants.TILE_SIZE, constants.START_INFORMATION_BOX_Y + 13 * constants.TILE_SIZE))

		if player.fighter.is_burdened() and not player.fighter.is_overburdened():
			scr.blit(burdened_TXT, ((constants.START_INFORMATION_BOX_X + 1) * constants.TILE_SIZE, constants.START_INFORMATION_BOX_Y + 14 * constants.TILE_SIZE))

		if player.fighter.is_overburdened():
			scr.blit(overburdened_TXT, ((constants.START_INFORMATION_BOX_X + 1) * constants.TILE_SIZE, constants.START_INFORMATION_BOX_Y + 15 * constants.TILE_SIZE))

	def draw_noise_indicators(self, noises, fov):

		sources = noises

		try:

			for noise in sources:

				icon = self.images[27]
				x = noise.x
				y = noise.y

				if fov[x][y] != 1:
					scr.blit(icon, (x * constants.TILE_SIZE, y * constants.TILE_SIZE))

		except IndexError:
			pass

	def draw_inventory_list(self, choose_item_text=None, title="Inventory", container=None, loot_all=False): # make this into a "listed_window" function

		escaped = False
		messages_IMAGES = [self.images[8], self.images[9], self.images[10], self.images[11], self.images[7], self.images[12]]

		items_and_keys = {}

		num = 97

		if container is None:
			container = player.fighter.inventory

		for item in container:

			items_and_keys[chr(num)] = item

			num += 1

		while not escaped:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit(0)
				if event.type == pygame.KEYDOWN:

					try:

						if loot_all:
							if event.key == pygame.K_LSHIFT:
								return items_and_keys.values()

						if items_and_keys:
							key_pressed = chr(event.key)

							if items_and_keys.has_key(key_pressed):
								return items_and_keys[key_pressed]
						escaped = True
					except ValueError:
						pass

			scr.fill(BLACK)

			self.draw_rect(0, 0, 42, 37, messages_IMAGES, scr, title)
			if choose_item_text is not None:

				txt = font.render(choose_item_text, False, WHITE)
				scr.blit(txt, (constants.TILE_SIZE, constants.TILE_SIZE))

			if loot_all:

				loot_all_text = font.render("Shift to loot all.", False, GOLD)
				y = constants.TILE_SIZE
				scr.blit(loot_all_text, ((constants.TILE_SIZE * 30) + 32, y * 35))


			y = 3 * constants.TILE_SIZE
			num = 97
			for item in container:

				items_and_keys[chr(num)] = item

				x = constants.TILE_SIZE * 2

				txt = font.render("{0} - ".format(chr(num)), True, WHITE)


				scr.blit(item.img, (x * 3, y))
				scr.blit(font.render(item.name, True, WHITE), (x * 4, y))
				scr.blit(txt, (x, y))

				y += constants.TILE_SIZE
				num += 1


			pygame.display.flip()

		return None
		# return item chosen

class Level(object): # move this to objects
	pass


def main():
	game = Game()
	game.init_pygame()
	game.run()

if __name__ == '__main__':
	main()


# Goals:

# Step 1: - Basics
# Moving player v 
# Basic monster v
# Cellular automata map v
# Items - scrolls v and potions v, equipment - sword, equipment slots v | And that involves calculations of attack and defense.
# Inventory v
# Line of sight - to targeting v, description menu v <- partially done, but i don't need to do this right now.
# Examining - if you get the item from the ground, you cannot look at it! <- if right click -> drop in examine menu v
# Using items and examining them via keyboard. - a new menu that is ordered by alphabet. -> not needed now | (t)hrowing and (a)ctivating have that menu - and! add that when player presses "i"

# Step 2: - Core mechanics that will seperate my game from others
# Lantern v and torches - increasing fov v refilling v - lantern is given at the beginning with one extra oil, and no lantern is spawned during the game
# Lantern makes player more visible. <- Very important
# Optimise code - make functions more general, input processing etc... and then: (the most important change i could add from that point is event queue - decide what is done in what order)
# Noise AI - possible need for an A* algorithm DONE
# Making noise, noise mechanic - either by shouting, tumbling over! or throwing!
# Walking carefully - sneaking (crouching) Done, know I need to make the player scream if he crouches for too long. ("Pysio's legs hurt!") done
# If monster is making noise detectable to player, blit an quesiton mark in the position he did the noise for a couple of turns DONE <- noise can be heard multiple times
# Noise (done by player) represented by exclamation marks : [!!!!!!!!!!!!] (Range, and with colors: level) (Level indicates how piercing through the walls it is, how many walls can it pierce till it fades) <- too demanding
# Monster's vision. DONE, too demanding!!! (by computer)
# Below 25 level of depth, abhorrent creatures will spawn and it will be necessary to crouch and sneak.
# To show what player has already explored, make new item called magic map, that will be taking notes automatically <- not necessary
# Couple of new enemies, equipment
# Monsters dropping items
# Demo version - 7 levels, and a portal to escape, saving!

# Step 3: - Polishing and roguelike elements such as permadeath, levels as well as menu etc.
# Spawning player randomly, in way which he does not spawn in walls
# Spawning enemies randomly, in way which they do not spawn in walls
# Identifying! - Aside from healing potion - this will be recognizable by player from the beginning, because he will receive 1 from mage. | Use random sprite for potion - that way, it will not be recognizable.
# Help in game - "?"
# Artifact items!
# Show items of monster on its image in show_info_window
# Smith like from Metin2 - only way to upgrade, beside finding some magic thing - BUT! it costs a lot of money, and if it goes bad - the item is destroyed. <- on level above middle one | Chance depending on blessing.
# Descending, loading maps, saving etc.
# Magic, spellbooks and spell menu.
# Endgame - [?] and intro text
# Main menu
# Home Level


# TO FIX:
# 1. Change FONT_SIZE to TILE_SIZE when necessary
# When player dies, game doesn't acknowledge that
# If there are several items on the ground, you have to pick up everything that is above from wanted item! <- Maybe allow only one item to be put in one spot? <- DONE, but I don't know if thats a good thing, maybe build a menu from which I can select what I want to get
# Getting images - one big array is very inconvenient.
# Object data in dictionary
# Multiple use functions
# Messages are out of bound - make text wrapping in messages field.

# Engine class?
# That processess input, puts action into queues, returns states etc

# Make the object that has the ai have its own fov map - it's not good that it works in ways of "If you can see me, I can see you", because it subtracts the tactical possibility of hiding, while still seing other object etc. DONE <- too laggy
# Another problem that this creates, is that when I will be going to implement lighting, and objects that create light (augment the fov when they're in my fov), simply augment the vision of enemies!
# Abhorrent creatures are pretty much blind - they can see only for one tile (other than themselves) - but they have excellent hearing
# Mage will tell in the beginning that the casting unleashed creatures that have weak sight.

# Maybe movable camera? although it is very hard it will certainly add more mystery and difficulty.
# HP does not regenerate but you can throw rocks to kill enemies.

# Make enemies that drop special items and special branches! for example: portal to the shadow realm with monster that drops scroll that can stun evil demons for 10 rounds.
# And with all that, keep the mystery and narrative theme going on. (Not shadow realm, but "you step into the portal, swirling and shaking you transmigrate beyond the realms of worlds!")
# When overburdened, player might tumble and make noise



# V - Deprecated
# Noise AI (Mechanic: the lower (lvl) the noise detected, the better the hearing is):
# 1. Monster has it's own fov map and Level Of Hearing, that is: WHICH LEVEL of noise monster can detect. (If it has good hearing, he can detect low levels of noise) done
# 2. The object that emits sound has: Max level of sound that can be created and range of that sound. done
# 3. Each turn, surrounding can make noise and it uses the same algorithm that fov does. done
# 4. Each noise type has to have an indicator, that shows how quickly the noise fades. done
# 5. If player makes noise that monster can hear, he gets message "something growls!" (Player gets a notification only if he hears the sound)
# 6. Sneaking is a good option, but it hurts your ankles. (If used too much, player will scream)
# 7. Sound is made: "fov" of sound traverses with it's own properties, hitting walls, fades etc.: Hits monster that can hear it: Monster goes to sound source. done


# New noise AI: Done v 0.27
#	1. Check if the algorithm will not be slow:
#	 a) Measure the distance between obj and another obj - if it's less or equal than the minimum range then the noise might be heard; proceed to throw random chance. -!draw bresenham line!-.
#	 b) Get rid of noise map - only check whether there was a sound and iterate over every enemy checking its distance first!
# Done

# Ok, now we have to create another creature on which we will test this. done

# After Noise, now add unique noise names for the creature - that way the player will be able to learn what monster makes what noises v - and then sneaking, knee health. v
# AND: don't show the noise in the message log - when player will be hearing many monsters, it will clog it, instead make so, that when player "looks" at noise indicator, it shows the noise name e.g - "it growls". v
# And after that, it's time for light sources! - chance to be seen, i don't know if it's a good idea, beside chance to seing in NoiseAI
# We have to optimize first... done
# Learn profiling.

# Add invisible traps

# Faktycznie mozna byloby wszystkie te metody wyrzucic z Game, czyniac te klase, a w niej zostawic same dane czy metody scisle do niej przynalezace.

# Too demanding:

# Noise map
# Monsters own fov map

# Way to hop over it: random chance <- add random chance to vision of monsters too!
# Modificators - they add or subtract to chances:

# 1. Seeing (e.g + 10)
# 2. Hearing (e.g - 20)
# 3. Chance to be heard
# 4. Chance to be seen - with lantern it's 100


#  v 0.28
# Next: Chance to seeing in NoiseAI V
#		When crouching, show that on the right side in ui. V
#		Throwing - add events to show pseudo-animation of object traversing the path. V | Increasing chance to miss, depending on the distance X <- now it is not important | Add sound on impact! V
#		Calculated chance of hearing and seeing from armour - decrease or increase V
#		Add miss chance V
#		Add STR INT DEX LUCK to introduce classes later on - class type that will determine the stats - player will roll them
#		Change attacking - random value from initial_attack_stat V
#		Being overburdened - bigger chance to tumble over | Tumbling over instantly V | Add Burdened - to show player that he is on the edge of being overburdened DONE
#		Add timed items - scroll of blessing for e.g 50 turns. - scroll of deafening <- timed effects <- multiple moded modificators
#		Add damage from thrown objects
#		Not "sended" - "sent"! DONE
#		Write a sentence, that shows when player wants to activate item that has 0 charges.
#		FSM done!
#		Container - Putting V | Taking V

# THROWING DOESNT WORK PROPERLY!!!

# v 0.29 - Demo version
#		In-game help.
#		Informations properly displayed in windows.
#		AOE! Wand of fire
#		Access message history
#		Saving, loading, deleting saves. <- one save state
#		Demo version - simple procedural progression of items and monsters, 7 levels <- this first, next menu - very important, we have to know if it is at all playable
#		Simple Menu without intro, but with [not in demo] classes except Warrior.
