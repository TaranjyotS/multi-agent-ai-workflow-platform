import pytest


@pytest.mark.asyncio
async def test_workflow_without_approval_completes(client, auth_headers):
    response = await client.post("/api/v1/workflows", headers=auth_headers, json={
        "title": "Automate research and reporting",
        "objective": "Build an enterprise AI workflow that researches, plans, reviews, and reports delivery risks.",
        "requires_human_approval": False
    })
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "completed"
    assert len(body["steps"]) == 6

@pytest.mark.asyncio
async def test_workflow_with_human_approval_resume(client, auth_headers):
    response = await client.post("/api/v1/workflows", headers=auth_headers, json={
        "title": "Governed workflow",
        "objective": "Create a governed multi-agent workflow with human approval before final reporting.",
        "requires_human_approval": True
    })
    assert response.status_code == 201
    workflow = response.json()
    assert workflow["status"] == "waiting_for_approval"
    assert len(workflow["steps"]) == 5
    approved = await client.post(f"/api/v1/workflows/{workflow['id']}/approvals", headers=auth_headers, json={"approved": True, "reason": "Meets quality bar"})
    assert approved.status_code == 200
    assert approved.json()["status"] == "completed"
    assert len(approved.json()["steps"]) == 6

@pytest.mark.asyncio
async def test_api_key_required(client):
    response = await client.get("/api/v1/agents")
    assert response.status_code == 401
