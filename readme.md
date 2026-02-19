# 🧠 Self-Correcting RAG Agent

> *A research-level Retrieval Augmented Generation system that retrieves knowledge, generates answers, evaluates its own outputs, and iteratively self-corrects with confidence scoring and memory support.*

---

## 🎯 What is this?

Most RAG systems retrieve → generate → done. This system goes further:

**Retrieve → Grade → Generate → Self-Evaluate → Fix if needed → Score Confidence → Respond**

If the answer is bad, the agent **rewrites the query and tries again** — automatically. It also tracks hallucination, completeness, and grounding in real time.

---

## 🏗️ Architecture Flow

```
User Question
      │
      ▼
┌─────────────────┐
│  Retrieve Docs  │◄────────────────────────┐
│  (ChromaDB)     │                         │
└────────┬────────┘                         │
         │                                  │ Rewrite Query
         ▼                                  │
┌─────────────────┐                         │
│  Grade Docs     │──── Not Relevant? ──────┘
│  (Relevance)    │
└────────┬────────┘
         │ Relevant
         ▼
┌─────────────────┐
│ Generate Answer │
│  (OpenRouter    │
│     LLM)        │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────┐
│      Self-Evaluation         │
│  ┌──────────────────────┐    │
│  │  Relevance Score     │    │
│  │  Grounding Score     │    │
│  │  Completeness Score  │    │
│  └──────────────────────┘    │
└────────┬─────────────────────┘
         │
    ┌────┴────┐
    │         │
  Pass      Fail
    │         │
    │         ▼
    │   ┌──────────────┐
    │   │ Revise Query │──► Retry (max 2x)
    │   └──────────────┘
    │         │
    │    Too Many Failures
    │         │
    ▼         ▼
┌─────────────────────┐
│  Confidence Score   │
│  (Weighted Average) │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Final Response    │
│  Answer + Scores +  │
│  Query History      │
└─────────────────────┘
```

---

## 📁 Project Structure

```
self_correcting_rag/
│
├── .env                       # 🔐 API keys (never commit this)
├── .gitignore                 # 🚫 Ignores .env, .venv, chroma_db
├── requirements.txt           # 📦 All dependencies
├── README.md
│
├── app/
│   ├── config.py              # 🔌 LLM + Embeddings setup (OpenRouter + HuggingFace)
│   ├── state.py               # 🧾 LangGraph shared state (question, docs, answer, scores)
│   │
│   ├── ingestion/
│   │   ├── loader.py          # 📥 PDF loader (PyPDF)
│   │   ├── splitter.py        # ✂️  Text chunker (RecursiveCharacterTextSplitter)
│   │   └── vectorstore.py     # 🗄️  ChromaDB vector store (lazy loading)
│   │
│   ├── retrieval/
│   │   └── retriever.py       # 🔎 Similarity search retriever (lazy loading)
│   │
│   ├── generation/
│   │   └── generator.py       # ✍️  LLM answer generation from context
│   │
│   ├── grading/
│   │   ├── relevance.py       # 📚 Are retrieved docs relevant?
│   │   ├── grounding.py       # ⚓ Is answer grounded in docs?
│   │   └── completeness.py    # ✅ Does answer fully address the question?
│   │
│   ├── confidence/
│   │   └── confidence_scorer.py  # 📊 Weighted confidence score
│   │
│   ├── memory/
│   │   └── memory.py          # 🧠 Conversation history tracking
│   │
│   ├── graph/
│   │   └── workflow.py        # 🔁 LangGraph agent loop (CORE)
│   │
│   └── ui/
│       └── streamlit_app.py   # 🖥️  Streamlit frontend
│
└── data/
    ├── chroma_db/             # 🗄️  Persistent vector database (auto-generated)
    └── temp.pdf               # 📄 Temporary uploaded file (auto-generated)
```

---

## ⚙️ How Each Component Works

### 🔌 `config.py` — Model Setup
Central configuration for all AI models. Connects to **OpenRouter** for LLM access and **HuggingFace** (`all-MiniLM-L6-v2`) for embeddings. Every module imports from here.

### 🧾 `state.py` — Shared Agent Memory
Pydantic model that acts as a "shared notebook" flowing through LangGraph. Stores: question, retrieved documents, generated answer, all scores, failed attempts, and past queries.

### 📥 `ingestion/` — Document Pipeline
1. **loader.py** — Reads uploaded PDFs using PyPDF
2. **splitter.py** — Breaks text into overlapping chunks using `RecursiveCharacterTextSplitter`
3. **vectorstore.py** — Converts chunks to embeddings and stores in ChromaDB. Uses **lazy loading** (no global objects) to prevent stale collection errors.

### 🔎 `retrieval/retriever.py` — Context Fetcher
Uses lazy loading to fetch a fresh retriever on every call. Searches ChromaDB with `k=3` most similar chunks.

### ✍️ `generation/generator.py` — Answer Creator
Takes the question + retrieved chunks → generates a grounded answer using the LLM.

### ⭐ `grading/` — The Self-Correction Brain
| File | What it checks | Score range |
|------|----------------|-------------|
| `relevance.py` | Are retrieved docs useful for the question? | 0.0 – 1.0 |
| `grounding.py` | Is the answer based on the docs (no hallucination)? | 0.0 – 1.0 |
| `completeness.py` | Does the answer fully address the question? | 0.0 – 1.0 |

### 📊 `confidence/confidence_scorer.py` — Trust Meter
Combines the three scores into a single weighted confidence percentage shown to the user.

### 🔁 `graph/workflow.py` — LangGraph Agent Loop
The core file. Defines the cyclic graph:
- If docs aren't relevant → rewrite query → retrieve again
- If answer is poor → regenerate
- After max 2 retries → accept best answer and score it

---

## 🚀 Getting Started

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/self-correcting-rag-langgraph
cd self-correcting-rag-langgraph
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=your_openrouter_key_here
```
Get your free API key at [openrouter.ai](https://openrouter.ai)

### 4. Run the App
```bash
streamlit run app/ui/streamlit_app.py --server.fileWatcherType none
```

Then open `http://localhost:8501` in your browser.

---

## 📦 Requirements

```
langchain
langgraph
langchain-community
langchain-openai
langchain-text-splitters
chromadb
sentence-transformers
faiss-cpu
pydantic
streamlit
pypdf
numpy
torch
transformers
openai
python-dotenv
```

---

## 🧪 Testing Hallucination & Scores

Use these questions to stress-test the agent:

| Test Type | Question | Expected Behaviour |
|-----------|----------|--------------------|
| ✅ Grounding | *"What was the exact misdiagnosis reduction rate?"* | High grounding, correct number |
| 🎯 Hallucination trap | *"What did GPT-5 achieve in medical exams?"* | Refuses to answer, low confidence |
| 📉 Completeness | *"How much does AI reduce drug timelines specifically?"* | Low completeness (vague doc section) |
| 📊 Relevance | *"What % of US equity trading is algorithmic?"* | Low relevance (off-topic section) |
| 🔀 Contradiction | *"What is the consensus AI accuracy for pneumonia?"* | Flags contradictory information |

---

## 📊 Score Interpretation

| Score | 🟢 High (≥0.85) | 🟡 Medium (0.65–0.85) | 🔴 Low (<0.65) |
|-------|-----------------|----------------------|----------------|
| **Relevance** | Retrieved docs are on-topic | Partially relevant | Off-topic retrieval |
| **Grounding** | No hallucination | Some unsupported claims | Hallucinated answer |
| **Completeness** | Fully answered | Partial answer | Incomplete/refused |
| **Confidence** | Trust the answer | Use with caution | Verify externally |

---

## 🩺 Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: langchain.text_splitter` | `pip install langchain-text-splitters` |
| `chromadb.errors.NotFoundError` | Delete `data/chroma_db/*` and re-upload PDF |
| `RuntimeError: no running event loop` | Add `--server.fileWatcherType none` to run command |
| `ImportError: chromadb` | `pip install chromadb` inside venv |
| `ImportError: sentence_transformers` | `pip install sentence-transformers` inside venv |
| Duplicate chunks retrieved | Clear `data/chroma_db/` before re-indexing |

---

## 🧩 Why This Architecture is Advanced

| Feature | Standard RAG | This Project |
|---------|-------------|--------------|
| Retrieval | ✅ | ✅ |
| Generation | ✅ | ✅ |
| Self-correction loop | ❌ | ✅ |
| Hallucination detection | ❌ | ✅ |
| Multi-criteria grading | ❌ | ✅ |
| Query reformulation | ❌ | ✅ |
| Confidence scoring | ❌ | ✅ |
| Conversation memory | ❌ | ✅ |
| LangGraph agent architecture | ❌ | ✅ |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | OpenRouter (GPT-4o-mini) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| Agent Framework | LangGraph |
| RAG Framework | LangChain |
| Frontend | Streamlit |
| PDF Parsing | PyPDF |

---

*Built with LangChain · LangGraph · ChromaDB · HuggingFace · OpenRouter · Streamlit*