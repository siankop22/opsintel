# OpsIntel

**Enterprise AI Investigation & Decision Agent**

OpsIntel is a full-stack AI investigation platform that combines structured operational metrics, unstructured incident documents, retrieval, reranking, tool calling, and persistent memory to explain operational problems and recommend actions.

Instead of answering from a language model alone, OpsIntel gathers evidence from data and documents before producing a finding.

**Live demo:** https://opsintel-gamma.vercel.app  
**Backend API:** https://opsintel.onrender.com  
**API docs:** https://opsintel.onrender.com/docs

---

## What OpsIntel Does

A user can ask a question such as:

> Investigate why NYC-02 throughput dropped on September 4.

OpsIntel can then:

1. Query structured operational metrics from PostgreSQL.
2. Search incident, staffing, and throughput documents.
3. Combine semantic and keyword retrieval.
4. Rerank the most relevant evidence.
5. Let the investigation agent decide which tools to call.
6. Produce an evidence-backed finding, likely cause, and recommended action.
7. Store conversation history for follow-up questions.

The frontend also shows agent activity, retrieved documents, SQL results, latency, and tool-call count.

---

## Key Features

- Multi-step AI investigation agent
- OpenAI Responses API tool orchestration
- Structured SQL operational analytics
- Semantic vector search with pgvector
- BM25 keyword retrieval
- Reciprocal Rank Fusion for hybrid retrieval
- Cross-encoder reranking
- Persistent session memory in PostgreSQL
- Agent activity and evidence visibility in the UI
- FastAPI REST backend
- Next.js + TypeScript frontend
- pytest regression tests
- GitHub Actions CI
- Production deployment with Vercel, Render, and Neon

---

## Architecture

```mermaid
flowchart TD
    A[Next.js Frontend] --> B[FastAPI Backend]
    B --> C[Investigation Agent]

    C --> D[query_operations]
    C --> E[search_documents]

    D --> F[PostgreSQL Operational Metrics]

    E --> G[Vector Search]
    E --> H[BM25 Search]
    G --> I[Reciprocal Rank Fusion]
    H --> I
    I --> J[Cross-Encoder Reranker]
    J --> K[Top Evidence]

    C --> L[OpenAI Responses API]
    C --> M[Persistent Session Memory]

    F --> N[Neon PostgreSQL]
    M --> N
```

### Production deployment

```text
Vercel
  └── Next.js frontend
        │
        ▼
Render
  └── FastAPI backend
        │
        ├── OpenAI API
        │
        └── Neon PostgreSQL + pgvector
```

---

## Retrieval Pipeline

OpsIntel combines semantic and keyword retrieval before reranking the final evidence.

```text
User Question
     │
     ├── Vector Search
     │
     └── BM25 Search
            │
            ▼
   Reciprocal Rank Fusion
            │
            ▼
   Cross-Encoder Reranking
            │
            ▼
       Top Evidence
```

Embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Reranker:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

---

## Agent Tools

### `query_operations`

Queries structured operational metrics including:

- site
- timestamp
- throughput
- staffing
- downtime

### `search_documents`

Searches written operational evidence such as:

- incident reports
- staffing reports
- throughput reports

The agent can call either tool multiple times during a single investigation.

---

## Example Investigation

For the synthetic NYC-02 incident, OpsIntel can identify that throughput fell during the afternoon disruption and connect the decline to evidence from both structured metrics and written reports.

A typical response contains:

- **Finding**
- **Evidence**
- **Likely cause**
- **Recommended action**

The UI also exposes the underlying agent activity so the user can see which data and documents were used.

---

## Persistent Memory

Each investigation uses a session ID.

Recent user and assistant messages are stored in PostgreSQL and can be reused for follow-up questions.

Example:

```text
User: Why did NYC-02 throughput drop?

OpsIntel: The conveyor control failure was the primary cause.

User: What was the main cause again?

OpsIntel: The conveyor control failure affecting packing stations 12-16.
```

---

## Retrieval Evaluation

OpsIntel includes a small synthetic benchmark containing 12 operational investigation queries.

| Method | Top-1 Accuracy | MRR@3 |
|---|---:|---:|
| Vector Search | 91.7% | 0.958 |
| BM25 | 75.0% | 0.861 |
| Hybrid Retrieval | 91.7% | 0.944 |
| Hybrid + Cross-Encoder Reranker | 91.7% | 0.958 |

These results are development metrics from a deliberately small synthetic benchmark and should not be interpreted as production-scale performance claims.

Run the benchmark with:

```bash
cd backend
python -m evals.run_retrieval_eval
```

---

## Tech Stack

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- psycopg
- pytest

### AI and Retrieval

- OpenAI Responses API
- Sentence Transformers
- BM25
- Reciprocal Rank Fusion
- Cross-encoder reranking
- Agent tool calling

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- React Markdown

### Infrastructure

- Neon PostgreSQL
- Render
- Vercel
- Docker Compose
- GitHub Actions

---

## Local Setup

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Configure the backend

Create `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://opsintel:opsintel@localhost:5432/opsintel
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_model_name
```

Never commit API keys or `.env` files.

### 3. Start the backend

```bash
cd backend
source .venv/bin/activate
fastapi dev app/main.py
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Configure the frontend

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

## Testing

Backend tests:

```bash
cd backend
pytest -q
```

Frontend lint:

```bash
cd frontend
npm run lint
```

Frontend production build:

```bash
cd frontend
npm run build
```

GitHub Actions automatically runs backend tests and frontend lint/build checks on repository updates.

---

## Synthetic Data Notice

All operational records included in this repository are **synthetic demonstration data**.

They are not real company records and do not contain confidential Amazon or employer information.

---

## Project Purpose

OpsIntel demonstrates an end-to-end AI engineering workflow across:

- agentic tool orchestration
- retrieval-augmented investigation
- structured and unstructured data
- vector databases
- reranking
- persistent memory
- API development
- frontend development
- testing and CI
- cloud deployment
