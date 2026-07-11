<div align="center">

#  Enterprise Agentic RAG Platform

### Production-Oriented Enterprise Retrieval-Augmented Generation (RAG) Platform
Enterprise-grade Retrieval-Augmented Generation platform demonstrating production backend engineering, intelligent retrieval, and modular AI agent architecture.

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
##  Table of Contents

- [Overview](#-overview)
- [Why This Project?](#-why-this-project)
- [Key Features](#-key-features)
- [Project Status](#-project-status)
- [Architecture](#-high-level-architecture)
- [AI Agent Workflow](#-ai-agent-workflow)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Docker Deployment](#-running-with-docker)
- [Authentication](#-authentication)
- [API Overview](#-api-overview)
- [Enterprise RAG Pipeline](#-enterprise-rag-pipeline)
- [Background Processing](#-background-document-processing)
- [Testing](#-testing)
- [CI/CD](#-continuous-integration)
- [Security](#-security)
- [Scalability](#-scalability)
- [Roadmap](#-development-roadmap)
- [Contributing](#-contributing)
- [Version](https://img.shields.io/badge/version-v0.5.0--dev-orange)

---
#  Overview

Enterprise Agentic RAG Platform is a **production-oriented Retrieval-Augmented Generation (RAG) backend** designed to demonstrate modern AI system engineering practices beyond a traditional chatbot implementation.

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
##  Enterprise Highlights

Production Architecture

JWT Authentication

RBAC

Multi-Tenant

Hybrid Retrieval

Conversation Memory

Background Processing

Metadata Filtering

Docker

GitHub Actions

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

```mermaid
flowchart TD

A[Client]

A --> B[FastAPI API]

B --> C[JWT Authentication]

C --> D[Query Agent]

D --> E[Planner Agent]

E --> F[Retriever Agent]

F --> G[Retrieval Orchestrator]

G --> H[Semantic Search]

G --> I[BM25 Search]

G --> J[Multi Query]

H --> K[Hybrid Retrieval]

I --> K

J --> K

K --> L[Context Compression]

L --> M[Conversation Memory]

M --> N[Ollama]

N --> O[Final Response]
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

| Layer            | Technology            |
| ---------------- | --------------------- |
| Language         | Python 3.12           |
| Backend          | FastAPI               |
| ORM              | SQLAlchemy            |
| Database         | PostgreSQL            |
| Vector Store     | Qdrant                |
| Queue            | Redis + RQ            |
| Embeddings       | Sentence Transformers |
| LLM              | Ollama                |
| Authentication   | JWT                   |
| Testing          | Pytest                |
| CI/CD            | GitHub Actions        |
| Containerization | Docker                |


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
|   ├── pytest.ini
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
#  Enterprise RAG Pipeline

The platform follows a modular Retrieval-Augmented Generation (RAG) workflow designed for enterprise document intelligence.

```text
                    User Question
                          │
                          ▼
                   Query Agent
                          │
                          ▼
                  Planner Agent
                          │
                          ▼
             Retrieval Orchestrator
                          │
        ┌─────────┬────────────┬────────────┐
        ▼         ▼            ▼
   Semantic     BM25      Multi-Query
        └─────────┴────────────┘
                  │
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
           Grounded Response
```

---

#  Agent Architecture

The current implementation separates responsibilities into specialized agents, making the platform modular and extensible.

| Agent | Responsibility |
|--------|----------------|
| Query Agent | Understand user intent, rewrite queries, extract entities and metadata filters |
| Planner Agent | Build an execution plan and choose the retrieval strategy |
| Retriever Agent | Retrieve relevant document chunks using semantic, lexical, hybrid, or multi-query search |
| Memory Services | Maintain conversation context and rewrite follow-up questions |
| LLM Service | Generate grounded responses using retrieved context |

This architecture provides a solid foundation for the advanced multi-agent workflow planned in the next development phase.

---

#  Current Retrieval Strategies

The platform supports multiple retrieval approaches depending on the execution plan.

| Strategy | Purpose |
|----------|---------|
| Semantic Search | Dense vector similarity search using Qdrant |
| BM25 Search | Traditional keyword-based retrieval |
| Hybrid Search | Combines semantic and lexical retrieval using Reciprocal Rank Fusion (RRF) |
| Multi-Query Retrieval | Generates multiple semantic search queries for improved recall |
| Metadata Filtering | Restricts search results using document metadata |

---

#  Background Document Processing

Document ingestion is performed asynchronously to improve scalability and responsiveness.

```text
Upload Document
       │
       ▼
Create Ingestion Job
       │
       ▼
Redis Queue (RQ)
       │
       ▼
Background Worker
       │
       ▼
Document Parsing
       │
       ▼
Metadata Extraction
       │
       ▼
Chunk Generation
       │
       ▼
Embedding Generation
       │
       ▼
Qdrant Indexing
       │
       ▼
Document Ready
```

---

#  Testing

The project includes automated tests covering core functionality.

Current test coverage includes:

- Agent Tests
- Authentication
- Document Upload
- Conversation APIs
- Integration Tests
- Retrieval Evaluation
- Hybrid Retrieval
- Context Compression
- Multi-Query Retrieval

Run the test suite:

```bash
pytest tests -v
```

Example output:

```text
==============================
18 passed
==============================
```

---

#  Continuous Integration

GitHub Actions automatically performs:

- Dependency installation
- PostgreSQL startup
- Redis startup
- Qdrant startup
- Database migrations
- Seed data generation
- Automated testing

Every push and pull request is validated before integration.

---

#  Performance Considerations

The platform is designed with scalability in mind.

Current optimizations include:

- Background document ingestion
- Redis-backed job queue
- Vector search using Qdrant
- Context compression
- Metadata-aware filtering
- Hybrid retrieval
- Modular service architecture

---

#  Security

Enterprise-oriented security features include:

- JWT Authentication
- Password Hashing
- Role-Based Access Control (RBAC)
- Multi-Tenant Data Isolation
- Protected API Endpoints
- Input Validation
- SQLAlchemy ORM Protection
- Environment-Based Configuration

---

#  Scalability

The architecture is designed to support future horizontal scaling.

Current design enables:

- Independent API services
- Separate worker processes
- External vector database
- Redis-backed queues
- Stateless FastAPI application
- Containerized deployment

---

#  Development Roadmap

##  Phase 1 — Foundation

- Authentication
- User Management
- Multi-Tenancy
- Document Upload
- Basic RAG Pipeline

---

##  Phase 2 — Production RAG

- Conversation Memory
- Metadata Filtering
- Background Ingestion
- Redis Queue
- Qdrant Integration

---

##  Phase 3 — Advanced Retrieval

- Hybrid Search
- BM25 Retrieval
- Reciprocal Rank Fusion
- Context Compression
- Multi-Query Retrieval
- Retrieval Evaluation

---

##  Phase 4 — Agentic RAG Foundation

- Query Agent
- Planner Agent
- Retriever Agent
- Query Understanding
- Execution Planning
- Agent Workflow Foundation

---

##  Phase 5 — Advanced Agentic AI

Planned work includes:

- Supervisor Agent
- Reflection Agent
- Verification Agent
- LangGraph Workflow
- Dynamic Agent Routing
- Self-Correcting Retrieval
- Confidence Scoring
- Agent Observability

---

##  Phase 6 — Production Readiness

Planned improvements:

- Advanced Monitoring
- Distributed Tracing
- Metrics Dashboard
- Production Deployment
- Infrastructure Automation
- Performance Optimization

---

#  Screenshots

> Screenshots and demonstration GIFs will be added as the user interface and monitoring dashboards evolve.

Suggested additions:

- Login Page
- Swagger UI
- Document Upload
- Chat Interface
- Retrieval Workflow
- Analytics Dashboard

---

#  Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit your changes

```bash
git commit -m "feat: add awesome feature"
```

4. Push the branch

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

#  Author

**vamsi krishna satvik .s**

Backend Engineer • AI Engineer • Platform Engineer

GitHub:

```
https://github.com/<your-username>
```

LinkedIn:

```
https://linkedin.com/in/<your-profile>
```

---

#  Acknowledgements

This project builds upon the excellent work of the open-source community.

Special thanks to:

- FastAPI
- SQLAlchemy
- Alembic
- Qdrant
- Redis
- RQ
- Sentence Transformers
- Ollama
- Hugging Face
- Docker
- GitHub Actions

---

<div align="center">

##  If you found this project useful, consider giving it a star!

Enterprise Agentic RAG Platform

Built with ❤️ using Python, FastAPI, Qdrant, Redis, Docker, and modern AI engineering practices, #chatgpt.

</div>
