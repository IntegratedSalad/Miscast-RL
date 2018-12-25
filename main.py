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
RED = (219, 0, 0)
GREEN = (3, 172, 37)
PALE = (172, 112, 100)

class Game(object):

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


		hp_potion_IMG = potions_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		ultimate_hp_potion_IMG = potions_SPRITES.image_at((1 * constants.TILE_SIZE, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		scroll_of_death_IMG = scrolls_SPRITES.image_at((5 * constants.TILE_SIZE, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		scroll_of_uncontrolled_teleportation_IMG = scrolls_SPRITES.image_at((4 * constants.TILE_SIZE, 2 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		oil_IMG = potions_SPRITES.image_at((2 * constants.TILE_SIZE, 2 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		iron_sword_IMG = medium_weapons_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		bronze_armor_IMG = armor_SPRITES.image_at((0, 6 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		crystal_armor_IMG = armor_SPRITES.image_at((7 * constants.TILE_SIZE, 6 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		crown_IMG = helmets_SPRITES.image_at((2 * constants.TILE_SIZE, 3 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		ui_MESSAGE_HORIZONTAL = ui_SPRITES.image_at((constants.TILE_SIZE, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_LEFT = ui_SPRITES.image_at((0, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_LEFT = ui_SPRITES.image_at((0, constants.TILE_SIZE * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_RIGHT = ui_SPRITES.image_at((2 * constants.TILE_SIZE, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_RIGHT = ui_SPRITES.image_at((2 * constants.TILE_SIZE, constants.TILE_SIZE * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_VERTICAL = ui_SPRITES.image_at((0, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE))

		return [player_IMG, wall_IMG, floor_IMG, empty_spaceIMG, worm_IMG, abhorrent_creature_IMG, corpse_IMG,
				ui_MESSAGE_HORIZONTAL, ui_MESSAGE_TOP_LEFT, ui_MESSAGE_BOTTOM_LEFT, ui_MESSAGE_TOP_RIGHT, ui_MESSAGE_BOTTOM_RIGHT, ui_MESSAGE_VERTICAL, hp_potion_IMG, scroll_of_death_IMG, inventory_slot_IMG, bronze_armor_IMG,
				scroll_of_uncontrolled_teleportation_IMG, crystal_armor_IMG, iron_sword_IMG, crown_IMG, 
				ultimate_hp_potion_IMG, great_steel_long_sword_IMG, lantern_IMG, oil_IMG, goblin_IMG, magic_bell_IMG, noise_indicator_IMG]

	def set_map(self):

		final_map = [[Tile(True, block_sight=True, is_map_structure=True) for x in range(constants.MAP_WIDTH)] for y in range(constants.MAP_HEIGHT)]

		for x in range(0, 30):
			for y in range(0, 30):
				if self.current_raw_map[x][y] == '.':
					final_map[x][y] = Tile(block_movement=False, block_sight=False)

		return final_map


	def init_pygame(self):
		global scr, player, font#, magic_bell, second_magic_bell

		pygame.init()
		pygame.font.init()
		pygame.mouse.set_visible(True)
		font = pygame.font.Font("Px437_IBM_VGA8.ttf", constants.FONT_SIZE)
		subscript_font = pygame.font.Font("Px437_IBM_VGA8.ttf", 8) # font will be used to tell how many of exact items are in the inventory | NOT USED

		scr = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))#, pygame.FULLSCREEN)

		pygame.display.set_caption("RL")

		self.images = self.get_images()

		player_fighter_component = objects.Fighter(500, 3, 5)
		# sprites in dict too
		player = objects.Object(1, 6, self.images[0], constants.PLAYER_NAME, blocks=True, fighter=player_fighter_component, initial_light_radius=3)
		player.noises['move'] = (10, 10, 10)
		player.description = constants.player_DESCRIPTION
		player.hearing_map = {} # only player has hearing map
		player.hearing = 1
		player.knee_health = 10

		worm_AI = objects.SimpleAI()
		worm_fighter_component = objects.Fighter(2, 2, 1)
		worm = objects.Object(1, 7, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component)

		# for variety only, demo implementation
		for n in range(constants.MAX_ENEMIES + 30):
			mon_x = random.randint(1, constants.MAP_WIDTH - 1)
			mon_y = random.randint(1, constants.MAP_HEIGHT - 1)
			if self.map[mon_x][mon_y].block_sight or (mon_x, mon_y) == (player.x, player.y):  
				continue
			else:
				pass
				#worm_AI = objects.SimpleAI()
				#worm_fighter_component = objects.Fighter(2, 2, 1)
				#worm = objects.Object(mon_x, mon_y, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component) # 2 7
				#worm = objects.Object(2, 7, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component) # 2 7
				#self.objects.append(worm)
 
 		abhorrent_creature_AI = objects.NoiseAI(hearing=1)
 		abhorrent_creature_fighter_component = objects.Fighter(constants.ABHORRENT_CREATURE_MAX_HP, 40, 50)
		abhorrent_creature = objects.Object(27, 28, self.images[5], 'Abhorrent Creature', blocks=True, block_sight=True, fighter=abhorrent_creature_fighter_component, ai=abhorrent_creature_AI, initial_fov=3)
		abhorrent_creature.sounds['sound_walk'] = "deep low humming."
		abhorrent_creature.description = constants.abhorrent_creature_DESCRIPTION

		goblin_AI = objects.NoiseAI(hearing=1)
		goblin_fighter_component = objects.Fighter(25, 10, 10)
		goblin = objects.Object(24, 11, self.images[25], 'Goblin', blocks=True, block_sight=True, fighter=goblin_fighter_component, ai=goblin_AI, initial_fov=5)
		goblin.sounds['sound_walk'] = "mumbling and shuffling."
		# you hear...
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

		oil_item_component = objects.Item(use_func=use_functions.refill_lantern, can_break=True, oil_value=500)
		oil = objects.Object(player.x + 3, player.y + 2, self.images[24], 'oil', item=oil_item_component)


		for n in range(5):
			scroll_of_uncontrolled_teleportation_item_component = objects.Item(use_func=use_functions.uncontrolled_teleportation, map=self.map)
			scroll_of_uncontrolled_teleportation = objects.Object(player.x + 2, player.y+1, self.images[17], 'scroll of uncontrolled teleportation', item=scroll_of_uncontrolled_teleportation_item_component)
			self.objects.append(scroll_of_uncontrolled_teleportation)



		self.ui = UI(player.fighter, self.images, 'game_screen')
		bronze_armor_equipment_component = objects.Equipment(slot='breastplate', defence_bonus=4)
		bronze_armor_item_component = objects.Item(use_func=use_functions.equip, name='bronze breastplate', equipment=bronze_armor_equipment_component, UI=self.ui)
		bronze_armor = objects.Object(player.x + 1, player.y + 1, self.images[16], 'bronze breastplate', item=bronze_armor_item_component)

		crystal_armor_equipment_component = objects.Equipment(slot='breastplate', defence_bonus=50)
		crystal_armor_item_component = objects.Item(use_func=use_functions.equip, name='crystal breastplate', equipment=crystal_armor_equipment_component, UI=self.ui)
		crystal_armor = objects.Object(player.x, player.y + 1, self.images[18], 'crystal breastplate', item=crystal_armor_item_component)

		crown_equipment_component = objects.Equipment(slot='helmet', defence_bonus=2, max_health_bonus=100)
		crown_item_component = objects.Item(use_func=use_functions.equip, name='golden crown of great health', equipment=crown_equipment_component, UI=self.ui)
		crown = objects.Object(player.x + 3, player.y + 1, self.images[20], 'golden crown of great health', item=crown_item_component)


		iron_sword_equipment_component = objects.Equipment(slot='right_hand', power_bonus=10) # for now fixed hand
		iron_sword_item_component = objects.Item(use_func=use_functions.equip, name='iron sword', equipment=iron_sword_equipment_component, UI=self.ui)
		iron_sword = objects.Object(player.x + 1, player.y - 1, self.images[19], 'iron sword', item=iron_sword_item_component)
		great_steel_long_sword_equipment_component = objects.Equipment(slot='left_hand', power_bonus=30)
		great_steel_long_sword_item_component = objects.Item(use_func=use_functions.equip, name='great steel long sword', equipment=great_steel_long_sword_equipment_component, UI=self.ui)
		great_steel_long_sword = objects.Object(player.x + 1, player.y + 2, self.images[22], 'great steel long sword', item=great_steel_long_sword_item_component)


		lantern_equipment_component = objects.Equipment(slot='accessory', charges=700 ,light_radius_bonus=10, activation_func=use_functions.light_lantern, deactivation_string="turns off", wear_off_string="run out of oil")
		lantern_item_component = objects.Item(use_func=use_functions.equip, name='lantern', equipment=lantern_equipment_component, UI=self.ui)
		lantern = objects.Object(player.x + 2, player.y+2, self.images[23], 'lantern', item=lantern_item_component)

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
		self.objects.append(goblin)
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
					item = player.fighter.get(self.objects)
					if item is not None:
						self.ui.add_item_to_UI(item)
						return 'took_turn'
				if event.key == pygame.K_SEMICOLON:
					return 'look'

				if event.key == pygame.K_PERIOD:
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
					player.sended_messages.append("You press your {0} but nothing happens.".format(item.name.title()))

				return 'took_turn'

			else:
				if action.has_key('item_to_drop'):

					item = action['item_to_drop']
					self.pause_menu()
					self.remove_equipment_by_mouse(item)
					player.sended_messages.append("You remove your {0}.".format(item.name.title()))
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
		player.fighter.drop(self.objects, item)


	def remove_equipment_by_mouse(self, item):
		self.ui.remove_item_from_equipment_slot(item)
		item.item.equipment.activated = False
		player.fighter.equipment.remove(item)

	def run(self):
		self.state = 'playing'
		clock = pygame.time.Clock()
		player.sended_messages.append("To exit, press ESC.")
		player.sended_messages.append("For more help press '?'.")
		player.sended_messages.append("You descend into your own basement.")
		self.listen_for_messagess(player)
		noises = None

		turn = 'player_turn'

		while self.state == 'playing':
			clock.tick(60)
			scr.fill(BLACK)
			screen_to_draw = 'game_screen'

			if self.state == 'playing':

				if turn == 'player_turn':

					player.hearing_map['noise_maps'] = list()
					player.hearing_map['sources'] = list()
					player.hearing_map['sounds'] = list()

					# make it into a function | use_ears()
					for obj in self.objects:
						if obj != player:
							if obj.noise_map['noise_map'] != '':
								player.hearing_map['noise_maps'].append(obj.noise_map['noise_map'])

							if obj.noise_map['source'] != '':
								player.hearing_map['sources'].append(obj.noise_map['source'])

							if obj.noise_map['sound'] != '':
								player.hearing_map['sounds'].append(obj.noise_map['sound'])

					player_action = self.handle_keys()
					mouse_action = self.handle_mouse()

					noises = objects.player_listen_to_noise(player)

					#print noises

					if player_action == 'look':
						noises = objects.player_listen_to_noise(player)
						target = self.enter_look_mode("Look at what?", got_noise=noises)
						if target is not None:
							self.ui.draw_info_window(target, scr)

					self.state = self.check_for_player_death()

					if player_action == 'took_turn' or mouse_action == 'took_turn':

						objects.player_hurt_or_heal_knees(player, self.map)

						x = player.noise_map.get('noise_map')

						try:
							if x is not None:
								for key in x.keys():
									_x = key[0] * constants.TILE_SIZE
									_y = key[1] * constants.TILE_SIZE
									scr.blit(self.images[0], (_x, _y))
								pygame.display.flip()
						except AttributeError:
							pass

						self.listen_for_messagess(player)
						turn = 'monster_turn'

						# add manage_player function, where there will be all this everything that is done with player, and recovering knee health.

				if turn == 'monster_turn':
					#magic_bell.make_noise(self.map, 10, 10, 10, 'Ding', 'Bell makes a fucking noise')
					#second_magic_bell.make_noise(self.map, 3, 10, 10, 'Ding', 'Bell makes a fucking noise')
					for obj in self.objects:

						self.check_for_death(obj)

						if obj.fighter:
							obj.fighter.manage_equipment()
		
						if obj.ai:
							obj.ai.noise_map = player.noise_map

							obj.clear_messages() # clear messages - any previous messages are not up to date
							obj.ai.take_turn(_map=self.map, fov_map=obj.fov_map, objects=self.objects, player=player)
		
							self.listen_for_messagess(obj)

					player.hearing_map = {}
					player.noise_map = {}

					turn = 'player_turn'

				self.draw_all()
				if noises: # move that to draw_all
						# display "!"
					self.ui.draw_noise_indicators(noises, self.fov_map)

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
				if field_of_view.is_in_fov(self.fov_map, obj):
					obj.draw(scr)

		for obj in self.objects:
			if obj.fighter is not None and obj.name != 'player':
				if field_of_view.is_in_fov(self.fov_map, obj):
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
			self.messages.extend(obj.sended_messages)
			self.messages_history.extend(obj.sended_messages)
		else:
			to_delete = abs(len(self.messages) - 5)
			del self.messages[:to_delete]
			self.messages.extend(obj.sended_messages)			

	def print_messages(self):
		y = constants.SCREEN_SIZE_HEIGHT - 2
		_y = y * constants.FONT_SIZE

		for message in reversed(self.messages): # last ones are the latest
			message_to_blit = font.render(message, False, WHITE)
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


	def enter_look_mode(self, title, **kwargs):

		action = None

		look_text = font.render(title, False, WHITE)

		noise = kwargs.get('got_noise')

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
							if (obj.x, obj.y) == (x, y) and (obj.fighter or obj.item) and self.fov_map[obj.x][obj.y] == 1:
								return obj

							if (obj.x, obj.y) == (x, y) and (obj.fighter or obj.item) and self.fov_map[obj.x][obj.y] != 1 and noise is not None: # sound
								sound = {'sound': noise, 'key': (x, y)}
								player.player_hear_sound(sound)
								self.listen_for_messagess(player)
						return None

			self.draw_all()
			self.draw_bresenham_line(player.x, player.y, x, y)
			self.print_messages()
			scr.blit(look_text, (0, 0))
			if noise is not None:
				self.ui.draw_noise_indicators(noise, self.fov_map)
			pygame.display.flip()

	def draw_bresenham_line(self, x0, y0, x1, y1):
	    "Bresenham's line algorithm - taken from: https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python"
	
	    line_img = font.render("*", False, WHITE)
	
	    dx = abs(x1 - x0)
	    dy = abs(y1 - y0)
	    x, y = x0, y0
	    sx = -1 if x0 > x1 else 1
	    sy = -1 if y0 > y1 else 1
	
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


class UI(object):
	# this class is responsible for drawing the inventory, drawing noise level, noise indicators and various windows
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
		l_hand = self.equipment_places['left_hand']
		r_hand = self.equipment_places['right_hand']
		l_foot = self.equipment_places['left_foot']
		r_foot = self.equipment_places['right_foot']
		l_ring = self.equipment_places['left_ring']
		r_ring = self.equipment_places['right_ring']
		amulet = self.equipment_places['amulet']
		accessory = self.equipment_places['accessory']

		items = [helmet, breastplate, l_hand, r_hand, l_foot, r_foot, l_ring, r_ring, amulet, accessory]

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


		health_BAD_rect = pygame.Rect((constants.START_INFORMATION_BOX_X + 4.3) * constants.TILE_SIZE, ((constants.START_INFORMATION_BOX_Y + 12.3) * constants.TILE_SIZE), 10 * 10, 8)
		health_GOOD_rect = pygame.Rect((constants.START_INFORMATION_BOX_X + 4.3) * constants.TILE_SIZE, ((constants.START_INFORMATION_BOX_Y + 12.3) * constants.TILE_SIZE), knee_health_to_display * 10, 8)
		scr.fill(RED, rect=health_BAD_rect)
		scr.fill(GREEN, rect=health_GOOD_rect)

		scr.blit(knees_to_blit, (((constants.START_INFORMATION_BOX_X + 1) * constants.TILE_SIZE, (constants.START_INFORMATION_BOX_Y + 12) * constants.TILE_SIZE)))

	def draw_noise_indicators(self, noises, fov):

		sources = noises[0]

		try:

			for noise in sources:

				icon = self.images[27]
				x = noise[0]
				y = noise[1]

				if fov[noise[0]][noise[1]] != 1:
					scr.blit(icon, (x * constants.TILE_SIZE, y * constants.TILE_SIZE))

		except IndexError:
			pass

class Level(object):
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
# Using items and examining them via keyboard. - a new menu that is ordered by alphabet. -> not needed now

# Step 2: - Core mechanics that will seperate my game from others
# Lantern v and torches - increasing fov v refilling v - lantern is given at the beginning with one extra oil, and no lantern is spawned during the game
# Lantern makes player more visible. <- Very important
# Objects that emit light. - they will augment the vision when seen
# Optimise code - make functions more general, input processing etc... and then: (the most important change i could add from that point is event queue - decide what is done in what order)
# Noise AI - possible need for an A* algorithm DONE
# Making noise, noise mechanic - either by shouting, tumbling over or throwing
# Smoke - a place that blocks sight but not movement
# Walking carefully - sneaking (crouching) Done, know I need to make the player scream if he crouches for too long. ("Pysio's legs hurt!")
# If monster is making noise detectable to player, blit an quesiton mark in the position he did the noise for a couple of turns DONE <- noise can be heard multiple times
# Noise (done by player) represented by exclamation marks : [!!!!!!!!!!!!] (Range, and with colors: level) (Level indicates how piercing through the walls it is, how many walls can it pierce till it fades)
# Monster's vision. DONE
# Below 25 level of depth, abhorrent creatures will spawn and it will be necessary to crouch and sneak.
# To show what player has already explored, make new item called magic map, that will be taking notes automatically

# After step 2 demo

# Step 3: - Polishing and roguelike elements such as permadeath, levels as well as menu etc.
# Spawning player randomly, in way which he does not spawn in walls
# Spawning enemies randomly, in way which they do not spawn in walls
# Identifying! - Aside from healing potion - this will be recognizable by player from the beginning, because he will receive 1 from mage.
# Help in game - "?"
# Artifact items!
# Smith from Metin2 - only way to upgrade, beside finding some magic thing - BUT! it costs a lot of money, and if it goes bad - the item is destroyed.
# Descending, loading maps, saving etc.
# Magic, spellbooks and spell menu.
# Endgame - [?] and intro text
# Main menu


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

# Make the object that has the ai have its own fov map - it's not good that it works in ways of "If you can see me, I can see you", because it subtracts the tactical possibility of hiding, while still seing other object etc. DONE
# Another problem that this creates, is that when I will be going to implement lighting, and objects that create light (augment the fov when they're in my fov), simply augment the vision of enemies!
# Abhorrent creatures are pretty much blind - they can see only for one tile (other than themselves) - but they have excellent hearing
# Mage will tell in the beginning that the casting unleashed creatures that have weak sight.

# Maybe movable camera? although it is very hard it will certainly add more mystery and difficulty.
# HP does not regenerate but you can throw rocks to kill enemies.

# Make enemies that drop special items and special branches! for example: portal to the shadow realm with monster that drops scroll that can stun evil demons for 10 rounds.
# And with all that, keep the mystery and narrative theme going on. (Not shadow realm, but "you step into the portal, swirling and shaking you transmigrate beyond the realms of worlds!")

# Noise AI (Mechanic: the lower (lvl) the noise detected, the better the hearing is):
# 1. Monster has it's own fov map and Level Of Hearing, that is: WHICH LEVEL of noise monster can detect. (If it has good hearing, he can detect low levels of noise) done
# 2. The object that emits sound has: Max level of sound that can be created and range of that sound. done
# 3. Each turn, surrounding can make noise and it uses the same algorithm that fov does. done
# 4. Each noise type has to have an indicator, that shows how quickly the noise fades. done
# 5. If player makes noise that monster can hear, he gets message "something growls!" (Player gets a notification only if he hears the sound)
# 6. Sneaking is a good option, but it hurts your ankles. (If used too much, player will scream)
# 7. Sound is made: "fov" of sound traverses with it's own properties, hitting walls, fades etc.: Hits monster that can hear it: Monster goes to sound source. done

# Ok, now we have to create another creature on which we will test this. done

# After Noise, now add unique noise names for the creature - that way the player will be able to learn what monster makes what noises v - and then sneaking, knee health.
# AND: don't show the noise in the message log - when player will be hearing many monsters, it will clog it, instead make so, that when player "looks" at noise indicator, it shows the noise name e.g - "it growls".
# And after that, it's time for light sources!