# Deployment Strategy

## Local

Use SQLite and deterministic local agents for fast development.

## Docker Compose

Use Docker Compose to run API, PostgreSQL, Redis, and Qdrant.

```bash
docker compose up --build
```

## Kubernetes

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## AWS

Recommended production path:

- ECS Fargate or EKS for the API
- Amazon RDS PostgreSQL for transactional persistence
- ElastiCache Redis for caching and future queues
- Qdrant on ECS/EKS or managed vector database alternative
- AWS Secrets Manager for API keys and DB credentials
- CloudWatch Logs and Metrics for observability
- ALB for ingress and TLS termination
