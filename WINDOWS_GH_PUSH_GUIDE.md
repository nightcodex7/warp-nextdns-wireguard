# Windows GitHub CLI Push Guide

**Author**: Tuhin Garai  
**Email**: 64925748+nightcodex7@users.noreply.github.com

## 🪟 Using GitHub CLI (gh) from Windows PowerShell

Since you have `gh` configured on Windows PowerShell, you can push ALL files including workflows without permission issues!

## ✅ Quick Solution

### From Windows PowerShell:
```powershell
# 1. Open PowerShell in your project directory
cd C:\path\to\warp-nextdns-wireguard

# 2. Check gh is authenticated
gh auth status

# 3. Push everything including workflows
gh repo sync --branch testing
```

That's it! No workflow permission errors! 🎉

## 📄 Windows Scripts Created for You

### 1. **push-with-gh.bat** (Double-click to run)
- Double-click this file in Windows Explorer
- Automatically pushes all files including workflows
- Shows colored output and status

### 2. **push-with-gh.ps1** (PowerShell script)
```powershell
# Run in PowerShell:
.\push-with-gh.ps1
```

### 3. **scripts/push-with-gh.py** (Python script)
```bash
# Run from Git Bash or PowerShell:
python scripts/push-with-gh.py
```

## 🛠️ Complete Windows Setup (If Needed)

### 1. Install GitHub CLI on Windows
```powershell
# Using winget (Windows Package Manager)
winget install --id GitHub.cli

# Or using Chocolatey
choco install gh

# Or download from: https://cli.github.com/
```

### 2. Authenticate GitHub CLI
```powershell
# Run in PowerShell
gh auth login

# Select:
# - GitHub.com
# - HTTPS
# - Login with web browser
# - Authorize in browser
```

### 3. Verify Authentication
```powershell
gh auth status
# Should show: ✓ Logged in to github.com as nightcodex7
```

## 📝 Common Windows Commands

### Push Current Branch
```powershell
# Get current branch name
$branch = git branch --show-current

# Push with gh
gh repo sync --branch $branch
```

### Push Specific Branch
```powershell
# Push testing branch
gh repo sync --branch testing

# Push main branch
gh repo sync --branch main
```

### Check Repository Status
```powershell
# View repository info
gh repo view

# Check workflow runs
gh run list

# View specific workflow
gh workflow view
```

## 🚀 One-Line Solutions

### PowerShell One-Liner
```powershell
git add -A; git commit -m "Your message" --author="Tuhin Garai <64925748+nightcodex7@users.noreply.github.com>"; gh repo sync --branch (git branch --show-current)
```

### Command Prompt One-Liner
```cmd
git add -A && git commit -m "Your message" --author="Tuhin Garai <64925748+nightcodex7@users.noreply.github.com>" && gh repo sync --branch testing
```

## ✅ Benefits of Using gh on Windows

1. **No Workflow Permission Errors** - gh has full permissions
2. **Works in PowerShell** - Native Windows experience
3. **Colorful Output** - Better visibility
4. **Automatic Authentication** - Uses Windows credential manager
5. **Faster Than Git** - Optimized for GitHub

## 🔧 Troubleshooting

### If gh command not found:
```powershell
# Add to PATH manually
$env:Path += ";C:\Program Files\GitHub CLI"

# Or restart PowerShell after installation
```

### If authentication fails:
```powershell
# Clear and re-authenticate
gh auth logout
gh auth login
```

### If push fails:
```powershell
# Check status
gh auth status

# Refresh token
gh auth refresh

# Try with explicit repo
gh repo sync nightcodex7/warp-nextdns-wireguard --branch testing
```

## 📊 Verify Success

After pushing with gh:
1. Check Actions: https://github.com/nightcodex7/warp-nextdns-wireguard/actions
2. All workflows should be ✅ green
3. No permission errors!

---

**Remember**: Using `gh` from Windows PowerShell completely bypasses the workflow permission issue! 🎉