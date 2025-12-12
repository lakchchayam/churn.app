# 🚀 Render pe Deploy Kaise Kare

## Step 1: GitHub pe Push Karo

```bash
cd "/Users/infinity/Desktop/customer churn"
git init
git add .
git commit -m "Churn Intelligence Platform - Ready for Render"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

## Step 2: Render Account Banao

1. [render.com](https://render.com) pe jao
2. GitHub se sign up/login karo
3. **"New +"** → **"Web Service"** click karo
4. Apna GitHub repo select karo

## Step 3: Render Configuration

Render automatically `render.yaml` detect kar lega. Bas yeh set karo:

- **Name**: `churn-intelligence-api` (ya kuch bhi)
- **Environment Variables**:
  - `PYTHONPATH` = `.`
  - `OPENAI_API_KEY` = `your-key` (optional, LLM ke liye)

## Step 4: Deploy

Click **"Create Web Service"** - 5 minutes mein deploy ho jayega!

## Step 5: Model Train Karo

Deploy ke baad, Render shell mein jao ya locally train karke model upload karo:

```bash
python src/train.py --input data/sample_customers.csv --model models/churn_model.pkl --metrics metrics.json
```

Phir `models/churn_model.pkl` file ko git mein commit karo ya Render file system pe upload karo.

## ✅ Done!

Tumhara app live hoga: `https://your-app-name.onrender.com`

**Features:**
- ✅ Free tier (750 hours/month)
- ✅ Auto HTTPS
- ✅ Auto-deploy on git push
- ✅ Web UI + API dono ek saath

## Recruiter ko Dene ke Liye

Bas yeh link share karo: `https://your-app-name.onrender.com`

UI mein already explanation hai ki kya use case hai aur kaha deploy kiya hai!

