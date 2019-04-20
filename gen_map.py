from map_utils import Tile
from map_utils import CA_CaveFactory as CA_map
import constants



def generate_map_list():

	map_obj = CA_map(constants.MAP_HEIGHT, constants.MAP_WIDTH)
	map_list = map_obj.gen_map()
	return map_list


def gen_map():
	row = ""
	with open("map.txt", "w") as f:
		for x in range(0, 30):
			for y in range(0, 30):
				f.write(map_list[x][y])

			f.write("\n")
#gen_map()

