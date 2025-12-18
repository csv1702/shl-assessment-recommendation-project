import pandas as pd
import json
import faiss
from sentence_transformers import SentenceTransformer
from urllib.parse import urlparse

# ========================
# CONFIG
# ========================

DATASET_PATH = r"data/given/Gen_AI Dataset.xlsx"
OUTPUT_PATH = "submission_predictions.csv"

FAISS_INDEX_PATH = "data/processed/faiss.index"
CORPUS_PATH = "data/processed/embedding_corpus.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5


# ========================
# HELPERS
# ========================

def extract_slug(url):
    if not isinstance(url, str):
        return None
    path = urlparse(url).path.strip("/")
    return path.split("/")[-1]


# ========================
# MAIN PREDICTION LOGIC
# ========================

def main():
    print("Loading test queries...")

    # Load test queries
    df = pd.read_excel(DATASET_PATH, sheet_name=1)
    queries = df["Query"].dropna().tolist()

    # Load FAISS + corpus
    index = faiss.read_index(FAISS_INDEX_PATH)

    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    model = SentenceTransformer(MODEL_NAME)

    results = []

    print(f"Generating predictions for {len(queries)} queries...\n")

    for q in queries:
        query_embedding = model.encode([q], normalize_embeddings=True)
        scores, indices = index.search(query_embedding, TOP_K)

        urls = []
        for idx in indices[0]:
            urls.append(corpus[idx]["url"])

        results.append({
            "Query": q,
            "Recommended_Assessments": ", ".join(urls)
        })

    # Save submission file
    pd.DataFrame(results).to_csv(OUTPUT_PATH, index=False)

    print(f"Submission file saved as: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
