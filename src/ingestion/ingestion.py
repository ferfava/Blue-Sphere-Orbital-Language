import requests
import json
import os

# Configuración del proyecto
SATELLITE_ID = '25338' # NOAA 15
URL = "https://db.satnogs.org/api/telemetry/"
TOKEN = '42c6280e7f6c83c7a72b80c0c557bffdec8f8392'

def fetch_data():
    print(f"🛰️ Iniciando protocolo de descarga para el satélite {SATELLITE_ID}...")
    
    headers = {'Authorization': f'Token {TOKEN}'}
    
    # --- AQUÍ VA EL CAMBIO ---
    # Pedimos datos de las últimas 24 horas para asegurar volumen
    params = {
        'satellite': SATELLITE_ID,
        'page_size': 100,
    }
    # -------------------------
    
    try:
        response = requests.get(URL, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            os.makedirs('data/raw', exist_ok=True)
            
            output_file = 'data/raw/noaa15_raw.json'
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
                
            print(f"✅ ¡Éxito! Se han descargado {len(data)} paquetes de telemetría.")
            print(f"📂 Archivo guardado en: {output_file}")
        else:
            print(f"❌ Falló: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_data()