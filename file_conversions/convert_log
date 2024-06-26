#!/usr/bin/python3
import argparse
import numpy as np
from my_functions import read_gaussian_output

# NB Add necessary keywords to arrays
calculation_array = ["spe", "sp", "opt", "opt freq", "ts"]
functional_array = ["wb97xd", "b3lyp", "m062x", "M062X", "pbe0", "b2plyp", "b3lyp", "b3lyp-d3bj"]
basis_set_array = ["def2svp", "def2tzvp", "def2tzvpp", "def2qzvp", "def2qzvpp", "6-31g(d,p)", "6-311g(d,p)", "6-311+g(d,p)", "6-311++g(d,p)"]
solvent_array = ["dichloromethane", "dimethylformamide", "dcm", "dmf", "h2o", "water"]
element_array = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", 
    "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", 
    "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", 
    "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"
]
grid_array = ["ultrafine", "fine", "default", "coarse", "xcoarse", "superfine"]
scf_array = ["tight", "verytight", "ultratight", "loose", "veryloose", "ultraloose"]
dispersion_array = ["d3", "d3bj", "d2"]

# Permit arguments to be used in the script
parser = argparse.ArgumentParser(description='Generate Gaussian input file')
parser.add_argument('-i', '--input', help='Log file name (with extension)', required=True)
parser.add_argument('-c', '--calculation', nargs='?', default='sp', choices=calculation_array, help='Calculation Type')
parser.add_argument('-f', '--functional', choices=functional_array, help='Functional')
parser.add_argument('-b', '--basis_set', choices=basis_set_array, help='Basis Set')
parser.add_argument('-s', '--solvent', choices=solvent_array, help='Solvent')
parser.add_argument('-ch', '--charge', nargs='?', default=0, type=int, help='Charge')
parser.add_argument('-m', '--multiplicity', nargs='?', default=1, type=int, help='Multiplicity')
parser.add_argument('-d', '--dispersion', choices=dispersion_array, help='Dispersion')
parser.add_argument('-g', '--grid', choices=grid_array, help='Integral Grid')

args = parser.parse_args()

log_file_name = args.input
calculation_type = args.calculation
functional = args.functional
basis_set = args.basis_set
solvent = args.solvent
charge = args.charge
multiplicity = args.multiplicity
dispersion = f"empiricaldispersion={args.dispersion}" if args.dispersion else ""
grid = f"int={args.grid}" if args.grid else ""

calculation_dict = {"spe": "", "sp": "", "ts": "opt=(calcfc,ts,noeigentest) freq"}
calculation_type = calculation_dict.get(calculation_type, calculation_type)
solvent_dict = {"dichloromethane": "dcm", "dimethylformamide": "dmf"}
dispersion__dict = {"d3": "gd3", "d2": "gd2", "d3bj":"gd3bj"}

coordinates = read_gaussian_output(log_file_name)

###########################
# Creating the input file #
###########################

# file extension
file_extension = "_sp.com" if calculation_type == "" else "_input.com"

# Create Gaussian Input File
# Creating output file & inserting last geometry & all keywords
file_name = log_file_name.strip(".log")
with open(f"{file_name}{file_extension}", "w") as file:
    file.write(
        f"# {calculation_type} {functional}/{basis_set} scrf=(smd,solvent={solvent}) {dispersion} {grid}\n\n"
    )
    file.write(f"{file_name}\n\n")
    file.write(f"{charge} {multiplicity}\n")
    for coord in coordinates:
        coord_str = f"{coord[0]:<2} {coord[1][0]:>12.6f} {coord[1][1]:>12.6f} {coord[1][2]:>12.6f}"
        file.write(f"{coord_str}\n")
    file.write("\n")

# Print to Command-Line
print(f"\033[0;32mFile {file_name}.com has been created with the following keywords:\033[0m")
print(
    f"# {calculation_type} {functional}/{basis_set} scrf=(smd,solvent={solvent}) {dispersion} {grid}"
)
print(f"{charge} {multiplicity}")
print("...")
print("Coordinates")
print("...")
