# ADR-001 — Use RAG Instead of Fine-Tuning

**Status:** Accepted  
**Date:** 2025-05  
**Author:** Khori Williams

---

## Context

When building an AI system that answers questions about SecureScale infrastructure documentation, two primary approaches were available: fine-tuning a foundation model on the documentation, or using Retrieval-Augmented Generation (RAG) to ground a foundation model's responses in retrieved context at query time.

The core problem was accuracy. A general-purpose AI model answering questions about a specific private infrastructure project would hallucinate — confidently generating plausible but incorrect answers about configurations, security decisions, and architecture details that it was never trained on.

---

## Decision

Use **Retrieval-Augmented Generation (RAG)** as the core architecture pattern.

Instead of training a model on the documentation, documents are chunked, converted to vector embeddings, and stored in a vector database. At query time, the question is converted to a vector, semantically similar chunks are retrieved, and those chunks are sent to the model as context alongside the question — grounding the response in real documentation.

---

## Alternatives Considered

**Fine-tuning a foundation model** — requires significant compute, cost, and time. Knowledge becomes stale the moment documentation changes, requiring another training run.

**Prompt stuffing** — sending the entire corpus in every prompt exceeds context window limits and dramatically increases token costs.

**Keyword search only** — cannot handle semantic queries. Cannot match meaning, only exact words.

---

## Consequences

✅ Responses are grounded in actual documentation — hallucination risk dramatically reduced  
✅ Documentation updates automatically improve answers — re-ingest, no retraining needed  
✅ Works on private data never in any model's training set  
✅ Significantly lower cost than fine-tuning  
⚠️ Answer quality depends on chunking strategy and retrieval relevance  
⚠️ Requires a vector database and embedding pipeline  
