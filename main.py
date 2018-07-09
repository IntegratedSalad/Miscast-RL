import pygame
import random
import constants
from spritesheet import Spritesheet
from map_utils import Tile
from map_utils import CA_CaveFactory as CA_map
from objects import Object

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game(object):
	def __init__(self, state=None):
		self.state = state
		self.current_raw_map = self.take_raw_map()
		self.map = self.set_map()
		self.images = []
		self.objects = []

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

		# move it to constants

		characters = Spritesheet("tiles/Player0.png")
		walls = Spritesheet("tiles/Tile.png")

		player_IMG = characters.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		wall_IMG = walls.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE))

		floor_IMG = pygame.image.load("tiles/floor.png")

		return [player_IMG, wall_IMG, floor_IMG]

	def set_map(self):

		final_map = [[Tile(True,True) for x in range(constants.MAP_WIDTH)] for y in range(constants.MAP_HEIGHT)]

		for x in range(0, 30):
			for y in range(0, 30):
				if self.current_raw_map[x][y] == '.':
					final_map[x][y] = Tile(False, False)

		return final_map

	def init_pygame(self):
		global scr, player

		pygame.init()
		pygame.font.init()
		scr = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_WIDTH))
		pygame.display.set_caption("RL")

		self.images = self.get_images()
		player = Object(1, 6, self.images[0], 'player')

		self.objects.append(player)

	def handle_keys(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_l:
					player.move(1, 0, self.map)
				if event.key == pygame.K_h:
					player.move(-1, 0, self.map)
				if event.key == pygame.K_k:
					player.move(0, -1, self.map)
				if event.key == pygame.K_j:
					player.move(0, 1, self.map)
				if event.key == pygame.K_y:
					player.move(-1, -1, self.map)
				if event.key == pygame.K_u:
					player.move(1, -1, self.map)
				if event.key == pygame.K_n:
					player.move(1, 1, self.map)
				if event.key == pygame.K_b:
					player.move(-1, 1, self.map)


	def run(self):
		self.state = 'playing'

		while self.state == 'playing':

			self.handle_keys()
			scr.fill(WHITE)
			self.draw_all()

			pygame.display.flip()


	def draw_all(self):

		self.clear_objects()

		for x in range(0, 30):
			for y in range(0, 30):
				_x = x * constants.TILE_SIZE
				_y = y * constants.TILE_SIZE
				if self.map[x][y].block_movement:
					scr.blit(self.images[1], (_x, _y))
				else:
					scr.blit(self.images[2], (_x, _y))

		for obj in self.objects:
			obj.draw(scr)

	def clear_objects(self):
		for obj in self.objects:
			obj.clear(self.images[2], scr)

	def spawn_objects(self):

		# first player
		# stairs
		# secondly objects
		# thirdly monsters

		while True:

			# get random number
			# check if it's not wall
			# place
			pass


game = Game()
game.init_pygame()
game.run()

# Goals:
# Moving player
# Spawning player randomly, in way that he does not spawn in walls
# Moving enemy
# Spawning enemies randomly, in way that he does not spawn in walls
# 
