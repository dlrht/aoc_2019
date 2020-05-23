from pathlib import Path
import itertools

POSITION_MODE = 0
IMMEDIATE_MODE = 1

# Returns num_values-tuple of values following intcode[ip] depending on modes
def get_values(intcode, ip, modes, num_values):
    values = []
    for i in range(num_values):
        values.append(intcode[intcode[ip+i+1]] if modes[i] == POSITION_MODE else intcode[ip+i+1])

    return tuple(values) if num_values > 1 else values[0]


# Executes an intcode program intcode_original starting at ip
# Returns a tuple of (program outputs from opcode 4, ip location after execution, modified intcode after execution)
def run_intcode(intcode_original, ip=0, noun=None, verb=None, input_set=[], halt_if_input_set_empty=False, verbose=0):
    intcode = intcode_original.copy()   # Never affect input incode, return modified intcode

    if noun is not None:
        intcode[1] = noun
    if verb is not None:
        intcode[2] = verb

    outputs = []

    while (True):
        instruction = str(intcode[ip])
        opcode = int(instruction[-2:])

        parameter_modes = [0] * 3
        for i,mode in enumerate(reversed(instruction[:-2])):
            parameter_modes[i] = int(mode)

        if verbose >= 2: # For debugging
            print("Input set:", input_set)
            print_intcode = intcode.copy()
            print_intcode[ip] = '***' + str(print_intcode[ip]) + '***'
            print(print_intcode, "-", "ip:"+str(ip), "opcode:"+str(opcode), "modes:"+str(parameter_modes))

        if opcode == 1: # Addition
            x,y = get_values(intcode, ip, parameter_modes, 2)
            intcode[intcode[ip+3]] = x+y
            ip += 4
        elif opcode == 2: # Multiplication
            x,y = get_values(intcode, ip, parameter_modes, 2)
            intcode[intcode[ip+3]] = x*y
            ip += 4
        elif opcode == 3: # Single int input
            if len(input_set) > 0:  # Inputs the values in input_set
                intcode[intcode[ip+1]] = input_set.pop(0)
                ip += 2
            elif halt_if_input_set_empty:   # Halt the program if no more items in input_set
                if verbose >= 2:
                    print("Input set empty, halting")
                break
            else:   # If no more values in input_set, prompts for user remaining inputs
                user_input = input("Enter input: ")
                intcode[intcode[ip+1]] = int(user_input)
                ip += 2
        elif opcode == 4: # Outputs value of only parameter and stores to output list
            src = get_values(intcode, ip, parameter_modes, 1)
            outputs.append(src)
            ip += 2           
            if verbose >= 1:
                print("Output: ", src)
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
        elif opcode == 99: # Halt opcode
            if verbose >= 1:
                print("Opcode 99 : Halting program.")
            break
        else:
            print("Error: Unexpected opcode="+str(opcode), "ip="+str(ip))
            break

    return outputs, ip, intcode


# Returns the signal given an intcode and phase settings
def find_signal(intcode, settings, feedback_loop=False):
    last_output = 0
    amps = []
    first_run = True

    # Set up an intcode program for each amp : (ip, intcode)
    for i in range(len(settings)): 
        amps.append((0, intcode.copy()))

    # Infinite feedback loop until Amp E halts.
    while (True):
        amp_E_ip = amps[-1][0]
        amp_E_intcode = amps[-1][1]

        # Amp E has halted, signal is last output (from amp E). Exit loop.
        if amp_E_ip >= len(amp_E_intcode) or amp_E_intcode[amp_E_ip] == 99:
            break

        # Amp A ---> Amp E
        for i,amp in enumerate(amps):
            amp_i_ip = amp[0]
            amp_i_intcode = amp[1]
            amp_i_input_set = []

            # Only use phase settings on first run through all amplifiers
            if first_run:
                amp_i_input_set.append(int(settings[i]))
                first_run = False if i == len(amps) - 1 else True
            
            # Output of last amp is input to current amp
            amp_i_input_set.append(last_output)

            # Store program state and ip
            outputs, new_ip, new_intcode = run_intcode(amp_i_intcode, 
                                                        ip=amp_i_ip, 
                                                        input_set=amp_i_input_set, 
                                                        halt_if_input_set_empty=True, 
                                                        verbose=0)
            
            # Output of current amp is input to next amp
            if len(outputs) > 0:
                last_output = outputs[-1]

            # Update program for amp
            amps[i] = (new_ip, new_intcode)

        if not feedback_loop:
            break

    return last_output


# Returns a tuple of (highest_signal, respective_phase_settings) given a set of phase_nums. Length of settings is # of amps.
def find_highest_signal(intcode, phase_nums, feedback_loop=False):
    highest_signal = (0, [])

    for settings in itertools.permutations(phase_nums):
        output = find_signal(intcode, settings, feedback_loop=feedback_loop)

        if output > highest_signal[0]:
            highest_signal = (output, settings)

    return highest_signal


intcode_original = list(map(int, (Path(__file__).parent / 'd7_input.txt').read_text().split(',')))  # Rose this is SO smooth, dang
print("Highest Signal: ", find_highest_signal(intcode_original, [0,1,2,3,4], feedback_loop=False))
print("Highest Signal with Feedback Loop: ", find_highest_signal(intcode_original, [5,6,7,8,9], feedback_loop=True))