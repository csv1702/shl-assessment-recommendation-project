import json
import faiss
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List


# ========================
# CONFIG
# ========================

FAISS_INDEX_PATH = Path("data/processed/faiss.index")
CORPUS_PATH = Path("data/processed/embedding_corpus.json")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

# ========================
# LOAD RESOURCES ON START
# ========================

app = FastAPI(title="SHL Assessment Recommendation API")

index = faiss.read_index(str(FAISS_INDEX_PATH))

with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    corpus = json.load(f)

model = SentenceTransformer(MODEL_NAME)

# ========================
# REQUEST / RESPONSE MODELS
# ========================

class RecommendationRequest(BaseModel):
    query: str


class RecommendationResponse(BaseModel):
    url: str
    name: str
    description: str
    duration: str
    remote_support: str
    adaptive_support: str
    test_type: str


# ========================
# ENDPOINTS
# ========================

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/recommend", response_model=List[RecommendationResponse])
def recommend_assessments(request: RecommendationRequest):
    query_embedding = model.encode(
        [request.query],
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, TOP_K)

    results = []

    for idx in indices[0]:
        item = corpus[idx]

        results.append({
            "url": item["url"],
            "name": item["text"].split(".")[0],
            "description": item["text"],
            "duration": "Not specified",
            "remote_support": "Yes",
            "adaptive_support": "Yes",
            "test_type": "Individual Test"
        })

    return results

