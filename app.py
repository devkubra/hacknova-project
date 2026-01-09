import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# ---------- Page Config ----------
st.set_page_config(
    page_title="Nightfall",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Global Styling ----------
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

# ---------- Header ----------
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center; font-size:52px;">
🌙 NIGHTFALL
</h1>
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
        <p style="font-size:16px; opacity:0.85;">
            Silent vigilance. Gentle warnings.  
            Nightfall watches so you don’t have to.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("🌙 Nightfall is awake. You’re not alone.")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌒 Control Panel")
    st.toggle("Night Mode", value=True)
    st.button("📍 Share Location")
    st.button("🚨 Emergency Alert")

# ---------- Location ----------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📍 Choose Your City")

cities = {
    "Ajmer": [26.4499, 74.6399],
    "Jaipur": [26.9124, 75.7873],
    "Delhi": [28.6139, 77.2090],
    "Mumbai": [19.0760, 72.8777],
    "Bangalore": [12.9716, 77.5946]
}


st.subheader("🗺️ Google Maps View (Powered by Google Maps)")



city = st.selectbox("City", list(cities.keys()))
map_center = cities[city]

# ---------- Load Data ----------
with open(r"C:\Users\kubra\Documents\CODING\Python\NIGHTFALL\data\incidents.json") as f:
    incidents = json.load(f)


google_maps_urls = {
    "Ajmer": "https://www.google.com/maps?q=Ajmer&output=embed",
    "Jaipur": "https://www.google.com/maps?q=Jaipur&output=embed",
    "Delhi": "https://www.google.com/maps?q=Delhi&output=embed",
    "Mumbai": "https://www.google.com/maps?q=Mumbai&output=embed",
    "Bangalore": "https://www.google.com/maps?q=Bangalore&output=embed",
}


map_url = google_maps_urls.get(city)

if map_url:
    st.components.v1.iframe(map_url, height=450)
else:
    st.warning("Google Maps view not available for this city yet.")



# ---------- Map ----------
m = folium.Map(
    location=map_center,
    zoom_start=13,
    tiles="CartoDB dark_matter"
)

def severity_style(sev):
    if sev == "High":
        return ("#ff4d4d", 10)
    elif sev == "Medium":
        return ("#ffa500", 7)
    else:
        return ("#4da6ff", 5)

for incident in incidents:
    color, radius = severity_style(incident["severity"])
    folium.CircleMarker(
        location=[incident["latitude"], incident["longitude"]],
        radius=radius,
        color=color,
        fill=True,
        fill_opacity=0.75,
        popup=f"""
        <b>{incident['type']}</b><br>
        Severity: {incident['severity']}
        """
    ).add_to(m)

# ---------- Map Legend ----------
legend_html = """
<div style="
position: fixed;
bottom: 40px;
left: 40px;
padding: 15px;
background: rgba(0,0,0,0.7);
border-radius: 12px;
color: white;
font-size: 14px;
">
<b>Incident Severity</b><br>
<span style="color:#ff4d4d;">●</span> High<br>
<span style="color:#ffa500;">●</span> Medium<br>
<span style="color:#4da6ff;">●</span> Low
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

st.markdown("<br>", unsafe_allow_html=True)
st_folium(m, width=1200, height=520)
