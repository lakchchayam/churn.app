# ⚡ Quick Start - Render Deploy

## 🎯 3 Simple Steps

### 1️⃣ GitHub pe Push
```bash
git init
git add .
git commit -m "Churn Intelligence Platform"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

### 2️⃣ Render pe Deploy
1. [render.com](https://render.com) → Sign up with GitHub
2. **New +** → **Web Service**
3. Connect repo → Auto-detects `render.yaml`
4. Add env var: `PYTHONPATH` = `.`
5. Click **Create** → Wait 5 min

### 3️⃣ Model Train Karo
Deploy ke baad, Render shell mein:
```bash
python src/train.py --input data/sample_customers.csv --model models/churn_model.pkl
```

**OR** locally train karke `models/churn_model.pkl` git mein commit karo.

## ✅ Done!

Live URL: `https://your-app.onrender.com`

**Recruiter ko bas yeh link share karo!** 🚀

---

## 📝 What's Included

- ✅ ML Churn Prediction
- ✅ LLM Explanations  
- ✅ Action Recommendations
- ✅ Beautiful Web UI
- ✅ What-If Simulator
- ✅ Free Hosting (Render)

