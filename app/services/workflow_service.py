from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.metrics import metrics
from app.db.models import AuditEvent, HumanApproval, Workflow, WorkflowStep
from app.orchestration.engine import AgentWorkflowEngine, WorkflowState
from app.services.knowledge_service import KnowledgeService


class WorkflowService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.engine = AgentWorkflowEngine()
        self.knowledge = KnowledgeService(db)

    async def create_and_run(self, title: str, objective: str, requires_human_approval: bool, metadata: dict) -> Workflow:
        workflow = Workflow(title=title, objective=objective, status="running", workflow_metadata=metadata)
        self.db.add(workflow)
        await self.db.flush()
        context = await self.knowledge.context_for(objective)
        state = WorkflowState(objective=objective, context=context, requires_human_approval=requires_human_approval)
        state = await self.engine.execute_until_checkpoint(state)
        for idx, item in enumerate(state.outputs, start=1):
            self.db.add(WorkflowStep(workflow_id=workflow.id, agent_name=item["agent_name"], input_text=objective, output_text=item["output"], step_order=idx))
        if state.paused:
            workflow.status = "waiting_for_approval"
            self.db.add(HumanApproval(workflow_id=workflow.id, question="Approve final report generation for this enterprise workflow?"))
        else:
            workflow.status = "completed"
            workflow.result = state.final_report
        self.db.add(AuditEvent(workflow_id=workflow.id, event_type="workflow_created", payload={"status": workflow.status}))
        await self.db.commit()
        metrics.inc("workflow_created")
        return await self.get(workflow.id)

    async def get(self, workflow_id: str) -> Workflow:
        stmt = (
            select(Workflow)
            .where(Workflow.id == workflow_id)
            .options(selectinload(Workflow.steps), selectinload(Workflow.approvals))
            .execution_options(populate_existing=True)
        )

        result = await self.db.execute(stmt)
        workflow = result.scalar_one_or_none()

        if workflow is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow '{workflow_id}' not found",
            )

        workflow.steps.sort(key=lambda s: s.step_order)
        return workflow

    async def list(self) -> list[Workflow]:
        stmt = select(Workflow).options(selectinload(Workflow.steps), selectinload(Workflow.approvals)).order_by(Workflow.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def decide_approval(self, workflow_id: str, approved: bool, reason: str) -> Workflow:
        workflow = await self.get(workflow_id)
        pending = next((a for a in workflow.approvals if a.status == "pending"), None)
        if not pending:
            return workflow
        pending.status = "approved" if approved else "rejected"
        pending.decision_reason = reason
        pending.resolved_at = datetime.now(UTC)
        if not approved:
            workflow.status = "rejected"
            self.db.add(AuditEvent(workflow_id=workflow.id, event_type="workflow_rejected", payload={"reason": reason}))
            await self.db.commit()
            return await self.get(workflow.id)
        existing_outputs = [{"agent_name": s.agent_name, "output": s.output_text} for s in workflow.steps]
        state = WorkflowState(objective=workflow.objective, outputs=existing_outputs, requires_human_approval=False)
        state = await self.engine.finalize(state)
        last = state.outputs[-1]
        self.db.add(WorkflowStep(workflow_id=workflow.id, agent_name=last["agent_name"], input_text=workflow.objective, output_text=last["output"], step_order=len(workflow.steps)+1))
        workflow.status = "completed"
        workflow.result = state.final_report
        self.db.add(AuditEvent(workflow_id=workflow.id, event_type="workflow_approved", payload={"reason": reason}))
        await self.db.commit()
        metrics.inc("workflow_approved")
        return await self.get(workflow.id)
