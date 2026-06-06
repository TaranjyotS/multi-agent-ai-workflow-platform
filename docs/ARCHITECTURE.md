# Architecture

## Executive Summary

This platform coordinates specialized agents through a durable workflow service. The API layer is stateless; all durable state lives in the database. Retrieval uses local deterministic embeddings by default and can be replaced with Qdrant-backed production embeddings.

## Design Principles

- Keep agent orchestration explicit and auditable.
- Persist state after each agent step.
- Keep model providers swappable.
- Support human approval gates for governed workflows.
- Use infrastructure components commonly seen in enterprise AI platforms.

## Component Responsibilities

| Component            | Responsibility                            |
| -------------------- | ----------------------------------------- |
| FastAPI              | Request validation, routing, OpenAPI docs |
| Workflow Service     | Transactional workflow lifecycle          |
| Orchestration Engine | Agent routing and checkpoint logic        |
| Agents               | Specialized execution units               |
| Knowledge Service    | Document chunking, embedding, retrieval   |
| PostgreSQL/SQLite    | Workflow and audit persistence            |
| Redis                | Cache/queue extension point               |
| Qdrant               | Production vector store extension point   |

## Extension Points

- Replace `LocalEmbeddingModel` with OpenAI, Bedrock, or Hugging Face embeddings.
- Replace deterministic agents with real LLM-backed agents.
- Convert `AgentWorkflowEngine` nodes into LangGraph `StateGraph` nodes for advanced branching.
- Add background workers with Celery/RQ/Arq for long-running workflows.
