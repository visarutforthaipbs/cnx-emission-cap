# Chiang Mai-Lamphun Emission Cap Calculator

[![Daily Calculation](https://github.com/YOUR-USERNAME/YOUR-REPO/actions/workflows/daily-emission-cap.yml/badge.svg)](https://github.com/YOUR-USERNAME/YOUR-REPO/actions/workflows/daily-emission-cap.yml)

This project calculates daily PM2.5 emission caps for the Chiang Mai-Lamphun air basin using the **Steady-State Box Model**, with automated daily updates and a live dashboard.

📊 **[View Live Dashboard](https://YOUR-USERNAME.github.io/YOUR-REPO/)** _(Update this URL after deployment)_

## 🔬 Scientific Method

The calculator uses the formula:

```
Q = (C × V) / τ
```

Where:

- **Q** = Emission Rate Cap (Tons/Day)
- **C** = Target Concentration (37.5 µg/m³)
- **V** = Volume of the air basin (m³)
- **τ** = Residence Time (seconds)

## ✨ Features

- 🤖 **Automated Daily Calculations** - Runs automatically via GitHub Actions at 6 AM Bangkok time
- 📊 **Interactive Dashboard** - Beautiful web interface with historical charts
- 📈 **Historical Data Tracking** - Maintains a complete record of daily calculations
- 🌐 **Real-time Atmospheric Data** - Uses Open-Meteo API for current conditions
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🚀 Quick Start

### For Users (View Dashboard Only)

Just visit the live dashboard at: **[YOUR-DASHBOARD-URL]**

### For Developers (Run Locally)

1. **Clone the repository:**

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the calculator:**

```bash
python emission_cap_calculator.py
```

4. **View the dashboard locally:**

```bash
# Open index.html in your browser
# Or use a simple HTTP server:
python -m http.server 8000
# Then visit http://localhost:8000
```

## 🔧 Setup for Automation

See **[SETUP.md](SETUP.md)** for detailed instructions on:

- Setting up GitHub repository
- Enabling GitHub Actions automation
- Configuring GitHub Pages
- Customizing the dashboard

## 📊 Output Files

- `emission_cap_result.json` - Latest calculation with full details
- `data/historical_data.json` - All daily results for historical analysis
- `index.html` - Dashboard web interface

## ⚙️ Configuration

Constants can be adjusted in `emission_cap_calculator.py`:

```python
TARGET_CONCENTRATION = 37.5  # µg/m³ (PM2.5 target)
BASIN_AREA_KM2 = 1500  # km² (Chiang Mai-Lamphun basin)
BASIN_LENGTH_KM = 80  # km (north-south length)
LATITUDE = 18.7883  # Chiang Mai coordinates
LONGITUDE = 98.9853
```

## 🌐 Data Source

Atmospheric data provided by [Open-Meteo API](https://open-meteo.com/) (free, no API key required).

## 📈 How It Works

1. **Daily Automation**: GitHub Actions workflow runs at 6 AM Bangkok time
2. **Data Fetching**: Script fetches boundary layer height and wind speed from Open-Meteo
3. **Calculation**: Applies the Steady-State Box Model formula
4. **Storage**: Saves results to JSON files
5. **Commit**: Automatically commits updated data to the repository
6. **Dashboard**: GitHub Pages serves the live dashboard with updated data

## 📄 License

This project is open source and available for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 References

- Steady-State Box Model for air quality assessment
- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Chart.js](https://www.chartjs.org/)
