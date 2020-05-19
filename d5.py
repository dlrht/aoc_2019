import os, sys

POSITION_MODE = 0
IMMEDIATE_MODE = 1

def get_values(intcode, ip, modes, num_values):
    values = []
    for i in range(num_values):
        values.append(intcode[intcode[ip+i+1]] if modes[i] == POSITION_MODE else intcode[ip+i+1])

    return tuple(values) if num_values > 1 else values[0]


def run_intcode(intcode, noun=None, verb=None):
    if noun is not None:
        intcode[1] = noun
    if verb is not None:
        intcode[2] = verb

    ip = 0

    while (True):
        instruction = str(intcode[ip])
        opcode = int(instruction[-2:])

        parameter_modes = [0] * 3
        for i,mode in enumerate(reversed(instruction[:-2])):
            parameter_modes[i] = int(mode)
                    
        if opcode == 1: # Addition
            x,y = get_values(intcode, ip, parameter_modes, 2)
            intcode[intcode[ip+3]] = x+y
            ip += 4
        elif opcode == 2: # Multiplication
            x,y = get_values(intcode, ip, parameter_modes, 2)
            intcode[intcode[ip+3]] = x*y
            ip += 4
        elif opcode == 3: # Single int input
            user_input = input("Enter input: ")
            intcode[intcode[ip+1]] = int(user_input)
            ip += 2
        elif opcode == 4: # Outputs value of only parameter
            src = get_values(intcode, ip, parameter_modes, 1)
            print("Output: ", src)
            ip += 2
        elif opcode == 5: # jump-if-true
            x,y = get_values(intcode, ip, parameter_modes, 2)
            ip = y if x != 0 else ip + 3
        elif opcode == 6: # jump-if-false
            x,y = get_values(intcode, ip, parameter_modes, 2)
            ip = y if x == 0 else ip + 3
        elif opcode == 7: # less than
            x,y = get_values(intcode, ip, parameter_modes, 2)
            intcode[intcode[ip+3]] = 1 if x < y else 0
            ip += 4
        elif opcode == 8: # equals
            x,y = get_values(intcode, ip, parameter_modes, 2)
            intcode[intcode[ip+3]] = 1 if x == y else 0
            ip += 4
        elif opcode == 99:
            # Halt
            break
        else:
            print("Error")
            break


def find_input_for_output(intcode, output):
    for i in range(100):
        for j in range(100):
            new_intcode = intcode.copy()
            run_intcode(new_intcode, i,j)
            if new_intcode[0] == output:
                return i,j


with open(os.path.join(sys.path[0], "d5_input.txt")) as f:
    line = f.readline()
    line = line.strip()

intcode_original = line.split(",")
intcode_original = [int(i) for i in intcode_original]

run_intcode(intcode_original)
