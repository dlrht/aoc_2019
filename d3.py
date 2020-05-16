with open("d3_input.txt") as f:
    line1 = f.readline().strip().split(",")
    line2 = f.readline().strip().split(",")

# Find coordinates of wire 1... store all of wire 1 as a list of line segments
center = (0,0)

def build_path(directions):
    cur_pos = center
    coords = [center]
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

wire1_coords = build_path(line1)
wire2_coords = build_path(line2)
wire1_steps_to_intersection = {}
wire2_steps_to_intersection = {}
dist_wire1 = 0
dist_wire2 = 0

intersections = []
# Build intersection list
# Find least steps to each intersection for wire 1
for i in range(len(wire1_coords)-1):
    x = wire1_coords[i][0] - wire1_coords[i+1][0]
    y = wire1_coords[i][1] - wire1_coords[i+1][1]

    dist = abs(x) if x != 0 else abs(y)

    for j in range(len(wire2_coords)-1):
            intersection = get_intersection(wire1_coords[i], wire1_coords[i+1], wire2_coords[j], wire2_coords[j+1])
            if intersection is not None:
                intersections.append(intersection)

                x1 = abs(wire1_coords[i][0] - intersection[0])
                y1 = abs(wire1_coords[i][1] - intersection[1])

                dist_intersection1 = dist_wire1 + (x1 if x1 != 0 else y1) 
                if intersection not in wire1_steps_to_intersection:
                    wire1_steps_to_intersection[intersection] = dist_intersection1

    dist_wire1 += dist

# Find least steps to each intersection for wire 2
for j in range(len(wire2_coords)-1):
    x = wire2_coords[j][0] - wire2_coords[j+1][0]
    y = wire2_coords[j][1] - wire2_coords[j+1][1]

    dist = abs(x) if x != 0 else abs(y)

    for i in range(len(wire1_coords)-1):
            intersection = get_intersection(wire2_coords[j], wire2_coords[j+1], wire1_coords[i], wire1_coords[i+1])
            if intersection is not None:
                x2 = abs(wire2_coords[j][0] - intersection[0])
                y2 = abs(wire2_coords[j][1] - intersection[1])

                dist_intersection2 = dist_wire2 + (x2 if x2 != 0 else y2) 
                if intersection not in wire2_steps_to_intersection:
                    wire2_steps_to_intersection[intersection] = dist_intersection2

    dist_wire2 += dist

min_dist = wire1_steps_to_intersection[intersections[0]] + wire2_steps_to_intersection[intersections[0]]
for i in intersections:
    steps = wire1_steps_to_intersection[i] + wire2_steps_to_intersection[i]
    
    if steps < min_dist:
        min_dist = steps

# Calculate manhattan distances for each intersection and find min
distances = [abs(i[0]) + abs(i[1]) for i in intersections]
print("Manhattan distance from the central port to closest intersection: ", min(distances))
print("Fewest combined steps to reach an intersection: ", min_dist)