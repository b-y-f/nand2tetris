# Use: python app.py xxx.asm -> new file created includes 16bit binary code

import sys
import symbol_table as SYMBOLS


var_symbol = {}

def load_asm_and_clean(file):
    """
    This function loads an assembly file, removes empty lines and comments, and returns a list of pure
    code lines.
    :return: The function `load_asm_and_clean()` is returning a list of strings that represent the pure
    code lines of an assembly file with comments and empty lines removed.
    """
    with open(file, "r") as file:
        lines = file.readlines()

    pure_code_lines = []
    for line in lines:
        if line != "\n":
            comment_index = line.find("//")
            if comment_index == -1:
                pure_code_lines.append(line.strip())
            elif comment_index > 0:
                pure_code_lines.append(line[:comment_index].strip())

    # print(pure_code_lines)
    return pure_code_lines


def is_typeA(instruction: str) -> bool:
    """Returns the current instruction type (constant):
    A_INSTRUCTION for @ xxx, where xxx is either a decimal number or a symbol
    C_INSTRUCTION for dest = comp ; jump
    L_INSTRUCTION for (label)
    """
    return "@" in instruction


def parse_instruction(instruction: str) -> tuple:
    """
    This function takes in a string instruction and parses it to extract the C symbol, which consists of
    the destination, computation, and jump components.

    :param instruction: The parameter `instruction` is a string representing a single line of an
    assembly language instruction in the Hack computer architecture
    :type instruction: str
    :return: The function `parse_instruction` is returning a tuple containing three strings: the
    destination (dest), computation (comp), and jump (jump) parts of the input instruction string. The
    strings are stripped of any leading or trailing whitespace before being returned.
    """
    dest = ""
    comp = ""
    jump = ""

    # Check for '=' and ';' and split the string accordingly
    if "=" in instruction and ";" in instruction:
        dest, rest = instruction.split("=", 1)
        comp, jump = rest.split(";", 1)
    elif "=" in instruction:
        dest, comp = instruction.split("=", 1)
    elif ";" in instruction:
        comp, jump = instruction.split(";", 1)

    # print(dest, comp, jump)
    return dest.strip(), comp.strip(), jump.strip()





def add_key(d, key):
    d[key] = d.get(max(d.keys(), default=15), 15) + 1
    return d


def parse_line(line, cache):
    if is_typeA(line):
        # tranlate to 16 bit
        var = line[1:]
        if var.isnumeric():
            bin_ = bin(int(var))[2:].zfill(16)
            return bin_

        if var in SYMBOLS.symbols:
            var = SYMBOLS.symbols[var]
        elif var in cache:
            var = cache[var]
        else:
            # save user defined var symbols
            if var not in var_symbol:
                add_key(var_symbol, var)
                var = var_symbol[var]
            else:
                var = var_symbol[var]

        bin_ = bin(int(var))[2:].zfill(16)
        return bin_
    else:
        # C instruction
        dest, comp, jump = parse_instruction(line)
        bin_code = "".join(
            ["111", SYMBOLS.comp[comp], SYMBOLS.dest[dest], SYMBOLS.jump[jump]]
        )
        return bin_code


def parse_file(file):
    lines = load_asm_and_clean(file)
    output = []
    lines, cache = save_labels(lines)

    for l in lines:
        output.append(parse_line(l, cache))
    return output


def save_labels(lines):
    label_cache = {}
    new_lines = []
    for idx, line in enumerate(lines):
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            label_cache[label] = idx
        else:
            new_lines.append(line)

    label_cache = {k: v - i for i, (k, v) in enumerate(label_cache.items())}
    return new_lines, label_cache


def main():
    file = sys.argv[1]
    output = parse_file(file)
    with open(f"{file}.hack", "w") as file:
        for item in output:
            file.write(f"{item}\n")


main()
