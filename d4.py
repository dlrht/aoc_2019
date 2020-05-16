
def count_variations(start, stop, allow_larger_matching):
    counter = 0
    for i in range(start, stop+1):
        test = str(i)

        # Two adjacent digits are the same 
        if test[0] != test[1] and test[1] != test[2] and test[2] != test[3] and test[3] != test[4] and test[4] != test[5]:
            continue

        # Digits never decreasing
        if test[0] > test[1] or test[1] > test[2] or test[2] > test[3] or test[3] > test[4] or test[4] > test[5]:
            continue

        if allow_larger_matching:
            counter += 1
            continue

        digits = {}
        for s in test:
            if s in digits:
                digits[s] += 1
            else:
                digits[s] = 1
        
        # Need at least one adjacent pair of digits
        valid = False
        for k in digits.keys():
            if digits[k] == 2:
                valid = True

        if valid:
            counter += 1

    return counter

print("Possible variations: ", count_variations(357253, 892942, True))
print("Possible variations w/o larger matching set: ", count_variations(357253, 892942, False))
