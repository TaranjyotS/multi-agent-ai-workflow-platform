<div align="center">

# 🤖 Multi-Agent AI Workflow Platform

### Production-grade multi-agent orchestration system for enterprise research, coding, review, planning, data, and reporting workflows.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Persistence-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20Search-DC244C?style=for-the-badge)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployable-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

</div>

---

## 📌 Overview

`multi-agent-ai-workflow-platform` is a portfolio-grade backend platform that coordinates specialized AI agents to solve complex enterprise workflows. It includes real workflow execution, agent state persistence, RAG-style knowledge retrieval, human-in-the-loop review gates, task delegation, API contracts, database models, tests, CI/CD, Docker, Kubernetes, monitoring hooks, and AWS deployment documentation.

This project is designed to demonstrate senior-level engineering across backend architecture, AI orchestration, DevSecOps, observability, testing, and cloud deployment.

> This project includes deterministic local AI agent execution for reproducible demos, with production extension points for OpenAI, Claude, Bedrock, Ollama, LangGraph, Redis, and Qdrant.
---

## 🎯 Business Problem

Enterprise teams often need to coordinate research, planning, coding, data analysis, review, and reporting across multiple tools and stakeholders. A single chatbot is not enough for regulated or production workflows because teams need traceability, approval gates, repeatable execution, structured state, audit trails, and retrieval from private knowledge sources.

This platform solves that by orchestrating specialized agents through a controlled workflow engine with persistence, knowledge retrieval, human approval, and operational visibility.

---

## 👥 Target Users

|           User            |                               Need                                      |
|---------------------------|-------------------------------------------------------------------------|
| Engineering Teams         | Automate planning, code generation, review, and reporting workflows     |
| Data Teams                | Query internal documents, summarize data context, and produce reports   |
| Platform Teams            | Deploy repeatable AI workflows with security and observability          |
| Product Managers          | Convert vague requirements into structured plans and delivery artifacts |
| Security/Compliance Teams | Enforce approvals, audit logs, and controlled execution                 |

---

## ✅ Functional Requirements

- Create and execute multi-agent workflows
- Support Research, Planning, Coding, Review, Data, and Reporting agents
- Persist workflow state, steps, approvals, and audit events
- Ingest internal knowledge documents
- Retrieve relevant context using vector-style search
- Trigger human-in-the-loop approval gates
- Resume workflows after approval
- Expose REST APIs with OpenAPI documentation
- Provide health and metrics endpoints
- Support local and containerized execution

---

## 🧱 Non-Functional Requirements

|    Category     |                          Requirement                                        |
|-----------------|-----------------------------------------------------------------------------|
| Scalability     | Stateless API layer, externalized DB/cache/vector services                  |
| Reliability     | Workflow state persisted after every step                                   |
| Security        | API key middleware, input validation, audit logging, dependency scanning    |
| Testability     | Unit and integration tests with dependency overrides                        |
| Observability   | Structured logs, Prometheus-style metrics, request correlation IDs          |
| Maintainability | Layered architecture with services, repositories, agents, schemas           |
| Portability     | SQLite quickstart, PostgreSQL production profile, Docker/Kubernetes support |

---

## 🏗️ High-Level Architecture

```mermaid
flowchart LR
    Client[Client / Frontend / API Consumer] --> API[FastAPI Gateway]
    API --> Auth[API Key Middleware]
    API --> Workflow[Workflow Orchestrator]
    Workflow --> Agents[Specialized AI Agents]
    Agents --> Tools[Tool Registry]
    Agents --> Memory[Agent Memory]
    Agents --> RAG[RAG Retrieval Service]
    RAG --> Qdrant[(Qdrant Vector Store)]
    Workflow --> DB[(PostgreSQL / SQLite)]
    Workflow --> Redis[(Redis Cache)]
    API --> Metrics[Metrics Endpoint]
```

---

## 🔍 Detailed Architecture

```mermaid
flowchart TD
    A[POST /api/v1/workflows] --> B[Workflow Service]
    B --> C[Create DB Workflow Record]
    C --> D[Orchestrator]
    D --> E[Planning Agent]
    E --> F[Research Agent]
    F --> G[Data Agent]
    G --> H[Coding Agent]
    H --> I[Review Agent]
    I --> J{Human Approval Required?}
    J -- Yes --> K[Pause Workflow]
    K --> L[POST /approvals]
    L --> M[Reporting Agent]
    J -- No --> M
    M --> N[Persist Final Report]
```

---

## 🗄️ Database Design

```mermaid
erDiagram
    WORKFLOWS ||--o{ WORKFLOW_STEPS : contains
    WORKFLOWS ||--o{ HUMAN_APPROVALS : requires
    WORKFLOWS ||--o{ AUDIT_EVENTS : records
    KNOWLEDGE_DOCUMENTS ||--o{ KNOWLEDGE_CHUNKS : contains

    WORKFLOWS {
        uuid id PK
        string title
        string objective
        string status
        json metadata
        datetime created_at
        datetime updated_at
    }

    WORKFLOW_STEPS {
        uuid id PK
        uuid workflow_id FK
        string agent_name
        string status
        text input_text
        text output_text
        int step_order
        datetime created_at
    }

    HUMAN_APPROVALS {
        uuid id PK
        uuid workflow_id FK
        string status
        text question
        text decision_reason
        datetime created_at
        datetime resolved_at
    }

    KNOWLEDGE_DOCUMENTS {
        uuid id PK
        string title
        string source
        datetime created_at
    }

    KNOWLEDGE_CHUNKS {
        uuid id PK
        uuid document_id FK
        int chunk_index
        text content
        json embedding
    }
```

---

## 🔌 API Design

| Method |              Endpoint              |            Purpose             |
|--------|------------------------------------|--------------------------------|
| `GET`  | `/health`                          | Service health                 |
| `GET`  | `/metrics`                         | Prometheus-style metrics       |
| `GET`  | `/api/v1/agents`                   | List available agents          |
| `POST` | `/api/v1/knowledge/documents`      | Ingest knowledge document      |
| `GET`  | `/api/v1/knowledge/search`         | Search knowledge base          |
| `POST` | `/api/v1/workflows`                | Create and execute workflow    |
| `GET`  | `/api/v1/workflows`                | List workflows                 |
| `GET`  | `/api/v1/workflows/{id}`           | Get workflow details           |
| `POST` | `/api/v1/workflows/{id}/approvals` | Approve/reject HITL checkpoint |

OpenAPI docs are available at `/docs` when the app is running.

---

<details>
<summary><strong>📁 Folder Structure</strong></summary>

```text
multi-agent-ai-workflow-platform/
├── app/
│   ├── agents/              # Specialized agent implementations
│   ├── api/                 # FastAPI routers
│   ├── core/                # Settings, security, logging, metrics
│   ├── db/                  # SQLAlchemy models/session/repositories
│   ├── orchestration/       # Workflow engine
│   ├── rag/                 # Knowledge ingestion and retrieval
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business services
│   └── main.py              # FastAPI app factory
├── docs/                    # Architecture, API, deployment, diagrams
├── k8s/                     # Kubernetes manifests
├── sample_data/             # Example enterprise documents
├── tests/                   # Unit and API tests
├── docker-compose.yml
├── .env.example           # Local development defaults
├── .env.docker            # Docker Compose service-name configuration
├── Dockerfile
├── Jenkinsfile
├── Makefile
├── requirements.txt
└── README.md
```

</details>

---

## 🚀 Quick Start

### Option A: Docker Compose Mode Recommended

Use this mode when you want the full platform stack: FastAPI, PostgreSQL, Redis, and Qdrant.

```bash
docker compose down -v
docker compose up --build
```

Then open:

|        Service       |                URL                |                                 Notes                          |
|----------------------|-----------------------------------|----------------------------------------------------------------|
| FastAPI Swagger Docs | `http://localhost:8000/docs`      | Main API testing interface                                     |
| FastAPI Root         | `http://localhost:8000`           | Service status and useful links                                |
| Health Check         | `http://localhost:8000/health`    | Load balancer health endpoint                                  |
| Metrics              | `http://localhost:8000/metrics`   | Prometheus-style metrics                                       |
| Qdrant Dashboard     | `http://localhost:6333/dashboard` | Vector database dashboard, if supported by your Qdrant version |
| Qdrant API Root      | `http://localhost:6333`           | Returns Qdrant version JSON                                    |

> Use `localhost` in the browser. Do not open `http://0.0.0.0:8000`; `0.0.0.0` is only the internal bind address shown by Uvicorn.

### Option B: Local Python Mode

Use this mode only when you want to run the API directly on your machine. For the simplest local start, `.env.example` uses SQLite.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

If you want local Python mode to connect to the Docker PostgreSQL container, update `.env` to use `localhost`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/multi_agent_ai
REDIS_URL=redis://localhost:6379/0
QDRANT_URL=http://localhost:6333
```

### Run Tests

```bash
pytest -q
```

### Try the API

```bash
curl -X POST http://localhost:8000/api/v1/workflows \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key" \
  -d '{
    "title": "Build customer churn analytics workflow",
    "objective": "Research churn drivers, propose architecture, generate API plan, review risks, and produce implementation report.",
    "requires_human_approval": true
  }'
```

---

## 📸 Screenshots

### Dashboard Overview

<p align="center">
  <img src="docs/screenshots/swagger-ui.png" width="45%"/>
  <img src="docs/screenshots/api-authentication.png" width="45%"/>
  <img src="docs/screenshots/knowledge-ingestion.png" width="45%"/>
  <img src="docs/screenshots/prometheus-metrics.png" width="45%"/>
  <img src="docs/screenshots/workflow-created.png" width="45%"/>
  <img src="docs/screenshots/workflow-approved.png" width="45%"/>
</p>

### Qdrant Dashboard

<p align="center">
  <img src="docs/screenshots/qdrant-dashboard.png" width="45%"/>
</p>

---

## 🧯 Troubleshooting Notes

These are the exact issues commonly hit while running this project locally.

### 1. `ModuleNotFoundError: No module named 'app'`

Run tests from the project root, not from inside the `tests/` folder:

```bash
pytest -q
```

The project includes this pytest configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = [".", "app"]
```

### 2. Browser shows `ERR_ADDRESS_INVALID` for `http://0.0.0.0:8000`

Use this in your browser:

```text
http://localhost:8000/docs
```

Do not browse to `0.0.0.0`. Uvicorn displays `0.0.0.0` because the app binds to all container interfaces.

### 3. Docker API crashes with `ConnectionRefusedError`

Inside Docker, service URLs must use Docker service names, not `localhost`. This project uses `.env.docker` for Docker Compose:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/multi_agent_ai
REDIS_URL=redis://redis:6379/0
QDRANT_URL=http://qdrant:6333
```

Then restart cleanly:

```bash
docker compose down -v
docker compose up --build
```

### 4. Local Uvicorn fails with `socket.gaierror: getaddrinfo failed`

This usually means local Uvicorn is trying to use Docker hostnames such as `postgres`, `redis`, or `qdrant`. In local Python mode, use `localhost` values in `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/multi_agent_ai
REDIS_URL=redis://localhost:6379/0
QDRANT_URL=http://localhost:6333
```

Or use the SQLite default from `.env.example`.

### 5. Running Docker and local Uvicorn at the same time

Do not run both on port `8000`. Either use Docker only, or run local Uvicorn on a different port:

```bash
uvicorn app.main:app --reload --port 8001
```

Then open:

```text
http://localhost:8001/docs
```

### 6. Redis URL does not open in the browser

Redis is not an HTTP service, so `http://localhost:6379` will not show a webpage. Verify Redis with:

```bash
docker exec -it multi-agent-redis redis-cli ping
```

Expected response:

```text
PONG
```

### 7. Qdrant page looks empty or boring

The Qdrant root URL returns version JSON. That is normal. Use:

```text
http://localhost:6333/dashboard
```

or inspect collections:

```text
http://localhost:6333/collections
```

### 8. Local database files should not be committed

SQLite files such as `multi_agent_ai.db` are local runtime artifacts. They are ignored through `.gitignore`:

```gitignore
*.db
*.sqlite
*.sqlite3
```

---

---

## 🧠 Agent System

|      Agent      |                          Responsibility                          |
|-----------------|------------------------------------------------------------------|
| Research Agent  | Extracts domain context, assumptions, and risks                  |
| Planning Agent  | Converts objective into executable workflow plan                 |
| Data Agent      | Identifies datasets, entities, metrics, and storage needs        |
| Coding Agent    | Produces implementation plan, modules, APIs, and test strategy   |
| Review Agent    | Reviews quality, security, scalability, and production readiness |
| Reporting Agent | Produces final executive and technical summary                   |

The default implementation uses deterministic local agents so the platform works without paid API keys. You can later plug in OpenAI, Bedrock, Ollama, or custom internal models behind the same `LLMProvider` interface.

---

## 🔐 Security Design

- API key middleware for protected endpoints
- Pydantic request validation
- SQLAlchemy ORM models instead of raw SQL
- Centralized settings through environment variables
- Bandit security scan in CI
- Dependency audit placeholder via pip-audit
- Audit event table for workflow actions
- Safe local deterministic LLM provider by default

---

## 📈 Monitoring Design

- `/metrics` endpoint with request and workflow counters
- Structured JSON logging
- Request correlation middleware
- Health endpoint for load balancers
- Prometheus scrape annotation in Kubernetes service
- CloudWatch deployment notes for AWS ECS/EKS

---

## 🔁 CI/CD Design

```mermaid
flowchart LR
    A[Push / Pull Request] --> B[GitHub Actions]
    B --> C[Ruff Lint]
    C --> D[Pytest]
    D --> E[Bandit]
    E --> F[Build Docker Image]
    F --> G[Optional Deploy]

    A --> H[Jenkins]
    H --> I[Install]
    I --> J[Test]
    J --> K[Security Scan]
    K --> L[Docker Build]
```

---

## ☁️ AWS Deployment Architecture

```mermaid
flowchart TD
    User[Users] --> CF[CloudFront]
    CF --> ALB[Application Load Balancer]
    ALB --> ECS[ECS Fargate / EKS]
    ECS --> RDS[(Amazon RDS PostgreSQL)]
    ECS --> ElastiCache[(ElastiCache Redis)]
    ECS --> Qdrant[Qdrant on ECS/EKS or Managed Vector DB]
    ECS --> CW[CloudWatch Logs & Metrics]
    Secrets[AWS Secrets Manager] --> ECS
```

---

## 🧪 Testing Strategy

- Unit tests for agents, tools, and retrieval logic
- API tests for workflow and knowledge endpoints
- Integration-style tests using SQLite test database
- Dependency overrides for isolated FastAPI testing
- CI runs lint, tests, and security scans

---

## 📄 License

This project is licensed under the MIT License.
