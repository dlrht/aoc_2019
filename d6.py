import os, sys        

# Returns the sum of every vertex's depth from v in a graph defined by parents
def DFS_sum_depths(parents, v, cur_depth):
    total = cur_depth
    if v in parents:
        for child in parents[v]:
            total += DFS_sum_depths(parents, child, cur_depth+1)

    return total


# Returns a path from v to goal given a graph defined by parents
# Returns None if no path exists
def DFS_search(parents, v, goal, path):
    path.append(v)

    if v == goal:
        return path

    if v in parents:
        for child in parents[v]:
            result = DFS_search(parents, child, goal, path.copy())

            if result is not None:
                return result

    return None


# Returns number of vertices in between child1 and child2 given a grpah defined by parents with root v
# Assumes child1 and child2 exist
def find_num_vertices_between(parents, v, child1, child2):
    # Find a path to each child
    path_to_child1 = DFS_search(parents, v, child1, [])
    path_to_child2 = DFS_search(parents, v, child2, [])

    # Find index at which the paths start to differ
    split_idx = 0
    for i in range(len(path_to_child1)):
        if path_to_child1[i] == path_to_child2[i]:
            split_idx += 1
    
    # Find number of objects in between child1 and child2
    return (len(path_to_child1) - split_idx) + (len(path_to_child2) - split_idx) - 2


# Construct graph using dictionary (key is parent, values are children). 
# Assumes there are no cycles

parents = {}

with open(os.path.join(sys.path[0], "d6_input.txt")) as f:
    for line in f:
        line = line.strip().split(")")
        parent = line[0]
        child = line[1]

        if parent not in parents:
            parents[parent] = [child]
        else:
            parents[parent].append(child)

print("Total # of orbits: ", DFS_sum_depths(parents, 'COM', 0))
print("# of planets between YOU and SAN: ", find_num_vertices_between(parents, 'COM', 'YOU', 'SAN'))
