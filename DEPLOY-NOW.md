# 🚀 Deploy RIGHT NOW - Web Interface Method

No CLI needed! Deploy using web interfaces only.

## 🎯 Backend: Railway (5 minutes)

### Step 1: Create Railway Account
1. Go to: **https://railway.app**
2. Click "Login" → Sign up with GitHub
3. Verify your email

### Step 2: Create New Project
1. Click "New Project"
2. Choose "Empty Project"
3. Name it: `aws-ai-backend`

### Step 3: Upload Your Code

**Option A: Via GitHub (Recommended)**
1. Push your code to GitHub:
   ```bash
   cd /Users/dwightpaganlugo/DJPL/aws-ai-learning-platform
   git init
   git add .
   git commit -m "Initial commit"
   # Create repo on GitHub, then:
   git remote add origin YOUR_GITHUB_URL
   git push -u origin main
   ```
2. In Railway: Connect GitHub repo
3. Select the repository
4. Railway will auto-detect and deploy!

**Option B: Manual Upload (If no GitHub)**
1. In Railway project, click "Settings"
2. Under "Source", upload files manually
3. Upload these files from `backend/` folder:
   - `main.py`
   - `requirements.txt`
   - `.env` (with your API key)
   - `chroma_db/` folder (entire folder)

### Step 4: Configure Environment Variables
1. In Railway project, click "Variables"
2. Add these variables:
   - **GOOGLE_API_KEY**: `AIzaSyA0BBT2dQbELCja-pWPIxzTDaSPMuZKtKE`
   - **CHROMA_PERSIST_DIRECTORY**: `./chroma_db`
   - **TEMPERATURE**: `0.7`
   - **MAX_TOKENS**: `2048`
3. Click "Add Variable" for each
4. Railway will auto-redeploy

### Step 5: Get Your Backend URL
1. In Railway project, click "Settings"
2. Under "Domains", click "Generate Domain"
3. Copy your URL: `https://yourapp.railway.app`
4. **SAVE THIS URL** - you'll need it for frontend!

### Step 6: Verify Backend Works
1. Visit: `https://yourapp.railway.app/`
2. You should see: `{"status": "online", ...}`
3. Visit: `https://yourapp.railway.app/docs` for API documentation

---

## 🎨 Frontend: Vercel (5 minutes)

### Step 1: Create Vercel Account
1. Go to: **https://vercel.com**
2. Click "Sign Up" → Use GitHub
3. Verify your account

### Step 2: Deploy Frontend

**Option A: Via GitHub (Recommended)**
1. If you pushed to GitHub in backend step, Vercel can use same repo
2. In Vercel dashboard, click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Click "Deploy"

**Option B: Vercel CLI (Alternative)**
```bash
cd frontend
npx vercel login
npx vercel
# Follow prompts
```

### Step 3: Add Environment Variable
1. In Vercel project, go to "Settings"
2. Click "Environment Variables"
3. Add:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Railway URL (e.g., `https://yourapp.railway.app`)
   - **Environments**: Check all (Production, Preview, Development)
4. Click "Save"

### Step 4: Redeploy
1. Go to "Deployments" tab
2. Click "..." on latest deployment
3. Click "Redeploy"
4. Or just push a new commit to trigger auto-deploy

### Step 5: Get Your Frontend URL
1. Vercel will show you the URL after deployment
2. Usually: `https://yourproject.vercel.app`
3. **SAVE THIS URL** - this is your live site!

---

## ✅ Final Configuration (3 minutes)

### Update CORS in Backend

1. **Edit backend/main.py:**

   Find this section (around line 26):
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       ...
   )
   ```

   Change to:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",
           "https://yourproject.vercel.app",  # Add your Vercel URL here!
       ],
       ...
   )
   ```

2. **Push update to Railway:**
   - If using GitHub: Commit and push the change
   - If manual: Re-upload `main.py` to Railway
   - Railway will auto-redeploy

---

## 🎉 Test Your Production App!

1. **Visit your Vercel URL**: `https://yourproject.vercel.app`

2. **Test the AI Tutor:**
   - Type: "What is Amazon SageMaker?"
   - Should get a response with source citations

3. **Test Quiz Generation:**
   - Click "Practice Quizzes"
   - Select "Amazon SageMaker"
   - Should generate 5 questions

4. **Test Topics:**
   - Click "Topics" tab
   - Browse AWS services
   - Click any service to learn about it

---

## 📋 Deployment Checklist

- [ ] Railway account created
- [ ] Backend deployed to Railway
- [ ] Environment variables set in Railway
- [ ] Backend URL copied
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] API URL configured in Vercel
- [ ] CORS updated in backend
- [ ] Backend redeployed
- [ ] Tested chat feature
- [ ] Tested quiz feature
- [ ] No console errors
- [ ] All features working!

---

## 🆘 Troubleshooting

### Backend Issues

**"Internal Server Error"**
- Check Railway logs: Project → View Logs
- Verify environment variables are set
- Check `chroma_db` folder was uploaded

**"Module not found"**
- Railway didn't install dependencies
- Check that `requirements.txt` is in root of project
- May need to add build command in Railway settings

### Frontend Issues

**"Failed to fetch" or CORS error**
- Check `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Verify backend URL is accessible
- Make sure CORS includes your Vercel URL
- Redeploy both backend and frontend

**"API endpoint not found"**
- Check the API URL doesn't have trailing slash
- Verify backend is actually running (visit backend URL)
- Check Vercel logs for errors

### Still Stuck?

1. Check Railway logs
2. Check Vercel logs
3. Try redeploying both services
4. Verify all environment variables
5. Test backend API directly in browser

---

## 📊 Your Live URLs

After deployment, you'll have:

**Frontend (User-facing):**
- https://your-project.vercel.app
- Share this with users!

**Backend (API):**
- https://your-app.railway.app
- API documentation: https://your-app.railway.app/docs

---

## 🎊 Success!

Congratulations! Your AWS AI Learning Platform is now LIVE!

**What you've deployed:**
- ✅ Full-stack RAG application
- ✅ Google Gemini AI integration
- ✅ Vector database with AWS docs
- ✅ Modern responsive UI
- ✅ Global CDN distribution
- ✅ Auto-scaling infrastructure
- ✅ HTTPS enabled
- ✅ 99.9% uptime SLA

**Cost:** $0/month (free tier)

**Share your app:** Send the Vercel URL to anyone!

---

## 🚀 Next Steps

1. **Share it!**
   - Post on LinkedIn
   - Share with study groups
   - Add to your portfolio

2. **Customize:**
   - Add your own AWS documentation
   - Change colors/branding
   - Add new features

3. **Monitor:**
   - Check Railway analytics
   - Review Vercel analytics
   - Track user engagement

4. **Improve:**
   - Add more AWS services
   - Implement user accounts
   - Add progress tracking

---

**You did it! Your production app is live! 🎉**
