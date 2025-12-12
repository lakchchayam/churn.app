# 🔐 GitHub CLI Authentication

## Step 1: Terminal Restart Karo

GitHub CLI install ke baad terminal restart karo ya yeh run karo:

```bash
export PATH="/usr/local/bin:$PATH"
```

## Step 2: GitHub Login Karo

```bash
gh auth login
```

**Options mein select karo:**
1. **GitHub.com** select karo
2. **HTTPS** select karo
3. **Login with a web browser** select karo
4. Browser khulega - GitHub pe login karo
5. Code copy karke terminal mein paste karo

## Step 3: Verify

```bash
gh auth status
```

Agar "Logged in" dikhe to ✅ ready hai!

## Step 4: Repo Create aur Push

```bash
cd "/Users/infinity/Desktop/customer churn"
gh repo create churn-intelligence-platform --public --source=. --remote=origin --push
```

**✅ Done!** Repo create ho gaya aur code push ho gaya!

---

## Alternative: Agar CLI nahi chale

Manual steps follow karo: `⚡_SIMPLE_STEPS.md`

