import constants

def heal(target, heal_val):

	heal_message = ""

	if target.fighter.hp < target.fighter.max_hp:
		target.fighter.hp += random.randint(1, heal_val)
		if target.fighter.hp > target.fighter.max_hp: target.fighter.hp = target.fighter.max_hp

		heal_message = "{0} was healed for {1}".format(target.name, heal_val)
		target.sended_messages.append(heal_message)
		return 'used'

	else:
		heal_message = "{0} feels as good as before...".format(target.name)
		target.sended_messages.append(heal_message)
		return 'used'

def instant_death(target, val=0):

	target.fighter.hp = 0

	target.sended_messages.append('{0} dies a horrible death!'.format(target.name.capitalize()))

	return 'used'
