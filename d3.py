with open("d3_input.txt") as f:
    line1 = f.readline()
    line1 = line1.strip()

    line2 = f.readline()
    line2 = line2.strip()

wire1 = line1.split(",")
wire2 = line2.split(",")

# Find coordinates of wire 1... store all of wire 1 as a list of line segments
center = (0,0)
curpos = center
coords1 = [center]
for path_part in wire1:
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
    
    curpos = (curpos[0] + x, curpos[1] + y)
    coords1.append(curpos)


# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
def get_intersection(l1_a, l1_b, l2_a, l2_b):
    x1 = l1_a[0]
    y1 = l1_a[1]
    x2 = l1_b[0]
    y2 = l1_b[1]
    x3 = l2_a[0]
    y3 = l2_a[1]
    x4 = l2_b[0]
    y4 = l2_b[1]

    if (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4) != 0:
        t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
        u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))

        if 0.0 <= t and t <= 1.0 and 0.0 <= u and u <= 1.0:
            return (round(x1 + t*(x2 - x1)), round(y1 + t*(y2 - y1)))
            # return (round(x3 + u*(x4 - x3)), round(y3 + u*(y4 - y3)))


# Iterate through all lines in wire 2 and check if they intersect with any lines in wire 1
wire1_steps_to_intersection = {}
wire2_steps_to_intersection = {}

intersections = []
curpos = center
dist_travelled_wire2 = 0
for path_part in wire2:
    dir = path_part[0]
    dist = int(path_part[1:])

    startpos = curpos
    x = y = 0
    if dir == 'R':
        x = dist
    elif dir == 'L':
        x = -dist
    elif dir == 'U':
        y = dist
    elif dir == 'D':
        y = -dist
    endpos = (curpos[0] + x, curpos[1] + y)
    curpos = endpos

    # Checking if this line segment in wire 1 intersects with any of the line segments in wire 2
    for i in range(len(coords1)-1):
        intersection = get_intersection(startpos, endpos, coords1[i], coords1[i+1])
        if intersection is not None:
            intersections.append(intersection)
            x = abs(startpos[0] - intersection[0])
            y = abs(startpos[1] - intersection[1])

            dist_intersection = dist_travelled_wire2 + (x if x != 0 else y) 
            wire2_steps_to_intersection[intersection] = dist_intersection

    dist_travelled_wire2 += dist     

# Calculate manhattan distances for each intersection and find min
distances = [abs(i[0]) + abs(i[1]) for i in intersections]
print("Manhattan distance from the central port to closest intersection: ", min(distances))

# Get steps for the first wire
curpos = center
dist_travelled_wire1 = 0
for path_part in wire1:
    dir = path_part[0]
    dist = int(path_part[1:])

    startpos = curpos
    x = y = 0
    if dir == 'R':
        x = dist
    elif dir == 'L':
        x = -dist
    elif dir == 'U':
        y = dist
    elif dir == 'D':
        y = -dist
    endpos = (curpos[0] + x, curpos[1] + y)
    curpos = endpos

    # Checking if this line segment in wire 1 intersects with any of the line segments in wire 2
    for i in range(len(coords1)-1):
        intersection = get_intersection(startpos, endpos, coords1[i], coords1[i+1])
        if intersection is not None:
            intersections.append(intersection)
            x = abs(startpos[0] - intersection[0])
            y = abs(startpos[1] - intersection[1])

            dist_intersection = dist_travelled_wire1 + (x if x != 0 else y) 
            wire2_steps_to_intersection[intersection] = dist_intersection

    dist_travelled_wire1 += dist     