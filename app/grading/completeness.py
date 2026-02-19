from app.config import get_llm

llm = get_llm()

PROMPT = """
Score how completely the answer addresses the question (0 to 1).

Question: {question}
Answer: {answer}

Return only a number.
"""

def score_completeness(state):
    score = llm.invoke(PROMPT.format(
        question=state.question,
        answer=state.answer
    )).content
    
    return {"completeness_score": float(score)}
