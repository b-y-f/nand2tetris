# Use: python app.py xxx.asm -> new file created includes 16bit binary code

import re
import sys
import symbol_table as symbols

def load_asm_and_clean():
    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    pure_code_lines = []
    for line in lines:
        if line != '\n':
            comment_index = line.find("//")
            if comment_index == -1:
                pure_code_lines.append(line.strip())
            elif comment_index > 0:
                pure_code_lines.append(line[:comment_index].strip())

    # print(pure_code_lines)
    return pure_code_lines

def instruction_type():
    """Returns the current instruction type (constant):
    A_INSTRUCTION for @ xxx, where xxx is either a decimal number or a symbol 
    C_INSTRUCTION for dest = comp ; jump
    L_INSTRUCTION for (label)
    """
    pass

def symbol(): 
    # Returns the instruction’s symbol (string) 
    pass
def dest(): 
    # Returns the instruction’s dest field (string) 
    pass
    
def comp(): 
    # Returns the instruction’s comp field (string) 
    pass
def jump(): 
    # Returns the instruction’s jump field (string)
    pass

def parse_line(line):
    if line in symbols:
        pass

    first_char = line[0]
    if first_char == '@':
        # tranlate to 16 bit
        bin_ = bin(int(line[1:]))[2:].zfill(16)
        print(bin_)
        return bin_
        
lines = load_asm_and_clean()

for l in lines:
    parse_line(l)
    break

