from pathlib import Path
import itertools

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

READ = 0
WRITE = 1

class Intcode():
    def __init__(self, intcode, ip=0, rel_base=0, memory_expand_factor=10):
        self.intcode = intcode.copy()
        self.intcode.extend([0] * len(self.intcode) * memory_expand_factor)
        self.ip = ip
        self.rel_base = rel_base
    

    # Returns a len(type_of_param)-tuple with appropriate values based on parameter modes
    # Returns appropriate value if a read command or destination to write to if a write command
    def get_values(self, modes, type_of_param):
        values = []
        for i in range(len(type_of_param)):
            val = None
            if type_of_param[i] == READ:
                if modes[i] == POSITION_MODE:
                    val = self.intcode[self.intcode[self.ip+i+1]]
                elif modes[i] == IMMEDIATE_MODE:
                    val = self.intcode[self.ip+i+1]
                elif modes[i] == RELATIVE_MODE:
                    val = self.intcode[self.rel_base + self.intcode[self.ip+i+1]]

            elif type_of_param[i] == WRITE:
                if modes[i] == POSITION_MODE:
                    val = self.intcode[self.ip+i+1]
                elif modes[i] == RELATIVE_MODE:
                    val = self.rel_base + self.intcode[self.ip+i+1]

            if val is None:
                print("Error getting value")
                
            values.append(val)

        return tuple(values) if len(type_of_param) > 1 else values[0]


    def Execute(self, input_set=[], new_ip=None, new_rel_base=None, halt_on_empty_input_set=False, verbose=0):
        self.ip = self.ip if new_ip == None else new_ip
        self.rel_base = self.rel_base if new_rel_base == None else new_rel_base
        outputs = []

        while (True):
            instruction = str(self.intcode[self.ip])
            opcode = int(instruction[-2:])

            parameter_modes = [0] * 3
            for i,mode in enumerate(reversed(instruction[:-2])):
                parameter_modes[i] = int(mode)

            if verbose >= 2: # For debugging
                print("Input set:", input_set)
                print_intcode = self.intcode.copy()
                print_intcode[self.ip] = '***' + str(print_intcode[self.ip]) + '***'
                print(print_intcode, "-", "ip:"+str(self.ip), "opcode:"+str(opcode), "modes:"+str(parameter_modes))

            if opcode == 1:     # Addition
                x,y,z = self.get_values(parameter_modes, [READ, READ, WRITE])
                self.intcode[z] = x+y
                self.ip += 4
            elif opcode == 2:   # Multiplication
                x,y,z = self.get_values(parameter_modes, [READ, READ, WRITE])
                self.intcode[z] = x*y
                self.ip += 4
            elif opcode == 3:   # Single int input
                x = self.get_values(parameter_modes, [WRITE])                
                if len(input_set) > 0:  # Inputs the values in input_set
                    self.intcode[x] = input_set.pop(0)
                    self.ip += 2
                elif halt_on_empty_input_set:   # Halt the program if no more items in input_set
                    if verbose >= 2:
                        print("Input set empty, halting")
                    break
                else:   # If no more values in input_set, prompts for user remaining inputs
                    user_input = input("Enter input: ")
                    self.intcode[x] = int(user_input)
                    self.ip += 2
            elif opcode == 4:   # Outputs value of only parameter and stores to output list
                src = self.get_values(parameter_modes, [READ])
                outputs.append(src)
                self.ip += 2           
                if verbose >= 1:
                    print("Output: ", src)
            elif opcode == 5:   # jump-if-true
                x,y = self.get_values(parameter_modes, [READ, READ])
                self.ip = y if x != 0 else self.ip + 3
            elif opcode == 6:   # jump-if-false
                x,y = self.get_values(parameter_modes, [READ, READ])
                self.ip = y if x == 0 else self.ip + 3
            elif opcode == 7:   # less than
                x,y,z = self.get_values(parameter_modes, [READ, READ, WRITE])
                self.intcode[z] = 1 if x < y else 0
                self.ip += 4
            elif opcode == 8:   # equals
                x,y,z = self.get_values(parameter_modes, [READ, READ, WRITE])
                self.intcode[z] = 1 if x == y else 0
                self.ip += 4
            elif opcode == 9:   # set relative base
                x = self.get_values(parameter_modes, [READ])
                self.rel_base += x
                self.ip += 2
            elif opcode == 99: # Halt opcode
                if verbose >= 1:
                    print("Opcode 99 : Halting program.")
                break
            else:
                print("Error: Unexpected opcode="+str(opcode), "ip="+str(self.ip))
                break

        return outputs


intcode_original = list(map(int, (Path(__file__).parent / 'd9_input.txt').read_text().split(',')))  # Rose this is SO smooth, dang

program = Intcode(intcode_original, memory_expand_factor=10)
print("BOOST keycode from test mode: ", program.Execute([1], verbose=0))

program = Intcode(intcode_original, memory_expand_factor=10)
print("Coordinates of distress signal: ", program.Execute([2], verbose=0))