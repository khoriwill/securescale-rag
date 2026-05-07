# ADR-005 — Use Amazon Nova Lite as the Generation Model

**Status:** Accepted  
**Date:** 2025-05  
**Author:** Khori Williams

---

## Context

Within Amazon Bedrock, multiple foundation models are available for answer generation — including Amazon's Nova family, Anthropic's Claude models, and Meta's Llama models. The generation model receives the retrieved context and the user's question and produces the final answer.

The model selection needed to balance answer quality, cost per token, latency, and alignment with the project's AWS-native architecture philosophy.

---

## Decision

Use **Amazon Nova Lite** as the generation model.

Nova Lite is Amazon's lightweight, cost-optimized foundation model in the Nova family. It delivers strong performance on structured Q&A tasks — exactly the pattern used in RAG — at a significantly lower cost per token than larger models like Claude Sonnet or Nova Pro.

---

## Alternatives Considered

**Anthropic Claude Sonnet (via Bedrock)** — higher quality responses and better complex reasoning, but significantly more expensive per token. For a RAG use case where the model synthesizes retrieved context rather than reasoning from scratch, Nova Lite's quality is sufficient.

**Amazon Nova Pro** — more capable but 8x more expensive than Nova Lite per token. The structured Q&A task in a RAG pipeline does not require Nova Pro's additional capability.

**Amazon Titan Text** — AWS's older text generation model. Nova Lite supersedes it with better quality and comparable cost.

**Meta Llama 3 (via Bedrock)** — performs well on Q&A tasks but Nova Lite was chosen to maintain full AWS-native tooling and align with Amazon's own model ecosystem.

---

## Consequences

✅ Lowest cost per token among quality Bedrock generation models  
✅ Fast response latency — optimized for speed  
✅ Strong performance on structured Q&A — the exact RAG task pattern  
✅ AWS-native — aligns with full Bedrock + IAM + boto3 architecture  
⚠️ Lower ceiling than Claude Sonnet for complex reasoning — acceptable for RAG  
⚠️ Requires explicit model enablement in Bedrock console per AWS region  

---

## Upgrade Path

If response quality becomes a bottleneck the model swap is a single line change:

```python
# Current
model_id = "amazon.nova-lite-v1:0"

# Upgrade path
model_id = "anthropic.claude-sonnet-4-5"
```
