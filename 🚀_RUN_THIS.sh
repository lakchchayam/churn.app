#!/bin/bash

# 🚀 Complete GitHub Setup Script
# Terminal mein yeh script run karo

set -e

echo "🚀 Churn Intelligence Platform - GitHub Setup"
echo "=============================================="
echo ""

cd "/Users/infinity/Desktop/customer churn"

# Add common GitHub CLI paths
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

# Check if GitHub CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found in PATH"
    echo ""
    echo "Please do ONE of these:"
    echo "1. Restart terminal completely"
    echo "2. Or run: export PATH=\"/usr/local/bin:/opt/homebrew/bin:\$PATH\""
    echo "3. Then run this script again"
    exit 1
fi

echo "✅ GitHub CLI found: $(gh --version | head -1)"
echo ""

# Check authentication
if gh auth status &>/dev/null; then
    echo "✅ Already authenticated with GitHub"
    USERNAME=$(gh api user --jq .login)
    echo "   Logged in as: $USERNAME"
else
    echo "🔐 GitHub authentication required..."
    echo "   Browser will open - please login and authorize"
    gh auth login --web --hostname github.com
fi

echo ""
echo "📦 Creating GitHub repository..."
REPO_NAME="churn-intelligence-platform"

# Check if repo exists
if gh repo view $REPO_NAME &>/dev/null 2>&1; then
    echo "⚠️  Repo already exists, pushing to it..."
    git remote remove origin 2>/dev/null || true
    USERNAME=$(gh api user --jq .login)
    git remote add origin "https://github.com/${USERNAME}/${REPO_NAME}.git" 2>/dev/null || true
    git push -u origin main
else
    echo "   Creating new repository: $REPO_NAME"
    gh repo create $REPO_NAME --public --source=. --remote=origin --push
fi

# Get repo URL
USERNAME=$(gh api user --jq .login)
REPO_URL="https://github.com/${USERNAME}/${REPO_NAME}"

echo ""
echo "✅ SUCCESS! Repository created and pushed!"
echo "   URL: $REPO_URL"
echo ""
echo "🌐 Next: Deploy on Streamlit Cloud"
echo "   1. Go to: https://share.streamlit.io"
echo "   2. Sign in with GitHub"
echo "   3. Click 'New app'"
echo "   4. Select repo: $REPO_NAME"
echo "   5. Main file: app/streamlit_app.py"
echo "   6. Click 'Deploy'"
echo ""
echo "🎉 Your app will be live in 2 minutes!"

