import boto3
import chromadb
import json

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="securescale_docs")

# Initialize Bedrock
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_embedding(text):
    """Get embedding for the query"""
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body=json.dumps({'inputText': text})
    )
    result = json.loads(response['body'].read())
    return result['embedding']

def retrieve_context(query, n_results=3):
    """Find most relevant chunks from ChromaDB"""
    query_embedding = get_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count())
    )
    
    if not results['documents'][0]:
        return ""
    
    context = "\n\n".join(results['documents'][0])
    return context

def ask(question):
    """Main RAG query function"""
    print(f"\nQuestion: {question}")
    print("Searching knowledge base...")
    
    # Retrieve relevant context
    context = retrieve_context(question)
    
    if not context:
        return "No relevant documents found in the knowledge base."
    
    # Build prompt with context
    prompt = f"""You are a helpful assistant with access to a private knowledge base about SecureScale cloud infrastructure.

Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't have that information in my knowledge base."

Context:
{context}

Question: {question}

Answer:"""

    # Send to Bedrock Nova Lite
    response = bedrock.invoke_model(
        modelId='amazon.nova-lite-v1:0',
        body=json.dumps({
            'messages': [
                {
                    'role': 'user',
                    'content': [{'text': prompt}]
                }
            ],
            'inferenceConfig': {
                'maxTokens': 500,
                'temperature': 0.1,
            }
        })
    )
    
    result = json.loads(response['body'].read())
    answer = result['output']['message']['content'][0]['text']
    
    print(f"\nAnswer: {answer}")
    return answer

if __name__ == "__main__":
    # Test queries
    questions = [
        "How does the ALB health check work in SecureScale?",
        "What security measures are in place for EC2 instances?",
        "What did the AI Ops Advisor find when it analyzed the infrastructure?",
    ]
    
    for question in questions:
        ask(question)
        print("\n" + "="*60)
