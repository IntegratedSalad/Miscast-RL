import pygame
import random
import constants
import field_of_view
import objects
import utils
from spritesheet import Spritesheet
from map_utils import Tile
from map_utils import CA_CaveFactory as CA_map

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game(object):

	def __init__(self, state=None):
		self.state = state
		self.current_raw_map = self.take_raw_map()
		self.map = self.set_map()
		self.images = []
		self.objects = []
		self.fov_map = []
		self.messages_history = []

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

		player_IMG = characters_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		wall_IMG = walls_SPRITES.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE))
		floor_IMG = pygame.image.load("tiles/floor.png")
		empty_spaceIMG = walls_SPRITES.image_at((0, 16 * 2, constants.TILE_SIZE, constants.TILE_SIZE))
		worm_IMG = enemies_pests_SPRITES.image_at((7 * 16, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 22 12
		abhorrent_creature_IMG = misc_enemies_SPRITES.image_at((0, 5*16, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 28 27
		corpse_IMG = corpses_SPRITES.image_at((4 * 16, 2 * 16, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)


		ui_MESSAGE_HORIZONTAL = ui_SPRITES.image_at((16, 16 * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_LEFT = ui_SPRITES.image_at((0, 16 * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_LEFT = ui_SPRITES.image_at((0, 16 * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_TOP_RIGHT = ui_SPRITES.image_at((2 * 16, 16 * 3, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_BOTTOM_RIGHT = ui_SPRITES.image_at((2 * 16, 16 * 5, constants.TILE_SIZE, constants.TILE_SIZE))
		ui_MESSAGE_VERTICAL = ui_SPRITES.image_at((0, 4 * 16, constants.TILE_SIZE, constants.TILE_SIZE))

		return [player_IMG, wall_IMG, floor_IMG, empty_spaceIMG, worm_IMG, abhorrent_creature_IMG, corpse_IMG,
				ui_MESSAGE_HORIZONTAL, ui_MESSAGE_TOP_LEFT, ui_MESSAGE_BOTTOM_LEFT, ui_MESSAGE_TOP_RIGHT, ui_MESSAGE_BOTTOM_RIGHT, ui_MESSAGE_VERTICAL]

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
		font = pygame.font.Font("SDS_6x6.ttf", constants.FONT_SIZE)
		scr = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
		pygame.display.set_caption("RL")

		self.images = self.get_images()

		player_fighter_component = objects.Fighter(20, 4)
		player = objects.Object(1, 6, self.images[0], 'player', blocks=True, fighter=player_fighter_component)

		for n in range(constants.MAX_ENEMIES + 10):
	
			mon_x = random.randint(1, constants.MAP_WIDTH - 1)
			mon_y = random.randint(1, constants.MAP_HEIGHT - 1)

			if self.map[mon_x][mon_y].block_sight or (mon_x, mon_y) == (player.x, player.y):  
				continue
			else:
				worm_AI = objects.SimpleAI()
				worm_fighter_component = objects.Fighter(2, 1)
				worm = objects.Object(mon_x, mon_y, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component) # 2 7
				#worm = objects.Object(22, 12, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component) # 2 7
				self.objects.append(worm)
 
 		abhorrent_creature_AI = objects.SimpleAI()
 		abhorrent_creature_fighter_component = objects.Fighter(100, 100, area_of_hearing=15)
		abhorrent_creature = objects.Object(28, 27, self.images[5], 'Abhorrent Creature', blocks=True, block_sight=True, fighter=abhorrent_creature_fighter_component, ai=abhorrent_creature_AI)

		self.objects.append(player)
		self.objects.append(worm)
		self.objects.append(abhorrent_creature)

		self.fov_map = field_of_view.set_fov(self.fov_map)
		field_of_view.cast_rays(player.x, player.y, self.fov_map, self.map)

	def handle_keys(self):
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

		return 'idle'


	def run(self):
		self.state = 'playing'
		clock = pygame.time.Clock()

		while self.state == 'playing':
			clock.tick(60)
			player_action = self.handle_keys()
			
			scr.fill(BLACK)

			print int(clock.get_fps())

			if player_action == 'move':
				# ai take turn
				for obj in self.objects:
					if obj.ai:
						#obj.clear(obj.x, obj.y, self.map)
						obj.ai.take_turn(_map=self.map, fov_map=self.fov_map, objects=self.objects, player=player)
			
			# check for death
			to_kill = self.check_for_death()
			if to_kill is not None:
				self.kill_obj(to_kill)


			self.listen_for_messagess()
			field_of_view.fov_recalculate(self.fov_map, player.x, player.y, self.map)
			self.draw_all()
			pygame.display.flip()

		while self.state == 'game_over':
			self.show_game_over_demo()


	def draw_all(self):

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


		self.draw_UI()
		self.draw_objects()
		player.draw(scr)

	def draw_objects(self):
		for obj in self.objects:
			if obj.block_sight:
				self.map[obj.x][obj.y].block_sight = True
			if field_of_view.is_in_fov(self.fov_map, obj) and obj.name != 'player':
				obj.draw(scr)

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


	def check_for_death(self):
		for obj in self.objects:
			if obj.fighter is not None:
				entity = obj
				if entity.fighter.hp <= 0:
					return entity


	def kill_obj(self, obj):
		obj.ai = None
		obj.fighter = None
		obj.block_sight = False
		obj.blocks = False
		obj.img = self.images[6] # instead, use specific image for every character and corpse stats overall
		obj.clear(obj.x, obj.y, self.map)
		field_of_view.fov_recalculate(self.fov_map, player.x, player.y, self.map)
		print obj.name.capitalize() + " is dead"
		if obj.name == 'player': 
			self.state = 'game_over'
			print "You died!"


	def show_game_over_demo(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)

		scr.fill(WHITE)

		for x in range(0, 30):
			for y in range(0, 30):
				_x = x * constants.TILE_SIZE
				_y = y * constants.TILE_SIZE
				if self.map[x][y].block_sight and self.map[x][y].is_map_structure:
					scr.blit(self.images[1], (_x, _y))
				else:
					scr.blit(self.images[2], (_x, _y))
		for obj in self.objects:
			obj.draw(scr)

		pygame.display.flip()


	def listen_for_messagess(self):

		y = constants.SCREEN_SIZE_HEIGHT - 2

		messages = []

		for obj in self.objects:
			if len(messages) <= 5:
				print 'd'
				messages.extend(obj.sended_messages)
			else:
				messages.pop(-1)
				self.messages_history.extend(messages)

		_y = y * constants.FONT_SIZE

		for message in messages:
			message_to_blit = font.render(message, True, WHITE)
			scr.blit(message_to_blit, (16, _y))
			_y -= constants.FONT_SIZE


	def draw_rect(self, start_x, start_y, width, height, border_tiles):
		# border tiles is a list with 5 tiles - basic and four corners

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



	def draw_UI(self):

		messages_IMAGES = [self.images[8], self.images[9], self.images[10], self.images[11], self.images[7], self.images[12]]
		information_IMAGES  = messages_IMAGES

		self.draw_rect(constants.START_MESSAGE_BOX_X, constants.START_MESSAGE_BOX_Y, 30, 7, messages_IMAGES)
		self.draw_rect(constants.START_INFORMATION_BOX_X, constants.START_INFORMATION_BOX_Y, 12, 20, messages_IMAGES)
		self.draw_rect(constants.START_INFORMATION_BOX_X, constants.START_INFORMATION_BOX_Y + 20, 12, 17, messages_IMAGES)
		

def main():
	game = Game()
	game.init_pygame()
	game.run()

if __name__ == '__main__':
	main()

# Goals:
# Moving player
# Spawning player randomly, in way that he does not spawn in walls
# Moving enemy
# Spawning enemies randomly, in way that he does not spawn in walls
# Items
