# ✅ Deployment Checklist

Use this checklist to deploy your AWS AI Learning Platform to production.

## Pre-Deployment

- [ ] Application is working locally
  - Backend: http://localhost:8000
  - Frontend: http://localhost:3000
  - Chat feature tested
  - Quiz feature tested

- [ ] Have all required credentials
  - Google Gemini API Key
  - GitHub account (for Vercel/Railway)

- [ ] Code is ready
  - No hardcoded API keys
  - Environment variables configured
  - Documentation up to date

## Backend Deployment (Choose One)

### Option A: Railway (Recommended - FREE)

- [ ] Create Railway account at railway.app
- [ ] Install Railway CLI: `npm install -g @railway/cli`
- [ ] Navigate to backend folder
- [ ] Run `railway login`
- [ ] Run `railway init`
- [ ] Run `railway up`
- [ ] Add environment variables in Railway dashboard:
  - `GOOGLE_API_KEY`
  - `CHROMA_PERSIST_DIRECTORY=./chroma_db`
  - `TEMPERATURE=0.7`
- [ ] Copy your Railway URL (e.g., `https://yourapp.railway.app`)
- [ ] Verify backend is working: Visit `https://yourapp.railway.app/`

### Option B: Render (Alternative - FREE)

- [ ] Create Render account at render.com
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub or use manual deployment
- [ ] Configure:
  - Root: `backend`
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables
- [ ] Deploy and copy URL

## Frontend Deployment (Vercel - Recommended)

- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Navigate to frontend folder
- [ ] Run `vercel login`
- [ ] Run `vercel`
- [ ] Go to Vercel dashboard
- [ ] Add environment variable:
  - Key: `NEXT_PUBLIC_API_URL`
  - Value: Your backend URL from step above
- [ ] Redeploy: `vercel --prod`
- [ ] Copy your Vercel URL
- [ ] Test your site!

## Post-Deployment Configuration

- [ ] Update backend CORS to allow frontend URL
  - Edit `backend/main.py`
  - Add your Vercel URL to `allow_origins`
  - Redeploy backend

- [ ] Test all features on production:
  - [ ] Homepage loads
  - [ ] Chat works
  - [ ] Quiz generation works
  - [ ] Topics page works
  - [ ] API responds correctly

## Optional Enhancements

- [ ] Add custom domain
  - Buy domain from Namecheap/Google Domains
  - Configure on Vercel
  - Update DNS records

- [ ] Set up monitoring
  - UptimeRobot for availability
  - Google Analytics for usage

- [ ] Enable error tracking
  - Sentry or LogRocket

- [ ] Backup strategy
  - Export vector database
  - Document environment variables

## Verification

Test these on your production URL:

- [ ] Visit homepage
- [ ] Ask AI Tutor: "What is Amazon SageMaker?"
- [ ] Generate a quiz on any topic
- [ ] Check all 3 tabs work (Chat, Quiz, Topics)
- [ ] Mobile responsiveness
- [ ] Check browser console for errors

## Troubleshooting

If something doesn't work:

1. **Check logs**
   - Railway: Dashboard → Logs
   - Vercel: Dashboard → Deployment → Logs

2. **Verify environment variables**
   - Both platforms: Check dashboard

3. **Test API directly**
   - Visit: `https://your-backend-url.com/`
   - Should see: `{"status": "online"}`

4. **CORS errors?**
   - Update `allow_origins` in `main.py`
   - Redeploy backend

5. **Still stuck?**
   - Check DEPLOYMENT-GUIDE.md
   - Review error messages in logs

## Success! 🎉

Once all checkboxes are checked:

✅ Your app is live!
✅ Anyone can access it!
✅ You're serving AI-powered AWS education!

**Share your URL:**
- Frontend: `https://your-site.vercel.app`
- Backend API: `https://your-api.railway.app`

## Next Steps

- Add more AWS documentation
- Implement user authentication
- Add progress tracking
- Build a community
- Get feedback from users

---

**Estimated Time:**
- Railway + Vercel: **15-20 minutes**
- With custom domain: **30-40 minutes**

**Total Cost:**
- Free tier: **$0/month**
- Perfect for getting started!
