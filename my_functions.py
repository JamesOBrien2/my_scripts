#!/usr/bin/python3
import numpy as np
import re 

# Function to read the coordinates from a Gaussian output file
## Input : log_file_name - Name of the Gaussian output file
## Output: coordinates - List of tuples with the element and the coordinates
#### 24-06-24

def read_gaussian_output(log_file_name):
    # Creating Arrays
    all_lines = []
    coordinates = []
    elements = []
    xyz_angs = []
    atomic_number = {"1": "H", "2": "He", "3": "Li", "4": "Be", "5": "B", "6": "C", "7": "N", "8": "O", "9": "F",   "10": "Ne", 
    "11": "Na", "12": "Mg", "13": "Al", "14": "Si", "15": "P", "16": "S", "17": "Cl", "18": "Ar", "19": "K",    "20": "Ca", 
    "21": "Sc", "22": "Ti", "23": "V", "24": "Cr", "25": "Mn", "26": "Fe", "27": "Co", "28": "Ni", "29": "Cu",  "30": "Zn", 
    "31": "Ga", "32": "Ge", "33": "As", "34": "Se", "35": "Br", "36": "Kr", "37": "Rb", "38": "Sr", "39": "Y",  "40": "Zr", 
    "41": "Nb", "42": "Mo", "43": "Tc", "44": "Ru", "45": "Rh", "46": "Pd", "47": "Ag", "48": "Cd", "49": "In",     "50": "Sn", 
    "51": "Sb", "52": "Te", "53": "I", "54": "Xe", "55": "Cs", "56": "Ba", "57": "La", "58": "Ce", "59": "Pr",  "60": "Nd", 
    "61": "Pm", "62": "Sm", "63": "Eu", "64": "Gd", "65": "Tb", "66": "Dy", "67": "Ho", "68": "Er", "69": "Tm",     "70": "Yb", 
    "71": "Lu", "72": "Hf", "73": "Ta", "74": "W", "75": "Re", "76": "Os", "77": "Ir", "78": "Pt", "79": "Au",  "80": "Hg", 
    "81": "Tl", "82": "Pb", "83": "Bi", "84": "Po", "85": "At", "86": "Rn", "87": "Fr", "88": "Ra", "89": "Ac",     "90": "Th", 
    "91": "Pa", "92": "U", "93": "Np", "94": "Pu", "95": "Am", "96": "Cm", "97": "Bk", "98": "Cf", "99": "Es",  "100": "Fm", 
    "101": "Md", "102": "No", "103": "Lr", "104": "Rf", "105": "Db", "106": "Sg", "107": "Bh", "108": "Hs",     "109": "Mt", 
    "110": "Ds", "111": "Rg", "112": "Uub", "113": "Uut", "114": "Uuq", "115": "Uup", "116": "Uuh", "117": "Uus",   "118": "Uuo"}
    
    # Open Gaussian Output File
    with open(log_file_name, "r") as file:
        all_lines = [line.strip() for line in file]

    if not all_lines:
        raise ValueError("No Data in File")

    # Find the start index for the optimized parameters
    start = next((s for s, line in enumerate(all_lines) if "Stationary point found." in line), None)
    if start is None:
        raise ValueError("No Optimized Parameters Found")

    # Find the end index for the optimized parameters
    i = 0
    start_optimized_parameters = None
    end = None
    for e in range(start, len(all_lines)):
        if "----" in all_lines[e]:
            i += 1
            if i == 6:
                start_optimized_parameters = e
            if i == 7:
                end = e
                break

    if end is None:
        raise ValueError("No End of Optimized Parameters Found")

    # Extracting the coordinates
    for line in all_lines[start_optimized_parameters + 1 : end]:
        words = line.split()
        elements.append(atomic_number.get(words[1]))
        xyz_angs.append(words[3:])

    xyz_angs = np.array(xyz_angs, float)

    coordinates = list(zip(elements, xyz_angs))
    coordinates.sort(key=lambda coord: coord[0])

    return coordinates


# Function to read the convergence data from a Gaussian output file
## Input : file_path - Name of the Gaussian output file
## Output: data - Dictionary with the convergence data
##         thresholds - Dictionary with the thresholds for the convergence data
#### 26-06-24
def convergence_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'Item\s+Value\s+Threshold\s+Converged\?\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n'
    matches = re.findall(pattern, content, re.DOTALL)

    data = {
        'Maximum Force': [],
        'RMS Force': [],
        'Maximum Displacement': [],
        'RMS Displacement': []
    }

    for match in matches:
        for line in match:
            parts = line.split()
            if len(parts) >= 3:
                key = ' '.join(parts[:-3])
                value = parts[-3]
                if value == '********':
                    value = 10.0
                else:
                    value = float(value)
                data[key].append(value)

    thresholds = {
        'Maximum Force': 0.000450,
        'RMS Force': 0.000300,
        'Maximum Displacement': 0.001800,
        'RMS Displacement': 0.001200
    }

    return data, thresholds

# Function to convert Bohr to Angstrom
## Input : bohr - Value in Bohr
## Output: Value in Angstrom
#### 15-07-24
def bohr_to_angstrom(bohr):
    return bohr * 0.529177249

# Function to convert coordinates from a .coord file to a .xyz file
## Input : input_file - Name of the .coord file
##         output_file - Name of the .xyz file
## Output: output_file - .xyz file with the coordinates
#### 15-07-24
def convert_coord_to_xyz(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    atoms = []
    for line in lines:
        if line.strip() == '$coord':
            continue
        if line.strip() == '$end':
            break
        parts = line.split()
        if len(parts) == 4:
            x, y, z, element = parts
            atoms.append((element, float(x), float(y), float(z)))

    with open(output_file, 'w') as f:
        f.write(f"{len(atoms)}\n")
        f.write("converted from coord file\n")
        for atom in atoms:
            element, x, y, z = atom
            x_ang = bohr_to_angstrom(float(x))
            y_ang = bohr_to_angstrom(float(y))
            z_ang = bohr_to_angstrom(float(z))
            f.write(f"{element.ljust(2)} {x_ang:12.6f} {y_ang:12.6f} {z_ang:12.6f}\n")

def read_xyz_or_com(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    if filename.endswith('.xyz'):
        return lines[2:]  # Skip the first two lines for XYZ files
    elif filename.endswith('.com'):
        start_index = next((i for i, line in enumerate(lines) if len(line.split()) == 2 and all(part.lstrip('-').isdigit() for part in line.split())), None)
        if start_index is not None:
            return lines[start_index + 1:]
    
    # If the file format is not recognized, return all lines
    return lines

def find_closest_to_optimised_step(convergence_data, thresholds):
    num_steps = len(next(iter(convergence_data.values())))
    total_differences = [0] * num_steps

    for key, values in convergence_data.items():
        threshold = thresholds[key]
        for i, value in enumerate(values):
            if value > threshold:
                total_differences[i] += (value - threshold)
            else:
                total_differences[i] += 0

    return total_differences.index(min(total_differences))
