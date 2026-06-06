from datetime import datetime

from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    objective: str = Field(min_length=10)
    requires_human_approval: bool = False
    metadata: dict = Field(default_factory=dict)

class ApprovalRequest(BaseModel):
    approved: bool
    reason: str = Field(default="Approved by reviewer", min_length=3)

class WorkflowStepRead(BaseModel):
    id: str
    agent_name: str
    status: str
    input_text: str
    output_text: str
    step_order: int
    created_at: datetime
    model_config = {"from_attributes": True}

class ApprovalRead(BaseModel):
    id: str
    status: str
    question: str
    decision_reason: str | None = None
    created_at: datetime
    resolved_at: datetime | None = None
    model_config = {"from_attributes": True}

class WorkflowRead(BaseModel):
    id: str
    title: str
    objective: str
    status: str
    result: str | None = None
    workflow_metadata: dict
    created_at: datetime
    updated_at: datetime
    steps: list[WorkflowStepRead] = []
    approvals: list[ApprovalRead] = []
    model_config = {"from_attributes": True}
