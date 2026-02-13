# 🚀 Project Overview

## Purpose
This project builds an AI-powered trademark risk assessment system that analyzes trademark applications against the USPTO Trademark Manual of Examining Procedure (TMEP), November 2025 edition. The goal is to enable deterministic, retrieval-based legal analysis grounded strictly in official TMEP provisions.
This system automates the initial review by retrieving relevant TMEP provisions and generating a structured, citation-backed issue analysis.

## Problem statement
Trademark examination risk assessment is time-consuming and requires attorneys to manually compare application details against voluminous TMEP guidelines. The TMEP contains thousands of subsections, making fast and consistent issue identification difficult.

## Core Functionality
- The system takes a trademark application, searches a structured version of the TMEP manual, identifies possible examination issues supported by exact TMEP sections, and assigns risk levels using predefined rules — producing a structured, defensible risk report.

## Tech-Stack Used
### Frontend
- **Streamlit** – Web-based UI for uploading trademark documents and displaying structured risk assessment reports.
- **HTML Rendering (via Streamlit components)** – For structured, readable output formatting.

---

### ⚙ Backend
- **Python** – Core programming language for entire system.
- **FastAPI** – Backend API framework for serving the RAG pipeline.
- **pdfplumber** – PDF text extraction for trademark document ingestion.
- **Regex (re)** – Structured parsing of LLM output.
- **dotenv** – Environment variable management.

---

### 🗄 Database / Vector Storage
- **Weaviate Cloud (Sandbox)** – Managed vector database for semantic retrieval.
- **weaviate-client (Python v4)** – Client SDK for schema creation, ingestion, and similarity search.
- **Bring-Your-Own-Embedding (BYOE) Architecture** – External embedding generation, vectorizer disabled in DB.

---

### 🤖 AI / ML Components
#### Retrieval Architecture
- **RAG (Retrieval-Augmented Generation)** – Grounded legal reasoning framework.
- **Bi-Encoder Vector Retrieval** – Separate passage and query embeddings.
- **Cosine Similarity Search (near_vector)** – Semantic matching mechanism.

#### Embedding Models
- **SentenceTransformer** – Embedding model interface.
- **intfloat/e5-base-v2** – Embedding model used for:
  - "passage:" prefix (TMEP sections)
  - "query:" prefix (Trademark queries)
- L2 Normalized Embeddings – For stable cosine similarity.

---

### 🧠 LLM Models
- **Groq Platform** – Inference provider.
- **Llama 3.3 70B (Versatile)** – Primary reasoning model for grounded legal issue analysis.
- **Llama 3.1 8B Instant** – Lightweight alternative for faster inference/testing.

---

### 📦 Core Python Libraries Used 
to be listed:
• `torch` – Backend for embedding model execution.
• `transformers` – Model loading and tokenizer support.
• `sentence-transformers` – Embedding interface wrapper.
• `tqdm` – Progress tracking during embedding generation.
• `json` – Data serialization.
• `pathlib` – File handling.
• `typing` – Type annotations.</json>}```]]>}}}]}]}]}] }}}}]}}]}] }}}}]}}]}] }}}}]}}]}] }}}}]}}]}] }}}}]}}]}] }}}}]}}]}] }}}}]}}]}] }}}}]}}] }}



# Setup Instructions

## (1) for `parse_tmep_html.py`
- **Install Required Dependency:**
  ```bash
  pip install beautifulsoup4
  ```

## (2) for `normalize_sections.py`
- ✔ No additional pip installs required.
- You must already have: Parsed TMEP sections from `parse_tmep_html.py`

## (3) for chunk_sections.py
- ✔ No additional pip installs required.
- You must already have: `data/parsed/tmep_sections.json`
- Generated via: `parse_tmep_html.py` → `normalize_sections.py`

# (4) for embed_chunks.py (E5 Query Embedding Layer)

## Install Required Dependencies
- `pip install sentence-transformers torch`

## Ensure Embedding Model Loader Exists
- `src/embeddings/model.py`

## Critical E5 Usage Rule
- `"query: " + query`
