#!/bin/bash
set -e
echo "🚀 FINAL DEPLOYMENT - Churn Intelligence Platform"
echo "=================================================="

# Check GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "📦 Installing GitHub CLI..."
    if command -v brew &> /dev/null; then
        brew install gh
    else
        echo "❌ Homebrew not found. Please install GitHub CLI manually:"
        echo "   brew install gh"
        echo "   gh auth login"
        exit 1
    fi
fi

# Authenticate GitHub
if ! gh auth status &>/dev/null; then
    echo "🔐 GitHub authentication required..."
    echo "Please login to GitHub:"
    gh auth login
fi

# Create repo
REPO_NAME="churn-intelligence-platform-$(date +%s)"
echo "📦 Creating GitHub repository: $REPO_NAME"
gh repo create $REPO_NAME --public --source=. --remote=origin --push 2>&1

# Get repo URL
REPO_URL=$(gh repo view --json url -q .url)
echo ""
echo "✅ Repository created: $REPO_URL"
echo ""
echo "🌐 Now deploying on Render..."
echo "1. Go to: https://render.com"
echo "2. Sign up with GitHub"
echo "3. New + → Web Service"
echo "4. Select repo: $REPO_NAME"
echo "5. Add env: PYTHONPATH = ."
echo "6. Create Web Service"
echo ""
echo "🎉 Your app will be live in 5 minutes!"
