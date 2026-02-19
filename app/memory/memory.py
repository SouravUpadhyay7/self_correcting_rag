from app.config import get_llm

llm = get_llm()

PROMPT = """
Rewrite the question to improve retrieval.

Original question: {question}
Past failed queries: {past}

Better query:
"""

def rewrite_query(state):
    new_q = llm.invoke(PROMPT.format(
        question=state.question,
        past=state.past_queries
    )).content
    
    return {
        "question": new_q,
        "past_queries": state.past_queries + [state.question],
        "failed_attempts": state.failed_attempts + 1
    }
