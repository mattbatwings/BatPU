def assemble(assembly_filename, output_filename):
    assembly_file = open(assembly_filename, 'r')
    machine_code_file = open(output_filename, 'w')
    lines = (line.strip() for line in assembly_file)

    def remove_comment(comment_symbol, line):
        return line.split(comment_symbol)[0]

    # remove comments and blanklines
    lines = [remove_comment("/", line) for line in lines]
    lines = [line for line in lines if line.strip()]
    
    # create symbols
    symbols = {'input': 0,
               'b_right': 1,
               'b_up': 2,
               'b_down': 4,
               'b_left': 8,
               'p_right': 16,
               'p_up': 32,
               'p_down': 64,
               'p_left': 128,
               'screen_opcode': 60,
               'noop': 0,
               'plot_pixel': 1,
               'delete_pixel': 2,
               'fill_screen': 4,
               'clear_screen': 8,
               'screen_x': 61,
               'screen_y': 62,
               'number_display': 63}
    
    registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
    for index, symbol in enumerate(registers):
        symbols[symbol] = index

    opcodes = ['nop', 'hlt', 'add', 'sub', 'orr', 'nor', 'and', 'xor', 'inc', 'dec', 'rsh', 'ldi', 'lod', 'str', 'jmp', 'bif']
    for index, symbol in enumerate(opcodes):
        symbols[symbol] = index

    flags = ['zero', 'msb']
    for index, symbol in enumerate(flags):
        symbols[symbol] = index
    
    def is_definition(word):
        return word == 'define'
    
    def is_label(word):
        return word[0] == '.'
    
    # add definitions and labels to symbol table
    # expects all definitions to be above assembly
    offset = 0
    for index, line in enumerate(lines):
        words = line.split()
        if is_definition(words[0]):
            symbols[words[1]] = int(words[2])
            offset += 1
        elif is_label(words[0]):
            symbols[words[0]] = index - offset
    
    # generate machine code
    def resolve(word):
        if word[0] == '#':
            return int(word[1:])
        return symbols.get(word)
    
    for i in range(offset, len(lines)):
        line = lines[i]
        words = line.split()

        # remove label, we have it in symbols now
        if is_label(words[0]):
            words = words[1:]
        
        # special ops
        if words[0] == 'lsh':
            words = ['add', words[1], words[2], words[2]]
        elif words[0] == 'cmp':
            words = ['sub', registers[0], words[1], words[2]]
        elif words[0] == 'cpy':
            words = ['add', words[1], words[2], registers[0]]
        elif words[0] == 'not':
            words = ['nor', words[1], words[2], registers[0]]

        # begin machine code translation
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
