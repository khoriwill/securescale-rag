import boto3
import chromadb
import os
import json
from pypdf import PdfReader

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="securescale_docs")

# Initialize Bedrock
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_embedding(text):
    """Get embeddings from Amazon Bedrock Titan Embeddings"""
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body=json.dumps({'inputText': text})
    )
    result = json.loads(response['body'].read())
    return result['embedding']

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest_text_file(filepath):
    """Ingest a plain text or markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def ingest_pdf_file(filepath):
    """Ingest a PDF file"""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def ingest_document(filepath):
    """Main ingestion function"""
    print(f"Ingesting: {filepath}")
    
    # Read file based on type
    if filepath.endswith('.pdf'):
        text = ingest_pdf_file(filepath)
    else:
        text = ingest_text_file(filepath)
    
    # Split into chunks
    chunks = chunk_text(text)
    print(f"  Created {len(chunks)} chunks")
    
    # Generate embeddings and store in ChromaDB
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"{os.path.basename(filepath)}_chunk_{i}"],
            metadatas=[{"source": filepath, "chunk": i}]
        )
    
    print(f"  Stored {len(chunks)} chunks in ChromaDB")

def ingest_all_documents():
    """Ingest all documents in the documents folder"""
    docs_folder = "./documents"
    files = os.listdir(docs_folder)
    
    if not files:
        print("No documents found in ./documents folder")
        return
    
    for filename in files:
        filepath = os.path.join(docs_folder, filename)
        if os.path.isfile(filepath):
            try:
                ingest_document(filepath)
            except Exception as e:
                print(f"Error ingesting {filename}: {e}")
    
    total = collection.count()
    print(f"\nTotal chunks in ChromaDB: {total}")

if __name__ == "__main__":
    ingest_all_documents()
