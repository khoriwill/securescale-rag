# ADR-003 — Use Amazon Bedrock Instead of OpenAI

**Status:** Accepted  
**Date:** 2025-05  
**Author:** Khori Williams

---

## Context

The RAG system requires two AI capabilities: converting text to vector embeddings, and generating grounded answers from retrieved context. The decision needed to account for the existing AWS infrastructure investment in SecureScale, data privacy posture, and alignment with enterprise cloud architecture patterns.

---

## Decision

Use **Amazon Bedrock** for both embedding generation (Titan Embeddings) and answer generation (Nova Lite).

Bedrock is AWS's managed foundation model service — it provides access to multiple foundation models via a single API without managing ML infrastructure. All calls stay within the AWS ecosystem, using the same IAM credentials and boto3 SDK already established in SecureScale.

---

## Alternatives Considered

**OpenAI (GPT-4o / text-embedding-3)** — best-in-class models but introduces a third-party dependency outside AWS, requires separate API key and billing, and raises data privacy concerns — queries and document context leave the AWS environment entirely.

**AWS SageMaker** — more control but significantly higher cost and operational overhead. Not appropriate for a free-tier-conscious project.

**Hugging Face Inference API** — lower cost but another external dependency and models require more prompt engineering for structured Q&A tasks.

**Ollama (fully local)** — eliminates API costs but local model quality for RAG tasks is significantly lower without a high-end GPU.

---

## Consequences

✅ Stays entirely within the AWS ecosystem — same IAM role, same boto3 SDK, no new credentials  
✅ Data privacy — document context never leaves AWS infrastructure  
✅ Direct alignment with enterprise cloud architecture patterns  
✅ Demonstrates AWS-native AI integration relevant to Solutions Architect roles  
⚠️ Bedrock token costs are not free — minimal for development but not zero  
⚠️ Requires explicit model access enablement in the AWS console before use  
