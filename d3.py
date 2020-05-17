with open("d3_input.txt") as f:
    line1 = f.readline().strip().split(",")
    line2 = f.readline().strip().split(",")


def build_path(directions):
    cur_pos = (0,0)
    coords = [(0,0)]
    for path_part in directions:
        dir = path_part[0]
        dist = int(path_part[1:])

        x = y = 0

        if dir == 'R':
            x = dist
        elif dir == 'L':
            x = -dist
        elif dir == 'U':
            y = dist
        elif dir == 'D':
            y = -dist

        cur_pos = (cur_pos[0] + x, cur_pos[1] + y)
        coords.append(cur_pos)

    return coords


# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
# Returns point of intersections for 2 line segments l1, l2, defined by two points A, B
# Returns None if no point of intersection/coincident lines
def get_intersection(l1_a, l1_b, l2_a, l2_b):
    x1 = l1_a[0]
    y1 = l1_a[1]
    x2 = l1_b[0]
    y2 = l1_b[1]
    x3 = l2_a[0]
    y3 = l2_a[1]
    x4 = l2_b[0]
    y4 = l2_b[1]

    if (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4) != 0:  # parallel/coincident line, ignore if it is
        t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
        u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))

        if 0.0 <= t and t <= 1.0 and 0.0 <= u and u <= 1.0: # intersection is within both line segments (and not on the lines)
            return (round(x1 + t*(x2 - x1)), round(y1 + t*(y2 - y1)))
            # return (round(x3 + u*(x4 - x3)), round(y3 + u*(y4 - y3)))
    
    return None


# Build intersection list
# Find minimal steps to reach any intersection for wire1 by tracing tracing along it and calculating distance for each intersection
# Also builds list of intersections
def find_intersections_steps(coords_wire1, coords_wire2):
    intersection_steps_dict = {}
    dist_total = 0

    for i in range(len(coords_wire1)-1):
        x = coords_wire1[i][0] - coords_wire1[i+1][0]
        y = coords_wire1[i][1] - coords_wire1[i+1][1]

        dist = abs(x) if x != 0 else abs(y)

        for j in range(len(coords_wire2)-1):
                intersection = get_intersection(coords_wire1[i], coords_wire1[i+1], coords_wire2[j], coords_wire2[j+1])
                if intersection is not None:
                    x1 = abs(coords_wire1[i][0] - intersection[0])
                    y1 = abs(coords_wire1[i][1] - intersection[1])

                    dist_to_intersection = dist_total + (x1 if x1 != 0 else y1) 
                    if intersection not in intersection_steps_dict:
                        intersection_steps_dict[intersection] = dist_to_intersection

        dist_total += dist
    
    return intersection_steps_dict


intersections = []
wire1_coords = build_path(line1)
wire2_coords = build_path(line2)
wire1_steps_to_intersection = find_intersections_steps(wire1_coords, wire2_coords)
wire2_steps_to_intersection = find_intersections_steps(wire2_coords, wire1_coords)

intersections = list(wire1_steps_to_intersection.keys())
min_dist = wire1_steps_to_intersection[intersections[0]] + wire2_steps_to_intersection[intersections[0]]
for i in intersections:
    steps = wire1_steps_to_intersection[i] + wire2_steps_to_intersection[i]
    
    if steps < min_dist:
        min_dist = steps

# Calculate manhattan distances for each intersection and find min
distances = [abs(i[0]) + abs(i[1]) for i in intersections]
print("Manhattan distance from the central port to closest intersection: ", min(distances))
print("Fewest combined steps to reach an intersection: ", min_dist)