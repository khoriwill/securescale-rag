# ADR-004 — Use FastAPI as the Backend Framework

**Status:** Accepted  
**Date:** 2025-05  
**Author:** Khori Williams

---

## Context

The RAG system needs an HTTP interface so that questions can be submitted and answers returned programmatically. This makes the system callable from a browser, a CLI, another service, or eventually a frontend UI — rather than being limited to direct Python script execution.

The backend framework needed to be lightweight, fast to set up, and well-suited for AI workloads where Python is the dominant language.

---

## Decision

Use **FastAPI** as the HTTP backend framework.

FastAPI is a modern Python web framework built on Starlette and Pydantic. It exposes the RAG pipeline as a REST API endpoint (POST /ask), handles request validation automatically, and generates interactive API documentation out of the box at /docs.

---

## Alternatives Considered

**Flask** — most widely used Python framework but lacks built-in async support and automatic request validation. For AI workloads that benefit from async I/O during model calls, FastAPI's native async support is a meaningful advantage.

**Django** — full-featured but significant overkill for a single API endpoint. The overhead is not justified for this use case.

**AWS Lambda + API Gateway** — the production architecture path, but adds deployment complexity during development phase. FastAPI locally first, Lambda deployment as a future improvement.

**No API layer (CLI only)** — sufficient for testing but not for integration with other systems, frontends, or automated pipelines.

---

## Consequences

✅ Clean REST API — callable from any HTTP client  
✅ Automatic request validation via Pydantic  
✅ Auto-generated interactive docs at /docs — self-documenting  
✅ Native async support — non-blocking I/O during Bedrock API calls  
✅ Minimal boilerplate — operational in under 20 lines of Python  
⚠️ Runs as a local server — production deployment requires Docker or Lambda migration  
⚠️ No authentication layer in current implementation — required before any public exposure  

---

## Future State

The natural production path is containerization via Docker and deployment as an AWS Lambda function behind API Gateway — keeping the system serverless, scalable, and AWS-native. The FastAPI app is already containerized and the migration path is straightforward.
