```markdown
# 📘 SHL Assessment Recommendation Engine

## Overview

This project implements an **end-to-end Assessment Recommendation Engine** using **SHL’s product catalogue**, developed as part of the **SHL AI Intern – Generative AI Assignment**.

The system accepts a **natural-language hiring or assessment requirement** and returns a **ranked list of relevant SHL individual test solutions** using **semantic search and vector similarity**.

### Key Capabilities

- Live crawling of SHL assessment catalogue
- Semantic embedding and vector-based retrieval
- Objective evaluation using labeled data
- REST API compliant with **SHL Appendix-2**
- Simple web frontend for interactive testing
- Submission-ready prediction output (Appendix-3 compliant)

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Data Collection](#data-collection)
- [Embedding & Retrieval](#embedding--retrieval)
- [Evaluation](#evaluation-labeled-train-data)
- [Test Set Predictions](#test-set-predictions)
- [REST API](#rest-api-appendix-2)
- [Web Frontend](#web-frontend)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run-quick-start)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)
- [Author](#author)

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

## Technologies Used

- **Python 3.10**
- **Sentence Transformers** (`all-MiniLM-L6-v2`)
- **FAISS** (vector similarity search)
- **FastAPI** (REST API)
- **Streamlit** (frontend UI)
- **Pandas / NumPy**
- **Requests**
- **BeautifulSoup** (web crawling)

---

## Data Collection

### SHL Catalogue Crawling

- The SHL product catalogue was **crawled directly from the SHL website**
- Only **Individual Test Solutions** were included
- **Pre-packaged Job Solutions** were explicitly excluded (as required)

📊 **Total Individual Test Solutions Collected:** `264`

⚠️ **Note on Data Coverage**
While the assignment specifies a target of **377+ assessments**, the SHL website’s public structure limits discoverability of certain assessments.
The crawler was intentionally designed to avoid:
- Invalid URLs
- Duplicate entries
- Non-assessment pages

This limitation is transparently acknowledged and discussed in the accompanying approach document.

---

## Embedding & Retrieval

- Each assessment description is converted into a dense vector using:

```

sentence-transformers/all-MiniLM-L6-v2

```

- All vectors are indexed using **FAISS (IndexFlatIP)** with **cosine similarity**
- User queries are embedded in the same vector space and matched against the index

### Why Semantic Search?

This approach enables **intent-aware retrieval**, allowing the system to understand semantic meaning rather than relying on keyword matching.

---

## Evaluation (Labeled Train Data)

The provided **labeled training dataset** was used to evaluate recommendation quality.

### Metrics Used

- **Recall@5**
- **Recall@10**
- **Mean Recall**

### Evaluation Highlights

- URLs across different SHL formats were **normalized using assessment slugs**
- Results demonstrate **meaningful retrieval** of human-labeled relevant assessments
- Evaluation implementation is available at:

```

pipeline/evaluate.py

```

---

## Test Set Predictions

Predictions were generated for the **unlabeled test queries**, as required by the assignment.

### Output Format (Appendix-3 Compliant)

```

Query,Assessment_url
Query 1,URL 1
Query 1,URL 2
Query 2,URL 1
...

```

📄 **Final Output File**

```

submission_predictions_final.csv

````

---

## REST API (Appendix-2)

A **FastAPI backend** exposes the recommendation engine.

### Available Endpoints

#### Health Check

**GET** `/health`

**Response**
```json
{ "status": "ok" }
````

---

#### Recommendation Endpoint

**POST** `/recommend`

**Request**

```json
{
  "query": "Looking for a cognitive assessment for graduates"
}
```

**Response**

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

📘 **Swagger UI**

```
http://127.0.0.1:8000/docs
```

---

## Web Frontend

A lightweight **Streamlit frontend** is provided for interactive testing.

### Features

- Text input for natural-language queries
- Displays top-K recommended assessments
- Connects directly to the FastAPI backend

### Run Frontend

```bash
python -m streamlit run frontend/app.py
```

🌐 **Frontend URL**

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

### 1️⃣ Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 2️⃣ Run API

```bash
python -m uvicorn api.app:app --reload
```

### 3️⃣ Run Frontend

```bash
python -m streamlit run frontend/app.py
```

---

## Future Improvements

- Expand crawling to additional SHL catalogue entry points
- Improve metadata extraction (duration, adaptive support, etc.)
- Add reranking using cross-encoder models
- Deploy API and frontend to cloud infrastructure

---

## Conclusion

This project demonstrates a **complete, production-style recommendation system**, covering:

- Data ingestion
- Semantic retrieval
- Objective evaluation
- API exposure
- Frontend testing

The solution closely follows **SHL’s specifications** while maintaining transparency around known data limitations.

---

## Author

**Chandra Shekhar**
GitHub: [csv1702](https://github.com/csv1702)

```

```
