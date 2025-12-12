#!/bin/bash

# 🚀 Complete Auto-Deploy Script
# This will create GitHub repo and push everything automatically

set -e

echo "🚀 Churn Intelligence Platform - Auto Deploy"
echo "=============================================="
echo ""

cd "/Users/infinity/Desktop/customer churn"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "📦 Installing GitHub CLI..."
    
    # Try to install via Homebrew
    if command -v brew &> /dev/null; then
        brew install gh
    else
        echo "❌ Homebrew not found."
        echo "Please install GitHub CLI manually:"
        echo "  brew install gh"
        echo "  gh auth login"
        exit 1
    fi
fi

# Check authentication
if ! gh auth status &>/dev/null; then
    echo "🔐 GitHub authentication required..."
    echo "Please login to GitHub:"
    gh auth login --web
    echo ""
fi

# Create unique repo name
REPO_NAME="churn-intelligence-platform"
TIMESTAMP=$(date +%s)
UNIQUE_NAME="${REPO_NAME}-${TIMESTAMP}"

echo "📦 Creating GitHub repository..."
echo "   Name: $REPO_NAME"

# Try to create repo (if exists, use existing)
gh repo create $REPO_NAME --public --source=. --remote=origin --push 2>&1 || {
    echo "⚠️  Repo might already exist, trying to push to existing repo..."
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://github.com/$(gh api user --jq .login)/${REPO_NAME}.git" 2>/dev/null || true
    git push -u origin main || {
        echo "❌ Push failed. Please check:"
        echo "   1. Repo exists at: https://github.com/$(gh api user --jq .login)/${REPO_NAME}"
        echo "   2. You have write access"
        exit 1
    }
}

# Get repo URL
REPO_URL=$(gh repo view $REPO_NAME --json url -q .url 2>/dev/null || echo "https://github.com/$(gh api user --jq .login)/${REPO_NAME}")

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "   Repository: $REPO_URL"
echo ""
echo "🌐 Next: Deploy on Streamlit Cloud"
echo "   1. Go to: https://share.streamlit.io"
echo "   2. Sign in with GitHub"
echo "   3. New app → Select repo: $REPO_NAME"
echo "   4. Main file: app/streamlit_app.py"
echo "   5. Deploy"
echo ""
echo "🎉 Your app will be live at: https://your-app-name.streamlit.app"

