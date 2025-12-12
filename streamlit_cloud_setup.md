# 🚀 Streamlit Cloud - EASIEST DEPLOYMENT

## Why Streamlit Cloud?
- ✅ **Easiest** - Just connect GitHub repo
- ✅ **Free** - Unlimited apps
- ✅ **Auto-deploy** - Push to GitHub = auto deploy
- ✅ **No config needed** - Just works!

## Steps (5 minutes):

### 1. Push to GitHub
```bash
cd "/Users/infinity/Desktop/customer churn"
# Create repo at github.com/new (name: churn-intelligence)
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo
5. Main file path: `app/streamlit_app.py`
6. Click **"Deploy"**

### 3. Done! 🎉
Your app is live at: `https://your-app-name.streamlit.app`

**That's it! No config, no env vars needed (unless you want LLM).**

---

## For LLM Explanations (Optional):
In Streamlit Cloud → Settings → Secrets:
```
OPENAI_API_KEY = your-key-here
```

