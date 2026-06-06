from dataclasses import dataclass


@dataclass(frozen=True)
class AgentResult:
    agent_name: str
    output: str

class BaseAgent:
    name = "base"
    role = "Generic agent"

    async def run(self, objective: str, context: str = "") -> AgentResult:
        raise NotImplementedError
