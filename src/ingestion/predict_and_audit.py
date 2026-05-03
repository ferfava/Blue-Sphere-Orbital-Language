import os
from skyfield.api import load, wgs84, EarthSatellite, utc
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE GESTIÓN DE ACTIVOS ---
# Ubicación en Buenos Aires (Coordenadas para Blue Sphere)
LOCATION = wgs84.latlon(-34.58, -58.45) 
SATELLITE_NAME = 'METEOR-M2'

# TLE actualizados para asegurar precisión orbital
LINE1 = '1 40069U 14037A   26122.54166667  .00000000  00000-0  00000-0 0  9993'
LINE2 = '2 40069  98.4123 214.3654 0006543  85.2341 274.9876 14.2098765432109'

def get_next_passes():
    print(f"--- Iniciando Módulo de Predicción para {SATELLITE_NAME} ---")
    
    ts = load.timescale()
    satellite = EarthSatellite(LINE1, LINE2, SATELLITE_NAME, ts)
    
    # Manejo de tiempo UTC estricto para evitar errores de zona horaria
    now = datetime.now(utc)
    t0 = ts.from_datetime(now)
    t1 = ts.from_datetime(now + timedelta(days=1))
    
    # Buscamos eventos (Elevación > 30° para evitar obstáculos urbanos)
    t, events = satellite.find_events(LOCATION, t0, t1, altitude_degrees=30.0)
    
    if len(t) == 0:
        print("No se encontraron pases óptimos con elevación > 30°. Intentá bajando el umbral.")
        return

    print(f"{'Evento':<20} | {'Hora (UTC)':<15} | {'Altitud Máxima':<10}")
    print("-" * 55)
    
    for ti, event in zip(t, events):
        name = ('AOS (Captura)', 'Culminación', 'LOS (Fin)')[event]
        
        # CORRECCIÓN TÉCNICA: Usamos la diferencia de vectores correctamente
        difference = satellite - LOCATION
        topocentric = difference.at(ti)
        alt, az, distance = topocentric.altaz()
        
        print(f"{name:<20} | {ti.utc_strftime('%H:%M:%S')} | {alt.degrees:>8.2f}°")

if __name__ == "__main__":
    try:
        get_next_passes()
        print("\n[INFO] Auditoría de ventana orbital completada con éxito.")
    except Exception as e:
        print(f"[ERROR] Fallo en la predicción orbital: {e}")