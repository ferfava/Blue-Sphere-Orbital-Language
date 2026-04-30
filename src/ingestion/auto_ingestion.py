import requests
import json
import os
from dotenv import load_dotenv

# 1. Cargamos la API Key obligando a refrescar el archivo .env
load_dotenv(override=True)
API_KEY = os.getenv('SATNOGS_API_KEY')

# 2. Configuración de objetivos (Satélites activos)
SATELLITES = {
    "NOAA-15": 25338,
    "NOAA-18": 28654,
    "METEOR-M2": 40069,
    "LIGHTSAIL-2": 44444
}

# 3. URL de la Base de Datos (la más estable)
BASE_URL = "https://db.satnogs.org/api/telemetry/"

def descargar_lote_definitivo():
    print("🚀 --- PROJECT BLUE SPHERE: INGESTA DE DATOS v3.0 ---")
    
    if not API_KEY:
        print("❌ ERROR: No se encontró la API Key en el archivo .env")
        return

    # Limpiamos la clave por si se coló algún espacio invisible
    token_limpio = API_KEY.strip()

    # Carpeta de salida
    output_dir = 'data/raw/batch'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for nombre, s_id in SATELLITES.items():
        print(f"\n📡 Conectando con {nombre} (ID: {s_id})...")
        
        # Enviamos el token en los parámetros y en el header por redundancia
        params = {
            'satellite': s_id,
            'limit': 5
        }
        
        headers = {
            'Authorization': f'Token {token_limpio}',
            'Accept': 'application/json',
            'User-Agent': 'BlueSphereProject/1.0'
        }
        
        try:
            response = requests.get(BASE_URL, params=params, headers=headers, timeout=60) # De 15 a 60
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    file_path = os.path.join(output_dir, f'{nombre}_raw.json')
                    with open(file_path, 'w') as f:
                        json.dump(data, f, indent=4)
                    print(f"✅ ÉXITO: {len(data)} paquetes guardados.")
                else:
                    print(f"⚠️ AVISO: {nombre} no tiene datos nuevos.")
            
            elif response.status_code == 401:
                print(f"❌ ERROR 401: No autorizado. Key intentada: ...{token_limpio[-4:]}")
                print("👉 Tip: Verificá en db.satnogs.org que tu cuenta esté activa.")
            elif response.status_code == 404:
                print(f"❌ ERROR 404: URL incorrecta. Revisar endpoint.")
            else:
                print(f"❌ ERROR {response.status_code}: Problema inesperado.")

        except Exception as e:
            print(f"💥 ERROR TÉCNICO: {e}")

    print("\n--- Proceso Finalizado --- 🛰️")

if __name__ == "__main__":
    descargar_lote_definitivo()