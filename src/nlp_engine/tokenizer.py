import json
import os

INPUT_FILE = 'data/raw/noaa15_raw.json'
OUTPUT_FILE = 'data/processed/orbital_corpus.txt'

def translate_to_tokens(value, category):
    """Convierte valores numéricos en etiquetas lingüísticas (Tokens)"""
    if category == 'temp':
        return "[TEMP_COLD]" if value < 10 else "[TEMP_WARM]" if value < 30 else "[TEMP_HOT]"
    # Podemos agregar más categorías luego
    return f"[{category.upper()}_{value}]"

def process_telemetry():
    if not os.path.exists(INPUT_FILE):
        print("❌ No se encontró el archivo de datos.")
        return

    with open(INPUT_FILE, 'r') as f:
        data = json.json_load(f)

    tokens = []
    for packet in data:
        timestamp = packet.get('timestamp', 'UNKNOWN')
        # Aquí es donde ocurre la magia del PLN
        # Por ahora usamos el ID del paquete como ejemplo de palabra
        token = f"OBSERVATION_{packet.get('id', 'NULL')}"
        tokens.append(token)

    # Guardamos el corpus como un archivo de texto para que lo use tu modelo de IA
    os.makedirs('data/processed', exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(" ".join(tokens))
    
    print(f"✅ Corpus generado: {len(tokens)} palabras creadas en {OUTPUT_FILE}")

if __name__ == "__main__":
    process_telemetry()