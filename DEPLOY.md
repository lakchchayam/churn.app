# 🚀 Render Deployment Guide

## Quick Deploy Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Configure:
   - **Name**: `churn-intelligence-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.server:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `PYTHONPATH` = `.`
     - `OPENAI_API_KEY` = `your-key-here` (optional, for LLM explanations)

6. Click **"Create Web Service"**
7. Wait for deployment (~5 minutes)

### 3. Train Model Before First Use

After deployment, you need to train the model once. SSH into Render or use their shell:

```bash
# In Render shell or locally then upload model
python src/train.py --input data/sample_customers.csv --model models/churn_model.pkl
```

**OR** upload `models/churn_model.pkl` via Render's file system or add it to git.

### 4. Access Your App

Once deployed, your app will be live at:
- **Web UI**: `https://your-app-name.onrender.com/`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **Health Check**: `https://your-app-name.onrender.com/health`

## Features

✅ **Free Tier**: 750 hours/month (enough for always-on demo)
✅ **Auto-deploy**: Pushes to main branch auto-deploy
✅ **HTTPS**: Free SSL certificate
✅ **Custom Domain**: Add your own domain (optional)

## Troubleshooting

- **Model not found**: Train model first (see step 3)
- **Port issues**: Render sets `$PORT` automatically
- **CORS errors**: Already configured in `api/server.py`
- **Static files not loading**: Check `/static/` path in API

## Notes

- First deploy takes ~5 minutes
- Free tier spins down after 15 min inactivity (wakes up on next request)
- Model file (`churn_model.pkl`) should be committed to git or uploaded separately

