# 🔗 GitHub Setup (One-Time)

## Step 1: Create GitHub Repo

1. Go to: https://github.com/new
2. Repository name: `churn-intelligence-platform` (ya kuch bhi)
3. Description: `ML + LLM powered Customer Churn Prediction Platform`
4. Make it **Public** (for free hosting)
5. **DON'T** initialize with README (we already have files)
6. Click **"Create repository"**

## Step 2: Copy Repo URL

After creating, GitHub will show you a URL like:
```
https://github.com/YOUR_USERNAME/churn-intelligence-platform.git
```

Copy this URL!

## Step 3: Run This Command

```bash
cd "/Users/infinity/Desktop/customer churn"
git remote add origin YOUR_COPIED_URL_HERE
git push -u origin main
```

## Step 4: Deploy on Render

After GitHub push succeeds:
1. Go to https://render.com
2. Sign up with GitHub
3. **New +** → **Web Service**
4. Select your repo
5. Render auto-detects `render.yaml`
6. Add env var: `PYTHONPATH` = `.`
7. Click **Create**

Done! 🎉

