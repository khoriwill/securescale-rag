from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import chromadb
import json
import os
import shutil

app = FastAPI(title="SecureScale RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="securescale_docs")
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

class QueryRequest(BaseModel):
    question: str

def get_embedding(text):
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body=json.dumps({'inputText': text})
    )
    result = json.loads(response['body'].read())
    return result['embedding']

def retrieve_context(query, n_results=3):
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count())
    )
    if not results['documents'][0]:
        return ""
    return "\n\n".join(results['documents'][0])

@app.get("/")
def root():
    return {
        "name": "SecureScale RAG API",
        "status": "running",
        "documents": collection.count()
    }

@app.post("/ask")
def ask(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    context = retrieve_context(request.question)
    
    if not context:
        return {"answer": "No relevant documents found in the knowledge base."}
    
    prompt = f"""You are a helpful assistant with access to a private knowledge base about SecureScale cloud infrastructure.

Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't have that information in my knowledge base."

Context:
{context}

Question: {request.question}

Answer:"""

    response = bedrock.invoke_model(
        modelId='amazon.nova-lite-v1:0',
        body=json.dumps({
            'messages': [{'role': 'user', 'content': [{'text': prompt}]}],
            'inferenceConfig': {'maxTokens': 500, 'temperature': 0.1}
        })
    )
    
    result = json.loads(response['body'].read())
    answer = result['output']['message']['content'][0]['text']
    
    return {
        "question": request.question,
        "answer": answer,
        "chunks_searched": collection.count()
    }

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    os.makedirs("./documents", exist_ok=True)
    filepath = f"./documents/{file.filename}"
    
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    words = text.split()
    chunks = []
    for i in range(0, len(words), 450):
        chunk = ' '.join(words[i:i + 500])
        if chunk:
            chunks.append(chunk)
    
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"{file.filename}_chunk_{i}"],
            metadatas=[{"source": file.filename, "chunk": i}]
        )
    
    return {
        "message": f"Successfully ingested {file.filename}",
        "chunks_created": len(chunks),
        "total_chunks": collection.count()
    }

@app.get("/stats")
def stats():
    return {
        "total_chunks": collection.count(),
        "status": "healthy"
    }
