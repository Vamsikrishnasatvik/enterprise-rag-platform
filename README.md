<div align="center">

#  Enterprise Agentic RAG Platform

### Production-Ready Enterprise Retrieval-Augmented Generation (RAG) Platform

*A scalable, multi-tenant AI platform featuring intelligent retrieval, conversation memory, hybrid search, and an extensible agent architecture built with modern backend engineering practices.*

---

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20Database-red)
![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-success?logo=githubactions)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

#  Overview

Enterprise Agentic RAG Platform is a **production-oriented Retrieval-Augmented Generation (RAG) backend** designed to demonstrate modern AI system engineering rather than a simple chatbot.

The platform combines enterprise backend architecture with intelligent retrieval techniques, conversation memory, background document ingestion, metadata-aware search, and an extensible agent-based workflow.

It is designed as a portfolio-quality project showcasing skills in:

- Enterprise Backend Development
- AI System Engineering
- Retrieval-Augmented Generation (RAG)
- Vector Search
- Production API Design
- Distributed Background Processing
- Secure Authentication
- Multi-Tenant Architecture
- CI/CD and Automated Testing

---

#  Why This Project?

Most RAG tutorials stop after implementing:

```
PDF
 ↓
Embeddings
 ↓
Vector Search
 ↓
LLM
```

Real enterprise AI systems require significantly more than semantic search.

This project demonstrates how a production-ready AI platform can be built using modern software engineering principles, including:

- Secure authentication
- Multi-tenant architecture
- Role-based access control (RBAC)
- Background document ingestion
- Metadata-aware retrieval
- Hybrid search strategies
- Conversation memory
- Agent-driven query planning
- Automated testing
- CI/CD pipelines

The goal is to showcase how enterprise AI applications are architected, implemented, and maintained in production environments.

---

#  Key Features

##  AI & Retrieval

- Intelligent Query Understanding
- Planner Agent for retrieval planning
- Retriever Agent with adaptive retrieval
- Semantic Vector Search
- BM25 Lexical Search
- Hybrid Search (Reciprocal Rank Fusion)
- Multi-Query Retrieval
- Query Expansion
- Self-Query Retrieval
- Context Compression
- Conversation Memory
- Memory-Based Query Rewriting
- Automatic Metadata Extraction
- Metadata-Aware Retrieval

---

##  Enterprise Features

- Multi-Tenant Architecture
- Role-Based Access Control (RBAC)
- JWT Authentication
- Conversation Management
- Background Document Processing
- Redis Queue Workers
- Document Version Metadata
- Enterprise API Design

---

##  Infrastructure

- FastAPI REST API
- PostgreSQL Database
- Qdrant Vector Database
- Redis
- Docker Compose
- Alembic Database Migrations
- GitHub Actions CI
- Automated Test Suite

---

##  Quality & Testing

- Unit Tests
- Integration Tests
- Retrieval Evaluation Tests
- Agent Tests
- CI Validation
- Automatic Database Migration
- Seeded Test Environment

---

#  Project Status

| Category | Status |
|-----------|--------|
| Backend | ✅ Production Ready |
| Authentication | ✅ Complete |
| Multi-Tenancy | ✅ Complete |
| Document Processing | ✅ Complete |
| Background Ingestion | ✅ Complete |
| Conversation Memory | ✅ Complete |
| Metadata Filtering | ✅ Complete |
| Hybrid Retrieval | ✅ Complete |
| Agentic Workflow Foundation | ✅ Complete |
| Automated Testing | ✅ 18 Passing Tests |
| GitHub Actions | ✅ Passing |
| Phase | 🚧 Preparing for Phase 5 |

---

#  High-Level Architecture

```text
                        Client Applications
                                │
                                ▼
                        FastAPI REST API
                                │
                    JWT Authentication & RBAC
                                │
                                ▼
                      Enterprise Agent Pipeline
                                │
      ┌───────────────┬───────────────┬───────────────┐
      ▼               ▼               ▼
 Query Agent     Planner Agent   Retriever Agent
                                │
                                ▼
                  Retrieval Orchestrator
                                │
        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼
    Semantic         BM25       Multi-Query Search
        └──────────────┬──────────────┘
                       ▼
            Hybrid Retrieval (RRF)
                       │
                       ▼
              Context Compression
                       │
                       ▼
            Conversation Memory
                       │
                       ▼
                  Ollama LLM
                       │
                       ▼
                Final AI Response
```

---

#  AI Agent Workflow

The current platform implements an extensible agent architecture that separates responsibilities into specialized components.

| Agent | Responsibility |
|--------|----------------|
| Query Agent | Understands user intent, rewrites queries, extracts entities and metadata filters |
| Planner Agent | Determines retrieval strategy and execution plan |
| Retriever Agent | Executes semantic, lexical, hybrid, or multi-query retrieval |
| Memory Services | Preserve conversation context and rewrite follow-up questions |
| LLM Service | Generates grounded responses using retrieved context |

This modular architecture enables future expansion into a complete multi-agent AI system in Phase 5.

---

#  Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Web Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Vector Database | Qdrant |
| Background Queue | Redis + RQ |
| Embedding Model | Sentence Transformers |
| LLM | Ollama |
| Authentication | JWT |
| Database Migrations | Alembic |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Containerization | Docker & Docker Compose |

---

#  Project Structure

The project follows a modular, enterprise-oriented architecture to separate API, business logic, AI services, infrastructure, and background processing.

```text
enterprise-rag-platform/
│
├── backend/
│   ├── alembic/                # Database migrations
│   ├── app/
│   │   ├── agents/             # AI agents
│   │   ├── api/                # REST API endpoints
│   │   ├── core/               # Configuration & utilities
│   │   ├── db/                 # Database session
│   │   ├── graph/              # Agent graph state
│   │   ├── models/             # SQLAlchemy models
│   │   ├── prompts/            # LLM prompt templates
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business & AI services
│   │   ├── workers/            # Background workers
│   │   └── main.py             # FastAPI application
│   │
│   ├── scripts/                # Database seed scripts
│   ├── tests/                  # Unit & integration tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Frontend application
├── docs/                       # Project documentation
├── infra/                      # Infrastructure files
├── storage/                    # Local document storage
├── docker-compose.yml
└── README.md
```

---

#  Getting Started

## Prerequisites

Before running the project, ensure the following software is installed:

| Software | Version |
|-----------|----------|
| Python | 3.12+ |
| Docker | Latest |
| Docker Compose | Latest |
| Git | Latest |

---

#  Clone the Repository

```bash
git clone https://github.com/<your-username>/enterprise-rag-platform.git

cd enterprise-rag-platform
```

---

#  Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/enterprise_rag

REDIS_URL=redis://redis:6379

QDRANT_URL=http://qdrant:6333

OLLAMA_BASE_URL=http://host.docker.internal:11434

OLLAMA_MODEL=llama3

SECRET_KEY=change-this-secret-key
```

> **Note:** Update values according to your local environment.

---

#  Running with Docker

Build all services:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

---

#  Database Migration

Apply all migrations:

```bash
docker compose exec backend alembic upgrade head
```

Verify current migration:

```bash
docker compose exec backend alembic current
```

---

#  Seed the Database

Populate the database with sample users and tenants.

```bash
docker compose exec backend python -m scripts.seed
```

---

#  Running the Application

After the containers are running:

Backend API:

```
http://localhost:8000
```

Interactive API Documentation:

```
http://localhost:8000/docs
```

OpenAPI Specification:

```
http://localhost:8000/openapi.json
```

---

#  Authentication

The platform uses **JWT-based authentication**.

Typical authentication flow:

```
Client
    │
    ▼
POST /auth/login
    │
    ▼
JWT Access Token
    │
    ▼
Authorization: Bearer <token>
    │
    ▼
Protected Enterprise APIs
```

---

#  API Overview

The platform exposes RESTful APIs for document management, conversations, authentication, and chat.

| Endpoint | Description |
|----------|-------------|
| `/auth/login` | Authenticate user |
| `/documents/upload` | Upload enterprise documents |
| `/chat/query` | Ask questions using the RAG pipeline |
| `/conversations` | Manage conversations |
| `/docs` | Interactive Swagger UI |
| `/openapi.json` | OpenAPI schema |

---

#  Example Authentication Request

```http
POST /auth/login
Content-Type: application/json

{
    "email": "admin@test.com",
    "password": "password123"
}
```

---

#  Example Response

```json
{
    "access_token": "<jwt-token>",
    "token_type": "bearer"
}
```

---

#  Example Chat Request

```http
POST /chat/query
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
    "question": "Explain the HR Leave Policy"
}
```

---

#  Example Chat Response

```json
{
    "answer": "Employees are entitled to annual leave according to company policy...",
    "conversation_id": 1,
    "sources": [
        {
            "document_id": 3,
            "chunk_id": 12
        }
    ]
}
```

---
