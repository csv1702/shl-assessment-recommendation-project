import numpy as np
import faiss
from pathlib import Path

EMBEDDING_PATH = Path("data/processed/embeddings.npy")
INDEX_PATH = Path("data/processed/faiss.index")


def main():
    print("Loading embeddings...")
    embeddings = np.load(EMBEDDING_PATH)

    dim = embeddings.shape[1]
    print(f"Embedding dimension: {dim}")

    print("Building FAISS index (IndexFlatIP)...")
    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    print(f"Total vectors indexed: {index.ntotal}")
    print(f"Index saved to: {INDEX_PATH}")


if __name__ == "__main__":
    main()
