import requests
import json
import os

# ID del Satélite NOAA 15
SATELLITE_ID = '25338' 
URL = "https://db.satnogs.org/api/telemetry/"

def fetch_data():
    print("🛰️ Conectando con SatNOGS para traer datos del espacio...")
    params = {'satellite': SATELLITE_ID}
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        # Crear la carpeta data/raw si no existe
        os.makedirs('data/raw', exist_ok=True)

        with open('data/raw/noaa15_raw.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        print("✅ Datos guardados exitosamente en data/raw/noaa15_raw.json")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    fetch_data()