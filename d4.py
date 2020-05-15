counter = 0
for i in range(357253, 892943):
    test = str(i)

    # Two adjacent digits are the same 
    if test[0] != test[1] and test[1] != test[2] and test[2] != test[3] and test[3] != test[4] and test[4] != test[5]:
        continue

    # Digits always decreasing
    if test[0] > test[1] or test[1] > test[2] or test[2] > test[3] or test[3] > test[4] or test[4] > test[5]:
        continue

    counter += 1

print("Possible variations: ", counter)
