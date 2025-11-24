"""
AWS Documentation Ingestion Script
Downloads and processes AWS AI/ML documentation into ChromaDB
"""

import os
import requests
from bs4 import BeautifulSoup
from typing import List
import time
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

# AWS AI/ML Documentation URLs
AWS_DOCS_URLS = {
    "sagemaker": [
        "https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html",
        "https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works.html",
        "https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects.html",
    ],
    "bedrock": [
        "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html",
        "https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html",
    ],
    "comprehend": [
        "https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html",
    ],
    "rekognition": [
        "https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html",
    ],
    "textract": [
        "https://docs.aws.amazon.com/textract/latest/dg/what-is.html",
    ],
    "lex": [
        "https://docs.aws.amazon.com/lex/latest/dg/what-is.html",
    ],
    "personalize": [
        "https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html",
    ],
}

# Sample AWS AI/ML documentation content (to get started quickly)
SAMPLE_DOCS = [
    {
        "title": "Amazon SageMaker Overview",
        "service": "SageMaker",
        "content": """
Amazon SageMaker is a fully managed machine learning service. With SageMaker, data scientists and developers can quickly and easily build and train machine learning models, and then directly deploy them into a production-ready hosted environment.

Key Features:
- SageMaker Studio: Web-based IDE for ML
- SageMaker Autopilot: Automatically builds, trains, and tunes ML models
- SageMaker Training: Managed training with distributed training capabilities
- SageMaker Inference: Deploy models for real-time or batch predictions
- SageMaker Feature Store: Centralized repository for ML features
- SageMaker Model Monitor: Monitor model quality in production
- SageMaker Clarify: Detect bias and explain model predictions

Common Use Cases:
1. Building and training custom ML models
2. Deploying models to production
3. Automating ML workflows with pipelines
4. Managing ML lifecycle end-to-end

Certification Relevance: Core service for AWS Certified Machine Learning - Specialty exam.
        """,
        "category": "AI/ML Services",
        "url": "https://docs.aws.amazon.com/sagemaker/"
    },
    {
        "title": "Amazon Bedrock Overview",
        "service": "Bedrock",
        "content": """
Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon via a single API.

Key Features:
- Access to multiple foundation models
- Customization with fine-tuning and RAG
- Agents for task automation
- Knowledge bases for RAG applications
- Guardrails for responsible AI
- Model evaluation and comparison

Available Models:
- Claude (Anthropic) - Advanced reasoning and analysis
- Llama 2 (Meta) - Open-source foundation model
- Jurassic (AI21 Labs) - Text generation
- Command (Cohere) - Conversational AI
- Stable Diffusion (Stability AI) - Image generation
- Amazon Titan - Amazon's foundation models

Use Cases:
1. Text generation and summarization
2. Conversational AI chatbots
3. Content creation and personalization
4. Code generation
5. Image generation from text

Certification Relevance: Important for AWS AI Practitioner certification.
        """,
        "category": "Generative AI",
        "url": "https://docs.aws.amazon.com/bedrock/"
    },
    {
        "title": "Amazon Comprehend",
        "service": "Comprehend",
        "content": """
Amazon Comprehend is a natural language processing (NLP) service that uses machine learning to uncover information in unstructured data and text.

Key Features:
- Entity Recognition: Identify people, places, brands, events
- Key Phrase Extraction: Extract key phrases from text
- Sentiment Analysis: Determine positive, negative, neutral, or mixed sentiment
- Language Detection: Automatically detect the language
- Topic Modeling: Discover topics in document collections
- Custom Classification: Train custom models
- Custom Entity Recognition: Identify custom entities
- PII Detection: Identify personally identifiable information

Common Use Cases:
1. Customer feedback analysis
2. Social media sentiment tracking
3. Content categorization
4. Document processing and analysis
5. Compliance and PII redaction

Integration:
- Works with S3, Lambda, Kinesis Data Firehose
- Can be used in real-time or batch processing
- SDK support for multiple programming languages

Certification Tip: Understand when to use Comprehend vs other NLP services.
        """,
        "category": "AI/ML Services",
        "url": "https://docs.aws.amazon.com/comprehend/"
    },
    {
        "title": "Amazon Rekognition",
        "service": "Rekognition",
        "content": """
Amazon Rekognition is a service that makes it easy to add image and video analysis to your applications using proven, highly scalable, deep learning technology.

Capabilities:
- Object and Scene Detection
- Facial Analysis and Recognition
- Face Comparison and Search
- Celebrity Recognition
- Text Detection in Images (OCR)
- Content Moderation
- Custom Labels for custom object detection
- Video Analysis

Key Features:
1. Rekognition Image: Analyze images
2. Rekognition Video: Analyze stored and streaming videos
3. Rekognition Custom Labels: Train custom models without ML expertise

Use Cases:
- User verification
- People counting
- Public safety monitoring
- Content moderation
- Media analysis
- Retail analytics

Best Practices:
- Use confidence scores to filter results
- Implement human review for critical decisions
- Consider privacy and compliance requirements
- Use Custom Labels for domain-specific object detection

Exam Focus: Understand use cases and differences between Rekognition features.
        """,
        "category": "Computer Vision",
        "url": "https://docs.aws.amazon.com/rekognition/"
    },
    {
        "title": "Amazon Textract",
        "service": "Textract",
        "content": """
Amazon Textract is a machine learning service that automatically extracts text, handwriting, and data from scanned documents.

Key Features:
- Text Detection: Extract printed text and handwriting
- Form Extraction: Extract key-value pairs from forms
- Table Extraction: Extract structured data from tables
- Document Analysis API
- Expense Analysis: Extract data from invoices and receipts
- Identity Document Analysis: Extract data from IDs and passports

Differences from Other Services:
- Rekognition: Basic text detection (OCR)
- Textract: Advanced document understanding with structure
- Comprehend: NLP analysis of extracted text

Use Cases:
1. Invoice processing automation
2. Form digitization
3. Document archival and search
4. Identity verification
5. Compliance documentation processing

Integration Patterns:
- S3 → Textract → Lambda → Database
- Synchronous API for single-page documents
- Asynchronous API for multi-page documents
- Human review loops with Amazon A2I

Certification Relevance: Know when to use Textract vs Rekognition for text extraction.
        """,
        "category": "Document AI",
        "url": "https://docs.aws.amazon.com/textract/"
    },
    {
        "title": "Amazon Lex",
        "service": "Lex",
        "content": """
Amazon Lex is a service for building conversational interfaces using voice and text. It's the same technology that powers Amazon Alexa.

Core Concepts:
- Bots: Conversational interface
- Intents: Actions the user wants to perform
- Utterances: Phrases users say to invoke intents
- Slots: Parameters needed to fulfill intents
- Fulfillment: Logic to complete the intent (Lambda)

Key Features:
- Automatic Speech Recognition (ASR)
- Natural Language Understanding (NLU)
- Multi-turn conversations
- Context management
- Built-in integration with AWS Lambda
- Multi-language support
- Sentiment analysis

Building a Lex Bot:
1. Define intents (what users want to do)
2. Add sample utterances for each intent
3. Define slots (required information)
4. Create fulfillment logic (Lambda function)
5. Test and deploy

Integration Options:
- Facebook Messenger
- Slack
- Twilio SMS
- Custom applications via SDK
- Amazon Connect for call centers

Use Cases:
- Customer service chatbots
- Application bots for task automation
- Information bots for FAQs
- Enterprise productivity bots

Exam Tip: Understand Lex components and how it integrates with Lambda and Connect.
        """,
        "category": "Conversational AI",
        "url": "https://docs.aws.amazon.com/lex/"
    },
    {
        "title": "Amazon Personalize",
        "service": "Personalize",
        "content": """
Amazon Personalize is a machine learning service that makes it easy to develop individualized recommendations for customers using your applications.

Core Components:
- Datasets: User interactions, item metadata, user metadata
- Recipes: Pre-configured algorithms for specific use cases
- Solutions: Trained recommendation models
- Campaigns: Deployed models for real-time recommendations

Common Recipes:
1. User-Personalization: General personalization
2. Similar-Items: Item-to-item similarities
3. Personalized-Ranking: Re-rank items for users
4. Popularity-Count: Trending/popular items

Use Cases:
- E-commerce product recommendations
- Content recommendations (videos, articles)
- Personalized search results
- Personalized marketing campaigns
- Dynamic homepage content

Data Requirements:
- Minimum 1000 interaction records
- At least 25 unique users
- Two interactions per user minimum
- Real-time event tracking for better recommendations

Best Practices:
- Start with historical data
- Add real-time event tracking
- Use categorical metadata when available
- Monitor and retrain models regularly
- A/B test recommendation strategies

Integration:
- Store data in S3
- Stream events via SDK or AWS Amplify
- Get recommendations via API
- Track metrics with CloudWatch

Certification Focus: Understand recipes and when to use Personalize vs other ML services.
        """,
        "category": "Recommendations",
        "url": "https://docs.aws.amazon.com/personalize/"
    },
    {
        "title": "SageMaker Training and Deployment",
        "service": "SageMaker",
        "content": """
SageMaker Training and Deployment provide managed infrastructure for ML model lifecycle.

Training Features:
- Built-in Algorithms: Pre-built algorithms for common use cases
- Script Mode: Bring your own training scripts (TensorFlow, PyTorch, etc.)
- Distributed Training: Multi-GPU and multi-node training
- Spot Instances: Cost savings up to 90%
- Automatic Model Tuning: Hyperparameter optimization
- Training Compiler: Optimize training performance

Built-in Algorithms:
1. Linear Learner: Linear regression and classification
2. XGBoost: Gradient boosting
3. Image Classification: CNN-based image classification
4. Object Detection: Identify and locate objects
5. Semantic Segmentation: Pixel-level classification
6. Seq2Seq: Sequence-to-sequence modeling
7. BlazingText: Text classification and word embeddings
8. K-Means: Clustering algorithm

Deployment Options:
- Real-time Endpoints: Low-latency predictions
- Serverless Inference: Pay per use, auto-scaling
- Batch Transform: Batch predictions on large datasets
- Async Inference: Long-running inference jobs
- Multi-Model Endpoints: Host multiple models on one endpoint

Inference Features:
- Auto-scaling based on traffic
- A/B testing with production variants
- Model monitoring for drift detection
- Shadow testing for new models
- Elastic Inference for cost optimization

Cost Optimization:
- Use Spot instances for training (90% savings)
- Serverless inference for variable traffic
- Multi-model endpoints to reduce costs
- Batch transform for non-real-time predictions

Exam Focus: Know deployment options and when to use each type of endpoint.
        """,
        "category": "ML Infrastructure",
        "url": "https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html"
    },
    {
        "title": "ML Model Monitoring and MLOps",
        "service": "SageMaker",
        "content": """
MLOps (Machine Learning Operations) practices and tools for production ML systems.

SageMaker Model Monitor:
- Data Quality Monitoring: Detect data drift
- Model Quality Monitoring: Track prediction accuracy
- Bias Drift Monitoring: Monitor for bias over time
- Feature Attribution Drift: Explain prediction changes

Key Concepts:
- Baseline: Reference dataset for comparison
- Schedule: Automated monitoring jobs
- Violations: Deviations from baseline
- Alerts: CloudWatch alarms for violations

SageMaker Pipelines:
- CI/CD for ML workflows
- DAG-based workflow orchestration
- Model registry integration
- Automated retraining
- Version control for models

Pipeline Components:
1. Data Processing: Feature engineering steps
2. Training: Model training with hyperparameters
3. Evaluation: Model evaluation metrics
4. Condition: Conditional execution
5. Register Model: Save to model registry
6. Deploy: Create or update endpoint

SageMaker Model Registry:
- Centralized model repository
- Model versioning
- Approval workflows
- Model lineage tracking
- Deployment automation

Best Practices:
- Monitor models continuously in production
- Set up automated retraining pipelines
- Use approval workflows for production deployments
- Track model lineage and metadata
- Implement A/B testing for new models
- Set up alerts for model degradation

MLOps Workflow:
1. Experiment and develop models
2. Create automated pipeline
3. Deploy to staging environment
4. Validate with shadow testing
5. Production deployment with monitoring
6. Continuous monitoring and retraining

Certification Tip: Understand the full MLOps lifecycle and SageMaker tools for each stage.
        """,
        "category": "MLOps",
        "url": "https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html"
    },
    {
        "title": "AWS AI/ML Certification Exam Topics",
        "service": "Certification",
        "content": """
AWS AI Practitioner and ML Specialty Certification Overview

AWS Certified AI Practitioner (AIF-C01):
Domain 1: Fundamentals of AI and ML (20%)
- AI/ML concepts and terminology
- Types of ML (supervised, unsupervised, reinforcement)
- Deep learning and neural networks
- Generative AI concepts

Domain 2: Fundamentals of Generative AI (24%)
- Foundation models and large language models
- Prompt engineering
- Retrieval Augmented Generation (RAG)
- Fine-tuning techniques
- Responsible AI practices

Domain 3: Applications of Foundation Models (28%)
- Text generation and analysis
- Code generation
- Image and video generation
- Chatbots and conversational AI

Domain 4: Guidelines for Responsible AI (14%)
- Bias and fairness
- Privacy and security
- Transparency and explainability
- Governance and compliance

Domain 5: Security, Compliance, and Governance (14%)
- AWS security best practices
- Data protection and encryption
- Compliance requirements
- Model governance

AWS Certified Machine Learning - Specialty (MLS-C01):
Domain 1: Data Engineering (20%)
- Data repositories (S3, RDS, DynamoDB)
- Data ingestion and transformation
- Feature engineering

Domain 2: Exploratory Data Analysis (24%)
- Data visualization
- Statistical analysis
- Feature selection
- Handling missing data and outliers

Domain 3: Modeling (36%)
- Algorithm selection
- Training and validation
- Hyperparameter tuning
- Model evaluation metrics

Domain 4: Machine Learning Implementation and Operations (20%)
- SageMaker deployment
- Model monitoring
- A/B testing
- MLOps practices

Key AWS Services to Know:
1. SageMaker (all components)
2. Bedrock
3. Comprehend
4. Rekognition
5. Textract
6. Translate
7. Transcribe
8. Polly
9. Lex
10. Personalize
11. Forecast
12. Kendra

Study Tips:
- Hands-on practice with SageMaker
- Understand when to use each service
- Know the limits and constraints
- Practice cost optimization strategies
- Review well-architected framework for ML
        """,
        "category": "Certification",
        "url": "https://aws.amazon.com/certification/"
    }
]


def create_sample_documents() -> List[Document]:
    """Create LangChain documents from sample data"""
    documents = []

    for doc_data in SAMPLE_DOCS:
        doc = Document(
            page_content=doc_data["content"],
            metadata={
                "title": doc_data["title"],
                "service": doc_data["service"],
                "category": doc_data["category"],
                "source": doc_data["url"]
            }
        )
        documents.append(doc)

    return documents


def scrape_aws_docs(url: str, service_name: str) -> Document:
    """
    Scrape AWS documentation page and create a LangChain document
    Note: This is a basic implementation. For production, consider using
    official AWS documentation APIs or downloading offline docs.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return Document(
            page_content=text[:10000],  # Limit size
            metadata={
                "source": url,
                "service": service_name,
                "type": "aws_docs"
            }
        )
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def ingest_documents(use_sample_data: bool = True):
    """
    Main ingestion function
    """
    print("🚀 Starting AWS Documentation Ingestion...")

    # Initialize embeddings - using HuggingFace (local, no API limits!)
    print("🔧 Loading local embedding model (HuggingFace)...")
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",  # Fast, lightweight model
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✅ Embedding model loaded!")

    # Get documents
    if use_sample_data:
        print("📚 Using sample documentation data (quick start)")
        documents = create_sample_documents()
    else:
        print("🌐 Scraping AWS documentation (this may take a while)...")
        documents = []
        for service, urls in AWS_DOCS_URLS.items():
            for url in urls:
                doc = scrape_aws_docs(url, service)
                if doc:
                    documents.append(doc)
                time.sleep(1)  # Be respectful to AWS servers

    print(f"📄 Loaded {len(documents)} documents")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    splits = text_splitter.split_documents(documents)
    print(f"✂️  Split into {len(splits)} chunks")

    # Create vector store
    persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

    print(f"💾 Creating vector store in {persist_directory}...")

    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="aws_docs"
    )

    print(f"✅ Successfully ingested {len(splits)} document chunks!")
    print(f"📊 Vector store created at: {persist_directory}")

    # Test retrieval
    print("\n🔍 Testing retrieval...")
    results = vector_store.similarity_search("What is Amazon SageMaker?", k=2)
    print(f"Found {len(results)} relevant chunks")
    if results:
        print(f"Sample result: {results[0].page_content[:200]}...")

    return vector_store


if __name__ == "__main__":
    import sys

    # Check if user wants to scrape real docs or use sample data
    use_sample = True
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scrape":
            use_sample = False
            print("⚠️  Live scraping mode - this will take longer")
        elif sys.argv[1] == "--quick-start":
            use_sample = True
            print("🚀 Quick start mode - using sample data")

    ingest_documents(use_sample_data=use_sample)
