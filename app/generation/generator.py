from app.config import get_llm

llm = get_llm()

PROMPT = """
You are a precise assistant. Answer using ONLY the provided context below.

Important rules:
- Read ALL context carefully before answering
- If the question asks about a specific product or feature, identify the EXACT product that has it
- Do NOT mix up different products — each product has its own distinct features
- If multiple products are mentioned, clearly distinguish between them
- If the answer is not in the context, say "The context does not provide information about this"
- Never guess or add information not present in the context

Context:
{context}

Question:
{question}

Answer:
"""

def generate(state):
    context = "\n\n".join(state.documents)
    response = llm.invoke(PROMPT.format(
        context=context,
        question=state.question
    ))
    return {"answer": response.content}