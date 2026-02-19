from app.config import get_llm

llm = get_llm()

PROMPT = """
You are a strict evaluator. Score how completely the answer addresses the question from 0 to 1.

Rules:
- If the answer says "not found", "not mentioned", or "no information" → score 0.0
- If the answer partially addresses the question → score 0.3 to 0.6
- If the answer fully and specifically addresses all parts of the question → score 0.8 to 1.0

Question: {question}
Answer: {answer}

Return only a single decimal number between 0 and 1. Nothing else.
"""

def score_completeness(state):
    score = llm.invoke(PROMPT.format(
        question=state.question,
        answer=state.answer
    )).content.strip()
    return {"completeness_score": float(score)}