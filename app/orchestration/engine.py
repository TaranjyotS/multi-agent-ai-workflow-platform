from dataclasses import dataclass, field

from app.agents.specialized import AGENT_REGISTRY


@dataclass
class WorkflowState:
    objective: str
    context: str = ""
    outputs: list[dict] = field(default_factory=list)
    requires_human_approval: bool = False
    paused: bool = False
    final_report: str | None = None


class AgentWorkflowEngine:
    """Deterministic graph-style workflow engine with a LangGraph-compatible mental model.

    The class keeps execution explicit and testable. In production, each node can be
    swapped with LangGraph StateGraph nodes while preserving the same persisted state contract.
    """

    route = ["planning_agent", "research_agent", "data_agent", "coding_agent", "review_agent"]

    async def execute_until_checkpoint(self, state: WorkflowState) -> WorkflowState:
        for agent_name in self.route:
            agent = AGENT_REGISTRY[agent_name]
            result = await agent.run(state.objective, state.context)
            state.outputs.append({"agent_name": result.agent_name, "output": result.output})
        if state.requires_human_approval:
            state.paused = True
            return state
        return await self.finalize(state)

    async def finalize(self, state: WorkflowState) -> WorkflowState:
        report_agent = AGENT_REGISTRY["reporting_agent"]
        combined_context = state.context + "\n\n" + "\n\n".join(item["output"] for item in state.outputs)
        result = await report_agent.run(state.objective, combined_context)
        state.outputs.append({"agent_name": result.agent_name, "output": result.output})
        state.final_report = result.output
        state.paused = False
        return state
