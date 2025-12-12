# ⚡ SIMPLE STEPS - Bas 3 Commands

## Option 1: GitHub CLI se (Recommended)

### Step 1: GitHub CLI Install Karo (Ek baar)

**Terminal mein yeh run karo:**
```bash
brew install gh
```

**Agar Homebrew nahi hai, pehle yeh:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: GitHub Login Karo

```bash
gh auth login
```

Browser khulega - GitHub pe login karo aur authorize karo.

### Step 3: Repo Create aur Push Karo

```bash
cd "/Users/infinity/Desktop/customer churn"
gh repo create churn-intelligence-platform --public --source=. --remote=origin --push
```

**✅ Done!** Repo create ho gaya aur code push ho gaya!

---

## Option 2: Manual (Agar CLI nahi chahiye)

### Step 1: GitHub pe Repo Banao
1. https://github.com/new
2. Name: `churn-intelligence-platform`
3. **Public** rakho
4. Create karo

### Step 2: URL Copy Karo
GitHub pe jo URL dikhega wo copy karo:
```
https://github.com/YOUR_USERNAME/churn-intelligence-platform.git
```

### Step 3: Push Karo

```bash
cd "/Users/infinity/Desktop/customer churn"
git remote add origin https://github.com/YOUR_USERNAME/churn-intelligence-platform.git
git push -u origin main
```

**✅ Done!**

---

## Phir Streamlit Cloud Pe:

1. https://share.streamlit.io
2. GitHub se sign in
3. New app → Repo select karo
4. Main file: `app/streamlit_app.py`
5. Deploy

**🎉 Live!**

---

## 🚀 FASTEST: Option 1 (GitHub CLI)

Bas 3 commands:
```bash
brew install gh
gh auth login
cd "/Users/infinity/Desktop/customer churn" && gh repo create churn-intelligence-platform --public --source=. --remote=origin --push
```

Done! 🎉

