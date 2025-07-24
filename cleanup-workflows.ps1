# PowerShell script to clean up GitHub Actions workflows

Write-Host "🧹 Cleaning up GitHub Actions workflows..." -ForegroundColor Blue

# Remove any .github directory and its contents
if (Test-Path ".github") {
    Write-Host "🗑️  Removing .github directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".github"
    Write-Host "✅ .github directory removed" -ForegroundColor Green
} else {
    Write-Host "✅ No .github directory found" -ForegroundColor Green
}

# Check for any workflow files in the repository
$workflowFiles = Get-ChildItem -Recurse -Include "*.yml", "*.yaml" | Where-Object { $_.FullName -like "*workflow*" -or $_.FullName -like "*action*" }
if ($workflowFiles) {
    Write-Host "🗑️  Removing workflow files..." -ForegroundColor Yellow
    foreach ($file in $workflowFiles) {
        Write-Host "   Removing: $($file.Name)" -ForegroundColor Gray
        Remove-Item $file.FullName -Force
    }
    Write-Host "✅ Workflow files removed" -ForegroundColor Green
} else {
    Write-Host "✅ No workflow files found" -ForegroundColor Green
}

# Add all changes to git
Write-Host "📝 Adding changes to git..." -ForegroundColor Blue
git add -A

# Check if there are any changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Committing changes..." -ForegroundColor Blue
    git commit -m "remove: all GitHub Actions workflows and configuration files"
    Write-Host "✅ Changes committed" -ForegroundColor Green
    
    Write-Host "📤 Pushing to remote..." -ForegroundColor Blue
    git push origin testing
    Write-Host "✅ Changes pushed to remote" -ForegroundColor Green
} else {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
}

Write-Host "`n🎉 Workflow cleanup completed!" -ForegroundColor Green
Write-Host "The unwanted workflows should now be removed from GitHub Actions." -ForegroundColor Cyan 