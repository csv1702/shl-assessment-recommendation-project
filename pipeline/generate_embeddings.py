import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

INPUT_PATH = Path("data/processed/embedding_corpus.json")
EMBEDDING_PATH = Path("data/processed/embeddings.npy")
META_PATH = Path("data/processed/embedding_metadata.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    print("Loading embedding corpus...")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    texts = [item["text"] for item in corpus]
    metadata = [{"id": item["id"], "url": item["url"]} for item in corpus]

    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    EMBEDDING_PATH.parent.mkdir(parents=True, exist_ok=True)

    np.save(EMBEDDING_PATH, embeddings)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Saved embeddings to: {EMBEDDING_PATH}")
    print(f"Saved metadata to: {META_PATH}")


if __name__ == "__main__":
    main()
