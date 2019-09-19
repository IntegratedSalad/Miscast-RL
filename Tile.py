
class Tile(object):
	def __init__(self, block_movement, block_sight=None, is_map_structure=False):
		self.block_movement = block_movement
		#if the tile is a wall - map structure
		self.is_map_structure = is_map_structure

		if block_sight is None: block_sight = block_movement
		self.block_sight = block_sight


def is_blocked(x, y, _map, objects):
	if _map[x][y].block_movement:
		return True

	for obj in objects:
		if obj.x == x and obj.y == y and obj.blocks:
			return True