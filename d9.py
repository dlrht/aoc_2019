from pathlib import Path

# Dictionary defining parameter behaviours for each opcode
class Intcode():
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    READ = 0
    WRITE = 1
    NONE = EXIT = 99

    op_params = {
        1 : [READ, READ, WRITE],
        2 : [READ, READ, WRITE],
        3 : [WRITE],
        4 : [READ],
        5 : [READ, READ],
        6 : [READ, READ], 
        7 : [READ, READ, WRITE],
        8 : [READ, READ, WRITE],
        9 : [READ],
        EXIT : []
    }

    def __init__(self, intcode, ip=0, rel_base=0, memory_expand_factor=10):
        self.intcode = intcode.copy()
        self.intcode.extend([0] * len(self.intcode) * memory_expand_factor)
        self.ip = ip
        self.rel_base = rel_base
    

    # Returns a len(type_of_param)-tuple with appropriate values based on parameter modes
    # Returns appropriate value if a read command or destination to write to if a write command
    def get_values(self, opcode, modes):
        num_params = len(self.op_params[opcode])
        modes.extend([0] * (num_params - len(modes)))
        values = []

        for i in range(num_params):
            val = idx = None

            if modes[i] == Intcode.POSITION_MODE:
                idx = self.intcode[self.ip+i+1]
            elif modes[i] == Intcode.IMMEDIATE_MODE:
                idx = self.ip+i+1
            elif modes[i] == Intcode.RELATIVE_MODE:
                idx = self.rel_base + self.intcode[self.ip+i+1]

            val = self.intcode[idx] if self.op_params[opcode][i] == Intcode.READ else idx

            if val is None or modes[i] == Intcode.IMMEDIATE_MODE and self.op_params[opcode][i] == Intcode.WRITE:
                print("Error getting value")

            values.append(val)

        return tuple(values)


    def Execute(self, input_set=[], new_ip=None, new_rel_base=None, halt_on_empty_input_set=False, verbose=0):
        self.ip = self.ip if new_ip == None else new_ip
        self.rel_base = self.rel_base if new_rel_base == None else new_rel_base
        outputs = []

        while (True):
            instruction = str(self.intcode[self.ip])
            opcode = int(instruction[-2:])
            parameter_modes = [int(i) for i in reversed(instruction[:-2])]

            if verbose >= 2: # For debugging
                self.print_debug(opcode, parameter_modes, input_set)

            params = self.get_values(opcode, parameter_modes)
            x = params[0] if len(params) >= 1 else None
            y = params[1] if len(params) >= 2 else None
            z = params[2] if len(params) >= 3 else None

            if opcode == 1:     # Addition
                self.intcode[z] = x + y
                self.ip += 4
            elif opcode == 2:   # Multiplication
                self.intcode[z] = x * y
                self.ip += 4
            elif opcode == 3:   # Single int input
                if len(input_set) == 0 and halt_on_empty_input_set:
                    if verbose >= 2:
                        print("Input set empty, halting")
                    break
                else:
                    self.intcode[x] = input_set.pop(0) if len(input_set) > 0 else int(input("Enter input: "))
                    self.ip += 2
            elif opcode == 4:   # Outputs value of only parameter and stores to output list
                outputs.append(x)
                self.ip += 2           
            elif opcode == 5:   # jump-if-true
                self.ip = y if x != 0 else self.ip + 3
            elif opcode == 6:   # jump-if-false
                self.ip = y if x == 0 else self.ip + 3
            elif opcode == 7:   # less than
                self.intcode[z] = 1 if x < y else 0
                self.ip += 4
            elif opcode == 8:   # equals
                self.intcode[z] = 1 if x == y else 0
                self.ip += 4
            elif opcode == 9:   # set relative base
                self.rel_base += x
                self.ip += 2
            elif opcode == 99: # Halt opcode
                if verbose >= 1:
                    print("Opcode 99 : Halting program.")
                break
            else:
                print("Error: Unexpected opcode")
                self.print_debug(opcode, parameter_modes, input_set)
                break
            
        return outputs


    def print_debug(self, opcode, param_modes, input_set):
        print("Input set:", input_set)
        print_intcode = self.intcode.copy()
        print_intcode[self.ip] = '***' + str(print_intcode[self.ip]) + '***'
        print(print_intcode, "-", "ip:"+str(self.ip), "opcode:"+str(opcode), "modes:"+str(param_modes))


intcode_original = list(map(int, (Path(__file__).parent / 'd9_input.txt').read_text().split(',')))  # Rose this is SO smooth, dang

program = Intcode(intcode_original, memory_expand_factor=10)
print("BOOST keycode from test mode: ", program.Execute([1], verbose=0))

program = Intcode(intcode_original, memory_expand_factor=10)
print("Coordinates of distress signal: ", program.Execute([2], verbose=0))