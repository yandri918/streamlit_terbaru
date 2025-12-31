# Push Notebooks to GitHub Portfolio Repository

## Step-by-Step Instructions

### 1. Clone the Portfolio Repository

```powershell
# Navigate to Desktop
cd C:\Users\yandr\OneDrive\Desktop

# Clone your portfolio repository
git clone https://github.com/yandri918/portofolio_data_science.git

# Navigate into the repository
cd portofolio_data_science
```

### 2. Copy Notebooks to Portfolio Repository

```powershell
# Copy all notebooks and documentation
Copy-Item -Path "..\agrisensa-api\notebooks\*" -Destination "." -Recurse -Force

# Verify files copied
dir
```

### 3. Add and Commit Files

```powershell
# Add all files
git add .

# Commit with descriptive message
git commit -m "Add Data Science portfolio notebooks: Soil Analysis, Yield Prediction (ML & SHAP), Price Forecasting"

# Push to GitHub
git push origin main
```

### Alternative: If Repository Doesn't Exist Yet

If the repository is empty or doesn't exist:

```powershell
# Initialize git in notebooks folder
cd C:\Users\yandr\OneDrive\Desktop\agrisensa-api\notebooks

# Initialize git
git init

# Add remote
git remote add origin https://github.com/yandri918/portofolio_data_science.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: Data Science portfolio notebooks"

# Push
git branch -M main
git push -u origin main
```

### Files to be Pushed:

1. `1_Soil_Fertility_Analysis.ipynb` (27 KB)
2. `2_Yield_Prediction_Model.ipynb` (3.4 KB)
3. `3_Price_Forecasting_Analysis.ipynb` (3.5 KB)
4. `README.md` (3.7 KB)
5. `requirements.txt` (378 bytes)

### After Pushing:

Your portfolio will be available at:
**https://github.com/yandri918/portofolio_data_science**

### Recommended: Add GitHub README

Create a professional README.md in the root:

```markdown
# Data Science Portfolio - Agricultural Analytics

Professional Jupyter notebooks demonstrating Data Science expertise in agricultural domain.

## Notebooks

1. **Soil Fertility Analysis** - Statistical analysis & EDA
2. **Yield Prediction Model** - ML with SHAP explanations
3. **Price Forecasting** - Time series analysis

## Tech Stack

Python, pandas, scikit-learn, SHAP, statsmodels, plotly

## Author

Andriyanto - Agricultural Data Scientist
```

---

**Ready to push!** Just run the commands above in PowerShell.
