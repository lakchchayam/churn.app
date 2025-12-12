#!/bin/bash

# 🚀 Complete Auto-Deploy Script for Churn Intelligence Platform
# This script does EVERYTHING possible automatically

set -e

echo "🚀 Churn Intelligence Platform - Auto Deploy"
echo "============================================"
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found!"
    
    # Check if logged in
    if gh auth status &>/dev/null; then
        echo "✅ GitHub authenticated"
        
        # Create repo
        REPO_NAME="churn-intelligence-platform"
        echo "📦 Creating GitHub repository: $REPO_NAME"
        
        gh repo create $REPO_NAME --public --source=. --remote=origin --push 2>&1 || {
            echo "⚠️  Repo might already exist or need manual creation"
            echo "Continuing with manual steps..."
        }
    else
        echo "⚠️  GitHub CLI not authenticated"
        echo "Run: gh auth login"
    fi
else
    echo "⚠️  GitHub CLI not installed"
    echo "Installing via Homebrew..."
    
    if command -v brew &> /dev/null; then
        brew install gh
        echo "✅ GitHub CLI installed"
        echo "Please run: gh auth login"
        echo "Then run this script again"
        exit 1
    else
        echo "❌ Homebrew not found"
        echo "Please install GitHub CLI manually or create repo via web"
    fi
fi

# If we have a remote, push
if git remote get-url origin >/dev/null 2>&1; then
    echo ""
    echo "⬆️  Pushing to GitHub..."
    git push -u origin main || {
        echo "⚠️  Push failed - might need to set remote manually"
    }
else
    echo ""
    echo "📋 Manual Steps Required:"
    echo "1. Create repo at: https://github.com/new"
    echo "2. Name: churn-intelligence-platform"
    echo "3. Copy the repo URL"
    echo "4. Run: git remote add origin YOUR_URL"
    echo "5. Run: git push -u origin main"
fi

echo ""
echo "✅ Git setup complete!"
echo ""
echo "📋 Next: Deploy on Render"
echo "1. Go to: https://render.com"
echo "2. Sign up with GitHub"
echo "3. New + → Web Service"
echo "4. Select your repo"
echo "5. Render auto-detects render.yaml"
echo "6. Add env: PYTHONPATH = ."
echo "7. Create Web Service"
echo ""
echo "🎉 Your app will be live in 5 minutes!"

