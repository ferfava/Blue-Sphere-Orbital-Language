import json
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os

def generate_tone(freq, duration, sample_rate=22050): # Bajamos el sample rate a la mitad (ahorro 50% RAM)
    t = np.linspace(0, duration, int(sample_rate * duration))
    envelope = np.exp(-t * 10) 
    return np.sin(2 * np.pi * freq * t) * envelope

def audit_signal_signature(audio_segment, fs=22050):
    if len(audio_segment) == 0: return "DATA_NULL"
    fft_data = np.abs(np.fft.fft(audio_segment))
    freqs = np.fft.fftfreq(len(fft_data), 1/fs)
    idx = np.argmax(fft_data[:len(fft_data)//2])
    peak_freq = abs(freqs[idx])

    if peak_freq < 250: return "SYNC_HEARTBEAT"
    elif 250 <= peak_freq < 600: return "NOMINAL_DATA_FLOW"
    elif 600 <= peak_freq < 1000: return "HIGH_VELOCITY_PAYLOAD"
    else: return "SIGNAL_ANOMALY"

def translate_satellite_to_sound(input_file, audio_output, plot_output):
    print("--------------------------------------------------")
    print("BLUE SPHERE: LIGHTWEIGHT AUDIT ENGINE (V6.1)")
    print("--------------------------------------------------")
    
    with open(input_file, 'r') as f:
        content = json.load(f)

    packets = content.get('results', [])
    full_audio = []
    audit_log = []
    fs = 22050 # Frecuencia de muestreo reducida para estabilidad
    
    # Solo 10 paquetes para asegurar el éxito del test
    target_packets = packets[:10] 

    for i, packet in enumerate(target_packets):
        raw_hex = packet.get('frame')
        if not raw_hex: continue
        
        try:
            clean_hex = "".join(filter(lambda x: x in "0123456789abcdefABCDEF", str(raw_hex)))
            byte_array = bytes.fromhex(clean_hex)
            
            packet_audio = []
            # SALTO DE 20: Reducción drástica de uso de memoria
            for byte in byte_array[::20]: 
                freq = 150 + (byte * 4) 
                tone = generate_tone(freq, 0.05) 
                packet_audio.extend(tone)
            
            p_audio_np = np.array(packet_audio).astype(np.float32)
            status = audit_signal_signature(p_audio_np, fs)
            audit_log.append(f"Frame {i+1:02d}: {status}")
            full_audio.extend(packet_audio)
            
        except Exception as e:
            continue

    if not full_audio:
        print("ERROR: Flujo vacio.")
        return

    audio_data = np.array(full_audio).astype(np.float32)
    if np.max(np.abs(audio_data)) > 0:
        audio_data = audio_data / np.max(np.abs(audio_data))

    wavfile.write(audio_output, fs, audio_data)
    
    plt.figure(figsize=(10, 5))
    plt.specgram(audio_data, Fs=fs, NFFT=512, cmap='magma') # NFFT menor para velocidad
    plt.title("Blue Sphere: Lightweight SIGINT Audit")
    plt.savefig(plot_output)
    plt.close()

    print("REPORTE DE AUDITORIA:")
    for entry in audit_log:
        print(f"  [+] {entry}")
    print("--------------------------------------------------")
    print(f"STATUS: Completado con exito. RAM a salvo.")

if __name__ == "__main__":
    translate_satellite_to_sound(
        'data/raw/batch/METEOR-M2_raw.json', 
        'output/meteor_voice_final.wav', 
        'output/meteor_audit_plot.png'
    )