# OpsIntel

OpsIntel is an enterprise AI investigation agent that combines document retrieval, structured analytics, tool calling, and persistent memory to investigate operational problems.

Instead of answering from a language model alone, OpsIntel gathers evidence from internal documents and operational metrics before producing findings and recommendations.

## Features

- FastAPI REST backend
- Next.js and TypeScript frontend
- PostgreSQL with pgvector
- Semantic vector search
- BM25 keyword search
- Reciprocal Rank Fusion for hybrid retrieval
- Cross-encoder reranking
- OpenAI Responses API
- Multi-step agent tool calling
- Structured SQL analytics
- Persistent conversation memory
- pytest unit tests
- GitHub Actions CI
- Docker Compose

## Example

A user can ask:

> Investigate why NYC-02 throughput dropped on September 4.

OpsIntel can search written incident reports, query structured operational metrics, combine the evidence, and return:

- Finding
- Evidence
- Likely cause
- Recommended action

It can also answer follow-up questions using stored conversation history.

## Architecture

    Next.js Frontend
            |
            v
      FastAPI Backend
            |
            v
    Investigation Agent
        /         \
       /           \
      v             v
    Document      SQL Analytics
    Retrieval     PostgreSQL
      |
      v
    Vector Search + BM25
      |
      v
    Reciprocal Rank Fusion
      |
      v
    Cross-Encoder Reranking
      |
      v
    PostgreSQL + pgvector

    Investigation Agent
            |
            v
    OpenAI Responses API

    Persistent conversation memory
    is stored in PostgreSQL.

## Retrieval Pipeline

OpsIntel combines semantic and keyword retrieval.

    User Question
         |
         +--> Vector Search
         |
         +--> BM25 Search
                |
                v
       Reciprocal Rank Fusion
                |
                v
       Cross-Encoder Reranking
                |
                v
          Top Evidence

The embedding model is:

    sentence-transformers/all-MiniLM-L6-v2

The reranker uses:

    cross-encoder/ms-marco-MiniLM-L-6-v2

## Agent Tools

### search_documents

Searches written operational evidence such as incident reports, staffing reports, and throughput reports.

### query_operations

Queries structured operational metrics including:

- Site
- Timestamp
- Throughput
- Staffing
- Downtime

The agent can call both tools during the same investigation.

## Memory

Each investigation uses a session ID.

Recent user and assistant messages are stored in PostgreSQL and reused for follow-up questions.

Example:

    User:
    Why did NYC-02 throughput drop?

    OpsIntel:
    The conveyor control failure was the primary cause.

    User:
    What was the main cause again?

    OpsIntel:
    The conveyor control failure affecting packing stations 12-16.

## Tech Stack

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- pytest

### AI and Retrieval

- OpenAI Responses API
- Sentence Transformers
- BM25
- Reciprocal Rank Fusion
- Cross-encoder reranking
- Agentic function calling

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- React Markdown

### DevOps

- Docker Compose
- Git
- GitHub Actions
- Backend CI
- Frontend lint and production-build CI

## Local Setup

Start PostgreSQL:

    docker compose up -d

Start the backend:

    cd backend
    source .venv/bin/activate
    fastapi dev app/main.py

Backend:

    http://127.0.0.1:8000

API documentation:

    http://127.0.0.1:8000/docs

Start the frontend in another terminal:

    cd frontend
    npm install
    npm run dev

Frontend:

    http://localhost:3000

## Environment Variables

Create:

    backend/.env

Example:

    DATABASE_URL=postgresql+psycopg://opsintel:opsintel@localhost:5432/opsintel
    OPENAI_API_KEY=your_openai_api_key
    OPENAI_MODEL=your_model_name

Never commit API keys or `.env` files.

## Testing

Backend:

    cd backend
    pytest -v

Frontend lint:

    cd frontend
    npm run lint

Frontend production build:

    npm run build

GitHub Actions automatically runs backend tests and frontend lint/build checks on pushes and pull requests.

## Synthetic Data Notice

All operational records included in this repository are synthetic demonstration data.

They are not real company records and do not contain confidential Amazon or employer information.

## Project Purpose

OpsIntel demonstrates practical experience with full-stack AI engineering, retrieval-augmented generation, structured and unstructured data, agentic tool orchestration, persistent memory, APIs, testing, and CI.
