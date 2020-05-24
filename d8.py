from pathlib import Path

# Returns the arr_raw data as a 3D array of layers, rows, columns
def get_layers_array(arr_raw, width, height):
    num_layers = len(arr_raw) // (width*height)
    layers = []

    for l in range(num_layers):
        layer = []
        layers.append(layer)

        for i in range(height):
            row = []
            layer.append(row)

            for j in range(width):
                row.append(int(arr_raw[(l * width * height) + (i * width) + j]))

    return layers


# Returns 2d array of final image given a 3D array of layers
def get_final_image_array(layers_arr):
    num_layers = len(layers_arr)
    height = len(layers_arr[0])
    width = len(layers_arr[0][0])

    final_image = []
    for i in range(height):
        final_image.append([2] * width)
    
    for l in range(num_layers):
        for i in range(height):
            for j in range(width):
                if final_image[i][j] == 2:
                    final_image[i][j] = layers_arr[l][i][j]

    return final_image


# This barely resembles anything... have to view from a distance
def display_final_image(image_arr, black_char, white_char):
    for row in image_arr:
        for i in row:
            c = black_char if i == 0 else white_char  # char to print depending on if black or white/transparent
            print(c, end="")
        print()


# Get layers
data = list(map(str, (Path(__file__).parent / 'd8_input.txt').read_text().split(',')))
layers = get_layers_array(data[0], width=25, height=6)

# Find layer with fewest zeros
fewest_zeros = (0, len(data[0])) # (index, # of zeroes)
for i,layer in enumerate(layers):
    num_zeroes_in_layer = sum([row.count(0) for row in layer])

    if num_zeroes_in_layer < fewest_zeros[1]:
        fewest_zeros = (i, num_zeroes_in_layer)

num_ones_in_layer = sum([row.count(1) for row in layers[fewest_zeros[0]]])
num_twos_in_layers = sum([row.count(2) for row in layers[fewest_zeros[0]]])

print("Number of 1 digits multiplied by the number of 2 digits in layer with fewest 0s:", num_ones_in_layer * num_twos_in_layers)
display_final_image(get_final_image_array(layers), black_char='W', white_char=' ')