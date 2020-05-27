from pathlib import Path
import math

# finds angle between 2 vectors u,v defined by 2 points x,y
def find_angle(u_x, u_y, v_x, v_y):
    dot_product = (u_x*v_x) + (u_y*v_y)
    u_magnitude = math.sqrt((u_x*u_x) + (u_y*u_y))
    v_magnitude = math.sqrt((v_x*v_x) + (v_y*v_y))
    cos_theta = dot_product/(u_magnitude * v_magnitude)
    theta = math.acos(cos_theta)

    # print("u,v: ", u_x, u_y, v_x, v_y)
    # print("vals: ", dot_product, u_magnitude, v_magnitude)
    # print("costheta: ", cos_theta)

    return theta

# Its not working cause we reversed things!!
def find_pts_visible(coords_dict, coord):
    angles = {}

    u_x, u_y = (1,0)

    for i in coords_dict.keys():
        if i != coord:
            v_x = i[0] - coord[0]
            v_y = i[1] - coord[1]

            v_x_unit = v_x/math.sqrt(v_x*v_x + v_y*v_y)
            v_y_unit = v_y/math.sqrt(v_x*v_x + v_y*v_y)

            angle = find_angle(u_x, u_y, v_x_unit, v_y_unit)

            quadrant_x = quadrant_y = 0
            if v_x_unit != 0:
                quadrant_x = v_x_unit // abs(v_x_unit)
            if v_y_unit != 0:
                quadrant_y = v_y_unit // abs(v_y_unit)

            # print(i, angle)
            angle = round(angle, 6) # OMG THIS FIXED IT

            if (angle, (quadrant_x, quadrant_y)) not in angles:
                angles[angle, (quadrant_x, quadrant_y)] = [i]
            else:
                angles[angle, (quadrant_x, quadrant_y)].append(i)

    return angles


def find_pts_visible_all(coords_dict):
    for i in coords_dict.keys():
        coords_dict[i] = find_pts_visible(coords_dict, i)

    return coords_dict


def get_closest_pt(source, list_of_coords):
    newlist = [(math.sqrt((pt[0] - source[0])**2 + (pt[1] - source[1])**2), pt) for pt in list_of_coords if pt != source]
    closest_pt = min(newlist) # does this work on tuples like this?

    return closest_pt


data = list(map(str, (Path(__file__).parent / 'd10_input.txt').read_text().split('\n')))  # Rose this is SO smooth, dang

asteroid_dict = {}
for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] == '#':
            asteroid_dict[(j, -i)] = 0

# print(find_pts_visible(asteroid_dict, (1,0)))

# print(asteroid_dict)
find_pts_visible_all(asteroid_dict)

# Find asteroid with max # of detections
# max_detected = ((0,0), 0)
# for i in asteroid_dict.keys():
#     if len(asteroid_dict[i]) > max_detected[1]:
#         max_detected = (i, len(asteroid_dict[i]))

# Convert dict to (coord, # of detection)
# for i in asteroid_dict.keys():
#     asteroid_dict[i] = len(asteroid_dict[i])

# Print each asteroid's # of detections
# for i in asteroid_dict.keys():
#     print(i, asteroid_dict[i], "\n")

# for i in range(len(data)):
#     row = ""
#     for j in range(len(data[0])):
#         if (j, -i) in asteroid_dict:
#             row = row + str(asteroid_dict[(j, -i)])
#         else:
#             row = row + "." 
#     print(row)

dict_coord = {
    (0,0): 0,
    (1,-1): 0,
    (2,-2): 0,
    (3,-4): 0,
    (0,1): 0,
}

test = list(asteroid_dict.keys())
print(asteroid_dict[test[1]])
# print(find_pts_visible(asteroid_dict, (4, -3)))

# print(max_detected)
# print(asteroid_dict[max_detected[0]])