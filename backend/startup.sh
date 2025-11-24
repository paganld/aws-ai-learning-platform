#!/bin/bash
set -e

echo "🚀 Starting AWS AI Learning Platform Backend..."

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ ERROR: GOOGLE_API_KEY environment variable is not set!"
    echo "Please set it in your Railway environment variables."
    exit 1
fi

# Check if ChromaDB has data, if not, initialize with sample data
if [ ! -f "chroma_db/chroma.sqlite3" ] && [ ! -d "chroma_db/.chroma" ]; then
    echo "📚 ChromaDB not found. Initializing with sample AWS documentation..."
    python ingest_docs.py --quick-start
    echo "✅ Sample data loaded successfully!"
else
    echo "✅ ChromaDB found with existing data"
fi

# Start the server
echo "🌐 Starting FastAPI server on port ${PORT:-8000}..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
