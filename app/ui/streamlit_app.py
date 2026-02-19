import sys
import shutil
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from app.graph.workflow import build_graph
from app.ingestion.loader import load_pdf
from app.ingestion.splitter import split_docs
from app.ingestion.vectorstore import add_documents

app = build_graph()

# Page config
st.set_page_config(page_title="Self-Correcting RAG", page_icon="🧠", layout="centered")

# Header
st.title("🧠 Self-Correcting RAG Agent")
st.markdown("*Upload a PDF and ask questions — the agent self-corrects until it finds the best answer.*")
st.divider()

# Track which PDF is already indexed
if "indexed_file" not in st.session_state:
    st.session_state.indexed_file = None

# Upload section
st.subheader("📄 Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    if st.session_state.indexed_file != uploaded_file.name:
        with st.spinner("📥 Indexing your PDF..."):
            with open("data/temp.pdf", "wb") as f:
                f.write(uploaded_file.read())
            docs = load_pdf("data/temp.pdf")
            split = split_docs(docs)
            add_documents(split)
            st.session_state.indexed_file = uploaded_file.name
        st.success(f"✅ **{uploaded_file.name}** indexed successfully!")
    else:
        st.info(f"📌 **{uploaded_file.name}** is already indexed. Ask away!")

    # Clear index button
    if st.button("🗑️ Clear Index & Re-upload", type="secondary"):
        if os.path.exists("data/chroma_db"):
            shutil.rmtree("data/chroma_db")
        st.session_state.indexed_file = None
        st.success("✅ Index cleared! Upload a new PDF.")
        st.rerun()

st.divider()

# Query section
st.subheader("💬 Ask a Question")
query = st.text_input("Type your question here...", placeholder="e.g. What are the main advantages of cloud computing?")

if st.button("🚀 Run Agent", use_container_width=True):
    if not uploaded_file:
        st.warning("⚠️ Please upload a PDF first!")
    elif not query:
        st.warning("⚠️ Please enter a question!")
    else:
        with st.spinner("🤔 Agent is thinking and self-correcting..."):
            result = app.invoke({"question": query})

        st.divider()

        # Answer
        st.subheader("💡 Answer")
        st.success(result["answer"])

        # Confidence meter
        st.subheader("📊 Confidence Score")
        confidence = result["confidence"]
        st.progress(confidence)
        if confidence >= 0.85:
            st.markdown(f"**{confidence:.2%}** 🟢 High confidence")
        elif confidence >= 0.65:
            st.markdown(f"**{confidence:.2%}** 🟡 Medium confidence")
        else:
            st.markdown(f"**{confidence:.2%}** 🔴 Low confidence")

        # Scores breakdown
        st.subheader("🔍 Score Breakdown")
        col1, col2, col3 = st.columns(3)
        col1.metric("📎 Relevance", f"{result['relevance_score']:.2f}")
        col2.metric("⚓ Grounding", f"{result['grounding_score']:.2f}")
        col3.metric("✅ Completeness", f"{result['completeness_score']:.2f}")

        # Self-correction attempts
        if result.get("failed_attempts", 0) > 0:
            st.subheader("🔄 Self-Correction Attempts")
            st.info(f"🔁 Agent reformulated the query **{result['failed_attempts']}** time(s)")
            if result.get("past_queries"):
                with st.expander("📝 See query history"):
                    for i, q in enumerate(result["past_queries"]):
                        st.markdown(f"**Attempt {i+1}:** {q}")

        # Retrieved documents
        with st.expander("📚 Retrieved Document Chunks"):
            for i, doc in enumerate(result["documents"]):
                st.markdown(f"**Chunk {i+1}:**")
                st.caption(doc)

        # Raw JSON
        with st.expander("🛠️ Raw JSON Output"):
            st.json(result)