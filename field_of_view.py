#!/usr/bin/python
# This code is public domain.
# By init. initd5@gmail.com
sintable = [
    0.00000, 0.01745, 0.03490, 0.05234, 0.06976, 0.08716, 0.10453,
    0.12187, 0.13917, 0.15643, 0.17365, 0.19081, 0.20791, 0.22495, 0.24192,
    0.25882, 0.27564, 0.29237, 0.30902, 0.32557, 0.34202, 0.35837, 0.37461,
    0.39073, 0.40674, 0.42262, 0.43837, 0.45399, 0.46947, 0.48481, 0.50000,
    0.51504, 0.52992, 0.54464, 0.55919, 0.57358, 0.58779, 0.60182, 0.61566,
    0.62932, 0.64279, 0.65606, 0.66913, 0.68200, 0.69466, 0.70711, 0.71934,
    0.73135, 0.74314, 0.75471, 0.76604, 0.77715, 0.78801, 0.79864, 0.80902,
    0.81915, 0.82904, 0.83867, 0.84805, 0.85717, 0.86603, 0.87462, 0.88295,
    0.89101, 0.89879, 0.90631, 0.91355, 0.92050, 0.92718, 0.93358, 0.93969,
    0.94552, 0.95106, 0.95630, 0.96126, 0.96593, 0.97030, 0.97437, 0.97815,
    0.98163, 0.98481, 0.98769, 0.99027, 0.99255, 0.99452, 0.99619, 0.99756,
    0.99863, 0.99939, 0.99985, 1.00000, 0.99985, 0.99939, 0.99863, 0.99756,
    0.99619, 0.99452, 0.99255, 0.99027, 0.98769, 0.98481, 0.98163, 0.97815,
    0.97437, 0.97030, 0.96593, 0.96126, 0.95630, 0.95106, 0.94552, 0.93969,
    0.93358, 0.92718, 0.92050, 0.91355, 0.90631, 0.89879, 0.89101, 0.88295,
    0.87462, 0.86603, 0.85717, 0.84805, 0.83867, 0.82904, 0.81915, 0.80902,
    0.79864, 0.78801, 0.77715, 0.76604, 0.75471, 0.74314, 0.73135, 0.71934,
    0.70711, 0.69466, 0.68200, 0.66913, 0.65606, 0.64279, 0.62932, 0.61566,
    0.60182, 0.58779, 0.57358, 0.55919, 0.54464, 0.52992, 0.51504, 0.50000,
    0.48481, 0.46947, 0.45399, 0.43837, 0.42262, 0.40674, 0.39073, 0.37461,
    0.35837, 0.34202, 0.32557, 0.30902, 0.29237, 0.27564, 0.25882, 0.24192,
    0.22495, 0.20791, 0.19081, 0.17365, 0.15643, 0.13917, 0.12187, 0.10453,
    0.08716, 0.06976, 0.05234, 0.03490, 0.01745, 0.00000, -0.01745, -0.03490,
    -0.05234, -0.06976, -0.08716, -0.10453, -0.12187, -0.13917, -0.15643,
    -0.17365, -0.19081, -0.20791, -0.22495, -0.24192, -0.25882, -0.27564,
    -0.29237, -0.30902, -0.32557, -0.34202, -0.35837, -0.37461, -0.39073,
    -0.40674, -0.42262, -0.43837, -0.45399, -0.46947, -0.48481, -0.50000,
    -0.51504, -0.52992, -0.54464, -0.55919, -0.57358, -0.58779, -0.60182,
    -0.61566, -0.62932, -0.64279, -0.65606, -0.66913, -0.68200, -0.69466,
    -0.70711, -0.71934, -0.73135, -0.74314, -0.75471, -0.76604, -0.77715,
    -0.78801, -0.79864, -0.80902, -0.81915, -0.82904, -0.83867, -0.84805,
    -0.85717, -0.86603, -0.87462, -0.88295, -0.89101, -0.89879, -0.90631,
    -0.91355, -0.92050, -0.92718, -0.93358, -0.93969, -0.94552, -0.95106,
    -0.95630, -0.96126, -0.96593, -0.97030, -0.97437, -0.97815, -0.98163,
    -0.98481, -0.98769, -0.99027, -0.99255, -0.99452, -0.99619, -0.99756,
    -0.99863, -0.99939, -0.99985, -1.00000, -0.99985, -0.99939, -0.99863,
    -0.99756, -0.99619, -0.99452, -0.99255, -0.99027, -0.98769, -0.98481,
    -0.98163, -0.97815, -0.97437, -0.97030, -0.96593, -0.96126, -0.95630,
    -0.95106, -0.94552, -0.93969, -0.93358, -0.92718, -0.92050, -0.91355,
    -0.90631, -0.89879, -0.89101, -0.88295, -0.87462, -0.86603, -0.85717,
    -0.84805, -0.83867, -0.82904, -0.81915, -0.80902, -0.79864, -0.78801,
    -0.77715, -0.76604, -0.75471, -0.74314, -0.73135, -0.71934, -0.70711,
    -0.69466, -0.68200, -0.66913, -0.65606, -0.64279, -0.62932, -0.61566,
    -0.60182, -0.58779, -0.57358, -0.55919, -0.54464, -0.52992, -0.51504,
    -0.50000, -0.48481, -0.46947, -0.45399, -0.43837, -0.42262, -0.40674,
    -0.39073, -0.37461, -0.35837, -0.34202, -0.32557, -0.30902, -0.29237,
    -0.27564, -0.25882, -0.24192, -0.22495, -0.20791, -0.19081, -0.17365,
    -0.15643, -0.13917, -0.12187, -0.10453, -0.08716, -0.06976, -0.05234,
    -0.03490, -0.01745, -0.00000
]
 
costable = [
    1.00000, 0.99985, 0.99939, 0.99863, 0.99756, 0.99619, 0.99452,
    0.99255, 0.99027, 0.98769, 0.98481, 0.98163, 0.97815, 0.97437, 0.97030,
    0.96593, 0.96126, 0.95630, 0.95106, 0.94552, 0.93969, 0.93358, 0.92718,
    0.92050, 0.91355, 0.90631, 0.89879, 0.89101, 0.88295, 0.87462, 0.86603,
    0.85717, 0.84805, 0.83867, 0.82904, 0.81915, 0.80902, 0.79864, 0.78801,
    0.77715, 0.76604, 0.75471, 0.74314, 0.73135, 0.71934, 0.70711, 0.69466,
    0.68200, 0.66913, 0.65606, 0.64279, 0.62932, 0.61566, 0.60182, 0.58779,
    0.57358, 0.55919, 0.54464, 0.52992, 0.51504, 0.50000, 0.48481, 0.46947,
    0.45399, 0.43837, 0.42262, 0.40674, 0.39073, 0.37461, 0.35837, 0.34202,
    0.32557, 0.30902, 0.29237, 0.27564, 0.25882, 0.24192, 0.22495, 0.20791,
    0.19081, 0.17365, 0.15643, 0.13917, 0.12187, 0.10453, 0.08716, 0.06976,
    0.05234, 0.03490, 0.01745, 0.00000, -0.01745, -0.03490, -0.05234, -0.06976,
    -0.08716, -0.10453, -0.12187, -0.13917, -0.15643, -0.17365, -0.19081,
    -0.20791, -0.22495, -0.24192, -0.25882, -0.27564, -0.29237, -0.30902,
    -0.32557, -0.34202, -0.35837, -0.37461, -0.39073, -0.40674, -0.42262,
    -0.43837, -0.45399, -0.46947, -0.48481, -0.50000, -0.51504, -0.52992,
    -0.54464, -0.55919, -0.57358, -0.58779, -0.60182, -0.61566, -0.62932,
    -0.64279, -0.65606, -0.66913, -0.68200, -0.69466, -0.70711, -0.71934,
    -0.73135, -0.74314, -0.75471, -0.76604, -0.77715, -0.78801, -0.79864,
    -0.80902, -0.81915, -0.82904, -0.83867, -0.84805, -0.85717, -0.86603, 
    -0.87462, -0.88295, -0.89101, -0.89879, -0.90631, -0.91355, -0.92050,
    -0.92718, -0.93358, -0.93969, -0.94552, -0.95106, -0.95630, -0.96126,
    -0.96593, -0.97030, -0.97437, -0.97815, -0.98163, -0.98481, -0.98769,
    -0.99027, -0.99255, -0.99452, -0.99619, -0.99756, -0.99863, -0.99939,
    -0.99985, -1.00000, -0.99985, -0.99939, -0.99863, -0.99756, -0.99619,
    -0.99452, -0.99255, -0.99027, -0.98769, -0.98481, -0.98163, -0.97815,
    -0.97437, -0.97030, -0.96593, -0.96126, -0.95630, -0.95106, -0.94552,
    -0.93969, -0.93358, -0.92718, -0.92050, -0.91355, -0.90631, -0.89879,
    -0.89101, -0.88295, -0.87462, -0.86603, -0.85717, -0.84805, -0.83867,
    -0.82904, -0.81915, -0.80902, -0.79864, -0.78801, -0.77715, -0.76604,
    -0.75471, -0.74314, -0.73135, -0.71934, -0.70711, -0.69466, -0.68200,
    -0.66913, -0.65606, -0.64279, -0.62932, -0.61566, -0.60182, -0.58779,
    -0.57358, -0.55919, -0.54464, -0.52992, -0.51504, -0.50000, -0.48481,
    -0.46947, -0.45399, -0.43837, -0.42262, -0.40674, -0.39073, -0.37461,
    -0.35837, -0.34202, -0.32557, -0.30902, -0.29237, -0.27564, -0.25882,
    -0.24192, -0.22495, -0.20791, -0.19081, -0.17365, -0.15643, -0.13917,
    -0.12187, -0.10453, -0.08716, -0.06976, -0.05234, -0.03490, -0.01745,
    -0.00000, 0.01745, 0.03490, 0.05234, 0.06976, 0.08716, 0.10453, 0.12187,
    0.13917, 0.15643, 0.17365, 0.19081, 0.20791, 0.22495, 0.24192, 0.25882,
    0.27564, 0.29237, 0.30902, 0.32557, 0.34202, 0.35837, 0.37461, 0.39073,
    0.40674, 0.42262, 0.43837, 0.45399, 0.46947, 0.48481, 0.50000, 0.51504,
    0.52992, 0.54464, 0.55919, 0.57358, 0.58779, 0.60182, 0.61566, 0.62932,
    0.64279, 0.65606, 0.66913, 0.68200, 0.69466, 0.70711, 0.71934, 0.73135,
    0.74314, 0.75471, 0.76604, 0.77715, 0.78801, 0.79864, 0.80902, 0.81915,
    0.82904, 0.83867, 0.84805, 0.85717, 0.86603, 0.87462, 0.88295, 0.89101,
    0.89879, 0.90631, 0.91355, 0.92050, 0.92718, 0.93358, 0.93969, 0.94552,
    0.95106, 0.95630, 0.96126, 0.96593, 0.97030, 0.97437, 0.97815, 0.98163,
    0.98481, 0.98769, 0.99027, 0.99255, 0.99452, 0.99619, 0.99756, 0.99863,
    0.99939, 0.99985, 1.00000
]

def set_fov(fov_map, unveil=False):
    for x in range(30 + 1): 
        fov_map.append([])     
        # Reset FOV
     
        for y in range(30 + 1):
            if unveil:
                fov_map[x].append(1)
            else:
                fov_map[x].append(0)

    return fov_map


def reset_fov(fov_map):
    for x in range(30 + 1):
        for y in range(30 + 1):
            fov_map[x][y] = 0

def is_in_fov(fov_map, obj):

    #print obj.name
    if fov_map[obj.x][obj.y] == 1: return True
    else: return False
 
# The FOV algo itself.
 
# It works like this:
# It starts at player coordinates and cast 360 rays
# (if step is 1, less is step is more than 1) in every direction,
# until it hits a wall.
# When ray hits floor, it is set as visible.
 
# Ray is casted by adding to x (initialy it is player's x coord)
# value of sin(i degrees) and to y (player's y) value of cos(i degrees),
# RAD times, and checking for collision with wall every step.
 

def cast_rays(px, py, fov_map, level_map, radius): # change that to x and y - so that anything can be a light source

    # but that light source must acivate only if it is in the player fov range

    RAYS = 360
    STEP = 3

    for i in range(0, RAYS + 1, STEP): 
        ax = sintable[i] # Get precalculated value sin(x / (180 / pi))
        ay = costable[i] # cos(x / (180 / pi))
     
        x = px # Player's x
        y = py # Player's y
     
        for z in range(radius): # Cast the ray

            if x < 0 or y < 0 or x > 30 or y > 30: # If ray is out of range
                break
     
            fov_map[int(round(x))][int(round(y))] = 1  # Make tile visible
     
            if level_map[int(round(x))][int(round(y))].block_sight:
                # Stop ray if it hits a wall.
                break

            x += ax
            y += ay
     

def fov_recalculate(fov_map, x, y, _map, radius):
    reset_fov(fov_map)
    cast_rays(x, y, fov_map, _map, radius)
