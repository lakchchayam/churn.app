# 🔧 GitHub CLI Fix

## Problem: `gh: command not found`

## Solution:

### Option 1: PATH Add Karo (Quick)

Terminal mein yeh run karo:

```bash
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
gh auth login
```

### Option 2: Find GitHub CLI Location

```bash
# Check common locations
ls -la /usr/local/bin/gh
ls -la /opt/homebrew/bin/gh
ls -la ~/.local/bin/gh

# Find where it's installed
find /usr -name "gh" 2>/dev/null
find /opt -name "gh" 2>/dev/null
```

### Option 3: Reinstall GitHub CLI

```bash
# Via Homebrew
brew install gh

# Or download from: https://cli.github.com/
```

### Option 4: Manual Setup (Agar CLI nahi chahiye)

GitHub web se repo banao aur manually push karo:

```bash
cd "/Users/infinity/Desktop/customer churn"

# 1. GitHub pe repo banao: https://github.com/new
# 2. URL copy karo
# 3. Push karo:
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

---

## After GitHub CLI Works:

```bash
cd "/Users/infinity/Desktop/customer churn"
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
gh auth login
gh repo create churn-intelligence-platform --public --source=. --remote=origin --push
```

