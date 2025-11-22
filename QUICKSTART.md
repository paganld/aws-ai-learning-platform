# ⚡ Quick Start Guide - 5 Minutes

Get your AWS AI Learning Platform running in 5 minutes!

## Step 1: Get Google Gemini API Key (1 minute)

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

## Step 2: Backend Setup (2 minutes)

```bash
cd aws-ai-learning-platform/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=YOUR_API_KEY_HERE" > .env
echo "CHROMA_PERSIST_DIRECTORY=./chroma_db" >> .env
echo "TEMPERATURE=0.7" >> .env

# Replace YOUR_API_KEY_HERE with your actual key
# On Mac: open .env
# Then paste your API key

# Ingest sample AWS documentation
python ingest_docs.py

# Start backend server (keep this terminal open)
python main.py
```

## Step 3: Frontend Setup (2 minutes)

**Open a NEW terminal window:**

```bash
cd aws-ai-learning-platform/frontend

# Install dependencies
npm install

# Start frontend (keep this terminal open)
npm run dev
```

## Step 4: Start Learning!

Open your browser: **http://localhost:3000**

Try asking:
- "What is Amazon SageMaker?"
- "Explain Amazon Bedrock"
- Click "Practice Quizzes" to test your knowledge!

## ✅ Checklist

- [ ] Got Google Gemini API key
- [ ] Created `.env` file with API key
- [ ] Ran `pip install -r requirements.txt`
- [ ] Ran `python ingest_docs.py` (creates knowledge base)
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Opened browser to http://localhost:3000

## 🎯 What You Get

- ✅ AI Tutor powered by Google Gemini
- ✅ Knowledge base with 10+ AWS AI/ML services
- ✅ Practice quizzes with instant feedback
- ✅ Certification prep materials
- ✅ Interactive learning interface

## 🆘 Quick Fixes

**Backend won't start?**
```bash
# Make sure you're in the venv
source venv/bin/activate
# Check if .env has your API key
cat .env
```

**Frontend won't start?**
```bash
# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**No data in knowledge base?**
```bash
# Re-run ingestion
cd backend
python ingest_docs.py
```

## 🚀 Next Steps

1. **Try the AI Tutor** - Ask questions about AWS services
2. **Take a Quiz** - Test your knowledge
3. **Explore Topics** - Browse AWS AI/ML services
4. **Add More Docs** - Edit `backend/ingest_docs.py` to add more content

Happy Learning! 🎓
