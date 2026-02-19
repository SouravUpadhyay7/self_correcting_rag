from app.config import get_llm
import numpy as np

llm = get_llm()

PROMPT = """
You are a strict relevance judge. Score how relevant this document chunk is to answering the question from 0 to 1.

Rules:
- If the document has no relation to the question → score 0.0
- If the document is loosely related but doesn't help answer → score 0.1 to 0.3
- If the document partially helps answer the question → score 0.4 to 0.6
- If the document directly contains the answer → score 0.8 to 1.0

Question: {question}
Document: {document}

Return only a single decimal number between 0 and 1. Nothing else.
"""

def score_relevance(state):
    scores = []
    for doc in state.documents:
        s = llm.invoke(PROMPT.format(
            question=state.question,
            document=doc
        )).content.strip()
        scores.append(float(s))
    return {"relevance_score": float(np.mean(scores)) if scores else 0.0}