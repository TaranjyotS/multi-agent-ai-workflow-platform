from app.agents.base import AgentResult, BaseAgent


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


class PlanningAgent(BaseAgent):
    name = "planning_agent"
    role = "Decomposes goals into execution plans"

    async def run(self, objective: str, context: str = "") -> AgentResult:
        output = "Execution Plan:\n" + _bullets([
            "Clarify business objective and success metrics",
            "Retrieve relevant internal knowledge and constraints",
            "Split work across research, data, coding, review, and reporting agents",
            "Persist each step output for auditability and replay",
            "Route high-risk decisions through human approval",
        ])
        return AgentResult(self.name, output)


class ResearchAgent(BaseAgent):
    name = "research_agent"
    role = "Finds assumptions, domain context, and risks"

    async def run(self, objective: str, context: str = "") -> AgentResult:
        output = f"Research Findings for objective: {objective}\n" + _bullets([
            "Primary stakeholders require reliable, explainable workflow outcomes",
            "Enterprise workflows need provenance, traceability, and governance",
            "Relevant retrieved context: " + (context[:400] if context else "No private knowledge matched yet"),
            "Key risks include hallucination, stale knowledge, unsafe tool execution, and missing approval controls",
        ])
        return AgentResult(self.name, output)


class DataAgent(BaseAgent):
    name = "data_agent"
    role = "Models data entities, metrics, and retrieval needs"

    async def run(self, objective: str, context: str = "") -> AgentResult:
        output = "Data Analysis:\n" + _bullets([
            "Core entities: workflows, steps, approvals, audit events, documents, chunks",
            "Recommended storage: PostgreSQL for transactional state, Qdrant for semantic retrieval, Redis for cache/queues",
            "Metrics: workflow completion rate, approval latency, agent error rate, retrieval hit rate",
            "Data governance: redact secrets, retain audit logs, track source metadata",
        ])
        return AgentResult(self.name, output)


class CodingAgent(BaseAgent):
    name = "coding_agent"
    role = "Produces implementation strategy and code delivery plan"

    async def run(self, objective: str, context: str = "") -> AgentResult:
        output = "Implementation Blueprint:\n" + _bullets([
            "Expose FastAPI routes for workflows, knowledge, agents, health, and metrics",
            "Use service/repository layers to separate API, orchestration, and persistence",
            "Represent agents behind a common BaseAgent interface",
            "Support deterministic local provider first and production LLM providers later",
            "Validate behavior with unit, API, and integration-style tests",
        ])
        return AgentResult(self.name, output)


class ReviewAgent(BaseAgent):
    name = "review_agent"
    role = "Reviews quality, security, and production readiness"

    async def run(self, objective: str, context: str = "") -> AgentResult:
        output = "Review Notes:\n" + _bullets([
            "Security: API key auth, environment-based secrets, input validation, audit trail",
            "Scalability: stateless API, external DB/cache/vector services, Kubernetes-ready manifests",
            "Reliability: durable workflow state and explicit paused/approved/completed states",
            "Testing: isolated database tests and contract-style API coverage",
            "Observability: structured logs, correlation IDs, health checks, Prometheus metrics",
        ])
        return AgentResult(self.name, output)


class ReportingAgent(BaseAgent):
    name = "reporting_agent"
    role = "Creates final business and technical report"

    async def run(self, objective: str, context: str = "") -> AgentResult:
        output = f"Final Report for: {objective}\n\n" + _bullets([
            "The workflow has been decomposed, researched, modeled, reviewed, and prepared for delivery",
            "The recommended architecture uses FastAPI, agent orchestration, PostgreSQL, Redis, Qdrant, Docker, Kubernetes, and AWS",
            "Human approval is supported before finalization for governed enterprise workflows",
            "Next step: connect a real LLM provider and production vector embeddings if required",
        ])
        return AgentResult(self.name, output)


AGENT_REGISTRY = {
    agent.name: agent
    for agent in [PlanningAgent(), ResearchAgent(), DataAgent(), CodingAgent(), ReviewAgent(), ReportingAgent()]
}
