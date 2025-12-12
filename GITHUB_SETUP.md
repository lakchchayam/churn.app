# 🔗 GitHub Repo Setup - Step by Step

## Problem: Streamlit Cloud pe repo nahi dikh rahi

## Solution: GitHub repo banao aur push karo

### Step 1: GitHub pe Repo Banao

1. **Jao**: https://github.com/new
2. **Repository name**: `churn-intelligence-platform`
3. **Description**: `ML + LLM Customer Churn Prediction Platform`
4. **Public** select karo (important!)
5. **DON'T** check "Add a README file"
6. **DON'T** check "Add .gitignore"
7. **DON'T** check "Choose a license"
8. **Click**: "Create repository"

### Step 2: Repo URL Copy Karo

After creating, GitHub will show you a page with commands. 
**Copy the HTTPS URL** - it will look like:
```
https://github.com/YOUR_USERNAME/churn-intelligence-platform.git
```

### Step 3: Terminal mein yeh commands run karo

```bash
cd "/Users/infinity/Desktop/customer churn"
git remote add origin https://github.com/YOUR_USERNAME/churn-intelligence-platform.git
git branch -M main
git push -u origin main
```

**Note**: Agar `git remote add` error de to pehle yeh try karo:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/churn-intelligence-platform.git
```

### Step 4: Verify

GitHub pe jao: `https://github.com/YOUR_USERNAME/churn-intelligence-platform`
- Files dikhni chahiye
- `app/streamlit_app.py` hona chahiye
- `models/churn_model.pkl` hona chahiye

### Step 5: Streamlit Cloud pe Deploy

1. **Jao**: https://share.streamlit.io
2. **Sign in** with GitHub (same account)
3. **New app** click karo
4. Ab repo dikhegi! Select karo
5. **Main file path**: `app/streamlit_app.py`
6. **Deploy** click karo

## ✅ Done!

---

## Troubleshooting

**Agar push error aaye:**
```bash
# Check if remote is set
git remote -v

# If wrong, remove and add again
git remote remove origin
git remote add origin YOUR_URL

# Try push again
git push -u origin main
```

**Agar authentication error aaye:**
- GitHub pe Personal Access Token banao
- Password ki jagah token use karo

**Agar repo private hai:**
- Streamlit Cloud free tier pe private repos nahi support karta
- Repo ko Public karo

