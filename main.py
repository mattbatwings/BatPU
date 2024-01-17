import mcschematic
from assembler import assemble
from simulator import simulate
from schematic import make_schematic

# for schematic
path = 'C:/Users/12483/AppData/Roaming/.minecraft/config/worldedit/schematics'
name = 'program'
version = mcschematic.Version.JE_1_18_2

def assemble_to_schematic(assembly_filename):
    machine_code_layer = 'output.mc'
    assemble(assembly_filename, machine_code_layer)
    make_schematic(machine_code_layer, path, name, version)

def assemble_and_simulate(assembly_filename):
    machine_code_layer = 'output.mc'
    assemble(assembly_filename, machine_code_layer)
    simulate(machine_code_layer)

def main():
    program = 'fib'
    
    assemble_to_schematic(f'programs/{program}.as')
    # assemble_and_simulate(f'programs/{program}.as')

if __name__ == "__main__":
    main()
