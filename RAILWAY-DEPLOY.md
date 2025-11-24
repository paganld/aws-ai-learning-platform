# Railway Deployment Guide

This guide will help you deploy the AWS AI Learning Platform to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **GitHub Repository**: Your code should be pushed to GitHub

## Backend Deployment (FastAPI + RAG)

### Step 1: Create New Project on Railway

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `paganld/aws-ai-learning-platform`

### Step 2: Configure Backend Service

1. Railway will detect your code and start building
2. Go to **Settings** tab
3. Update these settings:

**Build Settings:**
- Builder: `DOCKERFILE`
- Dockerfile Path: `backend/Dockerfile`
- Root Directory: Leave blank (monorepo setup)

**Deploy Settings:**
- Start Command: `./startup.sh`
- Health Check Path: `/`
- Health Check Timeout: `100` seconds

### Step 3: Add Environment Variables

Go to **Variables** tab and add:

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
FRONTEND_URL=https://your-frontend-url.vercel.app
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

**Important Notes:**
- Replace `your_google_gemini_api_key_here` with your actual API key
- You'll update `FRONTEND_URL` after deploying the frontend
- The backend will auto-initialize sample data on first startup

### Step 4: Deploy

1. Railway will automatically deploy after you add environment variables
2. Wait for build to complete (5-10 minutes first time)
3. Check **Logs** tab to see:
   ```
   🚀 Starting AWS AI Learning Platform Backend...
   📚 ChromaDB not found. Initializing with sample AWS documentation...
   ✅ Sample data loaded successfully!
   🌐 Starting FastAPI server...
   ```

4. Once you see "Application startup complete", your backend is ready!
5. Click **Settings** → **Networking** → **Generate Domain** to get your backend URL

### Step 5: Test Backend

Visit your backend URL (e.g., `https://your-app.railway.app`)

You should see:
```json
{
  "status": "online",
  "message": "AWS AI Learning Platform API",
  "rag_initialized": true,
  "documents_loaded": 20
}
```

## Frontend Deployment (Next.js)

### Option 1: Deploy to Vercel (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Install Command**: `npm install`

5. Add Environment Variables:
   ```bash
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```

6. Click **Deploy**

7. After deployment, copy your Vercel URL and update the `FRONTEND_URL` variable in Railway backend

### Option 2: Deploy Frontend to Railway

1. In Railway, click **"New Service"** in your project
2. Select **"GitHub Repo"** → Same repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm start`

4. Add Environment Variable:
   ```bash
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```

5. Generate domain for frontend service

## Post-Deployment Setup

### Update CORS Configuration

1. Go back to Railway backend service
2. Update `FRONTEND_URL` environment variable with your actual frontend URL
3. Redeploy backend (Railway will auto-redeploy when you change variables)

### Verify Everything Works

1. Visit your frontend URL
2. Try the AI Tutor:
   - Ask: "What is Amazon SageMaker?"
   - You should get a detailed answer with sources
3. Try Practice Quizzes:
   - Select a topic
   - Generate and take a quiz
4. Check that all features work

## Monitoring & Logs

### View Logs
- Railway Dashboard → Your Service → **Logs** tab
- Watch for errors or issues
- Logs show API requests and responses

### Check Metrics
- Railway Dashboard → Your Service → **Metrics** tab
- Monitor CPU, Memory, Network usage

### Health Check
- Backend health: `https://your-backend.railway.app/`
- API docs: `https://your-backend.railway.app/docs`

## Common Issues & Solutions

### Issue: "GOOGLE_API_KEY not found"
**Solution**: Make sure you added the environment variable in Railway and it's spelled correctly.

### Issue: "Vector store not initialized"
**Solution**:
- Check logs during startup
- Make sure `startup.sh` ran successfully
- Restart the deployment

### Issue: "Failed to fetch" from frontend
**Solution**:
- Check that `NEXT_PUBLIC_API_URL` points to correct backend URL
- Verify CORS settings in backend
- Make sure backend is running

### Issue: Build timeout
**Solution**:
- First build takes longer (downloads models)
- Increase health check timeout to 100+ seconds
- Check Dockerfile caches the sentence transformer model

### Issue: "ChromaDB not persisting"
**Solution**:
- Railway uses ephemeral storage by default
- For production, consider adding Railway Volume
- Or re-initialize on each startup (current approach)

## Adding More Documents

To add more AWS documentation to your knowledge base:

1. Clone your repository locally
2. Edit `backend/ingest_docs.py`
3. Add more sample documents or AWS doc URLs
4. Run locally: `python ingest_docs.py`
5. Commit the updated `chroma_db` folder
6. Push to GitHub
7. Railway will redeploy automatically

## Cost Optimization

### Railway Free Tier
- $5 free credits per month
- Should be enough for testing/hobby projects
- Monitor usage in Dashboard

### Google Gemini API
- Free tier: 60 requests per minute
- Upgrade if you need more

### Tips to Reduce Costs
1. Use Railway's sleep mode for inactive services
2. Limit API calls in development
3. Cache responses where possible
4. Use smaller models for embeddings

## Production Recommendations

### Before Going Live:

1. **Add Authentication**
   - Use Auth0, Clerk, or NextAuth.js
   - Protect API endpoints

2. **Add Rate Limiting**
   - Prevent abuse
   - Use Redis or in-memory cache

3. **Set up Monitoring**
   - Use Sentry for error tracking
   - Set up alerts for downtime

4. **Add Analytics**
   - Track user questions
   - Monitor popular topics
   - Analyze quiz performance

5. **Database Persistence**
   - Add Railway Volume for ChromaDB
   - Or use managed vector DB (Pinecone, Weaviate)

6. **Environment-Specific Configs**
   - Separate dev/staging/prod environments
   - Different API keys per environment

## Support

### Getting Help
- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Check GitHub Issues in your repository

### Useful Commands

```bash
# Local testing
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ingest_docs.py --quick-start
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Vercel/Railway
3. ✅ Test all features
4. 📝 Add more AWS documentation
5. 🔐 Add authentication
6. 📊 Add analytics
7. 🚀 Share with users!

Good luck with your deployment! 🎉
