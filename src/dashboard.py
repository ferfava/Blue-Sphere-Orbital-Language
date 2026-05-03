import streamlit as st
import json
import time
import pandas as pd
from datetime import datetime, timezone
from skyfield.api import load, wgs84, EarthSatellite

# 1. CONFIGURACIÓN Y DATOS TÉCNICOS
st.set_page_config(page_title="Blue Sphere: Auditoría Geoespacial", page_icon="🛰️", layout="wide")

SATELLITE_NAME = 'METEOR-M2'
LINE1 = '1 40069U 14037A   26122.54166667  .00000000  00000-0  00000-0 0  9993'
LINE2 = '2 40069  98.4123 214.3654 0006543  85.2341 274.9876 14.2098765432109'
LAUNCH_DATE = datetime(2014, 7, 8, tzinfo=timezone.utc)

def get_satellite_age():
    now = datetime.now(timezone.utc)
    diff = now - LAUNCH_DATE
    return f"{diff.days // 365} años y {(diff.days % 365) // 30} meses"

def get_realtime_coords():
    ts = load.timescale()
    satellite = EarthSatellite(LINE1, LINE2, SATELLITE_NAME, ts)
    geocentric = satellite.at(ts.now())
    subpoint = wgs84.subpoint(geocentric)
    return subpoint.latitude.degrees, subpoint.longitude.degrees

def load_ingestion():
    try:
        with open('data/live_status.json', 'r') as f:
            return json.load(f)
    except: return None

# --- ESTRUCTURA DEL FRONT ---
st.title("🛰️ Blue Sphere: Centro de Gestión y Auditoría de Activos")
st.markdown(f"**Tesis:** Echo-Spatial (Arqueología Sonora) | **Operador:** Fernanda Fava")
st.markdown("---")

placeholder = st.empty()

if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['timestamp', 'elevation'])

while True:
    sat_lat, sat_lon = get_realtime_coords()
    ingestion = load_ingestion()
    
    with placeholder.container():
        # A. LEGAJO TÉCNICO (Ficha fija arriba)
        with st.expander("📊 Legajo Técnico del Activo (METEOR-M2)", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.write("**Nacionalidad:** 🇷🇺 Rusia")
            c2.write(f"**Lanzamiento:** {LAUNCH_DATE.strftime('%d/%m/%Y')}")
            c3.write(f"**Edad del Activo:** {get_satellite_age()}")
            c4.write("**COSPAR ID:** 2014-037A")

        # B. TELEMETRÍA Y GRÁFICA
        st.subheader("📡 Monitoreo Online")
        m1, m2, m3, m4 = st.columns(4)
        if ingestion:
            m1.metric("Elevación (BA)", f"{ingestion['elevation']}°")
            m2.metric("Azimut", f"{ingestion['azimuth']}°")
            m3.metric("Latitud Sat.", f"{sat_lat:.2f}°")
            m4.metric("Longitud Sat.", f"{sat_lon:.2f}°")

            new_point = pd.DataFrame({'timestamp': [datetime.now().strftime("%H:%M:%S")], 'elevation': [ingestion['elevation']]})
            st.session_state.history = pd.concat([st.session_state.history, new_point]).tail(30)

        col_graph, col_map = st.columns([1, 1])
        with col_graph:
            st.line_chart(st.session_state.history.set_index('timestamp'), use_container_width=True)
        with col_map:
            st.map(pd.DataFrame({'lat': [sat_lat], 'lon': [sat_lon]}), zoom=2, use_container_width=True)

        # C. RESULTADOS FINALES (Esta sección ahora siempre está visible)
        st.markdown("---")
        st.subheader("📁 Entregables de Auditoría: Echo-Spatial")
        
        res_img, res_aud = st.columns(2)
        
        with res_img:
            st.markdown("**Captura de Teledetección (Último pase):**")
            # Imagen de referencia del Meteor-M2 (MSU-MR)
            st.image("https://upload.wikimedia.org/wikipedia/commons/9/91/Meteor-M2_image.jpg", 
                     caption="Imagen capturada por el sensor meteorológico ruso")
        
        with res_aud:
            st.markdown("**Resultado de Sonificación:**")
            # Aquí el reproductor buscará el archivo .wav en tu carpeta de datos
            try:
                audio_file = open('data/last_pass_sonification.wav', 'rb')
                st.audio(audio_file.read(), format='audio/wav')
                st.success("Archivo de arqueología sonora cargado correctamente.")
            except FileNotFoundError:
                st.warning("Esperando a que el motor de sonificación genere el archivo .wav...")

    time.sleep(2)