# SkyCast – Real-Time Weather App 🌤️

A beautiful, production-grade weather dashboard built with **Python + Streamlit**.  
Uses the **Open-Meteo API** — completely free, no API key needed.

---

## Features
- 🌡️ Current temperature, feels-like, humidity, wind, UV index, pressure, visibility
- 📊 Interactive 24-hour temperature + precipitation probability chart (Plotly)
- 📅 7-day daily forecast with weather icons
- 🌅 Sunrise / Sunset / Daylight duration
- 🔍 Search any city in the world via geocoding
- ⚡ Quick-pick dropdown for popular cities
- 🎨 Dark glassmorphism UI with gradient accents

---

## Local Setup

```bash
# 1. Clone / download the files
cd weather_app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run weather_app.py
```

The app opens at **http://localhost:8501**

---

## Deploy on Streamlit Community Cloud (Free)

1. Push these files to a **GitHub repository**
2. Go to → [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → connect your GitHub repo
4. Set **Main file path** → `weather_app.py`
5. Click **Deploy** — done! 🎉

Streamlit Cloud automatically reads `requirements.txt` and installs all dependencies.

---

## Project Structure

```
weather_app/
├── weather_app.py      # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## API Used

| API | Purpose | Cost |
|-----|---------|------|
| [Open-Meteo Forecast](https://open-meteo.com/en/docs) | Weather data | Free |
| [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) | City search | Free |

No API keys required. Data refreshes every 10 minutes (cached via `@st.cache_data`).
