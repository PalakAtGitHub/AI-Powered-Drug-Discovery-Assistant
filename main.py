from drug_target_interaction import predict_drug_target_interaction
from toxicity_prediction import predict_toxicity
from drug_drug_interaction import predict_drug_drug_interaction
from pathway_analysis import analyze_pathways
from scoring_ranking import score_and_rank

def evaluate_drug(drug_smiles, disease):
    # Step 1: Predict drug-target interaction
    target_score = predict_drug_target_interaction(drug_smiles, disease)

    # Step 2: Predict toxicity
    toxicity_score = predict_toxicity(drug_smiles)

    # Step 3: Predict drug-drug interactions
    interaction_score = predict_drug_drug_interaction(drug_smiles)

    # Step 4: Analyze pathways
    pathway_score = analyze_pathways(drug_smiles, disease)

    # Step 5: Aggregate scores and make a decision
    final_score, decision = score_and_rank(target_score, toxicity_score, interaction_score, pathway_score)

    return {
        "target_score": target_score,
        "toxicity_score": toxicity_score,
        "interaction_score": interaction_score,
        "pathway_score": pathway_score,
        "final_score": final_score,
        "decision": decision
    }

# Example usage
if __name__ == "__main__":
    drug_smiles = "CCO"  # Example SMILES string (ethanol)
    disease = "Alzheimer's"  # Example disease
    result = evaluate_drug(drug_smiles, disease)
    print(result)