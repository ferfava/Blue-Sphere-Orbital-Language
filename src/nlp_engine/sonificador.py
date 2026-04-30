import numpy as np
from scipy.io import wavfile
import os

# Configuración
INPUT_FILE = 'data/processed/orbital_corpus.txt'
OUTPUT_AUDIO = 'data/processed/satellite_voice.wav'
SAMPLE_RATE = 44100  # Calidad de CD
DURATION_PER_BYTE = 0.1  # Segundos que suena cada "palabra" espacial

def hex_to_freq(hex_byte):
    """Convierte un byte (00-FF) en una frecuencia entre 200 y 1000 Hz"""
    decimal_value = int(hex_byte, 16)
    # Mapeo lineal: (valor / 255) * rango + base
    return 200 + (decimal_value / 255) * 800

def generar_audio():
    if not os.path.exists(INPUT_FILE):
        print("❌ No encontré el corpus. Corré el generador de corpus primero.")
        return

    with open(INPUT_FILE, 'r') as f:
        lines = f.readlines()

    full_wave = []
    
    print("🎼 Traduciendo bytes a frecuencias...")
    
    # Solo procesamos la primera línea (una órbita) para probar
    first_orbit = lines[0].split()
    
    for byte in first_orbit:
        freq = hex_to_freq(byte)
        
        # Generamos la onda senoidal para ese byte
        t = np.linspace(0, DURATION_PER_BYTE, int(SAMPLE_RATE * DURATION_PER_BYTE))
        wave = 0.5 * np.sin(2 * np.pi * freq * t)
        full_wave.extend(wave)

    # Convertimos a formato de audio de 16 bits
    audio_data = np.array(full_wave).astype(np.float32)
    
    os.makedirs('data/processed', exist_ok=True)
    wavfile.write(OUTPUT_AUDIO, SAMPLE_RATE, audio_data)
    
    print(f"✅ ¡Sonificación completa! Escuchá el resultado en: {OUTPUT_AUDIO}")

if __name__ == "__main__":
    generar_audio()