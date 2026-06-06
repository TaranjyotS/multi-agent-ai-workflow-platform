# API Specification

Run the app and open `/docs` for interactive Swagger documentation.

## Protected Requests

Most `/api/v1` endpoints require:

```http
X-API-Key: dev-api-key
```

## Create Workflow

```http
POST /api/v1/workflows
Content-Type: application/json
X-API-Key: dev-api-key
```

```json
{
  "title": "Enterprise research workflow",
  "objective": "Research, plan, review, and report an AI modernization strategy.",
  "requires_human_approval": true,
  "metadata": { "priority": "high" }
}
```

## Approve Workflow

```http
POST /api/v1/workflows/{workflow_id}/approvals
```

```json
{
  "approved": true,
  "reason": "Approved after architecture review"
}
```
