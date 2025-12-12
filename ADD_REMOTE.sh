#!/bin/bash

# Add GitHub remote and push

cd "/Users/infinity/Desktop/customer churn"

echo "🔗 GitHub Remote Setup"
echo "======================"
echo ""

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    echo "✅ Remote already set:"
    git remote -v
    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main
else
    echo "⚠️  No remote found!"
    echo ""
    echo "Please provide your GitHub repo URL"
    echo "Example: https://github.com/YOUR_USERNAME/churn-intelligence-platform.git"
    echo ""
    read -p "Enter GitHub repo URL: " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo "❌ No URL provided"
        exit 1
    fi
    
    echo ""
    echo "Adding remote..."
    git remote add origin "$REPO_URL"
    
    echo "Pushing to GitHub..."
    git push -u origin main
    
    echo ""
    echo "✅ Successfully pushed!"
fi

