from fastapi import APIRouter, Depends

from app.agents.specialized import AGENT_REGISTRY
from app.core.security import verify_api_key

router = APIRouter(prefix="/agents", tags=["Agents"], dependencies=[Depends(verify_api_key)])

@router.get("")
async def list_agents() -> list[dict]:
    return [{"name": agent.name, "role": agent.role} for agent in AGENT_REGISTRY.values()]
