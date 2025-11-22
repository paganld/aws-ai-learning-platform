# 🚀 Production Deployment Guide

Complete guide to deploy your AWS AI Learning Platform to production.

## 📋 Table of Contents

1. [Quick Deploy (Recommended)](#quick-deploy-recommended)
2. [Backend Deployment Options](#backend-deployment-options)
3. [Frontend Deployment](#frontend-deployment)
4. [Environment Variables](#environment-variables)
5. [Post-Deployment](#post-deployment)
6. [Troubleshooting](#troubleshooting)

---

## Quick Deploy (Recommended)

### ⚡ Fastest Path to Production (FREE)

**Backend:** Railway (Free tier)
**Frontend:** Vercel (Free tier)
**Total Cost:** $0/month

---

## Backend Deployment Options

### Option 1: Railway (Recommended - FREE)

Railway offers 500 hours/month free tier - perfect for this project!

#### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy Backend**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login
   railway login

   # Navigate to backend
   cd /Users/dwightpaganlugo/DJPL/aws-ai-learning-platform/backend

   # Initialize project
   railway init

   # Deploy
   railway up
   ```

3. **Set Environment Variables**
   - Go to Railway dashboard
   - Click your project → Variables
   - Add:
     - `GOOGLE_API_KEY`: Your Gemini API key
     - `CHROMA_PERSIST_DIRECTORY`: `./chroma_db`
     - `TEMPERATURE`: `0.7`

4. **Upload Vector Database**
   ```bash
   # The chroma_db folder needs to be included in deployment
   # Railway will persist it automatically
   ```

5. **Get Your Backend URL**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Copy this for frontend configuration

---

### Option 2: Render (FREE)

Render offers free tier with 750 hours/month.

#### Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Deploy**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Or use "Deploy from Git URL"

3. **Configuration**
   - **Name:** aws-ai-learning-backend
   - **Region:** Oregon (US West)
   - **Branch:** main
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**
   - `GOOGLE_API_KEY`: Your API key
   - `CHROMA_PERSIST_DIRECTORY`: `./chroma_db`
   - `TEMPERATURE`: `0.7`

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Copy your URL: `https://your-app.onrender.com`

---

### Option 3: AWS EC2 (Paid - Most Control)

For production at scale.

#### Requirements:
- AWS Account
- Basic Linux knowledge

#### Steps:

1. **Launch EC2 Instance**
   ```bash
   # t2.micro (free tier eligible) or t3.small
   # Ubuntu 22.04 LTS
   # Open ports: 80, 443, 8000
   ```

2. **SSH and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip

   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python
   sudo apt install python3-pip python3-venv -y

   # Clone your repository or upload files
   git clone your-repo-url
   cd aws-ai-learning-platform/backend

   # Create venv and install
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Set environment variables
   nano .env
   # Add your GOOGLE_API_KEY

   # Run ingestion
   python ingest_docs.py

   # Install PM2 for process management
   sudo npm install -g pm2

   # Start server
   pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name aws-ai-api
   pm2 save
   pm2 startup
   ```

3. **Setup Nginx (Optional)**
   ```bash
   sudo apt install nginx -y

   # Configure reverse proxy
   sudo nano /etc/nginx/sites-available/default
   ```

   Add:
   ```nginx
   location / {
       proxy_pass http://localhost:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

4. **SSL with Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

---

## Frontend Deployment

### Vercel (Recommended - FREE & FAST)

Vercel is made for Next.js - deployment takes 2 minutes!

#### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend**
   ```bash
   cd /Users/dwightpaganlugo/DJPL/aws-ai-learning-platform/frontend

   # Login to Vercel
   vercel login

   # Deploy
   vercel

   # Follow prompts:
   # - Link to existing project? No
   # - Project name: aws-ai-learning-platform
   # - Directory: ./
   # - Override settings? No
   ```

3. **Set Environment Variable**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click your project → Settings → Environment Variables
   - Add:
     - Key: `NEXT_PUBLIC_API_URL`
     - Value: Your backend URL (e.g., `https://your-app.railway.app`)
   - Redeploy:
     ```bash
     vercel --prod
     ```

4. **Custom Domain (Optional)**
   - Go to Project Settings → Domains
   - Add your domain: `awslearning.com`
   - Update DNS records as instructed

---

### Alternative: Netlify (FREE)

1. **Deploy**
   ```bash
   cd frontend
   npm install -g netlify-cli
   netlify login
   netlify init
   netlify deploy --prod
   ```

2. **Environment Variables**
   - Netlify Dashboard → Site Settings → Environment Variables
   - Add `NEXT_PUBLIC_API_URL`

---

## Environment Variables

### Backend (.env)

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional (with defaults)
CHROMA_PERSIST_DIRECTORY=./chroma_db
MAX_TOKENS=2048
TEMPERATURE=0.7
```

### Frontend (.env.local)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Post-Deployment

### 1. Update Frontend API URL

Edit `frontend/app/page.tsx`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```

### 2. Update CORS in Backend

Edit `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-url.vercel.app",  # Add your production URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Re-run Document Ingestion on Production

On your production backend:

```bash
python ingest_docs.py
```

This creates the `chroma_db` folder with your knowledge base.

### 4. Test Your Deployment

1. Visit your frontend URL
2. Try asking a question in the chat
3. Generate a quiz
4. Check that everything works!

---

## Cost Breakdown

### FREE Tier (Recommended for Getting Started)

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| Railway | Hobby | $0 | 500 hrs/month, 512MB RAM |
| Vercel | Hobby | $0 | 100GB bandwidth |
| Google Gemini | Free | $0 | 60 requests/min |
| **Total** | | **$0/month** | Perfect for demo/personal use |

### Production Scale

| Service | Plan | Cost | Specs |
|---------|------|------|-------|
| Railway | Pro | $20/month | 8GB RAM, always-on |
| Vercel | Pro | $20/month | Unlimited bandwidth |
| AWS EC2 | t3.small | ~$15/month | 2GB RAM, full control |
| **Total** | | **$40-55/month** | Handles 10K+ users |

---

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt --upgrade
```

**Vector store not loading:**
```bash
# Re-run ingestion
python ingest_docs.py
```

**Port issues:**
```bash
# Railway/Render use $PORT automatically
# For custom servers, ensure $PORT is set
```

### Frontend Issues

**API connection failed:**
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Verify CORS allows your frontend domain
- Check backend is running

**Build errors:**
```bash
rm -rf .next node_modules
npm install
npm run build
```

### Database Issues

**ChromaDB not persisting:**
- Ensure `CHROMA_PERSIST_DIRECTORY` is set
- Check file permissions
- On Railway/Render, use volumes for persistence

---

## Monitoring & Logs

### Railway
- Dashboard → Your Service → Logs
- Real-time log streaming

### Render
- Dashboard → Your Service → Logs
- Automatic logging

### Vercel
- Dashboard → Your Project → Deployment → Logs
- Function logs available

---

## Scaling Considerations

### When to Upgrade:

**Move from Free → Paid when:**
- More than 500 concurrent users
- Need 99.9% uptime SLA
- Require more than 512MB RAM
- Need faster response times

### Optimization Tips:

1. **Cache responses** - Add Redis for frequently asked questions
2. **CDN** - Vercel provides this automatically
3. **Database** - Move to PostgreSQL for user data
4. **Load balancing** - Use AWS ALB or Cloudflare

---

## Security Checklist

Before going live:

- [ ] Environment variables are set (not hardcoded)
- [ ] CORS is configured correctly
- [ ] API keys are in secrets/environment variables
- [ ] HTTPS is enabled (automatic on Vercel/Railway)
- [ ] Rate limiting is configured
- [ ] Input validation is working
- [ ] Error messages don't expose sensitive data

---

## Next Steps

After deployment:

1. **Custom Domain**
   - Buy domain from Namecheap/Google Domains
   - Configure on Vercel

2. **Analytics**
   - Add Google Analytics
   - Track user engagement

3. **Monitoring**
   - Set up UptimeRobot for availability monitoring
   - Configure error tracking (Sentry)

4. **Backup**
   - Export ChromaDB regularly
   - Back up environment variables

---

## Quick Reference: Deployment Commands

### Railway
```bash
railway login
railway init
railway up
railway open  # Open dashboard
```

### Vercel
```bash
vercel login
vercel  # Deploy
vercel --prod  # Production deploy
vercel domains add your-domain.com  # Add domain
```

### Render
- Use dashboard (easier than CLI)
- Or: `render deploy`

---

## Support

**Issues?**
- Check logs first
- Verify environment variables
- Test API endpoints directly
- Check this guide's troubleshooting section

**Need Help?**
- Railway Discord
- Vercel Community
- Stack Overflow

---

**Congratulations! Your AWS AI Learning Platform is now live! 🎉**

Your students can access it from anywhere in the world!
