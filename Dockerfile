# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy ONLY the files we need
COPY backend/requirements.txt /app/requirements.txt
COPY backend/main.py /app/main.py
COPY backend/chroma_db /app/chroma_db

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start command - Railway provides PORT env variable
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
