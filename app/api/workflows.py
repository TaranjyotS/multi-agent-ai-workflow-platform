from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_api_key
from app.db.session import get_db
from app.schemas.workflow import ApprovalRequest, WorkflowCreate, WorkflowRead
from app.services.workflow_service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["Workflows"], dependencies=[Depends(verify_api_key)])

@router.post("", response_model=WorkflowRead, status_code=201)
async def create_workflow(payload: WorkflowCreate, db: AsyncSession = Depends(get_db)) -> WorkflowRead:
    return await WorkflowService(db).create_and_run(payload.title, payload.objective, payload.requires_human_approval, payload.metadata)

@router.get("", response_model=list[WorkflowRead])
async def list_workflows(db: AsyncSession = Depends(get_db)) -> list[WorkflowRead]:
    return await WorkflowService(db).list()

@router.get("/{workflow_id}", response_model=WorkflowRead)
async def get_workflow(workflow_id: str, db: AsyncSession = Depends(get_db)) -> WorkflowRead:
    return await WorkflowService(db).get(workflow_id)

@router.post("/{workflow_id}/approvals", response_model=WorkflowRead)
async def approve_workflow(workflow_id: str, payload: ApprovalRequest, db: AsyncSession = Depends(get_db)) -> WorkflowRead:
    return await WorkflowService(db).decide_approval(workflow_id, payload.approved, payload.reason)
