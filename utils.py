from field_of_view import sintable
from field_of_view import costable


def make_noise_map(x, y, level_map, radius, fade_value, top_noise_value):
    # fade value indicates how many tiles the sound can penetrate

    RAYS = 360
    STEP = 3

    audible_places = {}

    for i in range(0, RAYS + 1, STEP):
        ax = sintable[i]  # Get precalculated value sin(x / (180 / pi))
        ay = costable[i]  # cos(x / (180 / pi))
        level = top_noise_value
        penetrated_walls = 0

        fade_out = fade_value

        _x = x
        _y = y

        for z in range(radius):  # Cast the ray
            #print int(round(_x)), int(round(_y)), level

            if _x < 0 or _y < 0 or _x > 29 or _y > 29:  # If ray is out of range
                break

            if z != 0 and (z % fade_out) == 0:
                level -= 1

            if level <= 0:
                break

            if level_map[int(round(_x))][int(round(_y))].block_sight:
                penetrated_walls += 1

                # break according to the fade_value

                if penetrated_walls >= fade_value:
                    break

            audible_places[(int(round(_x)), int(round(_y)))] = level

            _x += ax
            _y += ay

    return audible_places  # key - cords, values - lvl: {(20, 20): 3}
