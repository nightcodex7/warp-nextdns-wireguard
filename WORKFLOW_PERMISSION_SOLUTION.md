# Workflow Permission Solution Guide

**Author**: Tuhin Garai  
**Email**: 64925748+nightcodex7@users.noreply.github.com

## 🚨 Permanent Solution for Workflow Permission Errors

### The Error:
```
refusing to allow a GitHub App to create or update workflow `.github/workflows/` without `workflows` permission
```

### 🛠️ Solutions (Choose One):

## Option 1: Use Personal Access Token (Recommended)

1. **Create a Personal Access Token:**
   - Go to: https://github.com/settings/tokens/new
   - Name: `WARP-NextDNS-Workflow-Token`
   - Select scopes:
     - ✅ `repo` (all)
     - ✅ `workflow`
   - Click "Generate token"
   - Copy the token

2. **Clone with Token:**
   ```bash
   git remote set-url origin https://nightcodex7:YOUR_TOKEN@github.com/nightcodex7/warp-nextdns-wireguard.git
   ```

3. **Push Normally:**
   ```bash
   git push origin testing
   ```

## Option 2: GitHub CLI (gh)

1. **Install GitHub CLI:**
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   sudo apt update
   sudo apt install gh
   ```

2. **Authenticate:**
   ```bash
   gh auth login
   # Choose GitHub.com
   # Choose HTTPS
   # Authenticate with browser
   ```

3. **Push with gh:**
   ```bash
   gh repo sync
   ```

## Option 3: Direct GitHub Upload

1. **Export Workflows:**
   ```bash
   # Create a zip of workflows
   cd .github
   zip -r workflows.zip workflows/
   ```

2. **Upload via GitHub Web:**
   - Go to: https://github.com/nightcodex7/warp-nextdns-wireguard
   - Switch to `testing` branch
   - Navigate to `.github/`
   - Click "Add file" → "Upload files"
   - Upload the `workflows` folder

## Option 4: Use SSH Instead of HTTPS

1. **Generate SSH Key:**
   ```bash
   ssh-keygen -t ed25519 -C "64925748+nightcodex7@users.noreply.github.com"
   ```

2. **Add to GitHub:**
   - Copy: `cat ~/.ssh/id_ed25519.pub`
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste the key

3. **Change Remote to SSH:**
   ```bash
   git remote set-url origin git@github.com:nightcodex7/warp-nextdns-wireguard.git
   ```

## 🔧 Permanent Prevention

### 1. Add to `.gitconfig`:
```bash
git config --global user.name "Tuhin Garai"
git config --global user.email "64925748+nightcodex7@users.noreply.github.com"
```

### 2. Repository Settings:
- Go to: Settings → Actions → General
- Under "Workflow permissions":
  - ✅ Read and write permissions
  - ✅ Allow GitHub Actions to create and approve pull requests

### 3. Use the Bypass Script:
```bash
# For emergency workflow updates
python3 scripts/push-without-workflows.py
```

## ✅ Verification

After implementing any solution:
1. Check Actions tab: https://github.com/nightcodex7/warp-nextdns-wireguard/actions
2. All workflows should show ✅
3. No permission errors

## 📝 Important Notes

- Always use `64925748+nightcodex7@users.noreply.github.com` for commits
- This email ensures commits are linked to your GitHub account
- The workflow permission issue is a GitHub App limitation
- Personal Access Tokens provide the most reliable solution