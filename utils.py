#from field_of_view import sintable
#from field_of_view import costable
import math
import random


#def make_noise_map(x, y, level_map, radius, fade_value, top_noise_value):
    # fade value indicates how many tiles the sound can penetrate

    # use bresenham line 
#    pass

def non_obj_distance_to(other, self_x, self_y):
    dx = other[0] - self_x
    dy = other[1] - self_y
    return math.sqrt(dx ** 2 + dy ** 2)

def can_hear(obj, obj_two, noise_range, noise_source, noise_chance):

    obj_mod_to_be_heard = obj_two.fighter.modificators['mod_to_be_heard'] # obj_two
    obj_mod_to_hearing = obj.fighter.modificators['mod_to_hearing'] # obj_one

    if noise_range > 0 and obj.distance_to(noise_source) <= noise_range and obj.distance_to(noise_source) > 1:
        # do the chance, it can be heard, but not have to.

        chance = random.randint(0, 100)

        throw = noise_chance + obj_mod_to_be_heard + obj_mod_to_hearing

        print  "{0}: Throws: {1}, Treshold: {2} | is {3} < {4}? : {5}".format(obj.name, str(chance), str(throw), str(chance), str(throw), str(chance < throw))

        if chance < throw:

            print obj.name + " heard"

            return True

    return False

def can_see(): # in NoiseAI
    pass 