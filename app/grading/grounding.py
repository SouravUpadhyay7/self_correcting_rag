from app.config import get_llm

llm = get_llm()

PROMPT = """
You are a strict fact-checker. Score how well the answer is grounded in the provided documents from 0 to 1.

Rules:
- If the answer contains claims NOT present in the documents → score 0.0 to 0.3
- If the answer says "not found" or "not mentioned" and the docs confirm this → score 0.7
- If every claim in the answer is directly supported by the documents → score 0.9 to 1.0
- If the answer adds outside knowledge not in the documents → penalize heavily

Documents: {documents}
Answer: {answer}

Return only a single decimal number between 0 and 1. Nothing else.
"""

def score_grounding(state):
    score = llm.invoke(PROMPT.format(
        documents=state.documents,
        answer=state.answer
    )).content.strip()
    return {"grounding_score": float(score)}