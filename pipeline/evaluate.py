import json
import pandas as pd
import faiss
import numpy as np
from urllib.parse import urlparse
from collections import defaultdict
from sentence_transformers import SentenceTransformer

# ========================
# PATHS & CONFIG
# ========================

DATASET_PATH = r"data/given/Gen_AI Dataset.xlsx"

FAISS_INDEX_PATH = "data/processed/faiss.index"
CORPUS_PATH = "data/processed/embedding_corpus.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# ========================
# HELPERS
# ========================

def extract_slug(url):
    """
    Normalize different SHL URL formats to a common slug.
    """
    if not isinstance(url, str):
        return None

    path = urlparse(url).path.strip("/")

    # New format: product-catalog/view/<slug>
    if "product-catalog/view" in path:
        return path.split("/")[-1]

    # Old / legacy formats
    if "products" in path:
        return path.split("/")[-1]

    return None


# ========================
# LOAD LABELED DATA
# ========================

def load_labeled_data():
    df = pd.read_excel(DATASET_PATH)

    grouped = defaultdict(set)

    for _, row in df.iterrows():
        query = str(row["Query"]).strip()
        slug = extract_slug(row["Assessment_url"])

        if query and slug:
            grouped[query].add(slug)

    print("✅ Labeled data loaded")
    print(f"Total unique queries: {len(grouped)}")

    return grouped


# ========================
# EVALUATION
# ========================

def evaluate_recall_at_k(labeled_data, k=5):
    print(f"\n📊 Evaluating Recall@{k}\n")

    # Load FAISS index
    index = faiss.read_index(FAISS_INDEX_PATH)

    # Load corpus
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    # Load model
    model = SentenceTransformer(MODEL_NAME)

    recalls = []

    for query, relevant_slugs in labeled_data.items():
        query_embedding = model.encode(
            [query],
            normalize_embeddings=True
        )

        scores, indices = index.search(query_embedding, k)

        retrieved_slugs = set()

        for idx in indices[0]:
            url = corpus[idx]["url"]
            slug = extract_slug(url)
            if slug:
                retrieved_slugs.add(slug)

        hits = len(retrieved_slugs & relevant_slugs)
        recall = hits / len(relevant_slugs)

        recalls.append(recall)

        print(f"Query: {query[:70]}...")
        print(f"Relevant: {len(relevant_slugs)} | Hits@{k}: {hits}")
        print(f"Recall@{k}: {recall:.2f}\n")

    avg_recall = sum(recalls) / len(recalls)
    print(f"✅ Average Recall@{k}: {avg_recall:.2f}")

    return avg_recall


# ========================
# MAIN
# ========================

if __name__ == "__main__":
    labeled_data = load_labeled_data()

    evaluate_recall_at_k(labeled_data, k=5)
    evaluate_recall_at_k(labeled_data, k=10)
