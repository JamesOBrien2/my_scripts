#!/usr/bin/python3
from rdkit import Chem
from rdkit.Chem import AllChem
import sys

def smiles_to_3d(smiles):
    my_mol = Chem.MolFromSmiles(smiles)
    my_mol_with_H = Chem.AddHs(my_mol)
    AllChem.EmbedMolecule(my_mol_with_H)
    AllChem.MMFFOptimizeMolecule(my_mol_with_H)
    return my_mol_with_H

def generate_gaussian_input(mol, title="Molecule", method="m062x", basis_set="def2svp"):
    gaussian_input = f"%chk={title}.chk\n"
    gaussian_input += f"%mem=8GB\n"
    gaussian_input += f"%nproc=4\n"
    gaussian_input += f"# {method}/{basis_set} opt freq\n\n" # Assuming methodology
    gaussian_input += f"{title}\n\n"
    gaussian_input += "0 1\n"  # Assuming neutral singlet state
    
    for atom in mol.GetAtoms():
        pos = mol.GetConformer().GetAtomPosition(atom.GetIdx())
        gaussian_input += f"{atom.GetSymbol():2s}  {pos.x:10.6f}  {pos.y:10.6f}  {pos.z:10.6f}\n"
    
    gaussian_input += "\n"
    return gaussian_input

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <SMILES>")
        sys.exit(1)

    smiles = sys.argv[1]
    
    # Generate 3D structure from SMILES (with hydrogens)
    mol_3d = smiles_to_3d(smiles)
    
    # Generate Gaussian input file content
    gaussian_input = generate_gaussian_input(mol_3d, title="SMILES_Molecule")
    
    # Print Gaussian input file content
    print(gaussian_input)
    
    # Optionally, save to a file
    with open("molecule.gjf", "w") as f:
        f.write(gaussian_input)

if __name__ == "__main__":
    main()
