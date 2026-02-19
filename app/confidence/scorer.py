def compute_confidence(state):
    confidence = (
        0.4 * state.grounding_score +
        0.35 * state.completeness_score +
        0.25 * state.relevance_score
    )
    return {"confidence": confidence}
