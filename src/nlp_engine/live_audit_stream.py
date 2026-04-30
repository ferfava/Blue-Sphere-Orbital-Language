import requests
import json
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import time

# Objetivo: METEOR-M2
SATELLITE_ID = "44387" 
# URL simplificada para evitar el error 400
API_URL = f"https://network.satnogs.org/api/observations/?satellite={SATELLITE_ID}"

def fetch_telemetry():
    print(f"[*] BLUE SPHERE: Iniciando protocolo de busqueda...")
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            observations = response.json()
            if isinstance(observations, list) and len(observations) > 0:
                # Buscamos la primera que tenga telemetria
                for obs in observations[:5]:
                    obs_id = obs.get('id')
                    tel_url = f"https://network.satnogs.org/api/telemetry/?observation_id={obs_id}"
                    t_res = requests.get(tel_url)
                    if t_res.status_code == 200 and len(t_res.json()) > 0:
                        print(f"[+] INTERCEPCION EXITOSA: Obs ID {obs_id}")
                        return t_res.json()
        
        print("[!] Red SatNOGS ocupada o requiere Token. Activando MODO LOCAL...")
    except Exception:
        print("[!] Error de red. Activando MODO LOCAL...")
    
    # MODO LOCAL (Respaldo)
    local_path = 'data/raw/batch/METEOR-M2_raw.json'
    if os.path.exists(local_path):
        with open(local_path, 'r') as f:
            content = json.load(f)
            return content.get('results', [])
    return None

def audit_engine_pro(audio_segment, fs=22050):
    if len(audio_segment) == 0: return "NULL"
    fft_data = np.abs(np.fft.fft(audio_segment))
    freqs = np.fft.fftfreq(len(fft_data), 1/fs)
    idx = np.argmax(fft_data[:len(fft_data)//2])
    peak_freq = abs(freqs[idx])
    
    if peak_freq < 250: return "HEALTH_BEAT"
    elif 250 <= peak_freq < 600: return "PAYLOAD_TRANSFER"
    else: return "ANOMALY_DETECTED"

def run_session():
    print("--------------------------------------------------")
    print("BLUE SPHERE: ROBUST INTERCEPTION MODE (v6.3)")
    print("--------------------------------------------------")
    
    data = fetch_telemetry()
    if not data:
        print("[!] No se encontraron datos para procesar.")
        return

    full_audio = []
    fs = 22050
    print(f"[*] Ejecutando Auditoria Forense...")

    for i, entry in enumerate(data[:15]):
        raw_hex = entry.get('frame')
        if not raw_hex: continue
        
        byte_array = bytes.fromhex(raw_hex)
        packet_audio = []
        for byte in byte_array[::25]: 
            freq = 150 + (byte * 4)
            t = np.linspace(0, 0.04, int(fs * 0.04))
            tone = np.sin(2 * np.pi * freq * t) * np.exp(-t * 15)
            packet_audio.extend(tone)
            
        status = audit_engine_pro(np.array(packet_audio), fs)
        print(f"  > [{time.strftime('%H:%M:%S')}] Frame {i+1:02d}: {status}")
        full_audio.extend(packet_audio)

    audio_data = np.array(full_audio).astype(np.float32)
    wavfile.write('output/interception_final.wav', fs, audio_data / np.max(np.abs(audio_data)))
    print("--------------------------------------------------")
    print("[SUCCESS] Auditoria finalizada. Evidencia: output/interception_final.wav")

if __name__ == "__main__":
    if not os.path.exists('output'): os.makedirs('output')
    run_session()