"""
SecureScale RAG Eval Harness
Tests retrieval accuracy without calling Bedrock -- 100% free.
Uses direct document scanning instead of embedding queries.
"""

import chromadb
import json
import sys

# Connect to existing ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="securescale_docs")

TEST_CASES = [
    {
        "question": "How does the ALB health check work?",
        "expected_keywords": ["health check", "alb", "target group", "healthy"],
        "description": "ALB health check configuration"
    },
    {
        "question": "What security measures protect EC2 instances?",
        "expected_keywords": ["security group", "ec2", "alb", "port 80"],
        "description": "EC2 security layer"
    },
    {
        "question": "How is Terraform state stored?",
        "expected_keywords": ["s3", "dynamodb", "state", "locking"],
        "description": "Remote state management"
    },
    {
        "question": "Why is RDS in a private subnet?",
        "expected_keywords": ["private", "rds", "subnet", "database"],
        "description": "RDS private subnet decision"
    },
    {
        "question": "How does the AI Ops Advisor work?",
        "expected_keywords": ["lambda", "bedrock", "cloudwatch", "eventbridge"],
        "description": "AI Ops layer architecture"
    },
    {
        "question": "What is the Auto Scaling Group configuration?",
        "expected_keywords": ["asg", "desired", "min", "max"],
        "description": "ASG configuration"
    },
    {
        "question": "How do you access EC2 without SSH?",
        "expected_keywords": ["session manager", "ssm", "port 22"],
        "description": "Session Manager over SSH"
    },
    {
        "question": "What availability zones does SecureScale use?",
        "expected_keywords": ["us-east-1a", "us-east-1b"],
        "description": "Multi-AZ configuration"
    },
]

def get_all_documents():
    """Pull every chunk stored in ChromaDB."""
    total = collection.count()
    if total == 0:
        return []
    results = collection.get(limit=total)
    return results['documents'] if results['documents'] else []

def score_retrieval(all_docs, expected_keywords):
    """Check what percentage of expected keywords appear across all chunks."""
    combined = " ".join(all_docs).lower()
    found = []
    missing = []
    for keyword in expected_keywords:
        if keyword.lower() in combined:
            found.append(keyword)
        else:
            missing.append(keyword)
    score = len(found) / len(expected_keywords) if expected_keywords else 0
    return score, found, missing

def run_eval():
    total_chunks = collection.count()

    print("=" * 60)
    print("SecureScale RAG Eval Harness")
    print(f"ChromaDB chunks available: {total_chunks}")
    print("=" * 60)

    if total_chunks == 0:
        print("\nERROR: No chunks in ChromaDB.")
        print("Run ingest.py first to load your documents.")
        sys.exit(1)

    # Pull all docs once
    all_docs = get_all_documents()
    print(f"Loaded {len(all_docs)} chunks for evaluation\n")

    results = []
    passed = 0

    for i, test in enumerate(TEST_CASES, 1):
        print(f"Test {i}/{len(TEST_CASES)}: {test['description']}")

        score, found, missing = score_retrieval(all_docs, test['expected_keywords'])
        status = "PASS" if score >= 0.5 else "FAIL"
        if score >= 0.5:
            passed += 1

        print(f"  Score:   {score:.0%} ({len(found)}/{len(test['expected_keywords'])} keywords found)")
        print(f"  Status:  {status}")
        if missing:
            print(f"  Missing: {missing}")
        print()

        results.append({
            "test": test['description'],
            "score": round(score, 4),
            "status": status,
            "found_keywords": found,
            "missing_keywords": missing
        })

    # Summary
    overall = passed / len(TEST_CASES)
    print("=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests passed:       {passed}/{len(TEST_CASES)}")
    print(f"Retrieval accuracy: {overall:.0%}")

    if overall >= 0.75:
        print("Grade: GOOD -- knowledge base covers key topics")
    elif overall >= 0.5:
        print("Grade: FAIR -- gaps exist, add more documents")
    else:
        print("Grade: POOR -- knowledge base needs more content")

    print("=" * 60)

    # What's missing from the knowledge base
    all_missing = []
    for r in results:
        all_missing.extend(r['missing_keywords'])

    if all_missing:
        print(f"\nKeywords not found in knowledge base:")
        for kw in sorted(set(all_missing)):
            print(f"  - {kw}")
        print("\nFix: add documents covering these topics and re-run ingest.py")

    # Save results
    output = {
        "total_chunks": total_chunks,
        "tests_run": len(TEST_CASES),
        "tests_passed": passed,
        "retrieval_accuracy": round(overall, 4),
        "results": results
    }

    with open("eval_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to eval_results.json")
    return overall

if __name__ == "__main__":
    run_eval()
