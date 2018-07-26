import constants
import random

def heal(**kwargs):

	heal_val = kwargs.get('heal_value')
	target = kwargs.get('target')

	heal_message = ""

	if target.fighter.hp < target.fighter.max_hp:
		heal_val = random.randint(1, heal_val)
		target.fighter.hp += heal_val
		if target.fighter.hp > target.fighter.max_hp: target.fighter.hp = target.fighter.max_hp

		heal_message = "{0} was healed for {1}".format(target.name.capitalize(), heal_val)
		target.sended_messages.append(heal_message)
		return 'used'

	else:
		heal_message = "{0} feels as good as before...".format(target.name.capitalize())
		target.sended_messages.append(heal_message)
		return 'used'

def instant_death(**kwargs):

	target = kwargs.get('target')

	target.fighter.hp = 0

	target.sended_messages.append("Vile force is about to be unleashed on earth!")
	target.sended_messages.append('{0} dies a horrible death!'.format(target.name.capitalize()))

	return 'used'

def increase_health(**kwargs):
	pass

def uncontrolled_teleportation(**kwargs):

	target = kwargs.get('target')
	_map = kwargs.get('map')

	while True:
		x = random.randint(1, constants.MAP_WIDTH - 1) 
		y = random.randint(1, constants.MAP_HEIGHT - 1)
		if not _map[x][y].block_sight:
			target.x = x
			target.y = y
			break

	target.sended_messages.append("{0} feels unstable!".format(target.name.capitalize()))
	target.sended_messages.append("{0} shifts through space and time.".format(target.name.capitalize()))

	return 'used'

def equip(**kwargs):

	target = kwargs.get('target')
	item = kwargs.get('item')
	UI = kwargs.get('UI')

	target.fighter.equipment.append(item)
	target.sended_messages.append("{0} wears {1}".format(target.name.capitalize(), item.name.title()))

	return 'used'
