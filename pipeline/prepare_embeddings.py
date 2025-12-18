import json
from pathlib import Path

INPUT_PATH = Path("data/processed/shl_catalogue.json")
OUTPUT_PATH = Path("data/processed/embedding_corpus.json")


def build_embedding_text(record):
    parts = [
        record.get("name", ""),
        record.get("description", ""),
        f"Job levels: {record.get('job_levels', 'Not specified')}",
        f"Languages: {record.get('languages', 'Not specified')}",
        f"Duration: {record.get('duration', 'Not specified')} minutes",
        f"Remote support: {record.get('remote_support', 'Not specified')}",
        f"Adaptive support: {record.get('adaptive_support', 'Not specified')}"
    ]
    return ". ".join(p for p in parts if p and p != "Not specified")


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    corpus = []

    for idx, record in enumerate(data):
        corpus.append({
            "id": idx,
            "url": record["url"],
            "text": build_embedding_text(record)
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2)

    print("✅ STEP 5.1 completed")
    print(f"Total documents prepared: {len(corpus)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
