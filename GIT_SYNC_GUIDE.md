# Git Sync Guide - Never Face Divergent Branches Again!

## 🛡️ Protection Against Divergent Branches

We've configured Git to automatically handle divergent branches using merge strategy instead of rebase, preventing those confusing error messages.

## 🚀 Quick Commands

### Sync Current Branch
```bash
git sync
# or
python3 scripts/git-sync-helper.py
```

### Sync All Branches
```bash
git sync-all
# or
python3 scripts/git-sync-helper.py --all
```

### Regular Git Pull (now safe)
```bash
git pull
# Will automatically merge instead of failing
```

## 🔧 What We've Configured

1. **`pull.rebase = false`**
   - Uses merge strategy instead of rebase
   - Prevents "divergent branches" errors

2. **`pull.ff = true`**
   - Allows fast-forward when possible
   - Keeps history clean when there are no conflicts

3. **`merge.conflictstyle = diff3`**
   - Shows better conflict markers
   - Easier to resolve conflicts

4. **`core.autocrlf = input`**
   - Handles line endings properly
   - Prevents issues between Windows/Mac/Linux

5. **`push.default = current`**
   - Pushes current branch by default
   - No need to specify branch name

## 📋 Common Scenarios

### Scenario 1: Normal Development
```bash
# Make changes
git add .
git commit -m "feat: new feature"

# Sync with remote
git sync

# Push changes
git push
```

### Scenario 2: After Manual GitHub Edits
```bash
# You edited files on GitHub website
# Now sync locally
git sync
# Everything merges automatically!
```

### Scenario 3: Divergent Branches
```bash
# If branches diverged (local and remote have different commits)
git sync
# Automatically handles the merge
```

### Scenario 4: Complete Repository Sync
```bash
# Sync all three branches at once
git sync-all
# Switches between branches and syncs each
```

## 🆘 Troubleshooting

### If you get merge conflicts:
```bash
# The sync script will show conflicts
# Fix them manually, then:
git add .
git commit -m "fix: resolve conflicts"
git push
```

### Force sync to remote version:
```bash
# WARNING: This discards local changes
git fetch origin
git reset --hard origin/$(git branch --show-current)
```

### Check sync status:
```bash
# See if you're ahead/behind
git status -sb
```

## 🎯 Best Practices

1. **Always sync before starting work**
   ```bash
   git sync
   ```

2. **Sync after GitHub web edits**
   ```bash
   git sync
   ```

3. **Use sync instead of pull**
   ```bash
   git sync  # Better than git pull
   ```

4. **Keep all branches updated**
   ```bash
   git sync-all  # Weekly maintenance
   ```

## ✅ You're Protected!

With these configurations:
- ❌ No more "divergent branches" errors
- ❌ No more failed pulls
- ✅ Automatic merge handling
- ✅ Safe synchronization
- ✅ Clear conflict resolution

Just use `git sync` and never worry about Git errors again! 🎉