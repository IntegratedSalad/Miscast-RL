import constants
import random
import objects

def heal(**kwargs):

	heal_val = kwargs.get('heal_value')
	target = kwargs.get('target')

	heal_message = ""

	if target.fighter.hp < target.fighter.max_hp:
		heal_val = random.randint(heal_val / 2, heal_val)
		target.fighter.hp += heal_val
		if target.fighter.hp > target.fighter.max_hp: target.fighter.hp = target.fighter.max_hp

		heal_message = "{0} was healed for {1}.".format(target.name.title(), heal_val)
		target.send_message(heal_message)
		return 'used'

	else:
		heal_message = "{0} feels as good as before...".format(target.name.title())
		target.send_message(heal_message)
		return 'used'

def instant_death(**kwargs):

	target = kwargs.get('target')
	user = kwargs.get('user')

	if target.fighter:
		target.fighter.hp = 0

		if not user == target:

			target.send_message("Vile force is about to be unleashed on earth!")
			target.send_message('{0} dies a horrible death!'.format(target.name.title()))

			user.send_message("You hear someone reetching violently.")
		else:
			user.send_message("You feel suicidal.")

		return 'used'

	return 'cancelled'

def increase_max_health(**kwargs):
	# permanently increases health
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

	target.send_message("{0} feels unstable!".format(target.name.title()))
	target.send_message("{0} shifts through space and time.".format(target.name.title()))

	return 'used'

def equip(**kwargs):

	target = kwargs.get('target')
	item = kwargs.get('item')
	UI = kwargs.get('UI')

	if target.name == constants.PLAYER_NAME:

		if UI.add_item_to_equipment_slot(item):
			target.fighter.equipment.append(item)
			target.send_message("{0} wears {1}.".format(target.name.title(), item.name.title()))
			return 'used'
		else:
			target.send_message("You already have something in this slot, you have to")
			target.send_message("remove it first.")
			return 'cancelled'

	else:

		slot = item.item.equipment.slot 
		for piece in target.fighter.equipment:
			if slot == piece.item.equipment.slot:
				target.fighter.inventory.append(item) # Warning: AI must NOT decide to wear something on the same slot!
				return 'cancelled'

		target.fighter.equipment.append(item)
		target.send_message("{0} wears {1}.".format(target.name.title(), item.name.title()))
		return 'used'


def light_lantern(**kwargs):

	item = kwargs.get('item')
	user = kwargs.get('user')

	user.send_message("{0} lits lantern.".format(user.name.title()))

	return 'activated'

def refill_lantern(**kwargs):

	player = kwargs.get('user')
	oil_amount = kwargs.get('oil_value')

	for obj in player.fighter.inventory:
		if obj.name == 'lantern':
			if obj.item.equipment.charges < 1500 and obj.item.equipment.charges + oil_amount < 1500:
				obj.item.equipment.charges += oil_amount
				player.send_message("{0} refills lantern.".format(player.name.title()))
				return 'used'

			if obj.item.equipment.charges + oil_amount > 1500:
				player.send_message("This will overfill the lantern.")
				return 'cancelled'

			else:
				player.send_message("Lantern is full.")
				return 'cancelled'

	# haven't found the lantern in inventory

	player.send_message("There is no lantern in your inventory.")
	return 'cancelled'
	

def confuse(**kwargs):

	target = kwargs.get('target')
	user = kwargs.get('user')

	if target.fighter:

		if target.name != constants.PLAYER_NAME:
			previous_ai = target.ai

		else:
			previous_ai = 'player_controls'

		brain = objects.FSM()
		confused_AI = objects.ConfusedAI(brain)
		target.ai = confused_AI
		confused_AI.owner = target
		target.ai.previous_ai = previous_ai

		if not target == user:
			target.send_message("You feel funny.")
			user.send_message("You see {0} stumbling on everything.".format(target.name))

		else:
			user.send_message("You confuse yourself!")
		return 'used'

	return 'cancelled'
	