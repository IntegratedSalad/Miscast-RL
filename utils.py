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

        throw = noise_chance + obj_mod_to_be_heard + obj_mod_to_hearing + obj.fighter.armor_to_hear_modificator + obj_two.fighter.armor_to_be_heard_modificator

        #print  "{0}: Throws: {1}, Treshold: {2} | is {3} < {4}? : {5}".format(obj.name, str(chance), str(throw), str(chance), str(throw), str(chance < throw))

        if chance < throw:

            #print obj.name + " heard"

            return True

    return False

def can_see(player_visibleness, monster_seeing): # in NoiseAI

    chance = random.randint(0, 100)

    throw = monster_seeing + player_visibleness 

    if chance < throw:
        print "Monster saw the player."
        return True

    return False


def bresenham_alg(x0, y0, x1, y1):
    "Bresenham's line algorithm - taken from: https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python"

    path = []

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
            path.append((x, y))

    else:
        count = 0
        err = dy / 2.0
        while y != y1:
            err -= dx
            if err <0:
                x += sx
                err += dy
            y += sy
            path.append((x, y))
    

    if x0==x1 and y0==y1: return 'dont throw'
    return path
