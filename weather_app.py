import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkyCast – Real-Time Weather",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 120% 80% at 50% -10%, #1a2744 0%, #0a0e1a 60%) !important;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 1.5rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #7dd3fc 0%, #a5b4fc 50%, #f0abfc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #64748b;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Search bar ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(125,211,252,0.2) !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 0.9rem 1.2rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(125,211,252,0.55) !important;
    box-shadow: 0 0 0 3px rgba(125,211,252,0.12) !important;
    outline: none !important;
}
.stTextInput > label { color: #94a3b8 !important; font-size: 0.8rem !important; letter-spacing: 0.1em; text-transform: uppercase; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 2rem !important;
    letter-spacing: 0.04em;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.15s;
    width: 100%;
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }

/* ── Main weather card ── */
.weather-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.03) 100%);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 2.2rem 2.4rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.weather-card::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(125,211,252,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.city-name {
    font-family: 'Syne', sans-serif;
    font-size: clamp(1.8rem, 4vw, 3rem);
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 0.1rem;
}
.country-tag {
    display: inline-block;
    background: rgba(125,211,252,0.15);
    color: #7dd3fc;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.75rem;
    border-radius: 99px;
    margin-bottom: 1.2rem;
}
.temp-display {
    font-family: 'Syne', sans-serif;
    font-size: clamp(4rem, 10vw, 7rem);
    font-weight: 800;
    color: #f8fafc;
    line-height: 1;
    letter-spacing: -0.04em;
}
.feels-like {
    font-size: 0.88rem;
    color: #64748b;
    margin-top: 0.3rem;
}
.weather-desc {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-top: 0.6rem;
    font-weight: 300;
}
.weather-icon-large { font-size: clamp(4rem, 8vw, 6rem); line-height: 1; }

/* ── Stat tiles ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-top: 1rem;
}
.stat-tile {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    transition: background 0.2s;
}
.stat-tile:hover { background: rgba(255,255,255,0.07); }
.stat-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #64748b;
    margin-bottom: 0.4rem;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e2e8f0;
}
.stat-icon { font-size: 1.3rem; margin-bottom: 0.3rem; }

/* ── Forecast row ── */
.forecast-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.2rem;
    text-align: center;
    transition: background 0.2s, transform 0.2s;
}
.forecast-card:hover { background: rgba(255,255,255,0.08); transform: translateY(-3px); }
.forecast-day {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.forecast-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.forecast-temps {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    color: #e2e8f0;
}
.forecast-temps span { color: #64748b; font-size: 0.85rem; }

/* ── Section header ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #475569;
    margin: 1.8rem 0 0.9rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding-bottom: 0.5rem;
}

/* ── Hourly chart ── */
.stPlotlyChart { border-radius: 16px; overflow: hidden; }

/* ── Alert / info boxes ── */
.info-banner {
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.9rem;
    color: #fbbf24;
}
.error-banner {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.9rem;
    color: #f87171;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(125,211,252,0.2) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Constants ─────────────────────────────────────────────────────────────────
WMO_CODES = {
    0:  ("Clear Sky",            "☀️"),
    1:  ("Mainly Clear",         "🌤️"),
    2:  ("Partly Cloudy",        "⛅"),
    3:  ("Overcast",             "☁️"),
    45: ("Fog",                  "🌫️"),
    48: ("Depositing Rime Fog",  "🌫️"),
    51: ("Light Drizzle",        "🌦️"),
    53: ("Moderate Drizzle",     "🌦️"),
    55: ("Dense Drizzle",        "🌧️"),
    61: ("Slight Rain",          "🌧️"),
    63: ("Moderate Rain",        "🌧️"),
    65: ("Heavy Rain",           "🌧️"),
    71: ("Slight Snowfall",      "🌨️"),
    73: ("Moderate Snowfall",    "❄️"),
    75: ("Heavy Snowfall",       "❄️"),
    77: ("Snow Grains",          "🌨️"),
    80: ("Slight Showers",       "🌦️"),
    81: ("Moderate Showers",     "🌧️"),
    82: ("Violent Showers",      "⛈️"),
    85: ("Slight Snow Showers",  "🌨️"),
    86: ("Heavy Snow Showers",   "❄️"),
    95: ("Thunderstorm",         "⛈️"),
    96: ("Thunderstorm w/ Hail", "⛈️"),
    99: ("Thunderstorm w/ Hail", "⛈️"),
}

CITIES = {
    "Ahmedabad, India":    (23.0225, 72.5714),
    "Mumbai, India":       (19.0760, 72.8777),
    "Delhi, India":        (28.6139, 77.2090),
    "London, UK":          (51.5074, -0.1278),
    "New York, USA":       (40.7128, -74.0060),
    "Tokyo, Japan":        (35.6762, 139.6503),
    "Paris, France":       (48.8566, 2.3522),
    "Sydney, Australia":   (-33.8688, 151.2093),
    "Dubai, UAE":          (25.2048, 55.2708),
    "Singapore":           (1.3521, 103.8198),
}


# ── API helpers ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def geocode(city: str):
    """Open-Meteo geocoding."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=10)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        return None
    g = results[0]
    return {
        "name":    g.get("name", city),
        "country": g.get("country", ""),
        "lat":     g["latitude"],
        "lon":     g["longitude"],
        "tz":      g.get("timezone", "auto"),
    }


@st.cache_data(ttl=600)
def fetch_weather(lat: float, lon: float, tz: str = "auto"):
    """Fetch current + hourly + daily weather from Open-Meteo (free, no key)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":  lat,
        "longitude": lon,
        "timezone":  tz,
        "current": ",".join([
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "weather_code", "wind_speed_10m", "wind_direction_10m",
            "surface_pressure", "visibility", "uv_index", "precipitation",
        ]),
        "hourly": ",".join([
            "temperature_2m", "apparent_temperature", "precipitation_probability",
            "weather_code", "wind_speed_10m", "relative_humidity_2m",
        ]),
        "daily": ",".join([
            "temperature_2m_max", "temperature_2m_min", "weather_code",
            "precipitation_sum", "wind_speed_10m_max", "sunrise", "sunset",
        ]),
        "forecast_days": 7,
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


def wind_direction_label(deg: float) -> str:
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    return dirs[round(deg / 45) % 8]


def uv_label(uv: float) -> str:
    if uv < 3:   return "Low"
    if uv < 6:   return "Moderate"
    if uv < 8:   return "High"
    if uv < 11:  return "Very High"
    return "Extreme"


# ── App layout ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">SkyCast</div>
  <div class="hero-sub">Real-Time Weather Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ── Search row ────────────────────────────────────────────────────────────────
col_input, col_btn, col_quick = st.columns([3, 1, 2])

with col_input:
    city_input = st.text_input("", placeholder="Search any city…", label_visibility="collapsed")

with col_btn:
    search_clicked = st.button("Search 🔍")

with col_quick:
    quick = st.selectbox("", ["— Quick pick —"] + list(CITIES.keys()), label_visibility="collapsed")

# Resolve city
city_query = None
lat, lon, tz = None, None, "auto"
location_info = {}

if search_clicked and city_input.strip():
    city_query = city_input.strip()
elif quick and quick != "— Quick pick —":
    city_query = quick
    lat, lon = CITIES[quick]

if city_query:
    if lat is None:
        with st.spinner("Locating city…"):
            geo = geocode(city_query)
        if not geo:
            st.markdown(f'<div class="error-banner">⚠️ City <b>{city_query}</b> not found. Try a different spelling.</div>', unsafe_allow_html=True)
            st.stop()
        lat, lon, tz = geo["lat"], geo["lon"], geo["tz"]
        location_info = geo
    else:
        parts = city_query.split(",")
        location_info = {"name": parts[0].strip(), "country": parts[1].strip() if len(parts) > 1 else "", "lat": lat, "lon": lon}

    # Fetch weather
    with st.spinner("Fetching weather data…"):
        try:
            data = fetch_weather(lat, lon, tz)
        except Exception as e:
            st.markdown(f'<div class="error-banner">⚠️ API error: {e}</div>', unsafe_allow_html=True)
            st.stop()

    cur  = data["current"]
    hr   = data["hourly"]
    day  = data["daily"]
    units = data.get("current_units", {})

    wcode = int(cur.get("weather_code", 0))
    wdesc, wicon = WMO_CODES.get(wcode, ("Unknown", "🌡️"))
    temp      = cur.get("temperature_2m", "--")
    feels     = cur.get("apparent_temperature", "--")
    humidity  = cur.get("relative_humidity_2m", "--")
    wind_spd  = cur.get("wind_speed_10m", "--")
    wind_dir  = cur.get("wind_direction_10m", 0)
    pressure  = cur.get("surface_pressure", "--")
    visibility= cur.get("visibility", "--")
    uv        = cur.get("uv_index", "--")
    precip    = cur.get("precipitation", "--")
    updated   = cur.get("time", "")

    city_name = location_info.get("name", city_query)
    country   = location_info.get("country", "")

    st.markdown('<div class="section-header">Current Conditions</div>', unsafe_allow_html=True)

    # ── Main weather card ──────────────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        st.markdown(f"""
        <div class="weather-card">
          <div class="city-name">{city_name}</div>
          <div class="country-tag">📍 {country} &nbsp;·&nbsp; {lat:.2f}°N, {lon:.2f}°E</div>
          <div style="display:flex; align-items:flex-end; gap:1.5rem;">
            <div>
              <div class="temp-display">{temp}°</div>
              <div class="feels-like">Feels like {feels}°C</div>
              <div class="weather-desc">{wicon} {wdesc}</div>
            </div>
          </div>
          <div style="margin-top:1rem; font-size:0.78rem; color:#475569;">
            Last updated · {updated.replace("T"," ")}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="weather-card" style="height:100%;">
          <div class="stat-grid">
            <div class="stat-tile">
              <div class="stat-icon">💧</div>
              <div class="stat-label">Humidity</div>
              <div class="stat-value">{humidity}%</div>
            </div>
            <div class="stat-tile">
              <div class="stat-icon">💨</div>
              <div class="stat-label">Wind</div>
              <div class="stat-value">{wind_spd} km/h</div>
            </div>
            <div class="stat-tile">
              <div class="stat-icon">🧭</div>
              <div class="stat-label">Direction</div>
              <div class="stat-value">{wind_direction_label(wind_dir)} {wind_dir}°</div>
            </div>
            <div class="stat-tile">
              <div class="stat-icon">🔭</div>
              <div class="stat-label">Visibility</div>
              <div class="stat-value">{int(visibility/1000) if isinstance(visibility,(int,float)) else visibility} km</div>
            </div>
            <div class="stat-tile">
              <div class="stat-icon">🌡️</div>
              <div class="stat-label">Pressure</div>
              <div class="stat-value">{pressure} hPa</div>
            </div>
            <div class="stat-tile">
              <div class="stat-icon">☀️</div>
              <div class="stat-label">UV Index</div>
              <div class="stat-value">{uv} <small style="font-size:0.7rem;color:#94a3b8">{uv_label(uv) if isinstance(uv,(int,float)) else ""}</small></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Hourly temperature chart ───────────────────────────────────────────────
    st.markdown('<div class="section-header">24-Hour Forecast</div>', unsafe_allow_html=True)

    try:
        import plotly.graph_objects as go
        hours = hr["time"][:24]
        temps_hr = hr["temperature_2m"][:24]
        precip_prob = hr.get("precipitation_probability", [0]*24)[:24]
        hour_labels = [h.split("T")[1][:5] for h in hours]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hour_labels, y=temps_hr,
            mode="lines+markers",
            name="Temp (°C)",
            line=dict(color="#7dd3fc", width=2.5, shape="spline"),
            marker=dict(size=5, color="#7dd3fc"),
            fill="tozeroy",
            fillcolor="rgba(125,211,252,0.07)",
            hovertemplate="%{y}°C<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            x=hour_labels, y=precip_prob,
            name="Precip %",
            marker_color="rgba(165,180,252,0.35)",
            yaxis="y2",
            hovertemplate="%{y}%<extra></extra>",
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(255,255,255,0.03)",
            font=dict(color="#64748b", family="Inter"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=240,
            legend=dict(orientation="h", x=0, y=1.12, font=dict(size=11)),
            xaxis=dict(showgrid=False, tickfont=dict(size=11), color="#475569"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                       tickfont=dict(size=11), color="#64748b", title="°C"),
            yaxis2=dict(overlaying="y", side="right", range=[0,100],
                        tickfont=dict(size=10), color="#a5b4fc", title="Precip %",
                        showgrid=False),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    except ImportError:
        st.info("Install plotly (`pip install plotly`) for interactive charts.")

    # ── 7-day forecast ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">7-Day Forecast</div>', unsafe_allow_html=True)

    forecast_cols = st.columns(7)
    for i, col in enumerate(forecast_cols):
        date_str  = day["time"][i]
        dt        = datetime.strptime(date_str, "%Y-%m-%d")
        day_label = "Today" if i == 0 else dt.strftime("%a")
        dcode     = int(day["weather_code"][i])
        d_desc, d_icon = WMO_CODES.get(dcode, ("?", "🌡️"))
        tmax      = day["temperature_2m_max"][i]
        tmin      = day["temperature_2m_min"][i]
        psum      = day["precipitation_sum"][i]

        with col:
            st.markdown(f"""
            <div class="forecast-card">
              <div class="forecast-day">{day_label}<br>{dt.strftime("%d %b")}</div>
              <div class="forecast-icon">{d_icon}</div>
              <div class="forecast-temps">{tmax}° <span>/ {tmin}°</span></div>
              <div style="font-size:0.7rem;color:#475569;margin-top:0.4rem">💧 {psum} mm</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Sunrise / sunset ───────────────────────────────────────────────────────
    if "sunrise" in day and "sunset" in day:
        sunrise_raw = day["sunrise"][0]
        sunset_raw  = day["sunset"][0]
        sunrise_t   = sunrise_raw.split("T")[1][:5] if "T" in sunrise_raw else sunrise_raw[-5:]
        sunset_t    = sunset_raw.split("T")[1][:5]  if "T" in sunset_raw  else sunset_raw[-5:]

        st.markdown('<div class="section-header">Sun Schedule</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f"""
            <div class="stat-tile" style="text-align:center; padding:1.3rem;">
              <div style="font-size:2rem">🌅</div>
              <div class="stat-label">Sunrise</div>
              <div class="stat-value">{sunrise_t}</div>
            </div>""", unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="stat-tile" style="text-align:center; padding:1.3rem;">
              <div style="font-size:2rem">🌇</div>
              <div class="stat-label">Sunset</div>
              <div class="stat-value">{sunset_t}</div>
            </div>""", unsafe_allow_html=True)
        with s3:
            try:
                fmt = "%H:%M"
                sr = datetime.strptime(sunrise_t, fmt)
                ss = datetime.strptime(sunset_t, fmt)
                day_len = ss - sr
                hrs, rem = divmod(int(day_len.total_seconds()), 3600)
                mins = rem // 60
            except Exception:
                hrs, mins = "--", "--"
            st.markdown(f"""
            <div class="stat-tile" style="text-align:center; padding:1.3rem;">
              <div style="font-size:2rem">⏱️</div>
              <div class="stat-label">Daylight</div>
              <div class="stat-value">{hrs}h {mins}m</div>
            </div>""", unsafe_allow_html=True)

    # ── Footer ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <hr style="margin:2.5rem 0 1rem"/>
    <div style="text-align:center; font-size:0.78rem; color:#334155; padding-bottom:2rem;">
      Powered by <a href="https://open-meteo.com" target="_blank" style="color:#475569;text-decoration:none;">Open-Meteo</a> · Free &amp; Open Weather API · No API key required
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Empty state ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:4rem 1rem; color:#334155;">
      <div style="font-size:5rem; margin-bottom:1rem;">🌍</div>
      <div style="font-family:'Syne',sans-serif; font-size:1.3rem; color:#475569; margin-bottom:0.5rem;">
        Search a city to get started
      </div>
      <div style="font-size:0.9rem; color:#334155;">
        Real-time temperature · Hourly charts · 7-day forecast · UV index · and more
      </div>
    </div>
    """, unsafe_allow_html=True)
