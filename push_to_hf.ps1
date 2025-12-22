# Automated Push to Hugging Face
# Usage: .\push_to_hf.ps1 "Your commit message"

param(
    [string]$CommitMessage = "Update AgriSensa"
)

Write-Host "🚀 AgriSensa - Automated Push to Hugging Face" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check git status
Write-Host "📊 Checking git status..." -ForegroundColor Yellow
git status --short

# Add all changes
Write-Host ""
Write-Host "➕ Adding changes..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host ""
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m $CommitMessage

# Push to GitHub
Write-Host ""
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

# Upload to Hugging Face using API (to bypass binary file restrictions)
Write-Host ""
Write-Host "⬆️  Uploading to Hugging Face using API..." -ForegroundColor Yellow
python push_to_hf_api.py

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Push completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Deployment URLs:" -ForegroundColor Cyan
Write-Host "   GitHub: https://github.com/yandri918/agriisensa" -ForegroundColor White
Write-Host "   Hugging Face: https://huggingface.co/spaces/yandri918/agrisensa-api" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Hugging Face Space will rebuild automatically (may take 2-3 minutes)" -ForegroundColor Yellow
