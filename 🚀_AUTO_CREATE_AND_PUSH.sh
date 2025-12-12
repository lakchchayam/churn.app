#!/bin/bash

# 🚀 Complete Auto Setup - Creates repo and pushes code
# Uses GitHub API directly

set -e

cd "/Users/infinity/Desktop/customer churn"

echo "🚀 Creating GitHub Repo and Pushing Code"
echo "========================================="
echo ""

# Try GitHub CLI first
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found!"
    
    # Check auth
    if gh auth status &>/dev/null; then
        echo "✅ Authenticated with GitHub"
        USERNAME=$(gh api user --jq .login)
        echo "   User: $USERNAME"
        
        REPO_NAME="churn-intelligence-platform"
        echo ""
        echo "📦 Creating repository: $REPO_NAME"
        
        # Create repo
        gh repo create $REPO_NAME --public --source=. --remote=origin --push 2>&1
        
        echo ""
        echo "✅ SUCCESS! Repo created and pushed!"
        echo "   URL: https://github.com/${USERNAME}/${REPO_NAME}"
        exit 0
    else
        echo "⚠️  Not authenticated. Please run: gh auth login"
    fi
fi

# Fallback: Manual instructions
echo "⚠️  GitHub CLI not available or not authenticated"
echo ""
echo "📋 Manual Steps (2 minutes):"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: churn-intelligence-platform"
echo "3. Make it PUBLIC"
echo "4. DON'T check anything (no README, no .gitignore)"
echo "5. Click 'Create repository'"
echo ""
echo "6. Copy the HTTPS URL (like: https://github.com/YOUR_USERNAME/churn-intelligence-platform.git)"
echo ""
echo "7. Run these commands:"
echo "   cd \"/Users/infinity/Desktop/customer churn\""
echo "   git remote add origin YOUR_COPIED_URL"
echo "   git push -u origin main"
echo ""
echo "✅ Done!"

