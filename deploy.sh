#!/bin/bash

# AWS AI Learning Platform - Quick Deploy Script
# This script helps you deploy to production

echo "🚀 AWS AI Learning Platform - Deployment Helper"
echo "================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found"
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found"
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo ""
echo "✅ All CLI tools ready!"
echo ""

# Menu
echo "Choose deployment option:"
echo ""
echo "1) Deploy Backend to Railway"
echo "2) Deploy Frontend to Vercel"
echo "3) Deploy Both (Full Stack)"
echo "4) Just show me the commands"
echo "5) Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🔧 Deploying Backend to Railway..."
        echo ""
        cd backend
        railway login
        echo ""
        read -p "Have you created a Railway project? (y/n): " project_exists
        if [ "$project_exists" = "n" ]; then
            railway init
        fi
        echo ""
        echo "📦 Deploying..."
        railway up
        echo ""
        echo "✅ Backend deployed!"
        echo ""
        echo "⚠️  IMPORTANT: Set these environment variables in Railway dashboard:"
        echo "   - GOOGLE_API_KEY: Your Gemini API key"
        echo "   - CHROMA_PERSIST_DIRECTORY: ./chroma_db"
        echo "   - TEMPERATURE: 0.7"
        echo ""
        railway open
        ;;

    2)
        echo ""
        echo "🎨 Deploying Frontend to Vercel..."
        echo ""
        read -p "Enter your backend URL (e.g., https://yourapp.railway.app): " backend_url

        cd frontend
        echo "NEXT_PUBLIC_API_URL=$backend_url" > .env.production

        vercel login
        echo ""
        echo "📦 Deploying..."
        vercel --prod
        echo ""
        echo "✅ Frontend deployed!"
        echo ""
        echo "⚠️  IMPORTANT: If you need to update API URL:"
        echo "   1. Go to Vercel dashboard"
        echo "   2. Settings → Environment Variables"
        echo "   3. Add NEXT_PUBLIC_API_URL = $backend_url"
        echo "   4. Redeploy"
        ;;

    3)
        echo ""
        echo "🚀 Full Stack Deployment"
        echo ""
        echo "Step 1: Backend Deployment"
        echo "=========================="
        cd backend
        railway login
        read -p "Have you created a Railway project? (y/n): " project_exists
        if [ "$project_exists" = "n" ]; then
            railway init
        fi
        railway up
        echo ""
        read -p "Enter your Railway backend URL: " backend_url
        echo ""

        echo "Step 2: Frontend Deployment"
        echo "==========================="
        cd ../frontend
        echo "NEXT_PUBLIC_API_URL=$backend_url" > .env.production
        vercel login
        vercel --prod
        echo ""
        echo "✅ Full stack deployed!"
        echo ""
        echo "🎉 Your app is live!"
        echo ""
        echo "⚠️  Don't forget to:"
        echo "   1. Set Railway environment variables"
        echo "   2. Update CORS in backend to allow your Vercel URL"
        echo "   3. Run document ingestion on production"
        ;;

    4)
        echo ""
        echo "📋 Manual Deployment Commands"
        echo "=============================="
        echo ""
        echo "BACKEND (Railway):"
        echo "------------------"
        echo "cd backend"
        echo "railway login"
        echo "railway init"
        echo "railway up"
        echo "railway open  # Set environment variables"
        echo ""
        echo "FRONTEND (Vercel):"
        echo "------------------"
        echo "cd frontend"
        echo "vercel login"
        echo "vercel --prod"
        echo ""
        echo "ENVIRONMENT VARIABLES:"
        echo "----------------------"
        echo "Backend (Railway):"
        echo "  - GOOGLE_API_KEY"
        echo "  - CHROMA_PERSIST_DIRECTORY=./chroma_db"
        echo "  - TEMPERATURE=0.7"
        echo ""
        echo "Frontend (Vercel):"
        echo "  - NEXT_PUBLIC_API_URL=https://your-backend.railway.app"
        echo ""
        ;;

    5)
        echo "Goodbye!"
        exit 0
        ;;

    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "📚 For detailed instructions, see DEPLOYMENT-GUIDE.md"
echo "✅ For a complete checklist, see DEPLOY-CHECKLIST.md"
echo ""
echo "Happy deploying! 🚀"
