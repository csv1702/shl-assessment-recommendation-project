# 📘 SHL Assessment Recommendation Engine

## Overview

This project implements an **end-to-end Assessment Recommendation Engine** using **SHL’s product catalogue**.

The system accepts a **natural-language hiring or assessment requirement** and returns a ranked list of **relevant SHL individual test solutions**, using **semantic search and vector similarity**.

The solution includes:

- Live crawling of SHL assessment catalogue
- Semantic embedding and vector search
- Objective evaluation using labeled data
- REST API (as per SHL Appendix-2)
- Simple web frontend for testing
- Submission-ready prediction output
- Live Deployed Link to FrontEnd- "https://shl-assessment-recommendation-project-aurkcstwfmzrusbhelr9yy.streamlit.app/"

---

## System Architecture

```
User Query
   ↓
Sentence Transformer (Embeddings)
   ↓
FAISS Vector Index
   ↓
Top-K Relevant SHL Assessments
   ↓
FastAPI API → Streamlit Frontend
```

---

## Key Technologies Used

- **Python 3.10**
- **Sentence Transformers** (`all-MiniLM-L6-v2`)
- **FAISS** (vector similarity search)
- **FastAPI** (REST API)
- **Streamlit** (frontend UI)
- **Pandas / NumPy**
- **Requests**
- **BeautifulSoup** (for crawling)

---

## Data Collection

### SHL Catalogue Crawling

- The SHL product catalogue was crawled directly from the SHL website.
- Only **Individual Test Solutions** were considered.
- **Pre-packaged Job Solutions were explicitly excluded**, as required.

📊 **Total Individual Test Solutions Collected:** **264**

> ⚠️ _Note:_ While the assignment specifies a target of 377+, the SHL website structure limits discoverability of some assessments through public catalogue endpoints. The crawling logic was carefully designed to avoid invalid, duplicate, or non-assessment URLs. This limitation is transparently acknowledged and discussed in the approach document.

---

## Embedding & Retrieval

- Each assessment description was converted into a dense vector using:

  ```
  sentence-transformers/all-MiniLM-L6-v2
  ```

- All vectors were indexed using **FAISS (IndexFlatIP)** with cosine similarity.
- Queries are embedded in the same vector space and matched against the index.

This approach enables **semantic retrieval**, allowing the system to understand intent rather than relying on keywords.

---

## Evaluation (Labeled Train Data)

The provided **labeled train dataset** was used to evaluate recommendation quality.

### Metrics Used

- **Recall@5**
- **Recall@10**
- **Mean Recall**

### Evaluation Highlights

- URLs from different SHL formats were normalized using assessment slugs.
- Results demonstrate meaningful retrieval of human-labeled relevant assessments.

Evaluation code is available in:

```
pipeline/evaluate.py
```

---

## Test Set Predictions

Predictions were generated for the **unlabeled test queries**, as required.

### Output Format (Appendix-3 Compliant)

```
Query,Assessment_url
Query 1,URL 1
Query 1,URL 2
Query 2,URL 1
...
```

📄 Output file:

```
submission_predictions_final.csv
```

---

## REST API (Appendix-2)

A **FastAPI backend** exposes the recommendation engine.

### Available Endpoints

#### Health Check

```
GET /health
```

Response:

```json
{ "status": "ok" }
```

#### Recommendation Endpoint

```
POST /recommend
```

Request:

```json
{
  "query": "Looking for a cognitive assessment for graduates"
}
```

Response:

```json
[
  {
    "url": "...",
    "name": "...",
    "description": "...",
    "duration": "...",
    "remote_support": "...",
    "adaptive_support": "...",
    "test_type": "Individual Test"
  }
]
```

Swagger UI available at:

```
http://127.0.0.1:8000/docs
```

---

## Web Frontend

A **simple Streamlit frontend** is provided to test the system interactively.

### Features

- Text input for natural-language queries
- Displays top-K recommended assessments
- Connects directly to the FastAPI backend

### Run Frontend

```bash
python -m streamlit run frontend/app.py
```

Frontend URL:

```
http://localhost:8501
```

---

## Project Structure

```
shl-assessment-recommendation-project/
│
├── api/
│   └── app.py                 # FastAPI backend
│
├── frontend/
│   └── app.py                 # Streamlit frontend
│
├── pipeline/
│   ├── data_loader.py
│   ├── generate_embeddings.py
│   ├── build_faiss_index.py
│   ├── query_engine.py
│   ├── evaluate.py
│   └── predict_test.py
│
├── scraper/
│   └── shl_scraper.py
│
├── data/
│   ├── given/
│   │   └── Gen_AI Dataset.xlsx
│   └── processed/
│       ├── embedding_corpus.json
│       ├── embeddings.npy
│       └── faiss.index
│
├── submission_predictions_final.csv
├── README.md
└── requirements.txt
```

---

## How to Run (Quick Start)

1️⃣ Activate virtual environment

```bash
venv\Scripts\activate
```

2️⃣ Run API

```bash
python -m uvicorn api.app:app --reload
```

3️⃣ Run Frontend

```bash
python -m streamlit run frontend/app.py
```

---

## Future Improvements

- Expand crawling to additional SHL catalogue entry points
- Improve metadata extraction (duration, adaptive support, etc.)
- Add reranking using cross-encoder models
- Deploy API & frontend to cloud infrastructure

---

## Conclusion

This project demonstrates a **complete, production-style recommendation system**, including data ingestion, semantic retrieval, evaluation, API exposure, and frontend testing.
It follows SHL’s specifications closely while maintaining transparency around known limitations.

---

**Author:**
Chandra Shekhar
GitHub: `csv1702`
