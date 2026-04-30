import numpy as np
from scipy.io import wavfile
import json
import os

# Configuración
INPUT_PATH = 'data/raw/noaa15_raw.json'
SAMPLE_RATE = 44100

def deconstruccion_sonora():
    with open(INPUT_PATH, 'r') as f:
        data = json.load(f)
    
    frame = data[0]['frame']
    bytes_data = [int(frame[i:i+2], 16) for i in range(0, len(frame), 2)]
    
    # Separamos los datos según su función técnica
    header_data = bytes_data[:16]   # Identidad (Bytes 0-15)
    telemetry_data = bytes_data[16:42] # Estado (Bytes 16-41)

    def sintetizar(lista_bytes, duracion_nota=0.2):
        audio = np.array([], dtype=np.float32)
        for valor in lista_bytes:
            t = np.linspace(0, duracion_nota, int(SAMPLE_RATE * duracion_nota))
            # Mapeo: Frecuencia base + (valor del dato * multiplicador)
            freq = 300 + (valor * 1.5) 
            wave = 0.3 * np.sin(2 * np.pi * freq * t)
            audio = np.concatenate([audio, wave])
        return audio

    # Generamos las dos pistas
    audio_identidad = sintetizar(header_data, duracion_nota=0.3) # Más lento para que se note
    audio_estado = sintetizar(telemetry_data, duracion_nota=0.15) # Más rápido, como un pulso

    # Guardamos los archivos
    wavfile.write('data/processed/pista_1_identidad.wav', SAMPLE_RATE, audio_identidad)
    wavfile.write('data/processed/pista_2_estado.wav', SAMPLE_RATE, audio_estado)
    
    print("✅ Deconstrucción completada.")
    print("📁 Archivos creados en data/processed:")
    print("   1. pista_1_identidad.wav (La 'firma' del satélite)")
    print("   2. pista_2_estado.wav (Los sensores de batería/temperatura)")

if __name__ == "__main__":
    deconstruccion_sonora()