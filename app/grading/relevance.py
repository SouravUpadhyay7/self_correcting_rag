from app.config import get_llm
import numpy as np

llm = get_llm()

PROMPT = """
Score document relevance to the question from 0 to 1.

Question: {question}
Document: {document}

Return only a number.
"""

def score_relevance(state):
    scores = []
    for doc in state.documents:
        s = llm.invoke(PROMPT.format(
            question=state.question,
            document=doc
        )).content
        scores.append(float(s))
    
    return {"relevance_score": float(np.mean(scores)) if scores else 0.0}
