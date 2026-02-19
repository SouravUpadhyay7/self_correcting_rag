from app.config import get_llm

llm = get_llm()

PROMPT = """
Score how well the answer is supported by the documents (0 to 1).

Documents: {documents}
Answer: {answer}

Return only a number.
"""

def score_grounding(state):
    score = llm.invoke(PROMPT.format(
        documents=state.documents,
        answer=state.answer
    )).content
    
    return {"grounding_score": float(score)}
