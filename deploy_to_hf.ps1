Write-Host "🚀 Preparing to deploy to Hugging Face Spaces..." -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git repository not found. Initializing..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for Hugging Face deployment"
}
else {
    git add .
    git commit -m "Prepare for Hugging Face deployment"
}

# Ask for Space name
$SpaceName = Read-Host "Enter your Hugging Face Space name (e.g., username/space-name)"

if ([string]::IsNullOrWhiteSpace($SpaceName)) {
    Write-Host "❌ Space name is required." -ForegroundColor Red
    exit 1
}

# Add remote
Write-Host "🔗 Adding remote for $SpaceName..." -ForegroundColor Cyan
if (git remote | Select-String "hf") { 
    git remote remove hf 
}
git remote add hf "https://huggingface.co/spaces/$SpaceName"

# Push
Write-Host "⬆️ Pushing to Hugging Face..." -ForegroundColor Cyan
Write-Host "Note: You may be asked for your Hugging Face username and token (password)." -ForegroundColor Yellow
git push hf main --force

Write-Host "✅ Deployment command finished. Check your Space URL!" -ForegroundColor Green
