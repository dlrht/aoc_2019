from pathlib import Path
import math

# Its not working cause we reversed things!!
def find_pts_visible(coords_dict, coord):
    angles = {}

    for i in coords_dict.keys():
        if i != coord:
            v_x = i[0] - coord[0]
            v_y = i[1] - coord[1]

            v_x_unit = v_x/math.sqrt(v_x*v_x + v_y*v_y)
            v_y_unit = v_y/math.sqrt(v_x*v_x + v_y*v_y)

            angle = math.atan2(v_y_unit, v_x_unit)
            angle = round(angle, 6) # OMG THIS FIXED IT

            if angle not in angles:
                angles[angle] = [i]
            else:
                angles[angle].append(i)

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
max_detected = ((0,0), 0)
for i in asteroid_dict.keys():
    if len(asteroid_dict[i]) > max_detected[1]:
        max_detected = (i, len(asteroid_dict[i]))

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

# dict_coord = {
#     (0,0): 0,
#     (1,-1): 0,
#     (2,-2): 0,
#     (3,-4): 0,
#     (0,1): 0,
# }

# test = list(asteroid_dict.keys())
# print(asteroid_dict[test[1]])
# print(find_pts_visible(asteroid_dict, (4, -3)))

# print(max_detected)
station_pos = max_detected[0]
detected_asteroids = asteroid_dict[station_pos]
print(detected_asteroids)
angles_list = detected_asteroids.keys()

print()
y_axis_pos = math.atan2(1, 0)
y_axis_neg = math.atan2(-1, 0)
sorted_angles = sorted(angles_list)
sorted_angles = list(reversed(sorted_angles))
angles_sorted_clockwise = [i for i in sorted_angles if i <= y_axis_pos] + [i for i in sorted_angles if i > y_axis_pos]
print(angles_sorted_clockwise)
print(station_pos)
print(detected_asteroids[angles_sorted_clockwise[0]])
print(get_closest_pt(station_pos, detected_asteroids[angles_sorted_clockwise[0]]))

counter = 1
for angle in angles_sorted_clockwise:
    asteroids = detected_asteroids[angle]
    closest_asteroid = get_closest_pt(station_pos, asteroids)
    asteroids.remove(closest_asteroid[1])

    print(counter, closest_asteroid)
    counter += 1
