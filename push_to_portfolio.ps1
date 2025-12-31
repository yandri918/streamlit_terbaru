# Automated script to push notebooks to portfolio repository
# Run this script to automatically setup and push to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Data Science Portfolio - GitHub Push" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Clone repository
Write-Host "[1/5] Cloning portfolio repository..." -ForegroundColor Yellow
cd C:\Users\yandr\OneDrive\Desktop
if (Test-Path "portofolio_data_science") {
    Write-Host "Repository already exists, pulling latest..." -ForegroundColor Green
    cd portofolio_data_science
    git pull
} else {
    git clone https://github.com/yandri918/portofolio_data_science.git
    cd portofolio_data_science
}

# Step 2: Copy notebooks
Write-Host ""
Write-Host "[2/5] Copying notebooks..." -ForegroundColor Yellow
Copy-Item -Path "..\agrisensa-api\notebooks\*" -Destination "." -Recurse -Force
Write-Host "Files copied successfully!" -ForegroundColor Green

# Step 3: List files
Write-Host ""
Write-Host "[3/5] Files to be pushed:" -ForegroundColor Yellow
Get-ChildItem | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor White }

# Step 4: Git add and commit
Write-Host ""
Write-Host "[4/5] Adding and committing files..." -ForegroundColor Yellow
git add .
git commit -m "Add Data Science portfolio: Soil Analysis (EDA), Yield Prediction (ML & SHAP), Price Forecasting (Time Series)"

# Step 5: Push to GitHub
Write-Host ""
Write-Host "[5/5] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ SUCCESS! Portfolio pushed to GitHub" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "View your portfolio at:" -ForegroundColor White
Write-Host "https://github.com/yandri918/portofolio_data_science" -ForegroundColor Cyan
Write-Host ""
