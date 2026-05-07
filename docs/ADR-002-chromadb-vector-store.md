# ADR-002 — Use ChromaDB as the Vector Store

**Status:** Accepted  
**Date:** 2025-05  
**Author:** Khori Williams

---

## Context

A RAG system requires a vector database to store document embeddings and perform semantic similarity search at query time. The vector store is the retrieval engine — its speed, simplicity, and local operability directly impact development velocity and system reliability.

For a development and portfolio-stage project, the vector store needed to run locally without external services, require minimal configuration, and integrate cleanly with Python.

---

## Decision

Use **ChromaDB** as the vector store.

ChromaDB is an open-source embedding database that runs entirely in-process or as a local server. It stores document embeddings, handles similarity search, and returns the most semantically relevant chunks for a given query — all without requiring a cloud service or API key.

---

## Alternatives Considered

**Pinecone** — managed cloud vector database, production-grade, but requires external API and has cost implications beyond free tier.

**pgvector** — adds vector search to PostgreSQL, but significant infrastructure overhead for a project that doesn't otherwise need a relational database.

**FAISS** — highly performant but requires more manual setup, no built-in persistence, more configuration than ChromaDB.

**Weaviate** — more powerful than ChromaDB but significantly more complex to configure and run locally.

---

## Consequences

✅ Runs entirely locally — no external service dependency, no API key required  
✅ Minimal configuration — operational in under 10 lines of Python  
✅ Built-in persistence — embeddings survive between sessions  
✅ Clean Python API — integrates naturally with FastAPI and boto3  
⚠️ Not designed for production scale — Pinecone or Weaviate would replace in enterprise deployment  
⚠️ No built-in replication or high availability  
