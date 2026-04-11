# Vercel Redeploy Guide - Traceability Module

## Problem
QR code scans correctly but Vercel shows default data instead of actual product data.

## Root Cause
Vercel is not auto-deploying when code is pushed to GitHub, or is using cached version.

## Solution Steps

### Option 1: Manual Redeploy (Recommended)
1. Go to https://vercel.com/dashboard
2. Find project: **vercel-scan2** (or similar name)
3. Click **"Deployments"** tab
4. Find the latest deployment
5. Click **"..."** menu → **"Redeploy"**
6. Wait 2-3 minutes for deployment to complete
7. Test the product link again

### Option 2: Check Auto-Deploy Settings
1. Go to project **Settings** → **Git**
2. Ensure **"Production Branch"** is set to `main`
3. Ensure **"Auto Deploy"** is enabled
4. Save changes if modified

### Option 3: Trigger Deploy via Git
1. Make a small change to trigger rebuild:
   ```bash
   cd agrisensa-vercel-api
   git commit --allow-empty -m "trigger deploy"
   git push origin main
   ```
2. Wait 3-5 minutes
3. Check Vercel dashboard for new deployment

### Option 4: Check Build Logs
1. Go to **Deployments** tab
2. Click on latest deployment
3. Check **"Build Logs"** for errors
4. Common issues:
   - Missing dependencies in requirements.txt
   - Python version mismatch
   - Import errors

## Verification
After redeploy, test with this URL:
```
https://vercel-scan2.vercel.app/product/eyJpZCI6IkFHUkktMjAyNTEyMjQtNTYxIiwibiI6IkJlcmFzIChQYW5kYW4gV2FuZ2kvUm9qb2xlbGUpIiwidiI6IkNpYW5qdXIgUGFuZGFuIFdhbmdpIChHcmFkZSBBKSIsImYiOiJHYXBva3RhbiBTZWphaHRlcmEiLCJsIjoiQmFueXVtYXMsIEphd2EgVGVuZ2FoIiwiZCI6IjIwMjUtMTItMjQiLCJ3IjoiMSBrZyIsImUiOiJcdWQ4M2NcdWRmM2UiLCJwIjoiNTAwMDAiLCJjIjp7InQiOiIyNC41IiwiaCI6Ijc1IiwicyI6IjExLjUifSwibSI6W3siZGF0ZSI6IjIwMjUtMTItMjQiLCJ0aW1lIjoiMDg6MzAiLCJldmVudCI6IlBhbmVuIChIYXJ2ZXN0aW5nKSIsImxvYyI6IkJhbnl1bWFzLCBKYXdhIFRlbmdhaCIsImljb24iOiJcdWQ4M2NcdWRmM2UifSx7ImRhdGUiOiIyMDI1LTEyLTI0IiwidGltZSI6IjEwOjE1IiwiZXZlbnQiOiJTb3J0aXIgJiBHcmFkaW5nIChRQyAxKSIsImxvYyI6Ikd1ZGFuZyBTb3J0aXIiLCJpY29uIjoiXHVkODNkXHVkZDBkIn0seyJkYXRlIjoiMjAyNS0xMi0yNCIsInRpbWUiOiIxMzowMCIsImV2ZW50IjoiUGFja2FnaW5nICYgTGFiZWxpbmciLCJsb2MiOiJQcm9jZXNzaW5nIEhvdXNlIiwiaWNvbiI6Ilx1ZDgzZFx1ZGNlNiJ9XX0
```

**Expected Result:**
- Name: **Beras (Pandan Wangi/Rojolele)** (not "Produk AgriSensa")
- Farmer: **Gapoktan Sejahtera** (not "Petani Indonesia")
- Location: **Banyumas, Jawa Tengah** (not "Indonesia")
- Date: **2025-12-24** (not "N/A")
- **Climate Proof section** with temperature, humidity, sun hours
- **Journey Timeline** with 3 milestones

## Latest Code Status
- Repository: https://github.com/yandri918/vercel_scan
- Latest commit: `3d0b53e` - "Ensure decoded data always overrides defaults"
- All code fixes are complete and pushed
- Issue is purely deployment/cache related

## Contact
If manual redeploy doesn't work, check Vercel build logs for specific errors.
