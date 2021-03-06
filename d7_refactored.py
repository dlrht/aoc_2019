from pathlib import Path
import itertools

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

class Intcode():
    def __init__(self, intcode, ip=0, rel_base=0, memory_expand_factor=10):
        self.intcode = intcode.copy()
        self.intcode.extend([0] * len(self.intcode) * memory_expand_factor)
        self.ip = ip
        self.rel_base = rel_base
    

    # Returns num_values-tuple of values following intcode[ip] depending on modes
    def get_values(self, modes, num_values):
        values = []
        for i in range(num_values):
            if modes[i] == POSITION_MODE:
                val = self.intcode[self.intcode[self.ip+i+1]]
            elif modes[i] == IMMEDIATE_MODE:
                val = self.intcode[self.ip+i+1]
            elif modes[i] == RELATIVE_MODE:
                val = self.intcode[self.rel_base+i]
            else:
                val = -1
            
            values.append(val)

        return tuple(values) if num_values > 1 else values[0]


    def Execute(self, input_set=[], new_ip=None, new_rel_base=None, halt_if_input_set_empty=False, verbose=0):
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
                x,y = self.get_values(parameter_modes, 2)
                self.intcode[self.intcode[self.ip+3]] = x+y
                self.ip += 4
            elif opcode == 2:   # Multiplication
                x,y = self.get_values(parameter_modes, 2)
                self.intcode[self.intcode[self.ip+3]] = x*y
                self.ip += 4
            elif opcode == 3:   # Single int input
                if len(input_set) > 0:  # Inputs the values in input_set
                    self.intcode[self.intcode[self.ip+1]] = input_set.pop(0)
                    self.ip += 2
                elif halt_if_input_set_empty:   # Halt the program if no more items in input_set
                    if verbose >= 2:
                        print("Input set empty, halting")
                    break
                else:   # If no more values in input_set, prompts for user remaining inputs
                    user_input = input("Enter input: ")
                    self.intcode[self.intcode[self.ip+1]] = int(user_input)
                    self.ip += 2
            elif opcode == 4:   # Outputs value of only parameter and stores to output list
                src = self.get_values(parameter_modes, 1)
                outputs.append(src)
                self.ip += 2           
                if verbose >= 1:
                    print("Output: ", src)
            elif opcode == 5:   # jump-if-true
                x,y = self.get_values(parameter_modes, 2)
                self.ip = y if x != 0 else self.ip + 3
            elif opcode == 6:   # jump-if-false
                x,y = self.get_values(parameter_modes, 2)
                self.ip = y if x == 0 else self.ip + 3
            elif opcode == 7:   # less than
                x,y = self.get_values(parameter_modes, 2)
                self.intcode[self.intcode[self.ip+3]] = 1 if x < y else 0
                self.ip += 4
            elif opcode == 8:   # equals
                x,y = self.get_values(parameter_modes, 2)
                self.intcode[self.intcode[self.ip+3]] = 1 if x == y else 0
                self.ip += 4
            elif opcode == 9:   # set relative base
                self.rel_base += self.get_values(parameter_modes, 1)
                self.ip += 2
            elif opcode == 99: # Halt opcode
                if verbose >= 1:
                    print("Opcode 99 : Halting program.")
                break
            else:
                print("Error: Unexpected opcode="+str(opcode), "ip="+str(self.ip))
                break

        return outputs


# Returns the signal given an intcode and phase settings
def find_signal(intcode, settings, feedback_loop=False):
    last_output = 0
    amps = []
    first_run = True

    # Set up an intcode program for each amp
    for i in range(len(settings)):
        amps.append(Intcode(intcode))

    # Infinite feedback loop until Amp E halts.
    while (True):
        amp_E_ip = amps[-1].ip
        amp_E_intcode = amps[-1].intcode
        if amp_E_ip >= len(amp_E_intcode) or amp_E_intcode[amp_E_ip] == 99:
            break

        # Amp A --B-C-D--> Amp E
        for i,amp in enumerate(amps):
            amp_i_input_set = []

            # Only use phase settings on first run through all amplifiers
            if first_run:
                amp_i_input_set.append(int(settings[i]))
                first_run = False if amp == amps[-1] else True
            
            # Output of last amp is input to current amp
            amp_i_input_set.append(last_output)

            # Store program state and ip
            outputs = amp.Execute(input_set=amp_i_input_set, halt_if_input_set_empty=True, verbose=0)
            
            # Output of current amp is input to next amp
            if len(outputs) > 0:
                last_output = outputs[-1]

        if not feedback_loop:
            break

    return last_output


# Returns a tuple of (highest_signal, respective_phase_settings) given a set of phase_nums. Length of phase_nums is # of amps.
def find_highest_signal(intcode, phase_nums, feedback_loop=False):
    highest_signal = (0, [])

    for settings in itertools.permutations(phase_nums): # Shafin this is SO smooth, dang
        output = find_signal(intcode, settings, feedback_loop=feedback_loop)

        if output > highest_signal[0]:
            highest_signal = (output, settings)

    return highest_signal


intcode_original = list(map(int, (Path(__file__).parent / 'd7_input.txt').read_text().split(',')))  # Rose this is SO smooth, dang
print("Highest Signal: ", find_highest_signal(intcode_original, [0,1,2,3,4], feedback_loop=False))
print("Highest Signal with Feedback Loop: ", find_highest_signal(intcode_original, [5,6,7,8,9], feedback_loop=True))