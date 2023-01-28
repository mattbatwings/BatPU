def main():    
    assembly_file = open('fib.as', 'r')
    machine_code_file = open('output.mc', 'w')
    lines = (line.rstrip() for line in assembly_file)

    def remove_comment(comment_symbol, line):
        for index, char in enumerate(line):
            if char == comment_symbol:
                return line[:index]
        return line

    # remove comments and blanklines
    lines = [remove_comment("/", line) for line in lines]
    lines = [line for line in lines if line]
    
    # add registers, opcodes, and flags to symbols
    symbols = {}
    
    registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
    for index, symbol in enumerate(registers):
        symbols[symbol] = index

    opcodes = ['nop', 'hlt', 'add', 'sub', 'orr', 'nor', 'and', 'xor', 'inc', 'dec', 'rsh', 'ldi', 'lod', 'str', 'jmp', 'bif']
    for index, symbol in enumerate(opcodes):
        symbols[symbol] = index

    flags = ['zero', 'carry']
    for index, symbol in enumerate(flags):
        symbols[symbol] = index

    special_opcodes = ['lsh', 'cmp', 'cpy', 'not']
    all_opcodes = opcodes + special_opcodes
    
    # add definitions and labels to symbol table
    offset = 0
    for index, line in enumerate(lines):
        words = line.split()
        if words[0] == 'define':
            symbols[words[1]] = int(words[2])
            offset += 1
        elif words[0] not in all_opcodes:
            symbols[words[0]] = index - offset

    def resolve(word):
        if word[0] == '#':
            return int(word[1:])
        return symbols.get(word)
    
    # generate machine code
    for i in range(offset, len(lines)):
        line = lines[i]
        words = line.split()
        
        machine_code = 0

        # remove label, we have it in symbols now
        if words[0] not in all_opcodes:
            words = words[1:]

        opcode = words[0]
        machine_code = (symbols[opcode] << 12)

        words = [resolve(word) for word in words]

        if opcode in ['add', 'sub', 'orr', 'nor', 'and', 'xor', 'inc', 'dec', 'rsh', 'ldi', 'lod']: # Reg Dest
            machine_code |= (words[1] << 9)
            
        if opcode in ['add', 'sub', 'orr', 'nor', 'and', 'xor', 'inc', 'dec', 'rsh']: # Reg A
            machine_code |= (words[2] << 3)
        elif opcode in ['str']:
            machine_code |= (words[1] << 3)

        if opcode in ['add', 'sub', 'orr', 'nor', 'and', 'xor']: # Reg B
            machine_code |= words[3]

        if opcode in ['ldi']: # Immediate
            machine_code |= words[2]
        
        if opcode in ['jmp']: # Address and Flag
            machine_code |= words[1]
        elif opcode in ['bif']:
            machine_code |= (words[1] << 6)
            machine_code |= words[2]

        as_string = bin(machine_code)[2:].rjust(16, '0')
        machine_code_file.write(f'{as_string}\n')


if __name__ == '__main__':
    main()