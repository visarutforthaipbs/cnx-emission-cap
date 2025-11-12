# Setup Guide for Automated Emission Cap Calculator

This guide will help you set up automated daily calculations and the public dashboard.

## 📋 Prerequisites

- A GitHub account
- Git installed on your local machine
- Python 3.7+ installed locally (for testing)

## 🚀 Setup Steps

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `cnx-emission-cap` or `chiang-mai-air-quality`
3. Make it **public** (required for GitHub Pages)
4. Don't initialize with README (we already have files)

### 2. Push Your Code to GitHub

Open terminal in the project directory and run:

```bash
cd /Users/visarutsankham/Desktop/CNX-CAP

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Emission cap calculator with dashboard"

# Add remote (replace YOUR-USERNAME and YOUR-REPO with your details)
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in left sidebar)
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. The dashboard will be available at: `https://YOUR-USERNAME.github.io/YOUR-REPO/`

### 4. Verify Automation

The daily automation will:

- Run automatically every day at 6:00 AM Bangkok time
- Fetch atmospheric data from Open-Meteo API
- Calculate the emission cap
- Save results to `emission_cap_result.json` and `data/historical_data.json`
- Commit the changes back to the repository
- Trigger dashboard update

To test immediately:

1. Go to **Actions** tab in your GitHub repository
2. Click **Daily Emission Cap Calculation** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for it to complete (~30 seconds)

### 5. View Your Dashboard

After the first workflow run:

1. Go to **Actions** tab → **Deploy Dashboard to GitHub Pages**
2. Wait for deployment to complete
3. Visit: `https://YOUR-USERNAME.github.io/YOUR-REPO/`

## 🔧 Customization

### Adjust Calculation Time

Edit `.github/workflows/daily-emission-cap.yml`:

```yaml
schedule:
  - cron: "0 23 * * *" # Change this (currently 6 AM Bangkok)
```

Cron format: `minute hour day month day-of-week` (in UTC)

### Modify Constants

Edit `emission_cap_calculator.py`:

```python
TARGET_CONCENTRATION = 37.5  # µg/m³
BASIN_AREA_KM2 = 1500  # km²
BASIN_LENGTH_KM = 80  # km
LATITUDE = 18.7883  # Chiang Mai
LONGITUDE = 98.9853
```

### Customize Dashboard

Edit `index.html`:

- Change colors in the `<style>` section
- Modify chart settings in the JavaScript section
- Add or remove cards/sections

## 📊 Data Files

- `emission_cap_result.json` - Latest calculation (detailed)
- `data/historical_data.json` - All daily results (simplified for charting)

## 🐛 Troubleshooting

### Workflow Fails

Check **Actions** tab for error messages. Common issues:

- API rate limits (unlikely with Open-Meteo)
- Invalid Python syntax
- Permission issues (ensure workflow has write permissions)

### Dashboard Not Updating

1. Check if GitHub Pages is enabled
2. Verify the workflow ran successfully
3. Clear browser cache
4. Check browser console for JavaScript errors

### No Historical Data

Run the calculator at least once:

```bash
python emission_cap_calculator.py
```

Then commit and push the generated `data/historical_data.json` file.

## 🔒 Security Note

This project uses **public data** only. The Open-Meteo API requires no authentication. GitHub Actions runs in a secure environment, and all code is open source.

## 📖 Additional Resources

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

## ✅ Success Checklist

- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] First workflow run completed successfully
- [ ] Dashboard is accessible online
- [ ] Historical data is accumulating
- [ ] Daily automation is working

---

**Need Help?** Check the GitHub Issues tab or review the workflow logs in the Actions tab.
