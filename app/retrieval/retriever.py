from app.ingestion.vectorstore import get_retriever

def retrieve(state):
    retriever = get_retriever()  # lazy - called only when needed
    docs = retriever.invoke(state.question)
    return {"documents": [d.page_content for d in docs]}