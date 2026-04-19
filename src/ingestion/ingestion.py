import requests
import json
import os

# Configuración del proyecto
SATELLITE_ID = '44387'  # LightSail-2 (Suele responder mucho mejor)
URL = "https://db.satnogs.org/api/telemetry/"
TOKEN = '42c6280e7f6c83c7a72b80c0c557bffdec8f8392'

def fetch_data():
    print(f"🛰️ Iniciando protocolo de descarga para el satélite {SATELLITE_ID}...")
    
    # Definimos las cabeceras con tu Token
    headers = {'Authorization': f'Token {TOKEN}'}
    
    # Parámetros para traer datos ya decodificados (legibles)
    params = {
        'satellite': SATELLITE_ID,
        'page_size': 50,
        'is_decoded': 'true' 
    }

    try:
        # Realizamos la petición a la API
        response = requests.get(URL, params=params, headers=headers)
        
        # Si la respuesta es exitosa (Código 200)
        if response.status_code == 200:
            data = response.json()
            
            # Verificamos si realmente trajo datos
            if not data:
                print("⚠️ No hay datos decodificados recientes para este satélite.")
                print("💡 Tip: Podés probar con el ID '44387' (LightSail-2) si el NOAA-15 está mudo.")
                return

            # Creamos la carpeta si no existe
            os.makedirs('data/raw', exist_ok=True)
            
            output_file = 'data/raw/noaa15_raw.json'
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
                
            print(f"✅ ¡Éxito! Se han descargado {len(data)} paquetes de telemetría.")
            print(f"📂 Archivo guardado en: {output_file}")
        
        elif response.status_code == 401:
            print("❌ Error 401: El Token es inválido o no tienes permisos.")
        else:
            print(f"❌ El servidor respondió con error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    fetch_data()