import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import json
import math

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Nightfall",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #0f2027, #050505);
        color: #f5f5f5;
    }
    h1, h2, h3 {
        color: #ffffff;
        letter-spacing: 1px;
    }
    .soft-card {
        padding: 35px;
        border-radius: 20px;
        background: rgba(255,255,255,0.06);
        box-shadow: 0 0 40px rgba(0,0,0,0.6);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center; font-size:52px;">🌙 NIGHTFALL</h1>
<p style="text-align:center; font-size:20px; opacity:0.85;">
Your quiet guardian after dark
</p>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="soft-card">
        <h2>🛡️ Stay Aware</h2>
        <p>Nightfall watches the streets so you don’t have to.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        st.info("🌙 Nightfall is awake. You’re not alone.")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🌒 Control Panel")
    st.button("🚨 Emergency Alert")
    st.button("📍 Share Location")

# ============================================================
# CITY DATA
# ============================================================

cities = {
    "Ajmer": [26.4499, 74.6399],
    "Jaipur": [26.9124, 75.7873],
    "Delhi": [28.6139, 77.2090],
    "Mumbai": [19.0760, 72.8777],
    "Bangalore": [12.9716, 77.5946]
}

# ============================================================
# CITY SELECTION
# ============================================================


st.markdown("<br>")

control_col, map_col = st.columns([1, 4])

with control_col:
    st.subheader("📍 Location Control")

    city = st.selectbox("City", list(cities.keys()))
    map_center = cities[city]
    lat, lon = map_center

    st.link_button("Open in Google Maps", f"https://www.google.com/maps?q={lat},{lon}")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("📡 Your Position")
    user_lat = st.number_input("Latitude", value=lat)
    user_lon = st.number_input("Longitude", value=lon)



# ============================================================
# LOAD INCIDENT DATA
# ============================================================

DATA_PATH = r"C:\Users\kubra\Documents\CODING\Python\NIGHTFALL\data\incidents.json"

with open(DATA_PATH) as f:
    incidents = json.load(f)

city_incidents = [i for i in incidents if i["city"] == city]

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def distance_km(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111

def severity_style(sev):
    if sev == "High":
        return "#ff4d4d", 10
    elif sev == "Medium":
        return "#ffa500", 7
    return "#4da6ff", 5

# ============================================================
# RISK CALCULATION
# ============================================================

danger = 0

for incident in city_incidents:
    d = distance_km(user_lat, user_lon, incident["latitude"], incident["longitude"])
    if d < 1:
        if incident["severity"] == "High":
            danger += 3
        elif incident["severity"] == "Medium":
            danger += 2
        else:
            danger += 1


with control_col:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🧭 Your Safety Level")

    if danger >= 6:
        st.error("🚨 HIGH RISK – Avoid this area")
    elif danger >= 3:
        st.warning("⚠️ Moderate risk – Stay alert")
    else:
        st.success("✅ Relatively safe")

    st.link_button(
        "🛣️ Take me to safety",
        f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{lat},{lon}"
    )



# ============================================================
# MAP
# ============================================================

m = folium.Map(location=map_center, zoom_start=13, tiles="CartoDB dark_matter")

# Heatmap
heat_data = []

for i in city_incidents:
    if i["severity"] == "High":
        weight = 1.0
    elif i["severity"] == "Medium":
        weight = 0.6
    else:
        weight = 0.3

    heat_data.append([i["latitude"], i["longitude"], weight])

HeatMap(heat_data, radius=35, blur=45).add_to(m)

# Incident markers
for incident in city_incidents:
    color, radius = severity_style(incident["severity"])
    folium.CircleMarker(
        location=[incident["latitude"], incident["longitude"]],
        radius=radius,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=f"<b>{incident['type']}</b><br>{incident['severity']}"
    ).add_to(m)

# ============================================================
# RENDER
# ============================================================

with map_col:
    st_folium(m, use_container_width=True, height=650)
