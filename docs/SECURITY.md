# Security Design

## Current Controls

- API key middleware
- Environment-based secrets
- Pydantic request validation
- ORM-based DB access
- Audit events for workflow lifecycle changes
- Bandit scan in CI

## Production Enhancements

- Replace API key with OAuth2/OIDC/JWT
- Add RBAC for workflow owners and reviewers
- Add rate limiting at API gateway/load balancer
- Encrypt sensitive fields if storing customer data
- Add secret scanning and SBOM generation
- Add tool execution sandboxing before enabling shell/code tools
