# Monitoring and Observability

## Current Signals

- `/health` for uptime checks
- `/metrics` for Prometheus-style counters
- `X-Request-ID` response header for correlation
- Structured server logs

## Recommended Production Stack

- Prometheus + Grafana for metrics
- CloudWatch Logs for AWS deployment
- OpenTelemetry for traces
- Sentry or similar for error tracking
- LangSmith or custom trace store for LLM/agent observability
