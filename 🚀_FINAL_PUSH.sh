#!/bin/bash

# 🚀 Final Push Script - Works without GitHub CLI

set -e

cd "/Users/infinity/Desktop/customer churn"

echo "🚀 Churn Intelligence Platform - Final Push"
echo "============================================="
echo ""

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ Remote already set: $REMOTE_URL"
    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main
    echo ""
    echo "✅ Successfully pushed!"
    echo ""
    echo "🌐 Next: Deploy on Streamlit Cloud"
    echo "   1. https://share.streamlit.io"
    echo "   2. Sign in with GitHub"
    echo "   3. New app → Select your repo"
    echo "   4. Main file: app/streamlit_app.py"
    echo "   5. Deploy"
else
    echo "⚠️  No GitHub remote found!"
    echo ""
    echo "Please create GitHub repo first:"
    echo "   1. Go to: https://github.com/new"
    echo "   2. Name: churn-intelligence-platform"
    echo "   3. Make it Public"
    echo "   4. Create repository"
    echo ""
    echo "Then run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/churn-intelligence-platform.git"
    echo "   git push -u origin main"
    echo ""
    echo "Or run this script again after adding remote"
fi

