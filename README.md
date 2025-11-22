# 🚀 AWS AI Learning Platform

A RAG-powered learning platform to master AWS AI/ML services and prepare for AWS certifications.

## ✨ Features

- 🤖 **AI Tutor**: Chat with Google Gemini powered by AWS documentation
- 📚 **RAG System**: Retrieval Augmented Generation with ChromaDB vector database
- 📝 **Practice Quizzes**: AI-generated quizzes on AWS AI/ML topics
- 🎓 **Certification Prep**: Focus on AWS AI Practitioner & ML Specialty exams
- 💬 **Interactive Learning**: Ask questions and get instant, accurate answers
- 🔍 **Source Citations**: See which AWS docs were used to answer your questions

## 🏗️ Architecture

```
Frontend (Next.js + React)
    ↓
Backend API (FastAPI)
    ↓
LangChain + Google Gemini
    ↓
ChromaDB (Vector Store) ← AWS Documentation
```

### Tech Stack

**Backend:**
- FastAPI (Python web framework)
- LangChain (RAG orchestration)
- Google Gemini (LLM)
- ChromaDB (Vector database)
- BeautifulSoup (Web scraping)

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Google Gemini API Key (free tier available)
- AWS Account (optional, for S3 storage)

## 🚀 Quick Start

### Step 1: Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### Step 2: Set Up Backend

```bash
# Navigate to backend directory
cd aws-ai-learning-platform/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_key_here
```

### Step 3: Ingest Documentation

```bash
# Run the ingestion script (uses sample data for quick start)
python ingest_docs.py

# This will:
# - Load AWS AI/ML documentation samples
# - Create embeddings using Google Gemini
# - Store in ChromaDB vector database
# - Takes about 2-3 minutes

# Optional: Scrape live AWS docs (takes longer)
# python ingest_docs.py --scrape
```

### Step 4: Start Backend Server

```bash
# Start FastAPI server
python main.py

# Or use uvicorn directly:
# uvicorn main:app --reload

# Backend will run on http://localhost:8000
```

### Step 5: Set Up Frontend

```bash
# Open a new terminal
cd aws-ai-learning-platform/frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will run on http://localhost:3000
```

### Step 6: Open Your Browser

Navigate to **http://localhost:3000** and start learning!

## 📖 Usage Guide

### Using the AI Tutor

1. Click on "AI Tutor" tab
2. Ask questions like:
   - "What is Amazon SageMaker?"
   - "How do I prepare for the AWS AI Practitioner exam?"
   - "Compare Amazon Bedrock and SageMaker"
   - "Explain Amazon Comprehend's sentiment analysis"

3. The AI will provide answers based on AWS documentation with source citations

### Taking Practice Quizzes

1. Click on "Practice Quizzes" tab
2. Select a topic (e.g., "Amazon SageMaker")
3. Answer multiple-choice questions
4. Get instant feedback with explanations
5. Track your score

### Exploring Topics

1. Click on "Topics" tab
2. Browse AWS AI/ML services by category
3. Click any topic to ask the AI about it
4. Generate practice quizzes for any topic

## 🎯 Covered AWS Services

### AI Services
- Amazon SageMaker (all components)
- Amazon Bedrock
- Amazon Comprehend
- Amazon Rekognition
- Amazon Textract
- Amazon Translate
- Amazon Transcribe
- Amazon Polly
- Amazon Lex
- Amazon Personalize

### ML Infrastructure
- SageMaker Studio
- SageMaker Training
- SageMaker Inference
- SageMaker Feature Store
- SageMaker Model Monitor
- SageMaker Autopilot

### Certifications
- AWS Certified AI Practitioner
- AWS Certified Machine Learning - Specialty

## 🔧 Configuration

### Backend Configuration (.env)

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional AWS (for storing docs in S3)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=aws-docs-learning-platform

# Application Settings
CHROMA_PERSIST_DIRECTORY=./chroma_db
MAX_TOKENS=2048
TEMPERATURE=0.7
```

### Customizing the Knowledge Base

To add more AWS documentation:

1. Edit `backend/ingest_docs.py`
2. Add URLs to `AWS_DOCS_URLS` dictionary
3. Or add sample documents to `SAMPLE_DOCS` list
4. Run `python ingest_docs.py` again

## 📚 API Endpoints

### Backend API (http://localhost:8000)

- `GET /` - Health check
- `POST /chat` - Send questions to AI tutor
- `POST /quiz` - Generate practice quizzes
- `GET /topics` - Get available AWS topics
- `GET /stats` - Get knowledge base statistics

### API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing the System

### Test Backend

```bash
cd backend

# Test with curl
curl http://localhost:8000/

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Amazon SageMaker?"}'

# Test quiz generation
curl -X POST http://localhost:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"topic": "Amazon SageMaker", "difficulty": "medium", "num_questions": 3}'
```

### Test Frontend

1. Open http://localhost:3000
2. Try sample questions
3. Generate a quiz
4. Browse topics

## 🎓 Study Plan for AWS Certifications

### AWS Certified AI Practitioner

**Focus Areas:**
1. Generative AI fundamentals
2. Amazon Bedrock and foundation models
3. Prompt engineering
4. RAG (Retrieval Augmented Generation)
5. Responsible AI practices

**Recommended Path:**
1. Start with "What is Amazon Bedrock?"
2. Learn about foundation models
3. Practice quizzes on Bedrock
4. Explore RAG concepts
5. Study responsible AI guidelines

### AWS Certified Machine Learning - Specialty

**Focus Areas:**
1. SageMaker (all features)
2. Data engineering
3. Model training and tuning
4. Deployment strategies
5. MLOps best practices

**Recommended Path:**
1. Master SageMaker components
2. Understand data preprocessing
3. Learn model training techniques
4. Practice deployment scenarios
5. Study MLOps workflows

## 🚢 Deployment

### Deploy Backend (AWS Lambda + API Gateway)

```bash
# Install serverless framework
npm install -g serverless

# Deploy backend
cd backend
serverless deploy
```

### Deploy Frontend (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel
```

## 📈 Adding More Content

### Adding New AWS Services

1. **Update Backend Documentation:**
   ```python
   # In ingest_docs.py, add to SAMPLE_DOCS:
   {
       "title": "Amazon Forecast",
       "service": "Forecast",
       "content": "...",
       "category": "Time Series",
       "url": "https://docs.aws.amazon.com/forecast/"
   }
   ```

2. **Re-run Ingestion:**
   ```bash
   python ingest_docs.py
   ```

3. **Update Topics List:**
   ```python
   # In main.py, update get_topics() endpoint
   ```

### Customizing Quiz Generation

Edit the quiz prompt in `backend/main.py`:

```python
quiz_prompt = f"""Generate quiz questions...
Focus on: [your specific focus areas]
Format: [your desired format]
"""
```

## 🐛 Troubleshooting

### Backend Issues

**"GOOGLE_API_KEY not found"**
- Make sure you created `.env` file in `backend/` directory
- Copy your API key from Google AI Studio
- Restart the backend server

**"Vector store not initialized"**
- Run `python ingest_docs.py` first
- Check that `chroma_db` directory was created

**"Module not found"**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**"Failed to fetch"**
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**"npm install" errors**
- Update Node.js to version 18+
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## 🤝 Contributing

Want to add more features or AWS services? Feel free to:

1. Add more AWS documentation to the knowledge base
2. Improve quiz generation prompts
3. Add new learning paths
4. Enhance the UI/UX
5. Add more certification topics

## 📝 License

MIT License - feel free to use for personal or commercial projects!

## 🙏 Acknowledgments

- AWS Documentation
- Google Gemini API
- LangChain Framework
- ChromaDB
- Next.js & React

## 📞 Support

Questions or issues?
- Check the API documentation at http://localhost:8000/docs
- Review the troubleshooting section above
- Test individual components

---

**Happy Learning! 🎓 Good luck with your AWS certifications! 🚀**
