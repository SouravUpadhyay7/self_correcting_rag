from app.config import get_llm

llm = get_llm()

PROMPT = """
Answer using ONLY the provided context.

Context:
{context}

Question:
{question}
"""

def generate(state):
    context = "\n\n".join(state.documents)
    response = llm.invoke(PROMPT.format(
        context=context,
        question=state.question
    ))
    return {"answer": response.content}
