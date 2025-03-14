def score_and_rank(target_score, toxicity_score, interaction_score, pathway_score):
    # Define weights for each score (customize based on importance)
    weights = {
        "target": 0.4,
        "toxicity": 0.3,
        "interaction": 0.2,
        "pathway": 0.1
    }

    # Calculate final score
    final_score = (
        target_score * weights["target"] +
        toxicity_score * weights["toxicity"] +
        interaction_score * weights["interaction"] +
        pathway_score * weights["pathway"]
    )

    # Make decision
    decision = "green light" if final_score >= 0.7 else "red light"
    return final_score, decision