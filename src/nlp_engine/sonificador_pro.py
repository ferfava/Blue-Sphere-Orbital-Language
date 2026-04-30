import numpy as np
from scipy.io import wavfile
import json
import os

# Configuración técnica
INPUT_PATH = 'data/raw/noaa15_raw.json'
OUTPUT_AUDIO = 'data/processed/orbital_audit.wav'
LOG_PATH = 'data/processed/sonification_log.txt'
SAMPLE_RATE = 44100

def generar_sonificacion_auditada():
    with open(INPUT_PATH, 'r') as f:
        data = json.load(f)
    
    # Trabajamos con el primer paquete de telemetría
    frame = data[0]['frame']
    bytes_data = [int(frame[i:i+2], 16) for i in range(0, len(frame), 2)]
    
    full_audio = np.array([], dtype=np.float32)
    log_entries = []

    print("Iniciando sonificación auditada")

    for i, valor in enumerate(bytes_data):
        # Duración de cada "evento" de dato: 0.15 segundos
        t = np.linspace(0, 0.15, int(SAMPLE_RATE * 0.15))
        
        # MAPEO CIENTÍFICO: 
        # Usamos una frecuencia base de 300Hz (hum de ciudad) 
        # y le sumamos el valor del byte para la variación.
        freq = 300 + (valor * 2) 
        
        # Generamos la onda
        wave = 0.3 * np.sin(2 * np.pi * freq * t)
        full_audio = np.concatenate([full_audio, wave])
        
        # Guardamos la evidencia para la tesis
        log_entries.append(f"Byte {i:02d} | Hex: {frame[i*2:i*2+2]} | Val: {valor:3d} | Freq: {freq:.2f}Hz")

    # Guardar archivos
    wavfile.write(OUTPUT_AUDIO, SAMPLE_RATE, full_audio)
    with open(LOG_PATH, 'w') as f:
        f.write("\n".join(log_entries))
        
    print(f"✅ Proceso terminado.")
    print(f"📄 Log de auditoría creado en: {LOG_PATH}")
    print(f"🎧 Audio generado en: {OUTPUT_AUDIO}")

if __name__ == "__main__":
    generar_sonificacion_auditada()