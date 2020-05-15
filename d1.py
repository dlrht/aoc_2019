import math

def required_fuel(mass):
    return math.floor(mass/3) - 2


def required_fuel_compounded(mass):
    fuel = required_fuel(mass)

    if fuel <= 0:
        return 0
    
    return fuel + required_fuel_compounded(fuel)


sum_A = sum_B = 0;
with open("d1_input.txt") as f:
    for line in f:
        sum_A += required_fuel(int(line))
        sum_B += required_fuel_compounded(int(line))

print("Part A: ", sum_A)
print("Part B: ", sum_B)