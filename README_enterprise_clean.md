<div align="center">

# Enterprise Agentic RAG Platform

### A Production-Ready Multi-Agent Retrieval-Augmented Generation (RAG) Platform Built with LangGraph, FastAPI, PostgreSQL, Qdrant, Redis, and Ollama

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)]()
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blue?style=for-the-badge)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)]()
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20Database-DC244C?style=for-the-badge)]()
[![Redis](https://img.shields.io/badge/Redis-Background%20Jobs-D82C20?style=for-the-badge&logo=redis&logoColor=white)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)]()


---

**Enterprise Agentic RAG Platform** is a production-oriented Retrieval-Augmented Generation (RAG) system that combines a multi-agent workflow, hybrid retrieval, conversation memory, document ingestion, reflection, verification, and retry mechanisms to deliver grounded, reliable AI responses over enterprise knowledge bases.

Unlike traditional RAG systems that rely on a single retrieval and generation step, this platform orchestrates specialized AI agents using **LangGraph**, enabling planning, query rewriting, retrieval, answer generation, citation, self-reflection, verification, and adaptive retry within a single workflow.

Designed with modularity and scalability in mind, the platform integrates **FastAPI**, **PostgreSQL**, **Qdrant**, **Redis**, **Ollama**, and **Docker** to provide a complete backend for enterprise knowledge assistants.

</div>
---

# 🚀 Project Overview

Modern enterprises generate vast amounts of internal knowledge across documents, policies, technical manuals, reports, knowledge bases, and collaborative platforms. While Large Language Models (LLMs) possess powerful reasoning capabilities, they cannot reliably answer organization-specific questions without access to relevant and trustworthy information.

Traditional Retrieval-Augmented Generation (RAG) systems address this challenge by retrieving documents and passing them to an LLM. However, most implementations follow a linear pipeline:

```
User Query
      │
      ▼
Retrieve Documents
      │
      ▼
Generate Answer
```

Although effective for simple use cases, this architecture often struggles with:

- Poor retrieval quality for complex queries
- Hallucinated or weakly supported answers
- Lack of reasoning before retrieval
- No answer verification
- No adaptive retry mechanism
- Limited conversation memory
- Minimal observability
- Difficulty extending the pipeline with new capabilities

---

## Why Agentic RAG?

Instead of treating retrieval as a single step, this project models the entire question-answering process as a coordinated workflow of specialized AI agents.

Each agent is responsible for one well-defined task, allowing the system to reason, retrieve, validate, and improve responses before returning them to the user.

The workflow is orchestrated using **LangGraph**, enabling stateful execution, conditional routing, retries, and modular agent composition.

```
User Question
       │
       ▼
 Memory Agent
       │
       ▼
 Planner Agent
       │
       ▼
 Query Rewriter
       │
       ▼
 Hybrid Retrieval
       │
       ▼
 Context Compression
       │
       ▼
 Answer Generation
       │
       ▼
 Citation Generation
       │
       ▼
 Reflection
       │
       ▼
 Verification
       │
       ▼
 Retry (if required)
       │
       ▼
 Final Response
```

This architecture enables each stage of the pipeline to focus on a single responsibility while maintaining a shared workflow state throughout execution.

---

## Design Goals

The platform was designed around several engineering principles:

### Modular Agent Architecture

Each capability is implemented as an independent agent with a clearly defined responsibility, making the workflow easier to extend, test, and maintain.

### Reliable Retrieval

The retrieval layer combines semantic vector search, keyword search, Reciprocal Rank Fusion (RRF), CrossEncoder reranking, and dynamic Top-K selection to improve the relevance of retrieved context.

### Grounded Responses

Every answer is generated using retrieved enterprise knowledge, followed by automated reflection and verification to improve factual consistency and reduce unsupported responses.

### Production-Oriented Design

The platform incorporates background document ingestion, conversation memory, multi-tenancy, role-based access control (RBAC), monitoring hooks, and modular services to support production deployments rather than proof-of-concept demonstrations.

### Extensibility

New agents, retrieval strategies, tools, or LLM providers can be integrated with minimal changes to the overall workflow due to the modular architecture.

---

## Intended Use Cases

This platform can serve as the foundation for a wide range of enterprise AI applications, including:

- Enterprise Knowledge Assistants
- Internal Documentation Search
- Technical Support Automation
- HR Policy Assistants
- IT Help Desk Systems
- Compliance & Regulatory Search
- Customer Support Knowledge Bases
- Research & Document Intelligence
- Multi-Department AI Assistants
- Organization-wide Knowledge Management

---

## Project Vision

The goal of this project is not simply to build another chatbot, but to demonstrate how modern AI systems can be engineered using modular agents, hybrid retrieval techniques, and production-ready software architecture.

By combining intelligent orchestration with enterprise search techniques, the platform provides a strong foundation for building scalable, trustworthy, and maintainable Retrieval-Augmented Generation systems.

---

# ✨ Features

The Enterprise Agentic RAG Platform combines modern Retrieval-Augmented Generation (RAG) techniques with a modular multi-agent architecture to deliver reliable, scalable, and production-ready AI workflows.

The platform is designed around independent AI agents, enterprise retrieval strategies, and production infrastructure, allowing each component to evolve without impacting the overall system.

---

# 🤖 Multi-Agent Workflow

Instead of relying on a single prompt, the platform orchestrates specialized AI agents using **LangGraph**.

| Feature | Description | Status |
|----------|-------------|:------:|
| Memory Agent | Builds conversation context using summaries and recent history | ✅ |
| Planner Agent | Determines the execution strategy for each query | ✅ |
| Query Rewriter Agent | Optimizes user queries for retrieval | ✅ |
| Retriever Agent | Coordinates hybrid document retrieval | ✅ |
| Compression Agent | Compresses retrieved context before generation | ✅ |
| Answer Agent | Generates grounded responses using enterprise context | ✅ |
| Citation Agent | Attaches citations to generated answers | ✅ |
| Reflection Agent | Evaluates answer quality and confidence | ✅ |
| Verification Agent | Checks whether responses are supported by retrieved evidence | ✅ |
| Retry Agent | Retries workflow when confidence is insufficient | ✅ |
| Tool Executor Agent | Executes external tools when required | ✅ |

---

# 🔍 Hybrid Retrieval Engine

The retrieval system combines multiple search strategies to maximize relevance and answer quality.

| Capability | Status |
|------------|:------:|
| Semantic Vector Search | ✅ |
| PostgreSQL Keyword Search | ✅ |
| Hybrid Retrieval | ✅ |
| Reciprocal Rank Fusion (RRF) utility | 🚧 |
| CrossEncoder Reranking | ✅ |
| Dynamic Top-K Selector | 🚧 |
| Query Rewriting | ✅ |
| Metadata Filtering Framework | 🚧 |
| Retrieval Context Builder | ✅ |

---

# 🧠 Conversation Memory

The platform maintains conversational continuity through intelligent memory management.

| Capability | Status |
|------------|:------:|
| Conversation Summaries | ✅ |
| Recent Message Memory | ✅ |
| Memory-Aware Prompting | ✅ |
| Context Reconstruction | ✅ |
| Long Conversation Support | ✅ |

---

# 📄 Enterprise Document Processing

The ingestion pipeline transforms uploaded documents into searchable knowledge.

| Capability | Status |
|------------|:------:|
| PDF Parsing | ✅ |
| DOCX Parsing | ✅ |
| TXT Parsing | ✅ |
| Automatic Chunking | ✅ |
| Embedding Generation | ✅ |
| Vector Indexing | ✅ |
| Background Ingestion Jobs | ✅ |

---

# 🛡️ Reliability & Answer Quality

Several validation stages help improve answer reliability.

| Capability | Status |
|------------|:------:|
| Reflection-Based Evaluation | ✅ |
| Answer Verification | ✅ |
| Confidence Scoring | ✅ |
| Citation Generation | ✅ |
| Retry Mechanism | ✅ |
| Grounded Responses | ✅ |

---

# 🏢 Enterprise Features

The platform includes capabilities commonly required in enterprise environments.

| Capability | Status |
|------------|:------:|
| Multi-Tenant Architecture | ✅ |
| Role-Based Access Control (RBAC) | ✅ |
| Modular Service Layer | ✅ |
| Background Workers | ✅ |
| Redis Queue Integration | ✅ |
| Qdrant Vector Database | ✅ |
| PostgreSQL Persistence | ✅ |
| Docker Support | ✅ |

---

# 📊 Observability

The workflow exposes execution information that can be used for monitoring and debugging.

| Capability | Status |
|------------|:------:|
| Execution Trace | ✅ |
| Agent Timing Collection | ✅ |
| Reflection Confidence | ✅ |
| Verification Confidence | ✅ |
| Retrieval Scores | ✅ |
| Error Tracking | ✅ |

---

# ⚙️ Modern Technology Stack

The platform is built using a modern Python ecosystem.

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI |
| Workflow Engine | LangGraph |
| LLM | Ollama |
| Embeddings | BAAI BGE Small |
| Reranker | CrossEncoder (MS MARCO MiniLM) |
| Vector Database | Qdrant |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Background Jobs | Redis + RQ |
| Document Parsing | PyMuPDF, python-docx |
| Containerization | Docker |
| Authentication | JWT |
| Language | Python 3.12+ |

---

# 🚀 Highlights

- 🧩 Modular multi-agent architecture powered by LangGraph
- 🔍 Hybrid retrieval combining semantic and keyword search
- 📈 Reciprocal Rank Fusion (RRF) with CrossEncoder reranking
- 🧠 Conversation memory with intelligent context management
- 📄 Enterprise-grade document ingestion pipeline
- 🛡️ Reflection and verification for grounded responses
- 🔁 Adaptive retry mechanism for improved answer quality
- 🏢 Multi-tenant architecture with RBAC support
- ⚡ Background ingestion using Redis and RQ
- 🐳 Docker-ready deployment
- 📊 Built-in execution tracing and monitoring hooks

---

# 🏗️ System Architecture

The Enterprise Agentic RAG Platform follows a layered architecture that separates API handling, workflow orchestration, AI agents, retrieval, services, and infrastructure.

Each layer has a single responsibility, making the platform modular, scalable, and easy to extend.

```text
                                   ┌─────────────────────────┐
                                   │       Frontend UI       │
                                   │  React • Next.js • API  │
                                   └─────────────┬───────────┘
                                                 │
                                                 ▼
                                   ┌─────────────────────────┐
                                   │       FastAPI API       │
                                   │ REST • Authentication   │
                                   └─────────────┬───────────┘
                                                 │
                                                 ▼
                             ┌─────────────────────────────────────┐
                             │      LangGraph Workflow Engine      │
                             │ Graph State • Routing • Retry Logic │
                             └─────────────┬───────────────────────┘
                                           │
          ┌────────────────────────────────┼────────────────────────────────┐
          ▼                                ▼                                ▼
 ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
 │  Memory Agent   │              │ Planner Agent   │              │ Tool Executor   │
 └────────┬────────┘              └────────┬────────┘              └────────┬────────┘
          │                                │                                │
          └────────────────────────────────┼────────────────────────────────┘
                                           ▼
                              ┌────────────────────────┐
                              │ Query Rewriter Agent   │
                              └────────────┬───────────┘
                                           ▼
                              ┌────────────────────────┐
                              │   Retriever Agent      │
                              └────────────┬───────────┘
                                           ▼
                ┌────────────────────────────────────────────────────────────┐
                │            Hybrid Retrieval Engine                         │
                │                                                            │
                │  Semantic Search • Keyword Search • Metadata Filtering     │
                │              Reciprocal Rank Fusion (RRF)                  │
                │              CrossEncoder Reranking                        │
                └────────────┬───────────────────────────────────────────────┘
                             ▼
                   ┌────────────────────────┐
                   │ Compression Agent      │
                   └────────────┬───────────┘
                                ▼
                   ┌────────────────────────┐
                   │ Answer Generation      │
                   └────────────┬───────────┘
                                ▼
                   ┌────────────────────────┐
                   │ Citation Agent         │
                   └────────────┬───────────┘
                                ▼
                   ┌────────────────────────┐
                   │ Reflection Agent       │
                   └────────────┬───────────┘
                                ▼
                   ┌────────────────────────┐
                   │ Verification Agent     │
                   └────────────┬───────────┘
                                ▼
                   ┌────────────────────────┐
                   │ Retry Agent            │
                   └────────────┬───────────┘
                                ▼
                        Final Response
```

---

# 🧩 Architecture Layers

The platform is divided into independent layers, each responsible for a specific part of the workflow.

## 1. API Layer

The API layer exposes REST endpoints for:

- User authentication
- Conversation management
- Document upload
- Knowledge retrieval
- Chat interactions
- Background job management

**Technologies**

- FastAPI
- Pydantic
- JWT Authentication

---

## 2. Workflow Layer

The workflow layer is powered by **LangGraph**, which orchestrates the execution of specialized AI agents.

Instead of relying on a single prompt, the system executes a stateful workflow where each agent contributes one part of the reasoning process.

Responsibilities include:

- Workflow routing
- Shared state management
- Retry handling
- Conditional execution
- Agent orchestration

---

## 3. Agent Layer

Each agent has a single responsibility.

| Agent | Responsibility |
|--------|----------------|
| Memory Agent | Builds conversation memory |
| Planner Agent | Creates execution plans |
| Query Rewriter | Optimizes retrieval queries |
| Retriever Agent | Retrieves relevant knowledge |
| Compression Agent | Reduces retrieved context |
| Answer Agent | Generates grounded responses |
| Citation Agent | Adds source references |
| Reflection Agent | Evaluates response quality |
| Verification Agent | Checks factual grounding |
| Retry Agent | Triggers adaptive retries |
| Tool Executor | Executes external tools |

This modular architecture makes it easy to replace, improve, or extend individual agents without affecting the rest of the workflow.

---

## 4. Retrieval Layer

The retrieval layer combines multiple search strategies to maximize relevance.

Current retrieval pipeline:

```text
User Query
     │
     ▼
Query Rewriter
     │
     ▼
Retrieval Strategy
     │
     ├── Semantic Search
     ├── Keyword Search
     └── Hybrid Search
              │
              ▼
       Candidate Merge
              │
              ▼
       CrossEncoder Reranker
              │
              ▼
       Top Ranked Context
```

The repository also contains RRF and metadata-retrieval components as extension points for the retrieval layer.

This hybrid approach significantly improves retrieval quality compared to relying solely on vector similarity search.

---

## 5. Service Layer

The service layer encapsulates reusable business logic.

Examples include:

- Memory Service
- Retrieval Service
- LLM Service
- Document Service
- Embedding Service
- Vector Service
- Conversation Service
- Authentication Service

This separation keeps agents focused on orchestration while services implement reusable functionality.

---

## 6. Infrastructure Layer

The infrastructure layer provides storage, indexing, background processing, and model execution.

| Component | Purpose |
|-----------|---------|
| PostgreSQL | Relational data storage |
| Qdrant | Vector database |
| Redis | Background job queue |
| RQ | Worker execution |
| Ollama | Local LLM inference |
| Docker | Containerized deployment |

---

# 🎯 Design Principles

The architecture is guided by several core engineering principles.

### Modularity

Each component has a clearly defined responsibility and can evolve independently.

---

### Extensibility

New agents, retrieval strategies, or external tools can be added without redesigning the workflow.

---

### Reliability

Reflection, verification, and adaptive retries improve answer quality while reducing unsupported responses.

---

### Scalability

The layered architecture enables independent scaling of API servers, workers, vector databases, and language models.

---

### Maintainability

Business logic, orchestration, retrieval, and infrastructure are isolated into dedicated modules, making the codebase easier to understand, test, and extend.

---

# 🤖 AI Agent Workflow

Unlike traditional Retrieval-Augmented Generation (RAG) systems that execute retrieval and generation as a single pipeline, the Enterprise Agentic RAG Platform decomposes the reasoning process into a coordinated workflow of specialized AI agents.

Each agent performs one well-defined responsibility while sharing a common workflow state managed by **LangGraph**.

This modular approach improves maintainability, enables conditional execution, and allows each stage of the pipeline to evolve independently.

---

# 🔄 End-to-End Workflow

```text
                         User Question
                               │
                               ▼
                      Memory Agent
                               │
                               ▼
                      Planner Agent
                               │
                               ▼
                  Query Rewriter Agent
                               │
                               ▼
                     Retriever Agent
                               │
                               ▼
                   Compression Agent
                               │
                               ▼
                      Answer Agent
                               │
                               ▼
                     Citation Agent
                               │
                               ▼
                    Reflection Agent
                               │
                      ┌────────┴────────┐
                      │                 │
                      ▼                 ▼
            Verification Agent      Retry Agent
                      │                 │
                      └────────┬────────┘
                               ▼
                        Final Response
```

---

# 🧠 Agent Responsibilities

Each agent contributes one stage of the reasoning process.

---

## 🧠 Memory Agent

### Purpose

Builds conversational context before planning begins.

### Responsibilities

- Loads conversation summary
- Retrieves recent messages
- Generates memory-aware context
- Maintains conversational continuity

### Input

- Conversation ID
- Current user question

### Output

```text
Memory Context
Conversation Summary
Recent Messages
```

---

## 📋 Planner Agent

### Purpose

Determines how the workflow should execute.

### Responsibilities

- Classifies the query
- Chooses execution strategy
- Generates an execution plan
- Determines whether retrieval is required

### Example

```text
Question

↓

Knowledge Query

↓

Execution Plan

↓

RAG Retrieval
```

---

## ✍️ Query Rewriter Agent

### Purpose

Improves retrieval quality by rewriting user queries into retrieval-optimized forms.

### Responsibilities

- Expand implicit context
- Clarify ambiguous wording
- Preserve user intent
- Reject unsafe rewrites

Example

```
Original

What is our leave policy?

↓

Rewritten

Employee annual leave policy vacation entitlement paid leave
```

---

## 🔍 Retriever Agent

### Purpose

Retrieves the most relevant enterprise knowledge.

### Retrieval Strategies

- Semantic Search
- Keyword Search
- Hybrid Retrieval

The retriever coordinates the retrieval pipeline and prepares context for downstream agents.

---

## 🗜️ Compression Agent

### Purpose

Reduces retrieved context before answer generation.

Benefits include:

- Lower token usage
- Faster inference
- Reduced prompt size
- Higher information density

---

## 💬 Answer Agent

### Purpose

Generates grounded answers using enterprise knowledge.

The Answer Agent receives:

- User Question
- Memory Context
- Retrieved Context

and produces a context-aware response.

---

## 📚 Citation Agent

### Purpose

Attaches citations to generated responses.

Benefits:

- Improves transparency
- Enables evidence tracing
- Makes responses easier to validate

---

## 🔍 Reflection Agent

### Purpose

Performs self-evaluation of the generated answer.

The Reflection Agent estimates:

- Answer quality
- Confidence
- Grounding
- Potential issues

Example Output

```json
{
  "passed": true,
  "confidence": 0.91,
  "grounded": true,
  "retry": false
}
```

---

## ✅ Verification Agent

### Purpose

Verifies that the generated answer is fully supported by the retrieved enterprise context.

Checks include:

- Evidence support
- Missing information
- Hallucinated statements
- Confidence estimation

This verification stage acts as a safeguard before returning responses to the user.

---

## 🔄 Retry Agent

### Purpose

Improves answer quality when reflection or verification detects issues.

Adaptive retry strategies include:

- Increasing retrieval depth
- Switching retrieval strategy
- Rewriting the query
- Running the workflow again

Current progression:

```text
Retry 1

Semantic Search

Top-K = 5

↓

Retry 2

Hybrid Retrieval

Top-K = 8

↓

Retry 3

Keyword Retrieval

Top-K = 10
```

---

## 🛠️ Tool Executor Agent

### Purpose

Provides a unified interface for integrating external tools into the workflow.

Examples include:

- Search APIs
- Calculators
- Database lookups
- Internal enterprise services
- Future MCP integrations

The current implementation provides the framework for extending the platform with external capabilities.

---

# 🔄 Shared Workflow State

All agents communicate through a shared **GraphState** managed by LangGraph.

Instead of passing data directly between agents, each agent reads from and writes to the workflow state.

```text
GraphState

├── Question
├── Memory Context
├── Execution Plan
├── Retrieval Query
├── Retrieved Chunks
├── Retrieval Context
├── Answer
├── Citations
├── Reflection
├── Verification
├── Retry Count
├── Execution Trace
└── Agent Timings
```

This shared state enables:

- Modular execution
- Conditional routing
- Retry mechanisms
- Execution tracing
- Agent independence

---

# ⚡ Why a Multi-Agent Workflow?

Traditional RAG systems execute retrieval and generation as a single operation.

This platform instead decomposes the workflow into specialized reasoning stages.

| Traditional RAG | Agentic RAG Platform |
|-----------------|----------------------|
| Single prompt | Multi-agent workflow |
| Static retrieval | Adaptive retrieval |
| No planning | Planner-driven execution |
| No self-evaluation | Reflection Agent |
| No verification | Verification Agent |
| No retry | Adaptive Retry |
| Limited memory | Conversation Memory |
| Fixed pipeline | Modular workflow |

This architecture improves modularity, extensibility, and answer reliability while making the system easier to maintain and evolve.

---

# 🔍 Hybrid Retrieval Pipeline

High-quality retrieval is the foundation of every Retrieval-Augmented Generation (RAG) system. Instead of relying solely on vector similarity search, the Enterprise Agentic RAG Platform employs a **hybrid retrieval architecture** that combines multiple retrieval strategies, ranking algorithms, and optimization techniques to maximize context relevance.

The retrieval pipeline is designed to improve recall, precision, and robustness while minimizing hallucinations during answer generation.

---

# 📊 Retrieval Workflow

```text
                    User Question
                           │
                           ▼
                 Query Rewriter Agent
                           │
                           ▼
                  Retrieval Strategy
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Semantic Search     Keyword Search     Metadata Filter
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
              Reciprocal Rank Fusion (RRF)
                           │
                           ▼
              CrossEncoder Reranker
                           │
                           ▼
                  Dynamic Top-K Selection
                           │
                           ▼
                  Context Construction
                           │
                           ▼
                 Compression Agent
                           │
                           ▼
                    Answer Generation
```

---

# 🚀 Retrieval Components

The retrieval engine consists of several independent stages that work together to produce high-quality context for the language model.

---

## ✍️ Query Rewriting

Before retrieval begins, the Query Rewriter Agent transforms the user's question into a retrieval-optimized query.

### Goals

- Clarify ambiguous wording
- Expand implicit context
- Preserve user intent
- Improve retrieval precision
- Avoid unsafe query expansion

### Example

```text
Original

What is our leave policy?

↓

Rewritten

Employee annual leave policy vacation entitlement paid leave
```

This improves retrieval without changing the original meaning of the question.

---

## 🧠 Semantic Search

Semantic search retrieves documents based on meaning rather than exact keyword matches.

The platform generates dense vector embeddings for both documents and queries, enabling concept-based retrieval.

### Advantages

- Handles synonyms
- Understands natural language
- Retrieves semantically similar documents
- Works well for conversational queries

### Technologies

- BAAI BGE Small Embedding Model
- Qdrant Vector Database
- Cosine Similarity Search

---

## 🔑 Keyword Search

Keyword search complements semantic retrieval by matching exact terms stored in the knowledge base.

This is particularly useful for:

- Policy identifiers
- Employee codes
- Product names
- Error codes
- Technical terminology
- Acronyms

Current implementation uses PostgreSQL pattern matching with a framework that can be extended to more advanced lexical search techniques in future versions.

---

## 🏷️ Metadata Filtering

The retrieval pipeline includes a metadata filtering layer designed for enterprise environments.

Planned filtering capabilities include:

- Department
- Document Type
- Document Owner
- Tags
- Status
- Custom Metadata

The current metadata retriever is an extensibility point and returns no results yet. The architecture leaves room for department, document type, owner, status, tags, and custom metadata filters.

---

# 🔀 Hybrid Retrieval

Semantic search and keyword search each have unique strengths.

The platform combines both approaches into a unified hybrid retrieval strategy.

```text
Semantic Results

+

Keyword Results

↓

Hybrid Candidate Set
```

This approach increases both recall and precision compared to relying on a single retrieval strategy.

---

# 📈 Reciprocal Rank Fusion (RRF)

The repository includes a **Reciprocal Rank Fusion (RRF)** utility for combining ranked retrieval result sets.

The current public hybrid search path merges semantic and keyword candidates and then applies CrossEncoder reranking. RRF remains an available retrieval component for further integration.

```text
Semantic Ranking

+

Keyword Ranking

↓

Reciprocal Rank Fusion

↓

Unified Ranking
```

### Benefits

- Balances multiple retrieval strategies
- Improves ranking stability
- Reduces dependence on a single search algorithm
- Increases retrieval robustness

---

# 🎯 CrossEncoder Reranking

The merged retrieval results are further refined using a CrossEncoder reranker.

Unlike vector search, which evaluates queries and documents independently, the CrossEncoder jointly evaluates each query-document pair to estimate semantic relevance.

```text
Candidate Documents

↓

CrossEncoder

↓

Relevance Scores

↓

Final Ranking
```

### Benefits

- Higher precision
- Better ranking quality
- Improved handling of nuanced queries
- More relevant context for answer generation

---

# 📚 Dynamic Top-K Selection

Not every question requires the same amount of retrieved context.

A `DynamicTopKSelector` is implemented as a rule-based retrieval component and can adjust retrieval depth based on query complexity.

Current selector behavior:

| Query Complexity | Retrieved Chunks |
|------------------|-----------------:|
| Simple | 2 |
| Medium | 4 |
| Complex | 6 |

This balances retrieval quality against inference cost and prompt size.

---

# 🗜️ Context Construction

Once retrieval is complete, the highest-ranked chunks are combined into a single retrieval context.

The context builder:

- Preserves chunk ordering
- Limits maximum context size
- Removes unnecessary content
- Prepares the context for downstream compression

---

# 🧩 Context Compression

Large language models have finite context windows.

The Compression Agent reduces retrieved context while preserving the information most relevant to the user's question.

Benefits include:

- Lower token usage
- Faster inference
- Higher information density
- Reduced prompt costs

---

# 🔄 Adaptive Retry Retrieval

If Reflection or Verification determines that the generated answer is insufficient, the Retry Agent modifies the retrieval strategy and executes the workflow again.

The workflow contains retry state and retry handling so that retrieval or generation can be revisited when quality checks fail.

The exact retry strategy is controlled by the workflow implementation and should not be interpreted as a fixed three-stage retrieval sequence.

This adaptive retrieval strategy increases the likelihood of retrieving missing evidence before generating another response.

---

# 📊 Retrieval Pipeline Summary

| Stage | Purpose |
|--------|---------|
| Query Rewriting | Improve retrieval query |
| Semantic Search | Meaning-based retrieval |
| Keyword Search | Exact term retrieval |
| Metadata Filtering | Enterprise document filtering |
| Hybrid Retrieval | Combine retrieval strategies |
| Reciprocal Rank Fusion | Merge ranked results |
| CrossEncoder Reranking | Improve ranking precision |
| Dynamic Top-K | Adaptive retrieval depth |
| Context Construction | Build retrieval context |
| Compression | Optimize prompt size |
| Retry Strategy | Improve retrieval when needed |

---

# 🎯 Why Hybrid Retrieval?

A single retrieval strategy rarely performs well across every type of enterprise query.

By combining semantic retrieval, lexical retrieval, rank fusion, reranking, adaptive retrieval depth, and intelligent retries, the platform produces more relevant context for downstream answer generation.

This layered retrieval architecture significantly improves answer quality while reducing unsupported responses and retrieval failures.

---

# 🛠️ Technology Stack

The Enterprise Agentic RAG Platform is built using a modern, production-oriented technology stack designed for scalability, modularity, and maintainability.

Each technology has been selected to address a specific layer of the system, from workflow orchestration and AI inference to storage, retrieval, and infrastructure.

---

# 📦 Technology Overview

| Layer | Technologies |
|--------|--------------|
| Frontend | React, Next.js, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.12 |
| AI Workflow | LangGraph |
| Language Models | Ollama |
| Embedding Model | BAAI BGE Small v1.5 |
| Reranker | CrossEncoder (MS MARCO MiniLM) |
| Vector Database | Qdrant |
| Relational Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Background Jobs | Redis + RQ |
| Document Processing | PyMuPDF, python-docx |
| Containerization | Docker & Docker Compose |
| API Validation | Pydantic |
| Logging | Python Logging |
| Package Management | pip |

---

# 🎨 Frontend

The frontend provides a modern web interface for interacting with the platform.

| Technology | Purpose |
|------------|---------|
| React | Component-based UI development |
| Next.js | Modern frontend framework |
| TypeScript | Type-safe frontend development |
| Tailwind CSS | Utility-first styling |
| Fetch API | Backend communication |

### Responsibilities

- Chat interface
- Document upload
- Conversation history
- Source visualization
- Retrieval analytics
- Agent execution visualization

---

# ⚙️ Backend

FastAPI serves as the primary backend framework responsible for API endpoints, request validation, dependency injection, and service orchestration.

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API framework |
| Python 3.12 | Primary programming language |
| Pydantic | Data validation |
| SQLAlchemy | ORM and database abstraction |

### Responsibilities

- REST APIs
- Authentication
- Conversation management
- Document management
- Agent orchestration
- Workflow execution

---

# 🤖 AI Workflow

The reasoning pipeline is orchestrated using **LangGraph**, enabling stateful, multi-agent execution.

| Technology | Purpose |
|------------|---------|
| LangGraph | Multi-agent workflow orchestration |

### Current Agents

- Memory Agent
- Planner Agent
- Query Rewriter Agent
- Retriever Agent
- Compression Agent
- Answer Agent
- Citation Agent
- Reflection Agent
- Verification Agent
- Retry Agent
- Tool Executor Agent

---

# 🧠 Language Models

The platform supports local LLM inference through Ollama.

| Technology | Purpose |
|------------|---------|
| Ollama | Local LLM serving |

### Responsibilities

- Query planning
- Memory summarization
- Query rewriting
- Context compression
- Answer generation
- Reflection
- Verification

The modular architecture allows future integration with cloud-based providers such as OpenAI, Anthropic, Azure OpenAI, or Google Gemini.

---

# 🔎 Retrieval & Search

The retrieval layer combines multiple search strategies to improve answer quality.

| Technology | Purpose |
|------------|---------|
| Qdrant | Vector similarity search |
| PostgreSQL | Keyword search |
| BGE Small | Dense embeddings |
| CrossEncoder | Neural reranking |

### Retrieval Pipeline

- Semantic Search
- Keyword Search
- Hybrid Retrieval
- Reciprocal Rank Fusion (RRF)
- CrossEncoder Reranking
- Dynamic Top-K Selection

---

# 📄 Document Processing

Uploaded documents are automatically transformed into searchable knowledge.

| Technology | Purpose |
|------------|---------|
| PyMuPDF | PDF parsing |
| python-docx | DOCX parsing |
| RecursiveCharacterTextSplitter | Intelligent document chunking |

### Supported Formats

- PDF
- DOCX
- TXT

Future versions may include:

- Excel
- PowerPoint
- HTML
- Markdown
- OCR-based image extraction

---

# 🗄️ Data Storage

The platform separates structured and vector data into specialized storage systems.

## PostgreSQL

Stores:

- Users
- Conversations
- Messages
- Documents
- Document Chunks
- Metadata
- Background Jobs

---

## Qdrant

Stores:

- Dense vector embeddings
- Chunk metadata
- Semantic search indexes

---

## Redis

Provides:

- Background job queue
- Worker communication
- Task scheduling

---

# 🔐 Authentication & Security

| Technology | Purpose |
|------------|---------|
| JWT | Stateless authentication |
| RBAC | Role-Based Access Control |

Current roles include:

- Admin
- Editor
- Viewer

---

# 🐳 Deployment

The project is fully containerized.

| Technology | Purpose |
|------------|---------|
| Docker | Application containers |
| Docker Compose | Multi-container orchestration |

Deployment services include:

- Frontend
- Backend API
- PostgreSQL
- Qdrant
- Redis
- Ollama

---

# 📊 Monitoring & Observability

The platform collects workflow execution information for debugging and analysis.

Current capabilities include:

- Agent execution trace
- Agent timing collection
- Reflection confidence
- Verification confidence
- Retrieval scores
- Error tracking

The architecture is designed to support future integration with:

- Prometheus
- Grafana
- OpenTelemetry

---

# 📈 Why This Stack?

The selected technologies were chosen to balance performance, scalability, and developer experience.

| Goal | Technology |
|------|------------|
| High-performance APIs | FastAPI |
| Stateful AI workflows | LangGraph |
| Reliable vector search | Qdrant |
| Structured persistence | PostgreSQL |
| Local LLM inference | Ollama |
| Background processing | Redis + RQ |
| Containerized deployment | Docker |
| Modular architecture | Python + SQLAlchemy |

Together, these technologies provide a solid foundation for building scalable, production-ready Retrieval-Augmented Generation systems while remaining flexible enough to support future enhancements and additional AI capabilities.

---

# 📂 Project Structure

The Enterprise Agentic RAG Platform follows a layered, modular architecture designed to separate business logic, workflow orchestration, retrieval, infrastructure, and presentation concerns.

Each directory has a clearly defined responsibility, making the codebase easier to navigate, maintain, and extend.

---

## Repository Structure

```text
enterprise-rag-platform/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── graph/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── observability/
│   │   ├── prompts/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tools/
│   │   ├── workers/
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── public/
│   ├── styles/
│   └── ...
│
├── docs/
├── docker-compose.yml
└── README.md
```

---

# 📁 Backend Overview

The backend is organized into independent modules, each responsible for a single layer of the system.

---

## 🤖 agents/

Contains all AI agents that participate in the LangGraph workflow.

```text
agents/

MemoryAgent

PlannerAgent

QueryRewriterAgent

RetrieverAgent

CompressionAgent

AnswerAgent

CitationAgent

ReflectionAgent

VerificationAgent

RetryAgent

ToolExecutorAgent
```

Each agent has a single responsibility and communicates through the shared `GraphState`.

---

## 🌐 api/

Contains all REST API endpoints exposed by FastAPI.

Typical responsibilities include:

- Authentication
- Conversations
- Chat
- Document upload
- Background jobs
- Health checks

The API layer remains thin and delegates business logic to the service layer.

---

## ⚙️ core/

Contains application-wide configuration and shared utilities.

Examples:

- Environment configuration
- Security
- Authentication helpers
- Constants
- Dependency injection

---

## 🗄️ db/

Database configuration and session management.

Responsibilities include:

- SQLAlchemy session
- Engine configuration
- Database initialization
- Migrations integration

---

## 🧠 graph/

Implements the LangGraph workflow.

Contains:

```text
graph/

nodes.py

state.py

workflow.py
```

Responsibilities:

- Workflow definition
- State management
- Agent routing
- Conditional execution
- Retry flow

---

## 📦 models/

SQLAlchemy ORM models.

Examples:

```text
User

Conversation

Message

Document

DocumentChunk

IngestionJob
```

These models define the relational data layer of the platform.

---

## 📝 prompts/

Stores all prompt templates used by the LLM.

Examples:

- Planner Prompt
- Memory Prompt
- Answer Prompt
- Reflection Prompt
- Verification Prompt
- Query Rewriter Prompt
- Compression Prompt

Keeping prompts separate from business logic makes prompt engineering easier and avoids mixing instructions with application code.

---

## 📋 schemas/

Contains Pydantic request and response models.

Responsibilities:

- API validation
- Request serialization
- Response serialization
- Type safety

---

## 🔧 services/

Implements the application's business logic.

Examples:

```text
Authentication

Memory

Retrieval

LLM

Conversation

Messages

Documents

Embeddings

Vector Database

Verification

Reflection

Planner
```

Services are reusable components shared across agents and API endpoints.

---

## 🔍 services/retrieval/

Implements the hybrid retrieval engine.

Components include:

```text
Semantic Retrieval

Keyword Retrieval

Hybrid Retrieval

Reciprocal Rank Fusion

Dynamic Top-K

Metadata Retrieval
```

This layer is responsible for retrieving the most relevant enterprise knowledge before answer generation.

---

## 🛠️ tools/

Provides a unified interface for integrating external tools into the workflow.

Examples include:

- Search services
- Calculators
- External APIs
- Enterprise integrations

The architecture allows new tools to be added without modifying existing agents.

---

## 👷 workers/

Contains background worker implementations.

Responsibilities include:

- Background document ingestion
- Queue processing
- Long-running jobs

Workers communicate through Redis and RQ.

---

## 📊 observability/

Provides the foundation for monitoring and debugging.

Current capabilities include:

- Execution tracing
- Agent timing
- Workflow monitoring
- Error tracking

Future integrations may include:

- Prometheus
- Grafana
- OpenTelemetry

---

# 🎨 Frontend Overview

The frontend provides a modern user interface for interacting with the platform.

Typical responsibilities include:

- Authentication
- Chat interface
- Document upload
- Conversation history
- Source visualization
- Workflow monitoring
- Retrieval analytics

The frontend communicates with the backend exclusively through REST APIs.

---

# 📖 Documentation

The `docs/` directory contains detailed documentation for:

- Architecture
- Backend
- Frontend
- Retrieval
- Agents
- Deployment
- Testing
- API Reference

This keeps the README concise while allowing more in-depth technical documentation to evolve independently.

---

# 🧪 Tests

Automated testing is currently being expanded as part of the production-readiness phase.

The planned test coverage includes:

- Unit tests
- Integration tests
- End-to-end workflow tests
- Retrieval validation
- API testing

The repository should not be considered fully test-complete until this phase is finished.

---

# 🏛️ Architectural Principles

The project structure follows several key engineering principles:

### Separation of Concerns

Each module has a clearly defined responsibility.

---

### Modular Design

New agents, services, retrieval strategies, or tools can be added without major architectural changes.

---

### Layered Architecture

The platform is organized into distinct layers:

```text
Frontend
      │
      ▼
FastAPI API
      │
      ▼
LangGraph Workflow
      │
      ▼
Agents
      │
      ▼
Services
      │
      ▼
Database / Infrastructure
```

---

### Scalability

The modular organization allows individual components to evolve independently, making the platform easier to maintain as it grows.

Whether adding new AI agents, integrating additional retrieval strategies, or supporting new infrastructure components, the project structure is designed to accommodate future expansion while keeping responsibilities clearly separated.

---

# 🚀 Installation & Quick Start

This guide walks through setting up the Enterprise Agentic RAG Platform for local development.

At the end of this section, you will have a fully functional environment consisting of:

- 🌐 Frontend
- ⚙️ FastAPI Backend
- 🗄️ PostgreSQL
- 🔍 Qdrant Vector Database
- ⚡ Redis
- 🤖 Ollama
- 👷 Background Workers

---

# 📋 Prerequisites

Before you begin, ensure the following software is installed.

| Software | Version |
|-----------|----------|
| Python | 3.12+ |
| Node.js | 20+ |
| PostgreSQL | 16+ |
| Docker | Latest |
| Docker Compose | Latest |
| Git | Latest |
| Redis | Latest |
| Ollama | Latest |

---

# 📥 Clone the Repository

```bash
git clone https://github.com/<your-username>/enterprise-rag-platform.git

cd enterprise-rag-platform
```

---

# 📂 Repository Structure

```text
enterprise-rag-platform/

backend/

frontend/

docs/

docker-compose.yml

README.md
```

---

# ⚙️ Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

---

## Create Virtual Environment

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/rag_db

REDIS_URL=redis://localhost:6379

QDRANT_URL=http://localhost:6333

OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=llama3.1:8b

JWT_SECRET_KEY=your-secret-key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> Replace credentials as appropriate for your environment.

---

# 🗄️ Database Setup

Create the PostgreSQL database.

```sql
CREATE DATABASE rag_db;
```

Run migrations.

```bash
alembic upgrade head
```

---

# 🤖 Ollama Setup

Install Ollama from the official website.

Start the Ollama server.

```bash
ollama serve
```

Pull the required model.

```bash
ollama pull llama3.1:8b
```

Verify installation.

```bash
ollama list
```

---

# 🔍 Qdrant

Run Qdrant using Docker.

```bash
docker run -p 6333:6333 qdrant/qdrant
```

The backend automatically creates the required collection on first startup.

---

# ⚡ Redis

Run Redis.

Docker

```bash
docker run -p 6379:6379 redis
```

or use a local installation.

---

# 👷 Background Worker

Start the RQ worker.

```bash
rq worker ingestion
```

The worker processes background document ingestion jobs.

---

# ▶️ Start Backend

```bash
uvicorn app.main:app --reload
```

Backend available at

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

OpenAPI

```
http://localhost:8000/openapi.json
```

---

# 🎨 Frontend Setup

Navigate to the frontend directory.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Create a `.env.local` file.

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run the development server.

```bash
npm run dev
```

Frontend available at

```
http://localhost:3000
```

---

# 🐳 Docker Deployment

The easiest way to start the complete platform is with Docker Compose.

```bash
docker compose up --build
```

This launches:

- Frontend
- Backend API
- PostgreSQL
- Redis
- Qdrant
- Ollama

---

# 🧪 Verify Installation

After all services are running, verify the platform.

## Backend

```
http://localhost:8000/docs
```

Swagger UI should be available.

---

## Frontend

```
http://localhost:3000
```

The chat interface should load successfully.

---

## Upload a Document

1. Open the application.
2. Upload a supported document.
3. Wait for background ingestion to complete.
4. Ask a question related to the uploaded content.

---

# 📄 Supported Document Formats

Current supported formats include:

- PDF
- DOCX
- TXT

Future versions may support:

- XLSX
- PPTX
- HTML
- Markdown
- Images (OCR)

---

# 🔧 Development Commands

### Start Backend

```bash
uvicorn app.main:app --reload
```

---

### Start Frontend

```bash
npm run dev
```

---

### Start Redis Worker

```bash
rq worker ingestion
```

---

### Run Tests

```bash
pytest
```

---

### Format Code

```bash
black .

ruff check .
```

---

### Build Docker Images

```bash
docker compose build
```

---

# 🎯 First Workflow

Once the platform is running, a typical interaction looks like this:

```text
Start Services

↓

Upload Document

↓

Background Ingestion

↓

Chunking

↓

Embedding

↓

Qdrant Indexing

↓

Open Chat

↓

Ask Question

↓

Agentic Workflow

↓

Grounded Response
```

At this point, the core platform can be run locally for development and experimentation. Some advanced retrieval, testing, frontend, and deployment capabilities remain under active development.

---

# 🐳 Docker Deployment

The Enterprise Agentic RAG Platform is fully containerized and can be deployed using **Docker Compose**. This provides a reproducible development environment where all required services are started together with minimal setup.

---

# 📦 Included Services

The default Docker Compose configuration launches the complete application stack.

| Service | Purpose | Default Port |
|----------|---------|-------------:|
| Frontend | Web application | 3000 |
| Backend API | FastAPI application | 8000 |
| PostgreSQL | Relational database | 5432 |
| Qdrant | Vector database | 6333 |
| Redis | Background job queue | 6379 |
| Ollama | Local LLM server | 11434 |
| RQ Worker | Background ingestion | - |

---

# 🏗️ Deployment Architecture

```text
                        ┌────────────────────────┐
                        │       Frontend         │
                        │     Next.js / React    │
                        └───────────┬────────────┘
                                    │
                                    ▼
                        ┌────────────────────────┐
                        │      FastAPI API       │
                        └───────────┬────────────┘
                                    │
        ┌───────────────┬───────────┼───────────────┬──────────────┐
        ▼               ▼           ▼               ▼              ▼
 PostgreSQL         Qdrant        Redis         Ollama        RQ Worker
```

---

# 🚀 Start the Platform

Build and start every service.

```bash
docker compose up --build
```

Run in detached mode.

```bash
docker compose up -d
```

Stop all services.

```bash
docker compose down
```

Remove containers, networks, and volumes.

```bash
docker compose down -v
```

---

# 📋 Verify Running Containers

```bash
docker ps
```

Expected services include:

```text
frontend

backend

postgres

redis

qdrant

ollama

rq-worker
```

---

# 🔍 Service Endpoints

After deployment the following services should be available.

| Service | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| OpenAPI Schema | http://localhost:8000/openapi.json |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| Ollama API | http://localhost:11434 |

---

# 📂 Persistent Data

Docker volumes are used to preserve application data across container restarts.

Persistent storage includes:

- PostgreSQL database
- Qdrant vector collections
- Uploaded documents
- Redis persistence (optional)
- Ollama models

---

# ⚙️ Environment Configuration

All services can be configured using environment variables.

Typical backend configuration:

```env
DATABASE_URL=postgresql://postgres:password@postgres:5432/rag_db

REDIS_URL=redis://redis:6379

QDRANT_URL=http://qdrant:6333

OLLAMA_BASE_URL=http://ollama:11434

OLLAMA_MODEL=llama3.1:8b
```

Frontend configuration:

```env
NEXT_PUBLIC_API_URL=http://backend:8000
```

---

# 👷 Background Processing

Document ingestion is handled asynchronously.

```text
Upload Document

↓

PostgreSQL

↓

Redis Queue

↓

RQ Worker

↓

Document Parsing

↓

Chunking

↓

Embedding

↓

Qdrant Indexing
```

This architecture keeps the API responsive even when processing large documents.

---

# 🔄 Updating the Platform

Pull the latest changes.

```bash
git pull
```

Rebuild containers.

```bash
docker compose build
```

Restart services.

```bash
docker compose up -d
```

---

# 🧹 Cleaning the Environment

Remove unused Docker resources.

```bash
docker system prune
```

Remove unused images.

```bash
docker image prune
```

Remove unused volumes.

```bash
docker volume prune
```

---

# 📈 Scaling

The containerized architecture allows individual services to be scaled independently.

Examples include:

- Multiple FastAPI instances behind a load balancer
- Dedicated RQ worker pools
- Separate Ollama inference servers
- External PostgreSQL clusters
- Managed Redis deployments
- High-availability Qdrant clusters

---

# ☁️ Production Deployment

Although Docker Compose is ideal for development, the platform can also be deployed using container orchestration platforms such as:

- Kubernetes
- Docker Swarm
- AWS ECS
- Azure Container Apps
- Google Cloud Run

Because each service is isolated, migrating to a production orchestration platform requires minimal architectural changes.

---

# ⚙️ Configuration Reference

The Enterprise Agentic RAG Platform is configured using environment variables.

Each service reads its configuration from a `.env` file, allowing the platform to be deployed consistently across development, staging, and production environments.

---

# 📁 Backend Environment Variables

Create a `.env` file inside the `backend/` directory.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/rag_db

REDIS_URL=redis://localhost:6379

QDRANT_URL=http://localhost:6333

OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=llama3.1:8b

JWT_SECRET_KEY=your-secret-key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# 📋 Environment Variable Reference

| Variable | Required | Description | Example |
|-----------|:--------:|-------------|---------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/rag_db` |
| `REDIS_URL` | ✅ | Redis server URL | `redis://localhost:6379` |
| `QDRANT_URL` | ✅ | Qdrant API endpoint | `http://localhost:6333` |
| `OLLAMA_BASE_URL` | ✅ | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | ✅ | Default LLM model | `llama3.1:8b` |
| `JWT_SECRET_KEY` | ✅ | Secret used to sign JWT tokens | `super-secret-key` |
| `JWT_ALGORITHM` | ✅ | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ✅ | Token expiration time | `60` |

---

# 🗄️ Database Configuration

The platform uses PostgreSQL for relational data storage.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/rag_db
```

Stores:

- Users
- Conversations
- Messages
- Documents
- Document Chunks
- Ingestion Jobs
- Metadata

---

# 🔍 Vector Database

Qdrant stores dense vector embeddings generated during document ingestion.

```env
QDRANT_URL=http://localhost:6333
```

Responsibilities:

- Vector indexing
- Similarity search
- Metadata storage
- Retrieval support

---

# 🤖 Language Model

The backend communicates with Ollama for local LLM inference.

```env
OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=llama3.1:8b
```

Current LLM responsibilities include:

- Memory summarization
- Planning
- Query rewriting
- Context compression
- Answer generation
- Reflection
- Verification

The architecture allows future integration with additional providers such as OpenAI, Anthropic, Azure OpenAI, or Google Gemini.

---

# ⚡ Redis

Redis provides the messaging layer for background task processing.

```env
REDIS_URL=redis://localhost:6379
```

Current usage:

- Background ingestion queue
- Worker communication

Future extensions may include:

- Response caching
- Embedding caching
- Rate limiting
- Session storage

---

# 🔐 Authentication

JWT is used for stateless authentication.

```env
JWT_SECRET_KEY=your-secret-key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

These values control:

- Token generation
- Token validation
- Authentication lifetime

> **Security Note:** Never commit production secrets or API keys to version control. Use a secure secret management solution or deployment-specific environment variables.

---

# 🎨 Frontend Configuration

Create a `.env.local` file inside the frontend directory.

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Base URL of the backend API |

---

# 🌍 Environment Profiles

Typical deployment environments include:

## Development

```text
Frontend

↓

localhost:3000

↓

Backend

↓

localhost:8000

↓

Local PostgreSQL

↓

Local Redis

↓

Local Qdrant

↓

Local Ollama
```

---

## Staging

```text
Frontend

↓

Cloud Deployment

↓

Staging Backend

↓

Managed PostgreSQL

↓

Managed Redis

↓

Managed Qdrant

↓

Dedicated Ollama Server
```

---

## Production

```text
Frontend

↓

Load Balancer

↓

FastAPI Cluster

↓

Managed PostgreSQL

↓

Redis Cluster

↓

Qdrant Cluster

↓

Dedicated Inference Servers
```

---

# 🔒 Security Recommendations

For production deployments:

- Use strong, randomly generated JWT secrets.
- Store secrets outside the repository.
- Enable HTTPS for all services.
- Restrict database access to trusted networks.
- Protect Qdrant and Redis from public exposure.
- Rotate credentials regularly.
- Apply the principle of least privilege for database users.

---

# 📦 Configuration Summary

| Component | Configured By |
|-----------|---------------|
| PostgreSQL | `DATABASE_URL` |
| Redis | `REDIS_URL` |
| Qdrant | `QDRANT_URL` |
| Ollama | `OLLAMA_BASE_URL`, `OLLAMA_MODEL` |
| Authentication | `JWT_*` variables |
| Frontend | `NEXT_PUBLIC_API_URL` |

The platform is fully environment-driven, allowing the same codebase to be deployed consistently across local development, staging, and production environments with minimal configuration changes.

---

# 📡 REST API Guide

The Enterprise Agentic RAG Platform exposes a RESTful API built with **FastAPI** for document management, authentication, conversations, and AI-powered question answering.

Interactive API documentation is automatically generated using OpenAPI and Swagger.

---

# 🌐 Base URL

Development

```text
http://localhost:8000
```

Swagger UI

```text
http://localhost:8000/docs
```

OpenAPI Specification

```text
http://localhost:8000/openapi.json
```

---

# 🔐 Authentication

Most protected endpoints require a JWT Bearer Token.

Authorization Header

```http
Authorization: Bearer <access_token>
```

---

# Authentication Flow

```text
Register

↓

Login

↓

Receive JWT Token

↓

Call Protected APIs

↓

Refresh/Login Again (when expired)
```

---

# 🔑 Authentication Endpoints

## Register User

```http
POST /api/v1/auth/register
```

### Request

```json
{
  "email": "john@example.com",
  "password": "StrongPassword123",
  "full_name": "John Doe"
}
```

### Response

```json
{
  "id": 1,
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

---

## Login

```http
POST /api/v1/auth/login
```

### Request

```json
{
  "email": "john@example.com",
  "password": "StrongPassword123"
}
```

### Response

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

# 💬 Conversation Endpoints

## Create Conversation

```http
POST /api/v1/conversations
```

### Response

```json
{
  "id": 12,
  "title": "New Conversation"
}
```

---

## Get Conversation

```http
GET /api/v1/conversations/{conversation_id}
```

---

# 🤖 Chat Endpoint

The chat endpoint executes the complete Agentic RAG workflow.

```http
POST /api/v1/chat
```

---

### Request

```json
{
  "conversation_id": 5,
  "question": "What is the annual leave policy?",
  "retrieval_strategy": "hybrid"
}
```

---

### Response

```json
{
  "answer": "...",
  "sources": [],
  "citations": [],
  "reflection": {},
  "verification": {},
  "confidence": 0.94,
  "query_type": "knowledge",
  "retrieval_score": 0.91,
  "retrieved_documents": 4,
  "retry_count": 0,
  "execution_trace": [],
  "agent_timings": {},
  "errors": []
}
```

---

# 📄 Document Endpoints

## Upload Document

```http
POST /api/v1/documents/upload
```

Supports multipart file uploads.

Supported formats:

- PDF
- DOCX
- TXT

---

## List Documents

```http
GET /api/v1/documents
```

---

## Get Document

```http
GET /api/v1/documents/{document_id}
```

---

## Delete Document

```http
DELETE /api/v1/documents/{document_id}
```

---

# 👷 Background Jobs

## Get Ingestion Job

```http
GET /api/v1/jobs/{job_id}
```

Example Response

```json
{
  "id": 25,
  "status": "COMPLETED",
  "document_id": 4
}
```

---

# ❤️ Health Check

```http
GET /health
```

Example Response

```json
{
  "status": "healthy"
}
```

---

# 🔍 Retrieval Strategies

The chat endpoint supports multiple retrieval strategies.

| Strategy | Description |
|----------|-------------|
| `semantic` | Vector similarity search |
| `keyword` | PostgreSQL keyword search |
| `hybrid` | Semantic + keyword + reranking |

Example

```json
{
  "retrieval_strategy": "hybrid"
}
```

---

# 🔄 Agentic Workflow

Every chat request executes the complete workflow.

```text
Client Request
      │
      ▼
Memory Agent
      │
      ▼
Planner Agent
      │
      ▼
Query Rewriter
      │
      ▼
Retriever
      │
      ▼
Compression
      │
      ▼
Answer Generation
      │
      ▼
Citation
      │
      ▼
Reflection
      │
      ▼
Verification
      │
      ▼
Retry (if required)
      │
      ▼
API Response
```

---

# 📊 Response Metadata

Each response includes additional metadata beyond the generated answer.

| Field | Description |
|--------|-------------|
| `answer` | Final generated response |
| `sources` | Retrieved document chunks |
| `citations` | Source references |
| `confidence` | Reflection confidence score |
| `query_type` | Planner classification |
| `retrieval_score` | Highest retrieval score |
| `retrieved_documents` | Number of retrieved chunks |
| `retry_count` | Workflow retry count |
| `execution_trace` | Agent execution sequence |
| `agent_timings` | Per-agent execution time |
| `errors` | Workflow errors (if any) |

---

# ❌ Error Responses

The API uses standard HTTP status codes.

| Status Code | Meaning |
|------------:|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Invalid Request |
| 401 | Authentication Required |
| 403 | Permission Denied |
| 404 | Resource Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

Example

```json
{
  "detail": "Document not found."
}
```

---

# 📚 Interactive API Documentation

FastAPI automatically generates interactive documentation.

| Tool | URL |
|------|-----|
| Swagger UI | `/docs` |
| ReDoc | `/redoc` *(if enabled)* |
| OpenAPI JSON | `/openapi.json` |

These endpoints provide a complete, always up-to-date API reference, allowing developers to explore, test, and integrate with the platform without additional tooling.

---

# 🎯 End-to-End Workflow

This section demonstrates how the Enterprise Agentic RAG Platform processes a user request from document ingestion to the final grounded response.

Instead of viewing the platform as a collection of independent components, this walkthrough illustrates how they collaborate to produce reliable, context-aware answers.

---

# 📄 Step 1 — Upload Enterprise Documents

A user uploads one or more enterprise documents through the web interface.

Supported formats include:

- PDF
- DOCX
- TXT

Example:

```text
HR_Policy.pdf
Employee_Handbook.pdf
IT_Security_Guide.pdf
```

The backend stores document metadata in PostgreSQL and schedules a background ingestion job.

---

# ⚡ Step 2 — Background Document Ingestion

The upload request immediately returns to the user while ingestion continues asynchronously.

```text
Upload Document

↓

PostgreSQL

↓

Redis Queue

↓

RQ Worker
```

This ensures that large documents do not block API requests.

---

# 📑 Step 3 — Document Processing

The ingestion worker performs several preprocessing stages.

```text
Document

↓

Parser

↓

Text Extraction

↓

Chunking

↓

Embedding Generation

↓

Vector Indexing
```

### Parsing

The parser extracts text while preserving document metadata.

Example metadata:

```json
{
  "filename": "HR_Policy.pdf",
  "content_type": "application/pdf",
  "page_count": 24
}
```

---

### Chunking

Large documents are divided into overlapping chunks.

```text
Document

↓

Chunk 1

Chunk 2

Chunk 3

Chunk 4
```

Chunking improves retrieval accuracy while keeping prompt sizes manageable.

---

### Embedding Generation

Each chunk is converted into a dense vector representation using the embedding model.

```text
Chunk

↓

Embedding Model

↓

384-dimensional Vector
```

---

### Vector Indexing

Embeddings are stored in Qdrant together with metadata.

Stored metadata includes:

- Document ID
- Chunk ID
- Tenant ID
- Chunk Content
- Custom Metadata

---

# 💬 Step 4 — User Asks a Question

Example question:

```text
What is the annual leave policy for employees?
```

The question is submitted to the chat endpoint.

---

# 🧠 Step 5 — Memory Agent

The workflow begins by gathering conversation context.

Sources include:

- Conversation summary
- Recent messages
- Previous interactions

Result:

```text
Memory Context
```

---

# 📋 Step 6 — Planner Agent

The planner analyzes the request.

Example output:

```text
Query Type

↓

Knowledge Query

↓

Needs Retrieval

↓

Execution Plan
```

The planner determines which downstream agents should execute.

---

# ✍️ Step 7 — Query Rewriter

The user question is optimized for retrieval.

Example:

Original

```text
What is the annual leave policy?
```

↓

Rewritten

```text
Employee annual leave vacation policy paid leave entitlement
```

The rewritten query improves retrieval quality while preserving the original intent.

---

# 🔍 Step 8 — Hybrid Retrieval

The retriever searches enterprise knowledge using multiple retrieval strategies.

```text
Query

↓

Semantic Search

+

Keyword Search

+

Metadata Filtering

↓

Reciprocal Rank Fusion

↓

CrossEncoder Reranking

↓

Top Ranked Chunks
```

Example retrieved chunks:

```text
Chunk 18

Annual leave policy...

Score: 0.93

↓

Chunk 42

Paid leave eligibility...

Score: 0.89

↓

Chunk 55

Leave approval workflow...

Score: 0.86
```

---

# 🗜️ Step 9 — Context Compression

Retrieved chunks are compressed before answer generation.

Benefits:

- Lower token usage
- Reduced latency
- Higher information density

---

# 🤖 Step 10 — Answer Generation

The Answer Agent receives:

- User question
- Memory context
- Compressed retrieval context

The language model generates a grounded response using enterprise knowledge.

---

# 📚 Step 11 — Citation Generation

The Citation Agent associates supporting document references with the generated response.

Example:

```text
Employees are entitled to 20 days of annual leave. [1]
```

This improves transparency and allows users to trace information back to the source material.

---

# 🔍 Step 12 — Reflection

The Reflection Agent evaluates the generated answer.

Example:

```json
{
  "passed": true,
  "confidence": 0.94,
  "grounded": true,
  "retry": false
}
```

Reflection estimates answer quality before returning a response.

---

# ✅ Step 13 — Verification

The Verification Agent validates that the answer is supported by retrieved evidence.

Checks include:

- Evidence support
- Missing information
- Hallucinated content
- Confidence

Example:

```json
{
  "supported": true,
  "confidence": 0.91,
  "hallucinations": []
}
```

---

# 🔄 Step 14 — Adaptive Retry (If Needed)

If Reflection or Verification determines that the answer is insufficient, the Retry Agent adjusts the retrieval strategy.

Possible actions include:

- Increasing Top-K
- Switching to hybrid retrieval
- Expanding the retrieval query
- Running another workflow iteration

```text
Retry

↓

Improved Retrieval

↓

Updated Context

↓

Regenerated Answer
```

This improves answer quality without requiring user intervention.

---

# 📤 Step 15 — Final Response

The API returns a structured response.

Example:

```json
{
  "answer": "...",
  "sources": [...],
  "citations": [...],
  "reflection": {
    "confidence": 0.94
  },
  "verification": {
    "supported": true
  },
  "retrieval_score": 0.91,
  "retrieved_documents": 4,
  "retry_count": 0
}
```

---

# 🔄 Complete Workflow

```text
Upload Document
       │
       ▼
Background Ingestion
       │
       ▼
Document Parsing
       │
       ▼
Chunking
       │
       ▼
Embedding Generation
       │
       ▼
Qdrant Indexing
       │
       ▼
────────────────────────────────────────────
               User Question
────────────────────────────────────────────
       │
       ▼
Memory Agent
       │
       ▼
Planner Agent
       │
       ▼
Query Rewriter
       │
       ▼
Hybrid Retrieval
       │
       ▼
Context Compression
       │
       ▼
Answer Generation
       │
       ▼
Citation Generation
       │
       ▼
Reflection
       │
       ▼
Verification
       │
       ▼
Retry (if required)
       │
       ▼
Final Response
```

---

# 🚀 Why This Workflow?

This architecture transforms a traditional RAG pipeline into a structured reasoning workflow.

Compared to conventional RAG systems, the Enterprise Agentic RAG Platform provides:

| Traditional RAG | Enterprise Agentic RAG |
|-----------------|------------------------|
| Single retrieval step | Multi-stage hybrid retrieval |
| Direct answer generation | Planner-guided workflow |
| Static prompts | Query rewriting & memory |
| No validation | Reflection & verification |
| Fixed retrieval | Adaptive retry mechanism |
| Basic chatbot | Production-oriented AI workflow |

By decomposing the problem into specialized stages, the platform produces more reliable, explainable, and maintainable AI-assisted responses while remaining flexible enough to support future extensions and enterprise use cases.

---

# 📸 Screenshots & Demo

Actual screenshots will be added after the frontend polish phase is complete.

---

# 💬 AI Chat Interface

The primary interface allows users to ask questions over enterprise documents using the complete Agentic RAG workflow.

<p align="center">
    <img src="docs/images/chat.png" width="95%">
</p>

### Highlights

- Natural language conversations
- Context-aware responses
- Source citations
- Reflection confidence
- Verification results

---

# 📄 Document Upload

Enterprise documents can be uploaded directly from the web interface.

<p align="center">
    <img src="docs/images/upload.png" width="95%">
</p>

Supported formats

- PDF
- DOCX
- TXT

Features

- Drag & Drop Upload
- Background Processing
- Automatic Indexing
- Upload Progress

---

# 📚 Document Library

Uploaded documents are organized in a searchable document library.

<p align="center">
    <img src="docs/images/documents.png" width="95%">
</p>

Displays

- Filename
- Upload Date
- Processing Status
- File Type
- Metadata

---

# 🔍 Hybrid Retrieval

Visual representation of retrieved document chunks.

<p align="center">
    <img src="docs/images/retrieval.png" width="95%">
</p>

Includes

- Semantic Score
- Keyword Score
- Reranker Score
- Retrieved Chunks

---

# 🤖 Agent Workflow

Real-time visualization of the LangGraph execution.

<p align="center">
    <img src="docs/images/workflow.png" width="95%">
</p>

Displays

- Active Agent
- Execution Order
- Workflow State
- Retry Path

---

# 📊 Reflection & Verification

Quality assurance results for every generated response.

<p align="center">
    <img src="docs/images/reflection.png" width="95%">
</p>

Metrics include

- Reflection Confidence
- Verification Confidence
- Grounding Status
- Retry Decision

---

# 📈 Analytics Dashboard

Monitor system performance and workflow execution.

<p align="center">
    <img src="docs/images/dashboard.png" width="95%">
</p>

Example Metrics

- Response Time
- Retrieval Latency
- LLM Latency
- Documents Indexed
- Questions Answered
- Average Confidence

---

# 🗂️ Conversation History

Conversation memory across multiple sessions.

<p align="center">
    <img src="docs/images/history.png" width="95%">
</p>

Features

- Conversation List
- Search
- Recent Messages
- Conversation Summary

---

# 📱 Responsive Design

The platform is designed to work across multiple screen sizes.

<p align="center">
    <img src="docs/images/responsive.png" width="95%">
</p>

Supports

- Desktop
- Laptop
- Tablet
- Mobile

---

# 🎥 Demo

A demonstration video will be added once the frontend and workflow presentation are finalized.

The demo covers

- Authentication
- Document Upload
- Background Ingestion
- Chat Interface
- Hybrid Retrieval
- Agent Workflow
- Reflection
- Verification
- Conversation Memory

---

# 📂 Screenshots Directory

```text
docs/

images/

chat.png

upload.png

documents.png

retrieval.png

workflow.png

reflection.png

dashboard.png

history.png

responsive.png
```

All screenshots are referenced from the `docs/images` directory to keep the repository organized and make future updates straightforward.


---

# 📈 Performance & Benchmarks

The Enterprise Agentic RAG Platform is designed around a modular architecture that prioritizes scalability, reliability, and maintainability. Rather than optimizing a single component, the platform improves overall performance by separating responsibilities across specialized services and AI agents.

---

# ⚡ Performance-Oriented Design

Several architectural decisions contribute to the responsiveness and scalability of the platform.

| Feature | Benefit |
|----------|---------|
| Background Document Ingestion | Uploads return immediately while indexing occurs asynchronously |
| Hybrid Retrieval | Improves retrieval quality without sacrificing flexibility |
| Dynamic Top-K Selection | Reduces unnecessary retrieval for simple queries |
| Context Compression | Lowers LLM token usage |
| CrossEncoder Reranking | Improves ranking precision before generation |
| Conversation Memory | Avoids repeatedly supplying entire conversation history |
| Modular Services | Independent optimization of retrieval, memory, and generation |
| LangGraph Workflow | Structured execution with conditional routing and retries |

---

# 🚀 Workflow Optimization

The platform minimizes unnecessary computation by executing only the stages required for a particular request.

```text
User Request
      │
      ▼
Planner Agent
      │
      ▼
Determines Required Execution Path
      │
      ├───────────────┐
      ▼               ▼
 Retrieval        Tool Execution
      │               │
      └───────┬───────┘
              ▼
      Answer Generation
```

This approach avoids treating every request identically and allows the workflow to adapt based on the characteristics of the query.

---

# 📄 Background Document Processing

Document ingestion is fully asynchronous.

```text
Upload

↓

API Response

↓

Redis Queue

↓

RQ Worker

↓

Parsing

↓

Chunking

↓

Embedding

↓

Vector Indexing
```

Benefits include:

- Faster user experience
- Non-blocking uploads
- Independent worker scaling
- Improved API responsiveness

---

# 🔍 Retrieval Efficiency

The retrieval engine combines multiple techniques to improve relevance while keeping context sizes manageable.

Current pipeline:

```text
Query

↓

Query Rewriting

↓

Semantic Search

+

Keyword Search

↓

Reciprocal Rank Fusion

↓

CrossEncoder Reranking

↓

Dynamic Top-K

↓

Context Builder
```

This layered approach helps balance retrieval quality and prompt efficiency.

---

# 🧠 Token Optimization

Several components are specifically designed to reduce unnecessary LLM context.

Current optimizations include:

- Context Compression
- Dynamic Top-K Retrieval
- Query Rewriting
- Conversation Summaries
- Recent Message Memory

These optimizations reduce prompt size while preserving relevant information.

---

# 📊 Observability

The platform captures execution metadata that can be used to analyze workflow behavior.

Current metrics include:

- Execution Trace
- Agent Timings
- Retrieval Scores
- Reflection Confidence
- Verification Confidence
- Retry Count
- Error Tracking

These metrics provide visibility into the reasoning pipeline and support debugging and future performance tuning.

---

# 📈 Scalability

The architecture is designed so that major components can scale independently.

```text
                    Load Balancer
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
    FastAPI Instance                  FastAPI Instance
          │                                 │
          └────────────────┬────────────────┘
                           ▼
                    PostgreSQL
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
         Qdrant         Redis         Ollama
                           │
                    Multiple Workers
```

Examples of independent scaling:

- API servers
- Background workers
- Redis
- PostgreSQL
- Qdrant
- Ollama inference servers

---

# 🎯 Reliability Features

The platform includes several mechanisms to improve answer quality and operational reliability.

| Capability | Purpose |
|------------|---------|
| Reflection | Self-evaluate generated responses |
| Verification | Validate answers against retrieved evidence |
| Retry Mechanism | Improve responses when confidence is low |
| Citation Generation | Increase transparency and traceability |
| Conversation Memory | Preserve context across interactions |

---

# 🧪 Benchmarking

This repository intentionally does **not** publish fixed benchmark numbers.

Actual latency and throughput depend on factors such as:

- Selected LLM
- Hardware configuration
- Document size
- Number of indexed documents
- Embedding model
- Retrieval strategy
- Concurrent users

Instead of reporting hardware-specific metrics, the platform provides observability hooks so deployments can measure performance in their own environments.

---

# 🔮 Future Performance Enhancements

The current architecture provides a foundation for additional optimizations, including:

- Embedding Cache
- Retrieval Cache
- LLM Response Cache
- Streaming Responses
- Batch Embedding Generation
- Distributed Workers
- Horizontal API Scaling
- Distributed Vector Search
- Prometheus Metrics
- OpenTelemetry Tracing
- Grafana Dashboards

---

# 📌 Performance Philosophy

The goal of the Enterprise Agentic RAG Platform is not simply to maximize raw throughput, but to balance **response quality**, **retrieval accuracy**, **operational scalability**, and **maintainability**.

By combining asynchronous processing, modular services, adaptive retrieval, and multi-agent orchestration, the platform provides a strong foundation for building reliable enterprise-grade Retrieval-Augmented Generation systems.

---

# 🗺️ Roadmap

The Enterprise Agentic RAG Platform is being developed incrementally, with each phase introducing new capabilities while maintaining a modular, production-oriented architecture.

The roadmap below highlights completed milestones as well as planned enhancements for future releases.

---

# ✅ Completed Milestones

## Phase 1 — Foundation

**Status:** ✅ Completed

Core platform and infrastructure.

### Features

- FastAPI Backend
- PostgreSQL Integration
- SQLAlchemy ORM
- JWT Authentication
- User Management
- Conversation Management
- Document Upload API
- Document Storage
- Modular Service Architecture

---

## Phase 2 — Production RAG

**Status:** ✅ Completed

Enterprise-ready Retrieval-Augmented Generation.

### Features

- Document Parsing
- Automatic Chunking
- Embedding Generation
- Qdrant Vector Database
- Background Ingestion
- Redis Queue
- RQ Workers
- Multi-Tenancy
- Role-Based Access Control (RBAC)
- Conversation Memory
- Metadata Support

---

## Phase 3 — Agentic Workflow

**Status:** ✅ Completed

LangGraph-powered multi-agent reasoning.

### Features

- Graph-Based Workflow
- Shared Graph State
- Conditional Routing
- Retry Flow
- Execution Trace
- Agent Timing Collection

---

## Phase 4 — AI Agents

**Status:** ✅ Completed

Specialized AI agents responsible for different stages of the reasoning process.

### Implemented Agents

- ✅ Memory Agent
- ✅ Planner Agent
- ✅ Query Rewriter Agent
- ✅ Retriever Agent
- ✅ Compression Agent
- ✅ Answer Agent
- ✅ Citation Agent
- ✅ Reflection Agent
- ✅ Verification Agent
- ✅ Retry Agent
- ✅ Tool Executor Agent

---

## Phase 5 — Advanced Retrieval

**Status:** 🚧 In Progress

Enterprise retrieval pipeline.

### Current / Implemented Components

- Semantic Search
- PostgreSQL Keyword Search
- Hybrid Retrieval
- CrossEncoder Reranking
- Context Builder
- Query Rewriting
- RRF utility
- Dynamic Top-K selector
- Metadata retrieval interface

### Remaining Integration Work

- Integrate RRF into the active hybrid search path
- Integrate dynamic Top-K selection into workflow execution
- Implement metadata-aware filtering

---

## Phase 6 — Production Readiness

**Status:** 🚧 In Progress

Current focus is on transforming the project into a polished, production-oriented portfolio project.

### Current Work

- ✅ Codebase Cleanup
- ✅ Consistent Logging
- ✅ Type Hints
- ✅ Docstrings
- ✅ Service Refactoring
- ✅ Documentation
- 🚧 Frontend Polish
- 🚧 Automated Testing
- 🚧 CI/CD Pipeline
- 🚧 Deployment Guides

---

# 🚀 Future Roadmap

The following features are planned for future releases.

---

## Phase 7 — Enterprise Integrations

**Planned**

### Goals

- Microsoft SharePoint Connector
- Confluence Connector
- Google Drive Connector
- OneDrive Connector
- Notion Connector
- Slack Knowledge Search
- GitHub Repository Search

---

## Phase 8 — Advanced Retrieval

**Planned**

### Enhancements

- PostgreSQL Full-Text Search
- BM25 Ranking
- Hybrid Score Calibration
- Metadata-Aware Ranking
- Query Expansion Strategies
- Learning-to-Rank
- Knowledge Graph Retrieval (GraphRAG)

---

## Phase 9 — Multi-Modal RAG

**Planned**

Support additional document formats and modalities.

### Planned Features

- OCR for Images
- PowerPoint Support
- Excel Support
- HTML Parsing
- Markdown Parsing
- Table Extraction
- Diagram Understanding

---

## Phase 10 — Tool Ecosystem

**Planned**

Expand the platform with external tool integrations.

### Planned Features

- Calculator Tool
- SQL Query Tool
- Web Search Tool
- Internal API Connectors
- MCP-Compatible Tool Integration
- Enterprise Tool Registry

---

## Phase 11 — Observability

**Planned**

Production-grade monitoring and diagnostics.

### Planned Features

- Prometheus Metrics
- Grafana Dashboards
- OpenTelemetry Tracing
- Request Analytics
- Token Usage Tracking
- Workflow Visualization

---

## Phase 12 — Scalability

**Planned**

Support larger enterprise deployments.

### Planned Features

- Distributed Workers
- Horizontal API Scaling
- Response Streaming
- Embedding Cache
- Retrieval Cache
- LLM Response Cache
- Distributed Vector Search

---

## Phase 13 — Evaluation Framework

**Planned**

Comprehensive evaluation of retrieval and generation quality.

### Planned Features

- Retrieval Evaluation
- Groundedness Metrics
- Hallucination Detection
- Agent Performance Reports
- Benchmark Dataset Support
- Regression Testing

---

## Phase 14 — Enterprise Platform

**Long-Term Vision**

The long-term objective is to evolve the platform into a complete enterprise AI knowledge platform.

Potential capabilities include:

- Multi-Agent Collaboration
- Autonomous Workflows
- Organization Knowledge Graphs
- Enterprise Search Portal
- AI Analytics Dashboard
- Workflow Builder
- Plugin Marketplace
- Fine-Grained Access Control
- Multi-Organization Deployments

---

# 📌 Development Philosophy

The project follows several guiding principles:

- **Modularity** — Components should have clear responsibilities and be independently replaceable.
- **Reliability** — Reflection, verification, and retrieval quality are prioritized over raw generation speed.
- **Extensibility** — New agents, tools, and retrieval strategies should integrate without major architectural changes.
- **Production Readiness** — Features are designed with maintainability, observability, and scalability in mind.
- **Open Architecture** — The platform should remain adaptable to new models, databases, and enterprise integrations.

---

# 🎯 Current Status

| Area | Status |
|------|:------:|
| Backend Architecture | ✅ Complete |
| Agentic Workflow | ✅ Complete |
| Hybrid Retrieval | 🚧 In Progress |
| Conversation Memory | ✅ Complete |
| Background Ingestion | ✅ Complete |
| Multi-Tenancy & RBAC | 🚧 In Progress |
| Documentation | 🚧 In Progress |
| Frontend | 🚧 In Progress |
| Automated Testing | 🚧 In Progress |
| CI/CD | 📅 Planned |
| Production Deployment | 📅 Planned |

---

# 🌟 Vision

The long-term vision is to build a modular, extensible, and production-ready Agentic RAG platform that serves as a foundation for enterprise AI assistants, intelligent knowledge systems, and advanced Retrieval-Augmented Generation applications.

The architecture is intentionally designed so that future capabilities can be added incrementally while preserving a clean separation of concerns and a maintainable codebase.

---

## 🤝 Contributing

This project is currently developed and maintained independently by a single developer.

Suggestions, bug reports, and improvement ideas are welcome. If you find an issue or have a meaningful suggestion, open a GitHub Issue with enough context to reproduce or evaluate it.

For substantial changes, please describe the proposed approach before submitting a pull request.

# 🙏 Acknowledgements

This project was developed independently and builds upon the work of the open-source community.

The platform uses and is inspired by projects including:

- FastAPI
- LangGraph
- LangChain
- Qdrant
- PostgreSQL
- SQLAlchemy
- Redis
- RQ
- Ollama
- Sentence Transformers
- Hugging Face
- PyMuPDF
- python-docx
- React
- Next.js
- Tailwind CSS
- Docker

Thanks to the maintainers and contributors of these projects for making the underlying technologies available.

<div align="center">

## ⭐ Support the Project

If you found this project useful or interesting, consider giving it a ⭐ on GitHub.

---

**Enterprise Agentic RAG Platform**

Production-Oriented • Modular • Explainable • Enterprise-Focused

Independently developed with FastAPI, LangGraph, PostgreSQL, Qdrant, Redis, Ollama, and Python.

</div>