import os
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# ✅ Set your OpenRouter API key here
OPENROUTER_API_KEY = ""

# Optional but recommended headers for OpenRouter
os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


# 🔹 LLM Configuration (OpenRouter)
def get_llm():
    return ChatOpenAI(
        model="openai/gpt-4o-mini",   # you can change model here
        temperature=0,
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )


# 🔹 Local Embeddings (NO API CALLS)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
