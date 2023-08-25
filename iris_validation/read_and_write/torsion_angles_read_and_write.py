import math 
from math import degrees
import numpy as np 
import pandas as pd
import sys
import gemmi

def calculate_omega(filename) -> None:
    """outputs list of vlaues 2 elements shorter than residues"""

    st = gemmi.read_structure(filename) # can access lvels of the structure this way 

    models = []
    chains = []
    residues = []
    omega_values = []

    for model in st:
        models.append(model.name)
        for chain in model:
            omega_values.append(0) # appends 0 to the list for each new chain as an omega value is not possible here
            chains.append(chain.name)
            for residue in chain:
                residues.append(residue.name)
                next_res = chain.next_residue(residue)
                if next_res:
                    omega = gemmi.calculate_omega(residue, next_res)
                    if math.isnan(omega):
                        omega = 0 
                    else:
                        pass
                    #print(residue.name, degrees(omega))
                    omega_values.append(degrees(omega))
    
    print(f'\n-Models in file: {len(models)}')
    print(f'-Chains in model: {chains}')
    print(f'-number of residues in model: {len(residues)}')
    print(f'-number of omega torsion values: {len(omega_values)} \n(where omega angle not possible, assigned value of 0)')

    #creating a df from phi, psi and residue lists 
    angles_dict = {"Residue":residues, "Omega":omega_values}
    df = pd.DataFrame(angles_dict)

    #remove all HOH rows from df
    remove_water = df[df['Residue'].str.contains('HOH', na = False)].index 
    df.drop(index = remove_water, inplace = True)
    df = df.reset_index(drop = True)

    print(f'\nDataframe:\n{df}')

    with open('omega_values.txt', 'w') as f:
        for value in df['Omega']:
            f.write('%s\n' % value)
                
def calculate_phi_psi(filename) -> None:

    st = gemmi.read_structure(filename) # can access lvels of the structure this way 

    residues = []
    phi_values = []
    psi_values = []

    for model in st:
        for chain in model:
            for residue in chain:
                prev_res = chain.previous_residue(residue)
                next_res = chain.next_residue(residue)
                phi, psi = gemmi.calculate_phi_psi(prev_res, residue, next_res)
                if math.isnan(phi):
                    phi = 0 
                else:
                        pass
                if math.isnan(psi):
                    psi = 0 
                else:
                        pass
                #print('%s %8.2f %8.2f' % (residue.name, degrees(phi), degrees(psi)))
                residues.append(residue.name)
                phi_values.append(degrees(phi))
                psi_values.append(degrees(psi))

    print(f'-number of residues in model: {len(residues)}')
    print(f'-number of Phi torsion angles in model: {len(phi_values)}')
    print(f'-number of Psi torsion angles in model: {len(psi_values)}')

    #creating a df from phi, psi and residue lists 
    angles_dict = {"Residue":residues, "Phi":phi_values, "Psi":psi_values}
    df = pd.DataFrame(angles_dict)

    #remove all HOH rows from df
    remove_water = df[df['Residue'].str.contains('HOH', na = False)].index 
    df.drop(index = remove_water, inplace = True)
    df = df.reset_index(drop = True)

    print(f'\nDataframe:\n{df}')

    with open('phi_values.txt', 'w') as f:
        for value in df['Phi']:
            f.write('%s\n' % value)

    with open('psi_values.txt', 'w') as f:
        for value in df['Psi']:
            f.write('%s\n' % value)
                   
if len(sys.argv) == 2:
    filename = sys.argv[1]
    calculate_omega(filename)
    calculate_phi_psi(filename)