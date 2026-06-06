import pytest


@pytest.mark.asyncio
async def test_ingest_and_search_knowledge(client, auth_headers):
    payload = {"title": "RAG Policy", "source": "sample", "content": "Enterprise AI workflows require traceability, approvals, vector search, audit logs, and monitoring."}
    created = await client.post("/api/v1/knowledge/documents", json=payload, headers=auth_headers)
    assert created.status_code == 200
    search = await client.get("/api/v1/knowledge/search?q=approval vector monitoring", headers=auth_headers)
    assert search.status_code == 200
    assert search.json()["results"]
