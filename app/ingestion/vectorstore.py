from langchain_community.vectorstores import Chroma
from app.config import get_embeddings

# Persistent storage folder
CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "rag_collection"

# Initialize embeddings
embeddings = get_embeddings()

def get_vectorstore():
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

def add_documents(texts):
    vs = get_vectorstore()
    existing = vs.get()
    if len(existing["ids"]) > 0:
        vs.delete_collection()
    # Always create fresh and add
    get_vectorstore().add_documents(texts)

def get_retriever():
    vs = get_vectorstore()
    return vs.as_retriever(search_kwargs={"k": 3})