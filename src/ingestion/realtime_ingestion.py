import time
import json
import os
from datetime import datetime, timezone
from skyfield.api import load, wgs84, EarthSatellite

# --- CONFIGURACIÓN ---
LOCATION = wgs84.latlon(-34.58, -58.45)
SATELLITE_NAME = 'METEOR-M2'
LINE1 = '1 40069U 14037A   26122.54166667  .00000000  00000-0  00000-0 0  9993'
LINE2 = '2 40069  98.4123 214.3654 0006543  85.2341 274.9876 14.2098765432109'

# Ruta para el reporte online que leerá el Front-end
OUTPUT_PATH = os.path.join('data', 'live_status.json')

def update_live_report(data):
    """Guarda el estado actual en un archivo JSON para el Front-end"""
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def start_live_stream():
    ts = load.timescale()
    satellite = EarthSatellite(LINE1, LINE2, SATELLITE_NAME, ts)
    
    print(f"[LIVE] Blue Sphere: Generando datos online en {OUTPUT_PATH}")
    
    try:
        while True:
            now = datetime.now(timezone.utc)
            t_now = ts.from_datetime(now)
            
            difference = satellite - LOCATION
            topocentric = difference.at(t_now)
            alt, az, dist = topocentric.altaz()
            
            # Creamos el paquete de datos online
            current_data = {
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "satellite": SATELLITE_NAME,
                "elevation": round(alt.degrees, 2),
                "azimuth": round(az.degrees, 2),
                "status": "Capturando" if alt.degrees > 0 else "Esperando pase"
            }
            
            # Guardamos para el Front-end
            update_live_report(current_data)
            
            # Mostramos en consola
            status_text = f"Elevación: {current_data['elevation']}° | Azimut: {current_data['azimuth']}°"
            print(f"[{current_data['status']}] {status_text}   ", end="\r")
            
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[STOP] Monitoreo finalizado.")

if __name__ == "__main__":
    # Aseguramos que la carpeta data exista
    if not os.path.exists('data'):
        os.makedirs('data')
    start_live_stream()