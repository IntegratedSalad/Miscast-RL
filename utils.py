#from field_of_view import sintable
#from field_of_view import costable
import math
import random


def non_obj_distance_to(other, self_x, self_y):
    dx = other[0] - self_x
    dy = other[1] - self_y
    return math.sqrt(dx ** 2 + dy ** 2)

def can_hear(obj_hearing, obj_heard, noise_range, noise_chance): # obj_heard = noise_source


    if ( type(obj_hearing) is not str ) and ( type(obj_heard) is not str ): # otherwise it is silence.

        #print obj_heard.name
        #print noise_range
        #print noise_chance
    
        obj_hearing_mod_to_hearing = obj_hearing.fighter.modificators['mod_to_hearing']

        if obj_heard.item is None:
            obj_heard_mod_to_be_heard = obj_heard.fighter.modificators['mod_to_be_heard']
            OBJ_HEARD_ARMOR_MOD = obj_heard.fighter.armor_to_be_heard_modificator

        else:
            OBJ_HEARD_ARMOR_MOD = 100
            obj_heard_mod_to_be_heard = 100

        if noise_range > 0 and obj_hearing.distance_to(obj_heard) <= noise_range and obj_hearing.distance_to(obj_heard) > 1:

            if obj_heard.fighter.sneaking:
                obj_heard_mod_to_be_heard /= 2

            chance = random.randint(0, 100)

            throw = noise_chance + obj_heard_mod_to_be_heard + obj_hearing_mod_to_hearing + obj_hearing.fighter.armor_to_hear_modificator + OBJ_HEARD_ARMOR_MOD

            #print noise_chance, obj_heard_mod_to_be_heard, obj_hearing_mod_to_hearing, obj_hearing.fighter.armor_to_hear_modificator, OBJ_HEARD_ARMOR_MOD

            #print  "{0}: Throws: {1}, Treshold: {2} | is {3} < {4}? : {5}".format(obj_hearing.name, str(chance), str(throw), str(chance), str(throw), str(chance < throw))

            if chance < throw:

                #print obj_heard.name + " was heard."

                return True

    return False

def can_see(player_visibleness, monster_seeing): # in NoiseAI

    chance = random.randint(0, 100)

    throw = monster_seeing + player_visibleness 

    if chance < throw:
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
