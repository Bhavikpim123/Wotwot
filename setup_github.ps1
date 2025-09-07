# GitHub Repository Setup Script
# Replace 'your-repo-name' with your actual repository name

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoName
)

Write-Host "Setting up GitHub repository: $RepoName" -ForegroundColor Green

# Add GitHub remote
git remote add origin "https://github.com/Bhavikpim123/$RepoName.git"

# Set main branch and push
git branch -M main
git push -u origin main

Write-Host "Successfully pushed to GitHub repository!" -ForegroundColor Green
Write-Host "Repository URL: https://github.com/Bhavikpim123/$RepoName" -ForegroundColor Cyan