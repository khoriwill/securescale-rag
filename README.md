# SecureScale RAG — AI Knowledge System
> A production-style Retrieval-Augmented Generation (RAG) system built on AWS, designed to answer questions about private infrastructure documentation using real AI — not hallucination.

---

## What This Is

Most AI tools make things up when they don't know the answer. This system doesn't.

SecureScale RAG is a **grounded AI knowledge system** that answers questions about the SecureScale cloud infrastructure project using only what's actually documented — no guessing, no hallucination. You ask a question, it searches the real documents, pulls the relevant context, and sends it to an AI model to generate an accurate, sourced answer.

This is the same pattern used by enterprise AI assistants, internal knowledge bases, and regulated-industry chatbots where accuracy is non-negotiable.

---

## The Problem It Solves

Cloud infrastructure documentation is dense. Architecture decisions, security configurations, and deployment steps are buried across dozens of files. A RAG system turns that static documentation into something you can have a conversation with.

**Instead of:** "Let me search through 13 Terraform files to find how the ALB health check is configured..."

**You ask:** *"How does SecureScale handle unhealthy EC2 instances?"*

And the system retrieves the exact relevant context, sends it to AI, and returns a precise answer — grounded in the actual documentation.

---

## Architecture
Your Question
│
▼
Bedrock Titan Embeddings        ← converts question to a vector
│
▼
ChromaDB Vector Search          ← finds the most relevant document chunks
│
▼
Context + Question → Prompt
│
▼
Amazon Bedrock Nova Lite        ← generates a grounded answer
│
▼
FastAPI Response                ← returns the answer via HTTP

### Components

| Component | Technology | Purpose |
|---|---|---|
| Embeddings | Amazon Bedrock Titan Embeddings | Converts text into semantic vectors |
| Vector Store | ChromaDB | Stores and searches document embeddings |
| AI Model | Amazon Bedrock Nova Lite | Generates answers from retrieved context |
| Backend API | FastAPI (Python) | Serves questions and returns answers via HTTP |
| Runtime | Python 3 + venv | Local execution environment |

---

## How RAG Works (Plain English)

**Step 1 — Ingestion (done once)**
Your documents are split into chunks. Each chunk is converted into a vector — a list of numbers that represents its meaning, not just its words. Those vectors are stored in ChromaDB.

**Step 2 — Query (every question)**
Your question is converted into a vector the same way. ChromaDB finds the chunks whose vectors are closest in meaning to your question. Those chunks are your context.

**Step 3 — Generation**
The context + your question are sent to Nova Lite as a structured prompt: "Using only this context, answer this question." The model responds with a grounded answer — it can only use what you gave it.

This is why RAG eliminates hallucination. The model isn't guessing from training data. It's reading your documents.

---

## What I Loaded Into It

The knowledge base for this system is the **SecureScale infrastructure documentation** — architecture decisions, Terraform configurations, security design, and the AI Ops layer from the [securescale-terraform](https://github.com/khoriwill/securescale-terraform) project.

**Example questions it can answer:**

- *"How does SecureScale handle a failed EC2 instance?"*
- *"What security groups protect the RDS database?"*
- *"How does the AI Ops layer work?"*
- *"What happens when the Auto Scaling Group launches a new instance?"*

Every answer comes from the actual documentation — not from what the model was trained on.

---

## Project Structure
securescale-rag/
├── app/
│   ├── ingest.py        # Loads documents, creates embeddings, populates ChromaDB
│   ├── query.py         # Handles question → vector search → Bedrock → answer
│   └── main.py          # FastAPI server — exposes /ask endpoint
├── documents/           # Source documentation loaded into the knowledge base
├── .gitignore           # Excludes venv, chroma_db, .env, aws artifacts
└── README.md

---

## Running It Locally

### Prerequisites
- Python 3.8+
- AWS credentials configured (`aws configure`)
- Amazon Bedrock access enabled (Titan Embeddings + Nova Lite models)

### Setup

```bash
# Clone the repo
git clone https://github.com/khoriwill/securescale-rag.git
cd securescale-rag

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn chromadb boto3

# Ingest your documents into ChromaDB
python app/ingest.py

# Start the API server
uvicorn app.main:app --reload
```

### Ask a Question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How does SecureScale handle unhealthy EC2 instances?"}'
```

---

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon Bedrock Titan Embeddings | Convert text to vectors |
| Amazon Bedrock Nova Lite | Generate grounded answers |

> **Cost note:** Both Bedrock models charge per token. A full ingestion and 20 test queries typically runs under $0.05.

---

## Why I Built This

SecureScale RAG is the second layer of the SecureScale project ecosystem. After building the infrastructure ([securescale-terraform](https://github.com/khoriwill/securescale-terraform)), I wanted to demonstrate that the same environment could power an AI application — not just serve web traffic.

RAG is the architecture behind enterprise AI assistants at companies like Salesforce, ServiceNow, and AWS itself. Building one from components — embeddings, vector search, prompt engineering, API serving — gives me direct experience with every layer of how those systems work.

This project demonstrates:
- **AI systems design** — embeddings, vector search, and grounded generation
- **AWS Bedrock integration** — Titan Embeddings + Nova Lite via boto3
- **API development** — FastAPI backend serving AI responses over HTTP
- **Prompt engineering** — structuring context + question prompts for accurate answers
- **Practical AI judgment** — knowing when RAG is the right pattern and why

---

## Related Projects

| Project | Description |
|---|---|
| [securescale-terraform](https://github.com/khoriwill/securescale-terraform) | The infrastructure this RAG system documents |
| [anbupath-mvp](https://github.com/khoriwill/anbupath-mvp) | AI-powered career coaching platform |

---

## Author

**Khori Williams**
Technical Program Manager · Cloud & AI Infrastructure · AWS Solutions Architect · CISM

[GitHub](https://github.com/khoriwill) · khoriwill@gmail.com