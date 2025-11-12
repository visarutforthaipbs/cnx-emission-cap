# 🚀 Quick Reference

## File Structure

```
CNX-CAP/
├── .github/
│   └── workflows/
│       ├── daily-emission-cap.yml    # Daily automation workflow
│       └── deploy-pages.yml          # Dashboard deployment
├── data/
│   └── historical_data.json          # Historical daily records
├── emission_cap_calculator.py        # Main calculation script
├── emission_cap_result.json          # Latest calculation result
├── index.html                        # Dashboard web interface
├── requirements.txt                  # Python dependencies
├── README.md                         # Main documentation
├── SETUP.md                          # Setup instructions
└── .gitignore                        # Git ignore rules
```

## Commands

### Run Calculator Locally

```bash
python emission_cap_calculator.py
```

### View Dashboard Locally

```bash
python -m http.server 8000
# Visit http://localhost:8000
```

### Deploy to GitHub

```bash
git add .
git commit -m "Update data"
git push
```

## Key URLs (After Deployment)

- **Dashboard**: `https://YOUR-USERNAME.github.io/YOUR-REPO/`
- **GitHub Repo**: `https://github.com/YOUR-USERNAME/YOUR-REPO`
- **Actions**: `https://github.com/YOUR-USERNAME/YOUR-REPO/actions`

## Workflow Schedule

- **Daily Calculation**: 6:00 AM Bangkok time (23:00 UTC previous day)
- **Manual Trigger**: Available via GitHub Actions "Run workflow" button

## Important Constants

| Constant      | Value                | Location                                          |
| ------------- | -------------------- | ------------------------------------------------- |
| Target PM2.5  | 37.5 µg/m³           | `emission_cap_calculator.py` line 25              |
| Basin Area    | 1,500 km²            | `emission_cap_calculator.py` line 26              |
| Basin Length  | 80 km                | `emission_cap_calculator.py` line 28              |
| Coordinates   | 18.7883°N, 98.9853°E | `emission_cap_calculator.py` lines 35-36          |
| Cron Schedule | `0 23 * * *`         | `.github/workflows/daily-emission-cap.yml` line 6 |

## Formula

```
Q = (C × V) / τ

Where:
  Q = Emission Cap (Tons/Day)
  C = Target Concentration (37.5 µg/m³)
  V = Basin Area × Boundary Layer Height
  τ = Basin Length / Wind Speed
```

## Data Sources

- **API**: Open-Meteo (https://open-meteo.com)
- **Parameters**: `boundary_layer_height`, `wind_speed_10m`
- **Frequency**: 24-hour forecast, daily average

## Troubleshooting Quick Fixes

### Dashboard not updating?

1. Check GitHub Actions ran successfully
2. Wait 2-3 minutes for GitHub Pages deployment
3. Hard refresh browser (Cmd+Shift+R on Mac)

### Workflow failing?

1. Go to Actions tab on GitHub
2. Click failed workflow
3. Check error logs
4. Common fix: Re-run workflow manually

### Missing data?

```bash
# Run locally once to generate initial data
python emission_cap_calculator.py
git add data/historical_data.json emission_cap_result.json
git commit -m "Add initial data"
git push
```

## Next Steps After Setup

1. ✅ Push code to GitHub
2. ✅ Enable GitHub Pages
3. ✅ Run workflow manually first time
4. ✅ Update README.md with your actual URLs
5. ✅ Share dashboard link!

## Maintenance

- **Weekly**: Check that workflow is running successfully
- **Monthly**: Review historical data for anomalies
- **As needed**: Adjust constants based on new research

---

**Need help?** Check SETUP.md for detailed instructions.
