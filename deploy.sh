#!/bin/bash

# Churn Intelligence Platform - Auto Deploy Script
# Run this after creating GitHub repo

set -e

echo "🚀 Churn Intelligence Platform - Deployment Script"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
fi

# Check if model exists
if [ ! -f "models/churn_model.pkl" ]; then
    echo "⚠️  Model not found. Training model first..."
    source .venv/bin/activate 2>/dev/null || python3 -m venv .venv && source .venv/bin/activate
    pip install -q -r requirements.txt
    PYTHONPATH=. python src/train.py --input data/sample_customers.csv --model models/churn_model.pkl --metrics metrics.json
    echo "✅ Model trained successfully"
fi

# Stage all files
echo "📝 Staging files..."
git add .

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ Remote already set: $REMOTE_URL"
else
    echo ""
    echo "⚠️  No GitHub remote found!"
    echo ""
    echo "Please create a GitHub repo first:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository (name: churn-intelligence)"
    echo "3. Copy the repo URL"
    echo "4. Run: git remote add origin YOUR_REPO_URL"
    echo "5. Then run this script again"
    exit 1
fi

# Commit if there are changes
if [ -n "$(git status --porcelain)" ]; then
    echo "💾 Committing changes..."
    git commit -m "Churn Intelligence Platform - Ready for Render deployment" || echo "No changes to commit"
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main || {
    echo "❌ Push failed. Make sure:"
    echo "   - GitHub repo exists"
    echo "   - You have write access"
    echo "   - Remote URL is correct"
    exit 1
}

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "📋 Next Steps for Render:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your repository"
echo "5. Render will auto-detect render.yaml"
echo "6. Add environment variable: PYTHONPATH = ."
echo "7. Click 'Create Web Service'"
echo ""
echo "🎉 Your app will be live at: https://your-app-name.onrender.com"

