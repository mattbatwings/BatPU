import sys

def main():
  debug = True

  if len(sys.argv) != 2:
    'Usage: simulator.py {machine code file}'
    exit()

  opcode_labels = {
    0: 'nop',
    1: 'hlt',
    2: 'add',
    3: 'sub',
    4: 'orr',
    5: 'nor',
    6: 'and',
    7: 'xor',
    8: 'inc',
    9: 'dec',
    10: 'rsh',
    11: 'ldi',
    12: 'lod',
    13: 'str',
    14: 'jmp',
    15: 'bif' }
  
  NUM_REGS = 8
  NUM_FLAGS = 2
  DATA_SIZE = 2**6
  PROGRAM_SIZE = 2**6

  registers = [0] * NUM_REGS
  flags = [False] * NUM_FLAGS
  data_memory = [0] * DATA_SIZE
  program_memory = [0] * PROGRAM_SIZE
  pc = 0

  mc_file = sys.argv[1]
  lines = open(mc_file).read().splitlines()
  
  for index, value in enumerate(lines):
    program_memory[index] = int(value, base=2)

  running = True
  cycles = 0

  screen_size = 32
  screen = [[0 for _ in range(screen_size)] for _ in range(screen_size)]
  
  while running:
    registers[0] = 0

    instruction = program_memory[pc]

    opcode = instruction >> 12
    regDest = (instruction >> 9) & 7
    regA = (instruction >> 3) & 7
    regB = instruction & 7
    immediate = instruction & 255
    address = instruction & 63
    flag = (instruction >> 6) & 1

    opcode = opcode_labels[opcode]
    match (opcode):
      case 'hlt':
        running = False
      case 'add':
        registers[regDest] = registers[regA] + registers[regB]
      case 'sub':
        registers[regDest] = registers[regA] - registers[regB]
      case 'orr':
        registers[regDest] = registers[regA] | registers[regB]
      case 'nor':
        registers[regDest] = ~(registers[regA] | registers[regB])
      case 'and':
        registers[regDest] = registers[regA] & registers[regB]
      case 'xor':
        registers[regDest] = registers[regA] ^ registers[regB]
      case 'inc':
        registers[regDest] = registers[regA] + 1
      case 'dec':
        registers[regDest] = registers[regA] - 1
      case 'rsh':
        registers[regDest] = registers[regA] >> 1
      case 'ldi':
        registers[regDest] = immediate
      case 'lod':
        registers[regDest] = data_memory[registers[7]] 
      case 'str':
        data_memory[registers[7]] = registers[regA]
      case 'jmp':
        pc = address
      case 'bif':
        pc = address if flags[flag] else pc + 1

    if opcode not in ['jmp', 'bif']:
      pc += 1

    cycles += 1

    if opcode in ['add', 'sub', 'orr', 'nor', 'and', 'xor', 'inc', 'dec', 'rsh']:
      flags[0] = True if (registers[regDest] == 0) else False
      registers[0] = 0
      flags[1] = True if (registers[regB] > registers[regA]) else False
      if opcode == 'rsh' and (registers[regA] % 2 == 1):
        flags[1] = True

    number_display = data_memory[63]
    screen_x = data_memory[62]
    screen_y = data_memory[61]
    screen_opcode = data_memory[60]

    match (screen_opcode):
      case 1: # clear screen
        screen = [[0 for _ in range(screen_size)] for _ in range(screen_size)]
      case 2:
        screen[screen_y][screen_x] = 1
      case 3:
        screen[screen_y][screen_x] = 0
    
    if debug:
      print(f'Cycle #{cycles}:')
      print(f'Instruction: {opcode}')
      print('----------------')
      for index, value in enumerate(registers):
        print(f'Register {index}: {value}')
      print(f'Flag Zero: {flags[0]}')
      print(f'Flag Carry: {flags[1]}')
      print(f'Data Memory: {data_memory}')
    
    print(f'NUMBER DISPLAY: {number_display}')
    print('SCREEN:')
    for row in screen:
      print(row)
    print()

if __name__ == '__main__':
    main()