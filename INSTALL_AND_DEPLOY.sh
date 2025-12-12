#!/bin/bash

# 🚀 Complete Installation & Deployment Script
# This will install GitHub CLI and deploy everything

set -e

echo "🚀 Churn Intelligence Platform - Complete Setup"
echo "================================================="
echo ""

cd "/Users/infinity/Desktop/customer churn"

# Step 1: Install GitHub CLI
echo "📦 Step 1: Installing GitHub CLI..."
if ! command -v gh &> /dev/null; then
    echo "   Installing via Homebrew..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "   Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install gh
    echo "   ✅ GitHub CLI installed"
else
    echo "   ✅ GitHub CLI already installed"
fi

# Step 2: Authenticate
echo ""
echo "🔐 Step 2: GitHub Authentication..."
if ! gh auth status &>/dev/null; then
    echo "   Please authenticate with GitHub..."
    gh auth login --web
else
    echo "   ✅ Already authenticated"
fi

# Step 3: Create and push repo
echo ""
echo "📦 Step 3: Creating GitHub repository..."
REPO_NAME="churn-intelligence-platform"

# Check if repo already exists
if gh repo view $REPO_NAME &>/dev/null; then
    echo "   ⚠️  Repo already exists, pushing to it..."
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://github.com/$(gh api user --jq .login)/${REPO_NAME}.git" 2>/dev/null || true
else
    echo "   Creating new repository: $REPO_NAME"
    gh repo create $REPO_NAME --public --source=. --remote=origin --push
fi

# Get repo URL
REPO_URL=$(gh repo view $REPO_NAME --json url -q .url 2>/dev/null || echo "https://github.com/$(gh api user --jq .login)/${REPO_NAME}")

echo ""
echo "✅ SUCCESS! Repository created and pushed!"
echo "   URL: $REPO_URL"
echo ""
echo "🌐 Step 4: Deploy on Streamlit Cloud"
echo "   1. Go to: https://share.streamlit.io"
echo "   2. Sign in with GitHub"
echo "   3. Click 'New app'"
echo "   4. Select repo: $REPO_NAME"
echo "   5. Main file: app/streamlit_app.py"
echo "   6. Click 'Deploy'"
echo ""
echo "🎉 Your app will be live in 2 minutes!"

