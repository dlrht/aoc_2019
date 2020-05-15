import math

with open("d2_input.txt") as f:
    line = f.readline()
    line = line.strip()

intcode_original = line.split(",")
intcode_original = [int(i) for i in intcode_original]

def run_intcode(noun, verb):
    intcode = intcode_original.copy()
    intcode[1] = noun
    intcode[2] = verb

    ip = 0
    opcode = intcode[ip]
    while (opcode != 99):
        x = intcode[intcode[ip+1]]
        y = intcode[intcode[ip+2]]

        if opcode == 1:
            intcode[intcode[ip+3]] = x+y
        elif opcode == 2:
            intcode[intcode[ip+3]] = x*y
        else:
            print("error")

        ip = ip + 4
        opcode = intcode[ip]
    
    return intcode[0]

def find_input_for_output(output):
    for i in range(100):
        for j in range(100):
            if run_intcode(i,j) == output:
                print(i, j)
                print(100 * i + j)
                return

find_input_for_output(19690720)