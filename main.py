import pygame
import random
import constants
import field_of_view
from spritesheet import Spritesheet
from map_utils import Tile
from map_utils import CA_CaveFactory as CA_map
import objects

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
		enemies_pests = Spritesheet("tiles/Pest0.png")
		misc_enemies = Spritesheet("tiles/Misc0.png")

		player_IMG = characters.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1)
		wall_IMG = walls.image_at((0, 0, constants.TILE_SIZE, constants.TILE_SIZE))
		floor_IMG = pygame.image.load("tiles/floor.png")
		empty_spaceIMG = walls.image_at((0, 16 * 2, constants.TILE_SIZE, constants.TILE_SIZE))
		worm_IMG = enemies_pests.image_at((7 * 16, 0, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 22 12
		abhorrent_creature_IMG = misc_enemies.image_at((0, 5*16, constants.TILE_SIZE, constants.TILE_SIZE), colorkey=-1) # 28 27

		return [player_IMG, wall_IMG, floor_IMG, empty_spaceIMG, worm_IMG, abhorrent_creature_IMG]

	def set_map(self):

		final_map = [[Tile(True, block_sight=True, is_map_structure = True) for x in range(constants.MAP_WIDTH)] for y in range(constants.MAP_HEIGHT)]

		for x in range(0, 30):
			for y in range(0, 30):
				if self.current_raw_map[x][y] == '.':
					final_map[x][y] = Tile(block_movement=False, block_sight=False)

		return final_map

	def init_pygame(self):
		global scr, player

		pygame.init()
		pygame.font.init()
		scr = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_WIDTH))
		pygame.display.set_caption("RL")

		self.images = self.get_images()

		player_fighter_component = objects.Fighter(10, 2)

		player = objects.Object(1, 6, self.images[0], 'player', blocks=True, fighter=player_fighter_component)

		worm_AI = objects.SimpleAI()
		worm_fighter_component = objects.Fighter(2, 1)
		worm = objects.Object(22, 12, self.images[4], 'worm', blocks=True, block_sight=True, ai=worm_AI, fighter=worm_fighter_component) # 2 7
 
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
			
			scr.fill(WHITE)

			#print int(clock.get_fps())

			if player_action == 'move':
				print player.x, player.y
				# ai take turn
				for obj in self.objects:
					if obj.ai:
						#obj.clear(obj.x, obj.y, self.map)
						obj.ai.take_turn(_map=self.map, fov_map=self.fov_map, objects=self.objects, player=player)
			
			field_of_view.fov_recalculate(self.fov_map, player.x, player.y, self.map)
			self.draw_all()
			pygame.display.flip()


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

		self.draw_objects()

	def draw_objects(self):
		for obj in self.objects:
			if obj.block_sight:
				self.map[obj.x][obj.y].block_sight = True
			if field_of_view.is_in_fov(self.fov_map, obj):
				obj.draw(scr)

	def spawn_objects(self):

		# first player
		# stairs
		# secondly objects
		# thirdly monsters

		while True:

			# get a random number
			# check if it's not wall
			# place
			pass

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
