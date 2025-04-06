import sys
sys.path.append("..")

import numpy as np
from multiprocessing import Pool
from rdkit import Chem
from rdkit.Chem import RDKFingerprint
from scipy import sparse as sp
import argparse

from src.data.descriptors.rdNormalizedDescriptors import RDKit2DNormalized


def parse_args():
    parser = argparse.ArgumentParser(description="Arguments")
    parser.add_argument("--data_path", type=str, required=True)
    parser.add_argument("--path_length", type=int, default=5)
    parser.add_argument("--n_jobs", type=int, default=32)
    return parser.parse_args()


def preprocess_dataset(args):
    with open(f"{args.data_path}/smiles.smi", 'r') as f:
        lines = f.readlines()
        smiless = [line.strip() for line in lines]

    print('Extracting fingerprints...')
    FP_list = []
    valid_smiless = []
    smiless = smiless[:2000]

    for i, smiles in enumerate(smiless):
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            print(f"[WARNING] Invalid SMILES at line {i + 1}: {smiles}")
            continue
        try:
            fp = list(RDKFingerprint(mol, minPath=1, maxPath=7, fpSize=512))
            FP_list.append(fp)
            valid_smiless.append(smiles)
        except Exception as e:
            print(f"[ERROR] Failed to generate fingerprint at line {i + 1}: {smiles}")
            print(f"        Error: {e}")
            continue

    FP_arr = np.array(FP_list)
    FP_sp_mat = sp.csc_matrix(FP_arr)

    print('Saving fingerprints...')
    sp.save_npz(f"{args.data_path}/rdkfp1-7_512.npz", FP_sp_mat)

    print('Extracting molecular descriptors...')
    generator = RDKit2DNormalized()
    with Pool(args.n_jobs) as pool:
        features_map = pool.imap(generator.process, valid_smiless)
        descriptor_array = np.array(list(features_map))

    print('Saving molecular descriptors...')
    np.savez_compressed(f"{args.data_path}/molecular_descriptors.npz", md=descriptor_array[:, 1:])

    # Optional: save the valid SMILES
    with open(f"{args.data_path}/valid_smiles.smi", "w") as out:
        for smiles in valid_smiless:
            out.write(smiles + '\n')

    print("Preprocessing completed successfully.")


if __name__ == '__main__':
    args = parse_args()
    preprocess_dataset(args)
