import mcschematic

def make_schematic(machinecode_filename, path, name, version):
    lines = open(machinecode_filename).read().splitlines()

    # swap rega <-> regb, im too lazy to fix redstone wiring
    for i, line in enumerate(lines):
        opcode = line[0:4]
        if opcode in ['0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1101']:
            pre = line[0:10]
            rega = line[10:13]
            regb = line[13:16]
            lines[i] = pre + regb + rega

    # fill to 64 lines
    noop = '0000000000000000'
    while (len(lines) < 64):
        lines.append(noop)
    
    pos = [9, -15, 2]

    schem = mcschematic.MCSchematic()

    # generate bottom bit locations for the right side
    right_side = []

    for _ in range(2):
        # row 1 and 3
        for i in range(8):
            if i % 2 == 1:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] += 2
            pos[1] = -15

        pos[2] -= 3

        for i in range(8):
            if i % 2 == 0:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] -= 2
            pos[1] = -15

        pos[2] += 2
        pos[0] += 8

        # row 2 and 4
        for i in range(8):
            if i % 2 == 1:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] += 2
            pos[1] = -15

        pos[2] -= 1

        for i in range(8):
            if i % 2 == 0:
                pos[1] += 1

            right_side.append(pos.copy())
            pos[2] -= 2
            pos[1] = -15

        pos[2] += 2
        pos[0] += 8


    # generated bottom bit locations for left side (flip z values of right side)
    left_side = []
    for bottom_bit in right_side:
        left_side.append([bottom_bit[0], bottom_bit[1], -bottom_bit[2]])

    # place barrels
    on_block = 'minecraft:barrel{Items:[{Slot:0,id:redstone,Count:1}]}'
    for pleft, pright, binary in zip(left_side, right_side, lines):
        for bit in binary[0:8]:
            if bit == '1':
                schem.setBlock(tuple(pright), on_block)
            pright[1] += 2
        
        for bit in binary[8:16][::-1]:
            if bit == '1':
                schem.setBlock(tuple(pleft), on_block)
            pleft[1] += 2

    schem.save(path, name, version)