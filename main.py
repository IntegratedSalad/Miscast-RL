#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random
import constants
import field_of_view
import objects
import utils
import use_functions
from spritesheet import Spritesheet
from map_utils import Tile
from map_utils import CA_CaveFactory as CA_map

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (219, 0, 0)

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

		player_IMG = characters_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		wall_IMG = walls_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE))
		floor_IMG = pygame.image.load("tiles/floor.png")
		empty_spaceIMG = walls_SPRITES.image_at((0, constants.TILE_SIZE * 2, constants.TILE_SIZE, constants.TILE_SIZE))
		worm_IMG = enemies_pests_SPRITES.image_at((7 * constants.TILE_SIZE, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 22 12
		abhorrent_creature_IMG = misc_enemies_SPRITES.image_at((0, 5 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 28 27
		corpse_IMG = corpses_SPRITES.image_at((4 * constants.TILE_SIZE, 2 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)

		hp_potion_IMG = potions_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		scroll_of_death_IMG = scrolls_SPRITES.image_at((5 * constants.TILE_SIZE, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)

		ui_MESSAGE_HORIZONTAL = ui_SPRITES.image_at((constants.TILE_SIZE, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_LEFT = ui_SPRITES.image_at((0, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_LEFT = ui_SPRITES.image_at((0, constants.TILE_SIZE * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_RIGHT = ui_SPRITES.image_at((2 * constants.TILE_SIZE, constants.TILE_SIZE * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_RIGHT = ui_SPRITES.image_at((2 * constants.TILE_SIZE, constants.TILE_SIZE * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_VERTICAL = ui_SPRITES.image_at((0, 4 * constants.TILE_SIZE, constants.TILE_SIZE, constants.TILE_SIZE))

		return [player_IMG, wall_IMG, floor_IMG, empty_spaceIMG, worm_IMG, abhorrent_creature_IMG, corpse_IMG,
				ui_MESSAGE_HORIZONTAL, ui_MESSAGE_TOP_LEFT, ui_MESSAGE_BOTTOM_LEFT, ui_MESSAGE_TOP_RIGHT, ui_MESSAGE_BOTTOM_RIGHT, ui_MESSAGE_VERTICAL, hp_potion_IMG, scroll_of_death_IMG]

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
		font = pygame.font.Font("Px437_IBM_VGA8.ttf", constants.FONT_SIZE)
		subscript_font = pygame.font.Font("Px437_IBM_VGA8.ttf", 8) # font will be used to tell how many of exact items are in the inventory
		scr = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
		pygame.display.set_caption("RL")

		self.images = self.get_images()

		player_fighter_component = objects.Fighter(20, 4)
		player = objects.Object(1, 6, self.images[0], 'player', blocks=True, fighter=player_fighter_component)

		worm_AI = objects.SimpleAI()
		worm_fighter_component = objects.Fighter(2, 2)
		worm = objects.Object(1, 7, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component)

		# for variety only, demo implementation
		for n in range(constants.MAX_ENEMIES + 20):
			mon_x = random.randint(1, constants.MAP_WIDTH - 1)
			mon_y = random.randint(1, constants.MAP_HEIGHT - 1)
			if self.map[mon_x][mon_y].block_sight or (mon_x, mon_y) == (player.x, player.y):  
				continue
			else:
				worm_AI = objects.SimpleAI()
				worm_fighter_component = objects.Fighter(2, 1)
				worm = objects.Object(mon_x, mon_y, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component) # 2 7
				#worm = objects.Object(2, 7, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component) # 2 7
				self.objects.append(worm)
 
 		abhorrent_creature_AI = objects.SimpleAI()
 		abhorrent_creature_fighter_component = objects.Fighter(constants.ABHORRENT_CREATURE_MAX_HP, 100, area_of_hearing=15)
		abhorrent_creature = objects.Object(28, 27, self.images[5], 'Abhorrent Creature', blocks=True, block_sight=True, fighter=abhorrent_creature_fighter_component, ai=abhorrent_creature_AI)


		for n in range(100):
			rand_x = random.randrange(constants.MAP_WIDTH)
			rand_y = random.randrange(constants.MAP_HEIGHT)

			if not self.map[rand_x][rand_y].block_sight:
				hp_potion_item_component = objects.Item(use_func=use_functions.heal, can_break=True, value_of=5)
				hp_potion = objects.Object(player.x + 1, player.y, self.images[constants.IMAGES_POTION_HP], 'healing potion', item=hp_potion_item_component)
				self.objects.append(hp_potion)

		scroll_of_death_item_component = objects.Item(10, use_func=use_functions.instant_death, targetable=True)
		scroll_of_death = objects.Object(player.x + 2, player.y, self.images[constants.IMAGES_SCROLL_OF_DEATH], 'scroll of death', item=scroll_of_death_item_component)

		self.objects.append(player)
		#self.objects.append(hp_potion)
		#self.objects.append(worm)
		self.objects.append(abhorrent_creature)
		self.objects.append(scroll_of_death)

		self.fov_map = field_of_view.set_fov(self.fov_map)
		field_of_view.cast_rays(player.x, player.y, self.fov_map, self.map)
		self.ui = UI(player.fighter, self.images, 'game_screen')

	def handle_keys(self):

		# change this to an action, for instance "up" can progress player along y axis and can scroll menus or move line of sight upwards

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_l:
					player.move(1, 0, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_h:
					player.move(-1, 0, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_k:
					player.move(0, -1, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_j:
					player.move(0, 1, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_y:
					player.move(-1, -1, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_u:
					player.move(1, -1, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_n:
					player.move(1, 1, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_b:
					player.move(-1, 1, self.map, self.fov_map, self.objects)
					return 'move'
				if event.key == pygame.K_g:
					item = player.fighter.get(self.objects)
					if item is not None:
						self.ui.add_item_to_UI(item)
						return 'move'
				if event.key == pygame.K_SEMICOLON:
					return 'look'

		return 'idle'


	def handle_mouse(self):
		m_x, m_y = pygame.mouse.get_pos()

		r_click = pygame.mouse.get_pressed()[2]
		l_click = pygame.mouse.get_pressed()[0]

		# make it more general

		if l_click == 1:
			# if mouse pos is in inventory
			for item in player.fighter.inventory:

				to_check = pygame.Rect(item.x * constants.FONT_SIZE, item.y * constants.FONT_SIZE, constants.FONT_SIZE, constants.FONT_SIZE)
				# it creates rect that bounds item on the screen

				if to_check.collidepoint(m_x, m_y):
					if item.item.use_func is not None:
						if not item.item.targetable:
							item.item.use(target=player)
						else:
							target = self.enter_look_mode("Target what?")
							for obj in self.objects:
								if (obj.x, obj.y) == target:
									item.item.use(target=obj, user=player)
						self.ui.remove_item_from_UI(item.x, item.y)
					return 'used_item'

		if r_click == 1:
			for item in player.fighter.inventory:
				to_check = pygame.Rect(item.x * constants.FONT_SIZE, item.y * constants.FONT_SIZE, constants.FONT_SIZE, constants.FONT_SIZE)


				if to_check.collidepoint(m_x, m_y):
					self.ui.remove_item_from_UI(item.x, item.y)
					player.fighter.drop(self.objects, item)
					return 'dropped_item'


		if self.ui.inventory_rect.collidepoint(m_x, m_y):


			for item in player.fighter.inventory:
				to_check = pygame.Rect(item.x * constants.FONT_SIZE, item.y * constants.FONT_SIZE, constants.FONT_SIZE, constants.FONT_SIZE)

				if to_check.collidepoint(m_x, m_y):
					to_blit = font.render(item.name, True, WHITE)
					return ('blit', to_blit)

		return 'idle'


	def run(self):
		self.state = 'playing'
		clock = pygame.time.Clock()

		player.sended_messages.append("You descend into your own basement.")
		self.listen_for_messagess(player)

		while self.state == 'playing':
			clock.tick(60)
			player_action = self.handle_keys()
			mouse_action = self.handle_mouse()
			listened = False

			# process input - make so, that the keys are universal for all the windows, but they do something different for all of them
			
			scr.fill(BLACK)

			# here will be the state, game or menu(description etc)

			print int(clock.get_fps())

			if player_action == 'look':
				self.enter_look_mode("Look at what?")
				# process request

			if player_action == 'move' or (mouse_action != 'idle' and mouse_action != 'dropped_item' and mouse_action[0] != 'blit'):

				screen_to_draw = 'game_screen'

				for obj in self.objects:

					self.check_for_death(obj)

					if obj.ai:
						obj.clear_messages() # clear messages - any previous messages are not up to date
						obj.ai.take_turn(_map=self.map, fov_map=self.fov_map, objects=self.objects, player=player)

					self.listen_for_messagess(obj)
					listened = True

			if mouse_action in ['used_item', 'dropped_item']:
				# sort inventory and pause game
				if not listened:
					self.listen_for_messagess(player)
				self.print_messages()
				self.pause_menu()

			else:
				self.print_messages()

			self.state = self.check_for_player_death()
			self.draw_all()

			if mouse_action[0] == 'blit':
				scr.blit(mouse_action[1], (0, (constants.START_MESSAGE_BOX_Y * constants.FONT_SIZE) - constants.FONT_SIZE))

			pygame.display.flip()

		while self.state == 'game_over':
			self.show_game_over_demo()

	def draw_all(self):

		# self.ui.draw_current_view

		if self.ui.current_view == 'game_screen' or 'inventory_screen':

			field_of_view.fov_recalculate(self.fov_map, player.x, player.y, self.map)

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

		self.ui.draw(scr)
		self.draw_objects()
		player.draw(scr)
		player.clear_messages() # we clear his messages after we process them, that is we cannot do that in run method

	def draw_objects(self):

		for obj in self.objects:

			if obj.block_sight:
				self.map[obj.x][obj.y].block_sight = True

			if field_of_view.is_in_fov(self.fov_map, obj) and obj.name != 'player':
				# change the priority
				obj.draw(scr)

			# here, we will clear all their messages
			obj.clear_messages() # clear messages - any previous messages are not up to date

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
		if obj.fighter is not None and obj.name != 'player':
			if obj.fighter.hp <= 0:
				obj.fighter.kill(self.fov_map, player.x, player.y, self.map, self.images)

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

		scr.fill(BLACK)

		self.draw_all()
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
			message_to_blit = font.render(message, True, WHITE)
			scr.blit(message_to_blit, (16, _y))
			_y -= constants.FONT_SIZE

	def use_item_by_mouse(self, m_x, m_y, l_click, r_click):

		if l_click == 1:
			pass

	def pause_menu(self):
		# used to prevent player from activating bunch of items at once

		unpause = False

		more_text = font.render("More... (hit enter)", True, WHITE)

		while not unpause:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						unpause = True


			self.draw_all()
			scr.blit(more_text, (0, 0))
			pygame.display.flip()

	def enter_look_mode(self, title):

		action = None

		look_text = font.render(title, True, WHITE)

		x = player.x
		y = player.y

		line_to_blit = font.render("*", True, WHITE)

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
						action = 'return'
						return (x, y)
						# here will be action

			self.draw_all()
			self.draw_bresenham_line(player.x, player.y, x, y)
			self.print_messages()
			scr.blit(look_text, (0, 0))
			pygame.display.flip()

	def draw_bresenham_line(self, x0, y0, x1, y1):
	    "Bresenham's line algorithm - taken from: https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python"
	
	    line_img = font.render("*", True, WHITE)
	
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
	# this class will be responsible for drawing the inventory, stacking the items and showing the amount of stacked items, drawing noise level and various windows
	def __init__(self, player, images, current_view):
		self.images = images
		self.current_view = current_view
		self.inv_start_pos_x = constants.INVENTORY_ITEMS_START_X * constants.FONT_SIZE
		self.inv_start_pos_y = constants.INVENTORY_ITEMS_START_Y * constants.FONT_SIZE

		self.x_cord = constants.INVENTORY_ITEMS_START_X
		self.y_cord = constants.INVENTORY_ITEMS_START_Y

		self.x_width = 0

		self.inventory_places = [[y, x, None] for y in range(constants.INVENTORY_ITEMS_START_Y, constants.INVENTORY_HEIGHT + constants.INVENTORY_ITEMS_START_Y) 
											  for x in range(constants.INVENTORY_ITEMS_START_X, constants.INVENTORY_WIDTH + constants.INVENTORY_ITEMS_START_X)]

		self.inventory_rect = pygame.Rect(constants.INVENTORY_ITEMS_START_X * constants.FONT_SIZE, constants.INVENTORY_ITEMS_START_Y * constants.FONT_SIZE,
										  constants.INVENTORY_WIDTH * constants.FONT_SIZE, constants.INVENTORY_HEIGHT * constants.FONT_SIZE)

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

		# add contents here
		# draw name of the rect in the middle of upper part of the rect

	def draw(self, scr):
		messages_IMAGES = [self.images[8], self.images[9], self.images[10], self.images[11], self.images[7], self.images[12]]
		information_IMAGES  = messages_IMAGES

		self.draw_rect(constants.START_MESSAGE_BOX_X, constants.START_MESSAGE_BOX_Y, 30, 7, messages_IMAGES, scr, 'MESSAGES')
		self.draw_rect(constants.START_INFORMATION_BOX_X, constants.START_INFORMATION_BOX_Y, 12, 20, messages_IMAGES, scr, player.name.upper())
		self.draw_rect(constants.INVENTORY_BOX_X, constants.INVENTORY_BOX_Y, 12, 17, messages_IMAGES, scr)
		self.draw_inventory(scr)

		hp_to_blit = font.render("HP: {0} / {1}".format(player.fighter.hp, player.fighter.max_hp), True, RED)

		scr.blit(hp_to_blit, (31 * constants.FONT_SIZE, 16))


	def draw_inventory(self, scr): # change that
		for item in player.fighter.inventory:

			_x = item.x * constants.FONT_SIZE
			_y = item.y * constants.FONT_SIZE

			scr.blit(item.img, (_x, _y))


	def add_item_to_UI(self, item, slot='inventory'):
		# checks how many items there is, basicly it changes the item x and y so that it goes to the inventory area

		x = 1
		y = 0
		slot = 2

		for place in self.inventory_places:
			if place[slot] is None:
				item.x = place[x]
				item.y = place[y]
				place[slot] = item
				break

	def remove_item_from_UI(self, item_x, item_y, slot='inventory'):

		# sort inventory - goes through all items and sets them again

		x = 1
		y = 0
		slot = 2

		for place in self.inventory_places:
			if place[x] == item_x and place[y] == item_y:
				place[slot] = None
				print place
				break

	def draw_info(self, object):

		# General description about any object
		# If fighter - draw additional info

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
# Moving player v 
# Items - scrolls v and potions v, equipment - sword, equipment slots
# Inventory v
# line of sight - to targeting v, description menu
# names of items after hovering over them v
# lantern and torches - use from the inventory - increasing fov
# Optimise code - make functions more general, input processing etc... and then:
# Spawning player randomly, in way that he does not spawn in walls
# Spawning enemies randomly, in way that they do not spawn in walls
# Noise AI

