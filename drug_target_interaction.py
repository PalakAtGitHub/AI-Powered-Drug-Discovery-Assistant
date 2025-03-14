import requests
# WITH API
def predict_drug_target_interaction(drug_smiles, disease):
    # Use SwissTargetPrediction API or similar
    url = "http://www.swisstargetprediction.ch/api/"
    payload = {"smiles": drug_smiles}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        # Extract relevant score for the disease target
        target_score = data.get("score", 0)  # Placeholder logic
        return target_score
    else:
        return 0  # Default score if prediction fails
    

import joblib  # For loading ML models
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

# Load a pre-trained ML model for drug-target interaction (random forest as an example)
model = joblib.load("models/drug_target_model.pkl")

def featurize_molecule(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(2048)  # Default vector if invalid
    return np.array(AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048))

def predict_drug_target_interaction(drug_smiles):
    features = featurize_molecule(drug_smiles)
    target_score = model.predict([features])[0]  # ML-based score
    return target_score
