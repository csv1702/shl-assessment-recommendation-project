import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# ========================
# CONFIG
# ========================

INDEX_PATH = Path("data/processed/faiss.index")
META_PATH = Path("data/processed/embedding_metadata.json")
CORPUS_PATH = Path("data/processed/embedding_corpus.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5


# ========================
# LOAD RESOURCES
# ========================

def load_resources():
    index = faiss.read_index(str(INDEX_PATH))

    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    model = SentenceTransformer(MODEL_NAME)

    return index, metadata, corpus, model


# ========================
# QUERY FUNCTION
# ========================

def recommend(query, index, metadata, corpus, model, top_k=TOP_K):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, top_k)

    recommendations = []

    for rank, idx in enumerate(indices[0]):
        item = corpus[idx]
        recommendations.append({
            "rank": rank + 1,
            "similarity": round(float(scores[0][rank]), 4),
            "url": item["url"],
            "text_preview": item["text"].split("Languages:")[0][:300] + "..."
        })

    return recommendations


# ========================
# MAIN (CLI DEMO)
# ========================

def main():
    index, metadata, corpus, model = load_resources()

    print("\n🔎 SHL Assessment Recommendation Engine")
    print("Type a job requirement (or 'exit' to quit)\n")

    while True:
        query = input("Query: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        if not query:
            print("⚠️ Please enter a valid query.\n")
            continue

        results = recommend(query, index, metadata, corpus, model)


        print("\nTop Recommendations:\n")
        for r in results:
            print(f"#{r['rank']} | Similarity: {r['similarity']}")
            print(f"URL: {r['url']}")
            print(f"Preview: {r['text_preview']}\n")

        print("-" * 60)


if __name__ == "__main__":
    main()
