"""
AWS AI Learning Platform - Simplified RAG Backend
FastAPI server with Google Gemini and ChromaDB
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import google.generativeai as genai

# LangChain/ChromaDB imports
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

app = FastAPI(title="AWS AI Learning Platform API")

# CORS middleware - Updated for production
# Allow frontend URLs from environment or use defaults
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Local development
    "http://localhost:3001",
    FRONTEND_URL,  # Production frontend
]

# Add Railway preview URLs if available
if os.getenv("RAILWAY_STATIC_URL"):
    ALLOWED_ORIGINS.append(f"https://{os.getenv('RAILWAY_STATIC_URL')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
vector_store = None
model = None
embeddings = None

# Request/Response Models
class ChatRequest(BaseModel):
    question: str
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: Optional[float] = None

class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    num_questions: int = 5

class QuizResponse(BaseModel):
    questions: List[dict]


# Initialize RAG system
def initialize_rag():
    """Initialize the RAG system"""
    global vector_store, model, embeddings

    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found")

    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Initialize HuggingFace embeddings (local, no API limits)
    print("🔧 Loading local embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✅ Embedding model loaded!")

    # Initialize ChromaDB
    persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    try:
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name="aws_docs"
        )
        doc_count = vector_store._collection.count()
        print(f"✅ Loaded vector store with {doc_count} documents")

        # If no documents found, warn but don't crash
        if doc_count == 0:
            print("⚠️  WARNING: Vector store is empty! Run ingest_docs.py to add documents.")
            print("   The API will start but won't be able to answer questions accurately.")
    except Exception as e:
        print(f"⚠️  Error loading vector store: {e}")
        print("   Creating empty vector store. Run ingest_docs.py to add documents.")
        vector_store = None

    print("✅ RAG system initialized successfully")


@app.on_event("startup")
async def startup_event():
    """Initialize RAG on startup"""
    try:
        initialize_rag()
    except Exception as e:
        print(f"❌ Error initializing RAG: {e}")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "AWS AI Learning Platform API",
        "rag_initialized": vector_store is not None,
        "documents_loaded": vector_store._collection.count() if vector_store else 0
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for RAG-powered Q&A"""
    if not vector_store or not model:
        raise HTTPException(status_code=503, detail="RAG system not initialized")

    try:
        # Retrieve relevant documents
        docs = vector_store.similarity_search(request.question, k=3)

        # Build context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in docs])

        # Build prompt
        prompt = f"""You are an expert AWS AI/ML instructor helping students prepare for AWS certifications.

Context from AWS documentation:
{context}

Question: {request.question}

Provide a clear, detailed answer that:
1. Directly answers the question
2. Includes relevant AWS service names and features
3. Explains concepts in an educational way
4. Relates to certification exam topics when relevant

If you don't know the answer based on the context, say so clearly.

Answer:"""

        # Generate response using Gemini
        response = model.generate_content(prompt)

        # Extract sources
        sources = []
        for doc in docs:
            if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                source = doc.metadata['source']
                if source not in sources:
                    sources.append(source)

        return ChatResponse(
            answer=response.text,
            sources=sources[:3]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """Generate a quiz on a specific AWS AI/ML topic"""
    if not model:
        raise HTTPException(status_code=503, detail="LLM not initialized")

    try:
        quiz_prompt = f"""Generate a {request.difficulty} difficulty quiz with {request.num_questions} multiple choice questions about {request.topic} in AWS.

Focus on topics relevant to AWS AI Practitioner and Machine Learning certifications.

Format the response as a JSON array with this exact structure:
[
  {{
    "question": "Question text here?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Brief explanation of why this is correct"
  }}
]

Make questions practical and exam-relevant. Return ONLY the JSON array, no other text."""

        response = model.generate_content(quiz_prompt)

        # Parse response
        import json
        import re

        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if json_match:
            questions = json.loads(json_match.group())
        else:
            # Fallback
            questions = [{
                "question": f"What is the primary use case for {request.topic}?",
                "options": ["A) Data storage", "B) Machine learning", "C) Networking", "D) Security"],
                "correct_answer": "B",
                "explanation": "Please try again - quiz generation needs refinement"
            }]

        return QuizResponse(questions=questions)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/topics")
async def get_topics():
    """Get available AWS AI/ML topics"""
    topics = {
        "ai_services": [
            "Amazon SageMaker",
            "Amazon Bedrock",
            "Amazon Comprehend",
            "Amazon Rekognition",
            "Amazon Textract",
            "Amazon Lex",
            "Amazon Personalize"
        ],
        "ml_infrastructure": [
            "SageMaker Studio",
            "SageMaker Training",
            "SageMaker Inference",
            "SageMaker Feature Store"
        ],
        "certifications": [
            "AWS Certified AI Practitioner",
            "AWS Certified Machine Learning - Specialty"
        ]
    }
    return topics


@app.get("/stats")
async def get_stats():
    """Get statistics about the knowledge base"""
    if not vector_store:
        return {"error": "Vector store not initialized"}

    try:
        count = vector_store._collection.count()
        return {
            "total_documents": count,
            "status": "healthy" if count > 0 else "needs_documents",
            "embedding_model": "all-MiniLM-L6-v2",
            "llm_model": "gemini-pro"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
