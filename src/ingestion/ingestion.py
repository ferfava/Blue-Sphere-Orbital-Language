import requests
import json
import os

# Configuración del proyecto
SATELLITE_ID = '44387'  # LightSail-2
URL = "https://db.satnogs.org/api/telemetry/"
TOKEN = '42c6280e7f6c83c7a72b80c0c557bffdec8f8392'

def fetch_data():
    print(f"🛰️ Iniciando protocolo de descarga para el satélite {SATELLITE_ID}...")
    
    headers = {'Authorization': f'Token {TOKEN}'}
    
    params = {
        'satellite': SATELLITE_ID,
        'page_size': 50
    }

    try:
        response = requests.get(URL, params=params, headers=headers)
        
        if response.status_code == 200:
            raw_payload = response.json()
            
            # --- CORRECCIÓN CLAVE: Extraemos la lista de la "caja" results ---
            if isinstance(raw_payload, dict) and 'results' in raw_payload:
                data = raw_payload['results']
            else:
                data = raw_payload

            if not data:
                print("⚠️ El servidor respondió bien, pero la lista de resultados está vacía.")
                return

            # Guardamos los datos
            os.makedirs('data/raw', exist_ok=True)
            output_file = 'data/raw/noaa15_raw.json' # Mantenemos el nombre para no romper el inspector
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
                
            print(f"✅ ¡Éxito! Se han extraído {len(data)} paquetes de telemetría.")
            print(f"📂 Archivo guardado en: {output_file}")
        
        elif response.status_code == 401:
            print("❌ Error 401: El Token es inválido.")
        else:
            print(f"❌ El servidor respondió con error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    fetch_data()