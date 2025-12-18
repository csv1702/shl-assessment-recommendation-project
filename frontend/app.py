import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# ========================
# CONFIG
# ========================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

INDEX_PATH = Path("data/processed/faiss.index")
CORPUS_PATH = Path("data/processed/embedding_corpus.json")

# ========================
# LOAD RESOURCES (CACHED)
# ========================

@st.cache_resource
def load_resources():
    index = faiss.read_index(str(INDEX_PATH))
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    model = SentenceTransformer(MODEL_NAME)
    return index, corpus, model


index, corpus, model = load_resources()

# ========================
# UI
# ========================

st.set_page_config(
    page_title="SHL Assessment Recommendation Engine",
    layout="centered"
)

st.title("🔍 SHL Assessment Recommendation Engine")
st.write(
    "Enter a hiring or assessment requirement to get relevant SHL individual test solutions."
)

query = st.text_input(
    "Enter your requirement:",
    placeholder="e.g. Looking for a cognitive assessment for graduates"
)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Finding relevant assessments..."):
            query_embedding = model.encode(
                [query],
                normalize_embeddings=True
            )

            scores, indices = index.search(query_embedding, TOP_K)

        st.success(f"Top {TOP_K} recommendations:")

        for rank, idx in enumerate(indices[0], start=1):
            item = corpus[idx]
            name = item["text"].split(".")[0]

            st.markdown(f"### {rank}. {name}")
            st.markdown(f"**URL:** {item['url']}")
            st.markdown(f"**Description:** {item['text']}")
            st.markdown(
                "- Duration: Not specified\n"
                "- Remote Support: Yes\n"
                "- Adaptive Support: Yes\n"
                "- Test Type: Individual Test"
            )
            st.markdown("---")
